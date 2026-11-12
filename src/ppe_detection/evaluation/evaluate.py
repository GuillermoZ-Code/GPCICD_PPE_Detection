"""Evaluación reproducible de un artefacto YOLO (HU-008).

El módulo no entrena ni descarga pesos. Carga un ``best.pt`` local, ejecuta
``YOLO.val`` sobre una partición etiquetada y escribe un informe JSON/Markdown con
la configuración, el SHA256 del modelo y las métricas globales y por clase.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ppe_detection.contracts import CLASSES

DEFAULT_IMGSZ = 640
DEFAULT_CONF = 0.001
DEFAULT_IOU = 0.7
DEFAULT_SEED = 42
DEFAULT_DEVICE = "cpu"
DEFAULT_OUTPUT = Path("artifacts/eval")
DEFAULT_NAME = "evaluation"
SPLITS = ("train", "valid", "test")
IMAGE_SUFFIXES = frozenset({".jpg", ".jpeg", ".png"})


class EvaluationError(RuntimeError):
    """Error controlado del proceso de evaluación."""


@dataclass(frozen=True)
class EvaluationConfig:
    """Parámetros reproducibles de una evaluación."""

    model: Path
    data: Path
    split: str = "test"
    imgsz: int = DEFAULT_IMGSZ
    conf: float = DEFAULT_CONF
    iou: float = DEFAULT_IOU
    seed: int = DEFAULT_SEED
    device: str = DEFAULT_DEVICE
    output: Path = DEFAULT_OUTPUT
    name: str = DEFAULT_NAME
    plots: bool = True


def sha256_file(path: Path) -> str:
    """Calcula el SHA256 de un archivo por bloques."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _normalize_names(names: Mapping[int, str] | Sequence[str]) -> dict[int, str]:
    if isinstance(names, Mapping):
        return {int(key): str(value) for key, value in names.items()}
    return {index: str(value) for index, value in enumerate(names)}


def validate_model_names(names: Mapping[int, str] | Sequence[str]) -> dict[int, str]:
    """Valida que el modelo use exactamente el catálogo canónico del proyecto."""
    normalized = _normalize_names(names)
    expected = dict(enumerate(CLASSES))
    if normalized != expected:
        raise EvaluationError(
            "El modelo no usa el catálogo canónico de EPP. "
            f"Esperado: {expected}. Recibido: {normalized}."
        )
    return normalized


def _jsonable(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "tolist") and not isinstance(value, (str, bytes)):
        return _jsonable(value.tolist())
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def _per_class(metrics: Any, names: Mapping[int, str]) -> dict[str, dict[str, float]]:
    box = metrics.box
    per_class: dict[str, dict[str, float]] = {}
    for index, class_index in enumerate(box.ap_class_index):
        per_class[names[int(class_index)]] = {
            "p": float(box.p[index]),
            "r": float(box.r[index]),
            "ap50": float(box.ap50[index]),
            "ap": float(box.ap[index]),
        }
    return per_class


def _count_images(data: Path, split: str) -> int:
    """Cuenta las imágenes de la partición declarada en el YAML."""
    try:
        yaml = importlib.import_module("yaml")
    except ImportError:
        return 0
    config = yaml.safe_load(data.read_text(encoding="utf-8")) or {}
    relative = config.get(split)
    if not relative:
        return 0
    root = Path(config.get("path") or data.parent)
    if not root.is_absolute():
        root = (data.parent / root).resolve()
    images_dir = root / relative
    if not images_dir.is_dir():
        return 0
    return sum(1 for path in images_dir.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)


def build_summary(
    config: EvaluationConfig,
    metrics: Any,
    model_names: Mapping[int, str] | Sequence[str],
    model_sha256: str,
    *,
    images: int = 0,
) -> dict[str, Any]:
    """Construye el resumen serializable a partir del resultado de Ultralytics."""
    names = _normalize_names(model_names)
    results = {key: float(value) for key, value in metrics.results_dict.items()}
    matrix = metrics.confusion_matrix.matrix
    instances = (
        int(sum(int(value) for value in metrics.nt_per_class))
        if hasattr(metrics, "nt_per_class")
        else 0
    )
    return {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "model": {
            "path": str(config.model),
            "sha256": model_sha256,
        },
        "dataset": {
            "path": str(config.data),
            "split": config.split,
            "yaml_sha256": sha256_file(config.data) if config.data.is_file() else None,
        },
        "config": {
            "imgsz": config.imgsz,
            "conf": config.conf,
            "iou": config.iou,
            "seed": config.seed,
            "device": config.device,
        },
        "images": images,
        "instances": instances,
        "metrics": results,
        "per_class": _per_class(metrics, names),
        "confusion_matrix": _jsonable(matrix),
        "speed_ms_per_image": {
            str(key): float(value) for key, value in getattr(metrics, "speed", {}).items()
        },
    }


