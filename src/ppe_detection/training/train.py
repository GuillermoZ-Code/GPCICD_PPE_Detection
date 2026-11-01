"""Fine-tuning de YOLO para detección de EPP.

Pensado para ejecutarse en Colab Pro (GPU) con un script versionado, no con un
notebook. También funciona en local para pruebas de CPU, aunque el entrenamiento
local no es viable (ver CONSTITUTION §6).

Ejemplo en Colab:

    uv run --with ultralytics --with onnx --with onnxruntime --with onnxslim \
        python -m ppe_detection.training.train \
        --data /content/drive/MyDrive/ppe/ds_base/data.yaml \
        --eval-data /content/drive/MyDrive/ppe/ds_base/data_eval_preentrenados.yaml \
        --device 0 --backup-dir /content/drive/MyDrive/ppe/runs --export-onnx
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import random
import shutil
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Colab/IPython exporta MPLBACKEND=module://matplotlib_inline; en un subproceso
# sin matplotlib_inline eso rompe matplotlib. Agg es seguro para entrenamiento.
if os.environ.get("MPLBACKEND", "").startswith("module://matplotlib_inline"):
    os.environ["MPLBACKEND"] = "Agg"

SPLITS = ("train", "valid", "test")
DEFAULT_MODEL = "yolov8n.pt"


@dataclass(frozen=True)
class TrainConfig:
    """Parámetros de una corrida de entrenamiento."""

    data: Path
    eval_data: Path | None
    model: str
    epochs: int
    imgsz: int
    batch: int
    device: str | None
    project: Path
    name: str
    seed: int
    patience: int
    workers: int
    save_period: int
    resume: bool
    export_onnx: bool
    backup_dir: Path | None
    mlflow_uri: str | None
    mlflow_experiment: str
    cache: bool
    amp: bool
    eval_split: str
    skip_eval: bool


def parse_args(argv: Sequence[str] | None = None) -> TrainConfig:
    """Parsea la CLI y deriva el YAML de evaluación si existe."""
    parser = argparse.ArgumentParser(
        prog="ppe-train",
        description="Fine-tuning de YOLO para detección de EPP (Colab Pro / GPU).",
    )
    parser.add_argument("--data", type=Path, required=True, help="data.yaml de entrenamiento")
    parser.add_argument("--eval-data", type=Path, default=None, help="data.yaml del eval sin fuga")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="pesos base (COCO o checkpoint)")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=-1, help="-1 = AutoBatch")
    parser.add_argument("--device", default=None, help="0, cpu, mps; vacío = automático")
    parser.add_argument("--project", type=Path, default=Path("runs/train"))
    parser.add_argument("--name", default="yolov8n_clean")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--patience", type=int, default=20)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--save-period", type=int, default=5)
    parser.add_argument("--resume", action="store_true", help="reanuda desde last.pt")
    parser.add_argument("--export-onnx", action="store_true")
    parser.add_argument("--backup-dir", type=Path, default=None, help="copia de artefactos (Drive)")
    parser.add_argument("--mlflow-uri", default=None, help="tracking URI de MLflow")
    parser.add_argument("--mlflow-experiment", default="ppe-detection")
    parser.add_argument("--cache", action="store_true", help="cachear imágenes en RAM")
    parser.add_argument("--amp", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--eval-split", choices=SPLITS, default="test")
    parser.add_argument("--skip-eval", action="store_true")
    args = parser.parse_args(argv)

    eval_data = args.eval_data
    if eval_data is None and not args.skip_eval:
        candidate = args.data.parent / "data_eval_preentrenados.yaml"
        if candidate.is_file():
            eval_data = candidate

    device = args.device.strip() if isinstance(args.device, str) else args.device
    if device == "":
        device = None

    return TrainConfig(
        data=args.data,
        eval_data=eval_data,
        model=args.model,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=device,
        project=args.project,
        name=args.name,
        seed=args.seed,
        patience=args.patience,
        workers=args.workers,
        save_period=args.save_period,
        resume=args.resume,
        export_onnx=args.export_onnx,
        backup_dir=args.backup_dir,
        mlflow_uri=args.mlflow_uri,
        mlflow_experiment=args.mlflow_experiment,
        cache=args.cache,
        amp=args.amp,
        eval_split=args.eval_split,
        skip_eval=args.skip_eval,
    )


def _import_optional(name: str) -> Any:
    try:
        return importlib.import_module(name)
    except ImportError as exc:
        raise RuntimeError(
            f"Falta la dependencia '{name}'. Instálala en el entorno de ejecución, "
            "por ejemplo con `uv run --with <paquete> ...`."
        ) from exc


def _load_yolo() -> Any:
    return _import_optional("ultralytics").YOLO


def load_data_config(path: Path) -> dict[str, Any]:
    """Lee el data.yaml y normaliza `names` a una lista ordenada."""
    if not path.is_file():
        raise FileNotFoundError(f"No existe el YAML: {path}")
    yaml = _import_optional("yaml")
    cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(cfg, dict):
        raise ValueError(f"{path} no contiene un objeto YAML válido")
    names = cfg.get("names")
    if isinstance(names, Mapping):
        names = [names[key] for key in sorted(names, key=lambda key: int(key))]
    if not names:
        raise ValueError(f"{path} no define 'names'")
    cfg["names"] = list(names)
    if "nc" in cfg and int(cfg["nc"]) != len(cfg["names"]):
        raise ValueError(f"{path}: nc={cfg['nc']} no coincide con {len(cfg['names'])} clases")
    for key in ("train", "val"):
        if key not in cfg:
            raise ValueError(f"{path} no define '{key}'")
    return cfg


def _normalize_class_name(name: str) -> str:
    return " ".join(name.strip().lower().replace("_", " ").split())


def _names_list(names: Mapping[int, str] | Sequence[str]) -> list[str]:
    if isinstance(names, Mapping):
        return [value for _, value in sorted(names.items(), key=lambda item: int(item[0]))]
    return list(names)


def verify_class_order(
    expected: Sequence[str],
    actual: Mapping[int, str] | Sequence[str],
) -> None:
    """Falla si el modelo y el data.yaml no tienen las mismas clases en orden."""
    expected_norm = [_normalize_class_name(name) for name in expected]
    actual_norm = [_normalize_class_name(name) for name in _names_list(actual)]
    if expected_norm != actual_norm:
        raise ValueError(
            "El orden de clases no coincide entre data.yaml y el modelo: "
            f"data.yaml={expected_norm} modelo={actual_norm}"
        )


def build_train_kwargs(config: TrainConfig) -> dict[str, Any]:
    """Construye los argumentos reproducibles de Ultralytics."""
    return {
        "data": str(config.data),
        "epochs": config.epochs,
        "imgsz": config.imgsz,
        "batch": config.batch,
        "device": config.device,
        "project": str(config.project.resolve()),
        "name": config.name,
        "exist_ok": True,
        "pretrained": True,
        "optimizer": "auto",
        "patience": config.patience,
        "seed": config.seed,
        "deterministic": True,
        "amp": config.amp,
        "cache": config.cache,
        "workers": config.workers,
        "plots": True,
        "save": True,
        "save_period": config.save_period,
        "verbose": True,
    }


def set_seed(seed: int) -> None:
    """Fija semillas de Python, NumPy y torch si están disponibles."""
    random.seed(seed)
    try:
        numpy = importlib.import_module("numpy")
    except ImportError:
        numpy = None
    if numpy is not None:
        numpy.random.seed(seed)
    try:
        torch = importlib.import_module("torch")
    except ImportError:
        return
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def _make_backup_callback(config: TrainConfig) -> Callable[[Any], None]:
    """Copia last.pt a Drive cada `save_period` épocas."""
    backup_dir = config.backup_dir

    def callback(trainer: Any) -> None:
        if backup_dir is None:
            return
        epoch = int(getattr(trainer, "epoch", 0)) + 1
        if epoch % max(config.save_period, 1) != 0:
            return
        save_dir = Path(getattr(trainer, "save_dir", config.project / config.name))
        destination_dir = backup_dir / config.name
        destination_dir.mkdir(parents=True, exist_ok=True)
        for relative in ("weights/last.pt", "args.yaml", "results.csv"):
            source = save_dir / relative
            if source.is_file():
                shutil.copy2(source, destination_dir / Path(relative).name)

    return callback


def train_model(config: TrainConfig) -> tuple[Path, Path]:
    """Entrena o reanuda y devuelve (run_dir, best.pt)."""
    yolo_class = _load_yolo()
    set_seed(config.seed)
    if config.resume:
        last = (config.project / config.name / "weights" / "last.pt").resolve()
        if not last.is_file():
            raise FileNotFoundError(f"No existe {last} para reanudar")
        model = yolo_class(str(last))
        if config.backup_dir is not None:
            model.add_callback("on_train_epoch_end", _make_backup_callback(config))
        model.train(resume=True)
    else:
        model = yolo_class(config.model)
        if config.backup_dir is not None:
            model.add_callback("on_train_epoch_end", _make_backup_callback(config))
        model.train(**build_train_kwargs(config))

    save_dir = Path(getattr(model.trainer, "save_dir", config.project / config.name)).resolve()
    best = save_dir / "weights" / "best.pt"
    if not best.is_file():
        raise FileNotFoundError(f"No se generó {best}")
    return save_dir, best


def _metrics_summary(
    model: Any,
    metrics: Any,
    data: Path,
    split: str,
    config: TrainConfig,
) -> dict[str, Any]:
    box = metrics.box
    names = _names_list(model.names)
    per_class: dict[str, dict[str, float]] = {}
    for index, class_index in enumerate(box.ap_class_index):
        per_class[names[int(class_index)]] = {
            "p": float(box.p[index]),
            "r": float(box.r[index]),
            "ap50": float(box.ap50[index]),
            "ap": float(box.ap[index]),
        }
    matrix = metrics.confusion_matrix.matrix
    return {
        "data": str(data),
        "split": split,
        "imgsz": config.imgsz,
        "conf": 0.001,
        "iou": 0.7,
        "seed": config.seed,
        "names": names,
        "results_dict": {key: float(value) for key, value in metrics.results_dict.items()},
        "speed_ms_per_image": {key: float(value) for key, value in metrics.speed.items()},
        "per_class": per_class,
        "confusion_matrix": matrix.tolist() if hasattr(matrix, "tolist") else matrix,
    }


def _metrics_markdown(summary: dict[str, Any]) -> str:
    results = summary.get("results_dict", {})
    lines = [
        f"# Evaluación — {summary.get('data')} ({summary.get('split')})",
        "",
        f"- `imgsz`: {summary.get('imgsz')} · `conf`: {summary.get('conf')} · "
        f"`iou`: {summary.get('iou')} · `seed`: {summary.get('seed')}",
        "",
        "| Clase | P | R | mAP50 | mAP50-95 |",
        "|-------|--:|---:|------:|---------:|",
        f"| **all** | {float(results.get('metrics/precision(B)', 0.0)):.3f} | "
        f"{float(results.get('metrics/recall(B)', 0.0)):.3f} | "
        f"{float(results.get('metrics/mAP50(B)', 0.0)):.3f} | "
        f"{float(results.get('metrics/mAP50-95(B)', 0.0)):.3f} |",
    ]
    for name, values in summary.get("per_class", {}).items():
        lines.append(
            f"| {name} | {values['p']:.3f} | {values['r']:.3f} | "
            f"{values['ap50']:.3f} | {values['ap']:.3f} |"
        )
    return "\n".join(lines) + "\n"


def evaluate_model(
    config: TrainConfig,
    weights: Path,
    data: Path,
    split: str,
    name: str,
) -> tuple[dict[str, Any], Path]:
    """Evalúa el modelo y guarda summary.json + summary.md."""
    yolo_class = _load_yolo()
    cfg = load_data_config(data)
    if split not in cfg:
        raise ValueError(f"{data} no define el split '{split}'")
    model = yolo_class(str(weights))
    verify_class_order(cfg["names"], model.names)
    eval_project = (config.project / "eval").resolve()
    metrics = model.val(
        data=str(data),
        split=split,
        imgsz=config.imgsz,
        batch=16,
        device=config.device,
        workers=0,
        conf=0.001,
        iou=0.7,
        seed=config.seed,
        deterministic=True,
        plots=True,
        project=str(eval_project),
        name=name,
        exist_ok=True,
        verbose=True,
    )
    summary = _metrics_summary(model, metrics, data, split, config)
    eval_dir = eval_project / name
    eval_dir.mkdir(parents=True, exist_ok=True)
    (eval_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (eval_dir / "summary.md").write_text(_metrics_markdown(summary), encoding="utf-8")
    return summary, eval_dir


def export_onnx(weights: Path, imgsz: int) -> Path:
    """Exporta el checkpoint a ONNX (opset 17, estático)."""
    for dependency in ("onnx", "onnxslim"):
        if importlib.util.find_spec(dependency) is None:
            raise RuntimeError(
                f"Falta '{dependency}' para exportar ONNX. "
                "Ejecuta con `--with onnx --with onnxruntime --with onnxslim`."
            )
    yolo_class = _load_yolo()
    model = yolo_class(str(weights))
    exported = model.export(format="onnx", opset=17, simplify=True, dynamic=False, imgsz=imgsz)
    return Path(exported)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def _git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def write_manifest(
    config: TrainConfig,
    run_dir: Path,
    best: Path,
    eval_dir: Path | None,
    onnx_path: Path | None,
    started_at: str,
) -> dict[str, Any]:
    """Escribe run_manifest.json con versiones, hashes y configuración."""
    manifest = {
        "started_at": started_at,
        "finished_at": datetime.now(UTC).isoformat(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "ultralytics": _package_version("ultralytics"),
        "torch": _package_version("torch"),
        "git_commit": _git_commit(),
        "config": _jsonable(asdict(config)),
        "dataset": {"path": str(config.data), "sha256": _sha256(config.data)},
        "eval": (
            {
                "path": str(config.eval_data),
                "sha256": _sha256(config.eval_data),
                "dir": str(eval_dir) if eval_dir else None,
            }
            if config.eval_data is not None
            else None
        ),
        "weights": {"path": str(best), "sha256": _sha256(best)},
        "onnx": str(onnx_path) if onnx_path is not None else None,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return manifest


def backup_artifacts(
    config: TrainConfig,
    run_dir: Path,
    eval_dir: Path | None,
    onnx_path: Path | None,
) -> None:
    """Copia pesos y reportes a `backup_dir` (por ejemplo, Google Drive)."""
    if config.backup_dir is None:
        return
    destination = (config.backup_dir / config.name).resolve()
    destination.mkdir(parents=True, exist_ok=True)
    for relative in (
        "weights/best.pt",
        "weights/last.pt",
        "results.csv",
        "args.yaml",
        "run_manifest.json",
    ):
        source = run_dir / relative
        if source.is_file():
            shutil.copy2(source, destination / Path(relative).name)
    if eval_dir is not None:
        eval_destination = destination / "eval"
        eval_destination.mkdir(parents=True, exist_ok=True)
        for filename in (
            "summary.json",
            "summary.md",
            "confusion_matrix.png",
            "confusion_matrix_normalized.png",
            "BoxPR_curve.png",
            "BoxF1_curve.png",
        ):
            source = eval_dir / filename
            if source.is_file():
                shutil.copy2(source, eval_destination / filename)
    if onnx_path is not None and onnx_path.is_file():
        shutil.copy2(onnx_path, destination / onnx_path.name)
    print(f"Artefactos respaldados en {destination}")


def log_mlflow(
    config: TrainConfig,
    run_dir: Path,
    eval_dir: Path | None,
    summary: dict[str, Any],
) -> None:
    """Registra parámetros, métricas y artefactos en MLflow (opcional)."""
    if config.mlflow_uri is None:
        return
    mlflow = _import_optional("mlflow")
    mlflow.set_tracking_uri(config.mlflow_uri)
    mlflow.set_experiment(config.mlflow_experiment)
    with mlflow.start_run(run_name=config.name):
        mlflow.log_params({key: str(value) for key, value in _jsonable(asdict(config)).items()})
        for key, value in summary.get("results_dict", {}).items():
            metric = key.replace("/", "_").replace("(", "").replace(")", "")
            mlflow.log_metric(metric, float(value))
        for class_name, values in summary.get("per_class", {}).items():
            safe_name = class_name.replace(" ", "_")
            for key, value in values.items():
                mlflow.log_metric(f"{safe_name}_{key}", float(value))
        manifest = run_dir / "run_manifest.json"
        if manifest.is_file():
            mlflow.log_artifact(str(manifest))
        if eval_dir is not None and eval_dir.is_dir():
            mlflow.log_artifacts(str(eval_dir), artifact_path="eval")
        mlflow.log_artifacts(str(run_dir), artifact_path="run")


def _validate_config(config: TrainConfig) -> None:
    if not config.data.is_file():
        raise FileNotFoundError(f"No existe el data.yaml: {config.data}")
    if config.eval_data is not None and not config.eval_data.is_file():
        raise FileNotFoundError(f"No existe el eval YAML: {config.eval_data}")
    if config.epochs <= 0:
        raise ValueError("--epochs debe ser > 0")
    if config.imgsz <= 0:
        raise ValueError("--imgsz debe ser > 0")
    if config.save_period <= 0:
        raise ValueError("--save-period debe ser > 0")
    if config.eval_split not in SPLITS:
        raise ValueError(f"--eval-split debe ser uno de {SPLITS}")
    if config.batch == 0:
        raise ValueError("--batch no puede ser 0")
    if config.export_onnx:
        for dependency in ("onnx", "onnxslim"):
            if importlib.util.find_spec(dependency) is None:
                raise RuntimeError(
                    f"Falta '{dependency}' para exportar ONNX. "
                    "Añade `--with onnx --with onnxruntime --with onnxslim`."
                )
    if config.mlflow_uri is not None and importlib.util.find_spec("mlflow") is None:
        raise RuntimeError("Pediste `--mlflow-uri` pero falta 'mlflow'. Añade `--with mlflow`.")


def main(argv: Sequence[str] | None = None) -> int:
    """Orquesta entrenamiento, evaluación, exportación y respaldo."""
    config = parse_args(argv)
    _validate_config(config)
    started_at = datetime.now(UTC).isoformat()
    print("Configuración:")
    print(json.dumps(_jsonable(asdict(config)), indent=2, ensure_ascii=False))

    run_dir, best = train_model(config)
    print(f"Entrenamiento terminado: {run_dir}")

    eval_summary: dict[str, Any] | None = None
    eval_dir: Path | None = None
    if not config.skip_eval and config.eval_data is not None:
        eval_summary, eval_dir = evaluate_model(
            config, best, config.eval_data, config.eval_split, "best"
        )
        print(_metrics_markdown(eval_summary))

    onnx_path = export_onnx(best, config.imgsz) if config.export_onnx else None
    write_manifest(config, run_dir, best, eval_dir, onnx_path, started_at)
    backup_artifacts(config, run_dir, eval_dir, onnx_path)

    if eval_summary is not None:
        log_mlflow(config, run_dir, eval_dir, eval_summary)

    print(f"Listo. Mejor checkpoint: {best}")
    if onnx_path is not None:
        print(f"ONNX: {onnx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