def render_markdown(summary: Mapping[str, Any]) -> str:
    """Genera un informe Markdown legible a partir del resumen."""
    metrics = summary.get("metrics", {})
    per_class = summary.get("per_class", {})
    lines = [
        "# Evaluación del detector",
        "",
        f"- **Modelo:** `{summary.get('model', {}).get('path')}`",
        f"- **SHA256:** `{summary.get('model', {}).get('sha256')}`",
        f"- **Partición:** `{summary.get('dataset', {}).get('split')}`",
        f"- **Imágenes:** {summary.get('images')}",
        f"- **Objetos:** {summary.get('instances')}",
        f"- **Configuración:** `imgsz={summary.get('config', {}).get('imgsz')}`, "
        f"`conf={summary.get('config', {}).get('conf')}`, "
        f"`iou={summary.get('config', {}).get('iou')}`, "
        f"`seed={summary.get('config', {}).get('seed')}`, "
        f"`device={summary.get('config', {}).get('device')}`",
        "",
        "| Clase | P | R | mAP50 | mAP50-95 |",
        "|---|---:|---:|---:|---:|",
    ]
    lines.append(
        "| **all** | "
        f"{float(metrics.get('metrics/precision(B)', 0.0)):.3f} | "
        f"{float(metrics.get('metrics/recall(B)', 0.0)):.3f} | "
        f"{float(metrics.get('metrics/mAP50(B)', 0.0)):.3f} | "
        f"{float(metrics.get('metrics/mAP50-95(B)', 0.0)):.3f} |"
    )
    for name, values in per_class.items():
        lines.append(
            f"| {name} | {float(values['p']):.3f} | {float(values['r']):.3f} | "
            f"{float(values['ap50']):.3f} | {float(values['ap']):.3f} |"
        )
    return "\n".join(lines) + "\n"


def _load_yolo() -> Any:
    try:
        return importlib.import_module("ultralytics").YOLO
    except ImportError as exc:
        raise EvaluationError(
            "Falta ultralytics. Instala el extra con `uv sync --extra inference` "
            "o ejecuta con `uv run --with ultralytics ...`."
        ) from exc


def evaluate(config: EvaluationConfig) -> dict[str, Any]:
    """Ejecuta la evaluación y escribe ``summary.json`` y ``summary.md``."""
    if not config.model.is_file():
        raise FileNotFoundError(f"No existe el modelo: {config.model}")
    if not config.data.is_file():
        raise FileNotFoundError(f"No existe el data.yaml: {config.data}")
    if config.split not in SPLITS:
        raise EvaluationError(f"split inválido: {config.split}")
    if config.imgsz <= 0 or config.conf < 0 or config.iou <= 0:
        raise EvaluationError("imgsz, conf e iou deben ser válidos")

    yolo_class = _load_yolo()
    model = yolo_class(str(config.model))
    names = validate_model_names(model.names)
    metrics = model.val(
        data=str(config.data),
        split=config.split,
        imgsz=config.imgsz,
        conf=config.conf,
        iou=config.iou,
        seed=config.seed,
        deterministic=True,
        device=config.device,
        workers=0,
        project=str(config.output),
        name=config.name,
        exist_ok=True,
        plots=config.plots,
        verbose=False,
    )
    summary = build_summary(
        config,
        metrics,
        names,
        sha256_file(config.model),
        images=_count_images(config.data, config.split),
    )
    output_dir = config.output / config.name
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (output_dir / "summary.md").write_text(render_markdown(summary), encoding="utf-8")
    return summary


def parse_args(argv: Sequence[str] | None = None) -> EvaluationConfig:
    """Parsea la CLI de evaluación."""
    parser = argparse.ArgumentParser(
        prog="ppe-evaluate",
        description="Evalúa un artefacto YOLO sobre una partición etiquetada.",
    )
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--split", choices=SPLITS, default="test")
    parser.add_argument("--imgsz", type=int, default=DEFAULT_IMGSZ)
    parser.add_argument("--conf", type=float, default=DEFAULT_CONF)
    parser.add_argument("--iou", type=float, default=DEFAULT_IOU)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--device", default=DEFAULT_DEVICE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--name", default=DEFAULT_NAME)
    parser.add_argument("--no-plots", action="store_true")
    args = parser.parse_args(argv)
    return EvaluationConfig(
        model=args.model,
        data=args.data,
        split=args.split,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        seed=args.seed,
        device=args.device,
        output=args.output,
        name=args.name,
        plots=not args.no_plots,
    )


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada de la CLI."""
    config = parse_args(argv)
    summary = evaluate(config)
    print(render_markdown(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
