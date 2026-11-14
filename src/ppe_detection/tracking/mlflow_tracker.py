"""Registro de evaluaciones y comparación de runs en MLflow (HU-009).

El módulo no importa MLflow hasta que se usa ``MlflowTracker``. El paquete base y
las pruebas unitarias funcionan con un tracker inyectado; MLflow vive en el extra
``tracking``.
"""

from __future__ import annotations

import argparse
import contextlib
import importlib
import json
import math
import re
import shutil
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

DEFAULT_TRACKING_URI = "sqlite:///mlflow.db"
DEFAULT_EXPERIMENT = "ppe-detection-eval"
DEFAULT_BENCHMARK_EXPERIMENT = "ppe-detection-inference"
DEFAULT_MODEL_NAME = "ppe-detection"
DEFAULT_MODEL_ALIAS = "production"

WEIGHT_SUFFIXES: frozenset[str] = frozenset({".pt", ".pth", ".onnx", ".safetensors", ".h5"})
DATASET_SUFFIXES: frozenset[str] = frozenset({".zip"})
MODEL_SHA_PATTERN = re.compile(r"[0-9A-Fa-f]{64}")

PREFERRED_KEYS: tuple[str, ...] = (
    "model_reference",
    "model_sha256",
    "dataset_split",
    "dataset_yaml_sha256",
    "dataset_sha256",
    "images",
    "instances",
    "imgsz",
    "conf",
    "iou",
    "seed",
    "device",
    "precision",
    "recall",
    "map50",
    "map50_95",
)


class TrackingError(ValueError):
    """Error controlado del registro o la consulta de experimentos."""


@dataclass(frozen=True, slots=True)
class RunPayload:
    """Parámetros, métricas, etiquetas y artefactos de un run."""

    params: dict[str, str]
    metrics: dict[str, float]
    tags: dict[str, str]
    artifacts: tuple[Path, ...] = ()


@dataclass(frozen=True, slots=True)
class RunView:
    """Vista de un run consultado en MLflow."""

    run_id: str
    run_name: str
    params: dict[str, str]
    metrics: dict[str, float]
    tags: dict[str, str]


class RunTracker(Protocol):
    """Protocolo mínimo para registrar y consultar runs."""

    def log_run(self, run_name: str, payload: RunPayload) -> str:
        """Registra el payload y devuelve el identificador del run."""
        ...

    def get_run(self, run_id: str) -> RunView:
        """Devuelve la vista del run solicitado."""
        ...


def _section(summary: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = summary.get(key)
    if not isinstance(value, Mapping):
        raise TrackingError(f"El resumen no contiene la sección '{key}'.")
    return value


def _text(section: Mapping[str, Any], key: str, label: str) -> str:
    value = section.get(key)
    if not isinstance(value, str) or not value.strip():
        raise TrackingError(f"Falta '{label}.{key}' en el resumen.")
    return value


def _optional_text(section: Mapping[str, Any], key: str) -> str | None:
    value = section.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise TrackingError(f"'{key}' debe ser texto en el resumen.")
    return value


def _number(section: Mapping[str, Any], key: str, label: str) -> float:
    value = section.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TrackingError(f"Falta un número en '{label}.{key}'.")
    number = float(value)
    if not math.isfinite(number):
        raise TrackingError(f"'{label}.{key}' debe ser un número finito.")
    return number


def _integer(section: Mapping[str, Any], key: str, label: str) -> int:
    value = section.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise TrackingError(f"Falta un entero en '{label}.{key}'.")
    return value


def _validate_artifacts(artifacts: Sequence[Path]) -> tuple[Path, ...]:
    result: list[Path] = []
    for artifact in artifacts:
        path = Path(artifact)
        suffix = path.suffix.lower()
        if suffix in WEIGHT_SUFFIXES:
            raise TrackingError(f"No se registran pesos como artefactos: {path.name}.")
        if suffix in DATASET_SUFFIXES:
            raise TrackingError(f"No se registran datasets como artefactos: {path.name}.")
        if path not in result:
            result.append(path)
    return tuple(result)


def build_run_payload(
    summary: Mapping[str, Any],
    *,
    dataset_sha256: str | None = None,
    artifacts: Sequence[Path] = (),
) -> RunPayload:
    """Construye el payload de un run a partir del ``summary.json`` de HU-008."""
    model = _section(summary, "model")
    dataset = _section(summary, "dataset")
    config = _section(summary, "config")
    metrics_section = _section(summary, "metrics")
    per_class = summary.get("per_class")
    if not isinstance(per_class, Mapping) or not per_class:
        raise TrackingError("El resumen no contiene métricas por clase ('per_class').")

    model_path = _text(model, "path", "model")
    model_sha = _text(model, "sha256", "model")
    if not MODEL_SHA_PATTERN.fullmatch(model_sha):
        raise TrackingError("'model.sha256' debe ser un SHA256 hexadecimal de 64 caracteres.")
    dataset_path = _text(dataset, "path", "dataset")
    split = _text(dataset, "split", "dataset")
    yaml_sha = _optional_text(dataset, "yaml_sha256")
    images = _integer(summary, "images", "summary")
    instances = _integer(summary, "instances", "summary")

    metrics: dict[str, float] = {}
    for key, name in (
        ("metrics/precision(B)", "precision"),
        ("metrics/recall(B)", "recall"),
        ("metrics/mAP50(B)", "map50"),
        ("metrics/mAP50-95(B)", "map50_95"),
    ):
        metrics[name] = _number(metrics_section, key, "metrics")

    for class_name, values in per_class.items():
        if not isinstance(class_name, str) or not class_name.strip():
            raise TrackingError("'per_class' debe usar nombres de clase no vacíos.")
        if not isinstance(values, Mapping):
            raise TrackingError(f"'per_class.{class_name}' debe ser un objeto de métricas.")
        for key, suffix in (
            ("p", "precision"),
            ("r", "recall"),
            ("ap50", "map50"),
            ("ap", "map50_95"),
        ):
            metrics[f"{class_name}_{suffix}"] = _number(values, key, f"per_class.{class_name}")

    params = {
        "model_path": model_path,
        "model_sha256": model_sha,
        "dataset_path": dataset_path,
        "dataset_split": split,
        "imgsz": str(_integer(config, "imgsz", "config")),
        "conf": str(_number(config, "conf", "config")),
        "iou": str(_number(config, "iou", "config")),
        "seed": str(_integer(config, "seed", "config")),
        "device": _text(config, "device", "config"),
        "images": str(images),
        "instances": str(instances),
    }
    if yaml_sha:
        params["dataset_yaml_sha256"] = yaml_sha

    tags = {
        "source": "ppe_detection.evaluation",
        "model_reference": f"sha256:{model_sha}",
        "model_sha256": model_sha,
        "dataset_split": split,
    }
    if yaml_sha:
        tags["dataset_yaml_sha256"] = yaml_sha
    generated_at = _optional_text(summary, "generated_at")
    if generated_at:
        tags["evaluation_generated_at"] = generated_at
    if dataset_sha256:
        if not MODEL_SHA_PATTERN.fullmatch(dataset_sha256):
            raise TrackingError("'dataset_sha256' debe ser un SHA256 hexadecimal de 64 caracteres.")
        tags["dataset_sha256"] = dataset_sha256

    return RunPayload(
        params=params,
        metrics=metrics,
        tags=tags,
        artifacts=_validate_artifacts(artifacts),
    )


@dataclass(frozen=True, slots=True)
class LatencyStats:
    """Resumen de latencias de inferencia (ms) y throughput derivado."""

    mean_ms: float
    p95_ms: float
    max_ms: float
    throughput_fps: float


def latency_stats(samples_ms: Sequence[float]) -> LatencyStats:
    """Resume latencias con p95 por rango más cercano y throughput en fps.

    Las muestras deben ser finitas y positivas; el p95 usa el rango más cercano
    (índice ``ceil(0.95 * n) - 1``), que es el criterio conservador para muestras
    pequeñas.
    """
    values = [float(value) for value in samples_ms]
    if not values:
        raise TrackingError("Se requiere al menos una muestra de latencia.")
    if any(not math.isfinite(value) or value <= 0 for value in values):
        raise TrackingError("Las latencias deben ser finitas y positivas.")
    ordered = sorted(values)
    index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    mean = sum(ordered) / len(ordered)
    return LatencyStats(
        mean_ms=mean,
        p95_ms=ordered[index],
        max_ms=ordered[-1],
        throughput_fps=1000.0 / mean,
    )


def build_benchmark_payload(
    *,
    model_path: str,
    model_sha256: str,
    samples_ms: Sequence[float],
    imgsz: int,
    conf: float,
    iou: float,
    device: str,
    images: int,
    iterations: int,
    seed: int = 42,
    detections_total: int = 0,
    warmup: int = 1,
) -> RunPayload:
    """Construye el payload de una sesión de inferencia medida (rúbrica M3).

    Es una medición de servicio: parámetros reproducibles, latencia media/p95,
    throughput y conteo de detecciones. No registra hiperparámetros de
    entrenamiento porque el proyecto no entrena en el M3.
    """
    if not MODEL_SHA_PATTERN.fullmatch(model_sha256):
        raise TrackingError("'model_sha256' debe ser un SHA256 hexadecimal de 64 caracteres.")
    if images < 1:
        raise TrackingError("Se requiere al menos una imagen para la medición.")
    if iterations < 1:
        raise TrackingError("Se requiere al menos una iteración para la medición.")
    stats = latency_stats(samples_ms)
    metrics = {
        "latency_mean_ms": round(stats.mean_ms, 4),
        "latency_p95_ms": round(stats.p95_ms, 4),
        "latency_max_ms": round(stats.max_ms, 4),
        "throughput_fps": round(stats.throughput_fps, 4),
        "detections_total": float(detections_total),
        "detections_per_image": round(detections_total / images, 4),
    }
    params = {
        "model_path": model_path,
        "model_sha256": model_sha256,
        "imgsz": str(imgsz),
        "conf": str(conf),
        "iou": str(iou),
        "device": device,
        "seed": str(seed),
        "images": str(images),
        "iterations": str(iterations),
        "warmup": str(warmup),
    }
    tags = {
        "source": "ppe_detection.benchmark",
        "experiment_kind": "inference",
        "model_reference": f"sha256:{model_sha256}",
        "model_sha256": model_sha256,
        "backend": device,
    }
    return RunPayload(params=params, metrics=metrics, tags=tags)


def build_model_bundle(
    directory: Path,
    *,
    identity: Mapping[str, Any],
    model_path: Path,
    model_card: Path | None = None,
    include_weights: bool = True,
) -> Path:
    """Prepara el paquete de modelo que se registra como versión en MLflow.

    Incluye la identidad verificable, la Model Card y, opcionalmente, los pesos.
    Los pesos quedan en el almacén local de artefactos de MLflow, nunca en Git.
    """
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "model_identity.json").write_text(
        json.dumps(dict(identity), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (directory / "README.md").write_text(
        "# Paquete de modelo — GPCICD PPE Detection\n\n"
        "Versión registrada desde un run de MLflow. La identidad se verifica por\n"
        "SHA256; los pesos no se versionan en Git y viven en el almacén local de\n"
        "artefactos de MLflow.\n",
        encoding="utf-8",
    )
    if model_card is not None and model_card.is_file():
        shutil.copy2(model_card, directory / "MODEL_CARD.md")
    if include_weights:
        shutil.copy2(model_path, directory / model_path.name)
    return directory


def default_run_name(summary: Mapping[str, Any]) -> str:
    """Nombre determinista: partición y prefijo del SHA256 del modelo."""
    dataset = _section(summary, "dataset")
    model = _section(summary, "model")
    split = _text(dataset, "split", "dataset")
    sha = _text(model, "sha256", "model")
    return f"eval-{split}-{sha[:12].lower()}"


def log_evaluation_run(
    summary: Mapping[str, Any],
    *,
    tracker: RunTracker,
    run_name: str | None = None,
    dataset_sha256: str | None = None,
    artifacts: Sequence[Path] = (),
) -> str:
    """Registra la evaluación y devuelve el ``run_id``."""
    payload = build_run_payload(
        summary,
        dataset_sha256=dataset_sha256,
        artifacts=artifacts,
    )
    for artifact in payload.artifacts:
        if not artifact.is_file():
            raise TrackingError(f"El artefacto no existe: {artifact}")
    return tracker.log_run(run_name or default_run_name(summary), payload)


def compare_runs(run_ids: Sequence[str], tracker: RunTracker) -> tuple[RunView, ...]:
    """Consulta dos o más runs distintos y devuelve sus vistas."""
    identifiers = [run_id.strip() for run_id in run_ids]
    if len(identifiers) < 2:
        raise TrackingError("La comparación requiere al menos dos runs.")
    if any(not run_id for run_id in identifiers):
        raise TrackingError("Los run_id no pueden estar vacíos.")
    if len(set(identifiers)) != len(identifiers):
        raise TrackingError("Los run_id deben ser distintos para comparar.")
    return tuple(tracker.get_run(run_id) for run_id in identifiers)


def _escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def _reference(run: RunView) -> str:
    reference = run.tags.get("model_reference")
    if reference:
        return reference
    sha = run.params.get("model_sha256")
    return f"sha256:{sha}" if sha else "—"


def _comparison_keys(runs: Sequence[RunView]) -> list[str]:
    available: set[str] = set()
    for run in runs:
        available.update(run.params)
        available.update(run.metrics)
        available.update(key for key in run.tags if not key.startswith("mlflow."))
    available.difference_update({"run_id", "run_name", "model_reference"})
    ordered = [key for key in PREFERRED_KEYS if key in available]
    ordered.extend(sorted(available - set(ordered)))
    return ordered


def _cell(run: RunView, key: str) -> str:
    if key in run.metrics:
        return f"{run.metrics[key]:.4f}"
    if key in run.params:
        return _escape(run.params[key])
    if key in run.tags:
        return _escape(run.tags[key])
    return "—"


def render_comparison(runs: Sequence[RunView]) -> str:
    """Genera una tabla Markdown que distingue los runs y sus métricas."""
    if not runs:
        raise TrackingError("No hay runs para comparar.")
    labels = [_escape(f"{run.run_name or 'run'} ({run.run_id[:8]})") for run in runs]
    rows: list[tuple[str, list[str]]] = [
        ("run_id", [run.run_id for run in runs]),
        ("run_name", [_escape(run.run_name or "—") for run in runs]),
        ("model_reference", [_reference(run) for run in runs]),
    ]
    rows.extend((key, [_cell(run, key) for run in runs]) for key in _comparison_keys(runs))

    lines = [
        "# Comparación de runs",
        "",
        "| Campo | " + " | ".join(labels) + " |",
        "|---|" + "---|" * len(runs),
    ]
    lines.extend(f"| **{name}** | " + " | ".join(values) + " |" for name, values in rows)
    lines.extend(
        [
            "",
            "> Los pesos no se copian al run: la referencia es `sha256:<hash>`.",
            "",
        ]
    )
    return "\n".join(lines)


class MlflowTracker:
    """Implementación real sobre la API de MLflow, con import perezoso."""

    def __init__(
        self,
        tracking_uri: str = DEFAULT_TRACKING_URI,
        experiment_name: str | None = None,
    ) -> None:
        try:
            self._mlflow = importlib.import_module("mlflow")
            tracking = importlib.import_module("mlflow.tracking")
        except ImportError as exc:
            raise TrackingError(
                "Falta mlflow. Instala el extra con `uv sync --extra tracking` "
                "o ejecuta con `uv run --extra tracking ...`."
            ) from exc
        self._mlflow.set_tracking_uri(tracking_uri)
        self._client = tracking.MlflowClient(tracking_uri=tracking_uri)
        if experiment_name:
            self._mlflow.set_experiment(experiment_name)

    def log_run(self, run_name: str, payload: RunPayload) -> str:
        """Crea un run, registra el payload y devuelve su identificador."""
        with self._mlflow.start_run(run_name=run_name) as run:
            self._mlflow.log_params(payload.params)
            self._mlflow.log_metrics(payload.metrics)
            self._mlflow.set_tags(payload.tags)
            for artifact in payload.artifacts:
                self._mlflow.log_artifact(str(artifact))
            return str(run.info.run_id)

    def log_artifacts(self, run_id: str, directory: Path, artifact_path: str = "model") -> None:
        """Adjunta un directorio de artefactos a un run existente."""
        with self._mlflow.start_run(run_id=run_id):
            self._mlflow.log_artifacts(str(directory), artifact_path=artifact_path)

    def register_model_version(
        self,
        name: str,
        run_id: str,
        *,
        artifact_path: str = "model",
        alias: str | None = None,
        tags: Mapping[str, str] | None = None,
    ) -> str:
        """Registra una versión del modelo apuntando al artefacto del run."""
        with contextlib.suppress(Exception):
            # Si el modelo ya existe, se reutiliza; es el caso normal al re-registrar.
            self._client.create_registered_model(name)
        version = self._client.create_model_version(
            name=name,
            source=f"runs:/{run_id}/{artifact_path}",
            run_id=run_id,
            tags=dict(tags or {}),
        )
        if alias:
            self._client.set_registered_model_alias(name, alias, version.version)
        return str(version.version)

    def get_run(self, run_id: str) -> RunView:
        """Consulta un run por identificador."""
        try:
            run = self._client.get_run(run_id)
        except Exception as exc:  # frontera de la CLI: MLflow lanza tipos variables
            raise TrackingError(f"No se encontró el run '{run_id}'.") from exc
        return RunView(
            run_id=str(run.info.run_id),
            run_name=str(run.info.run_name or ""),
            params={str(key): str(value) for key, value in run.data.params.items()},
            metrics={str(key): float(value) for key, value in run.data.metrics.items()},
            tags={str(key): str(value) for key, value in run.data.tags.items()},
        )


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de la CLI ``log`` / ``compare``."""
    parser = argparse.ArgumentParser(
        prog="ppe-tracking",
        description="Registra y compara evaluaciones en MLflow (HU-009).",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    log_parser = subparsers.add_parser("log", help="Registra un summary.json como run.")
    log_parser.add_argument("--summary", type=Path, required=True)
    log_parser.add_argument("--tracking-uri", default=DEFAULT_TRACKING_URI)
    log_parser.add_argument("--experiment", default=DEFAULT_EXPERIMENT)
    log_parser.add_argument("--run-name", default=None)
    log_parser.add_argument("--dataset-sha256", default=None)
    log_parser.add_argument("--artifact", type=Path, action="append", default=[])

    compare_parser = subparsers.add_parser("compare", help="Compara dos o más runs.")
    compare_parser.add_argument("--tracking-uri", default=DEFAULT_TRACKING_URI)
    compare_parser.add_argument("--run-id", action="append", required=True)

    benchmark_parser = subparsers.add_parser(
        "benchmark", help="Mide latencia y throughput de inferencia y lo registra."
    )
    benchmark_parser.add_argument("--model", type=Path, required=True)
    benchmark_parser.add_argument(
        "--images",
        type=Path,
        action="append",
        required=True,
        help="Archivo o carpeta con imágenes JPEG/PNG; se puede repetir.",
    )
    benchmark_parser.add_argument("--iterations", type=int, default=30)
    benchmark_parser.add_argument("--imgsz", type=int, default=640)
    benchmark_parser.add_argument("--conf", type=float, default=0.25)
    benchmark_parser.add_argument("--iou", type=float, default=0.7)
    benchmark_parser.add_argument("--device", default="cpu")
    benchmark_parser.add_argument("--seed", type=int, default=42)
    benchmark_parser.add_argument("--tracking-uri", default=DEFAULT_TRACKING_URI)
    benchmark_parser.add_argument("--experiment", default=DEFAULT_BENCHMARK_EXPERIMENT)
    benchmark_parser.add_argument("--run-name", default=None)

    register_parser = subparsers.add_parser(
        "register", help="Registra el modelo y su identidad en el Model Registry."
    )
    register_parser.add_argument("--run-id", required=True)
    register_parser.add_argument("--model", type=Path, required=True)
    register_parser.add_argument("--name", default=DEFAULT_MODEL_NAME)
    register_parser.add_argument("--version", default=None)
    register_parser.add_argument("--alias", default=DEFAULT_MODEL_ALIAS)
    register_parser.add_argument("--model-card", type=Path, default=Path("docs/model-card.md"))
    register_parser.add_argument("--no-weights", action="store_true")
    register_parser.add_argument("--tracking-uri", default=DEFAULT_TRACKING_URI)
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parsea los argumentos de la CLI."""
    return build_parser().parse_args(argv)


IMAGE_SUFFIXES: frozenset[str] = frozenset({".jpg", ".jpeg", ".png"})


def _collect_images(paths: Sequence[Path]) -> list[Path]:
    """Recolecta imágenes JPEG/PNG de archivos o carpetas, sin duplicados."""
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(p for p in path.iterdir() if p.suffix.lower() in IMAGE_SUFFIXES))
        elif path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            files.append(path)
        else:
            raise TrackingError(f"Ruta de imágenes no válida: {path}")
    unique = list(dict.fromkeys(files))
    if not unique:
        raise TrackingError("No se encontraron imágenes JPEG/PNG para medir.")
    return unique


def _default_model_version(model_path: Path) -> str:
    """Deduce un nombre legible del artefacto: `run/weights/best.pt` → `run`."""
    if model_path.parent.name == "weights" and model_path.parent.parent.name:
        return model_path.parent.parent.name
    return model_path.stem


def _run_benchmark(args: argparse.Namespace) -> int:
    """Mide latencia de inferencia y registra la sesión como run."""
    import tempfile
    from dataclasses import replace
    from time import perf_counter

    from ppe_detection.detection.yolo import YoloDetector
    from ppe_detection.detector_config import sha256_file
    from ppe_detection.io import load_image

    files = _collect_images(args.images)
    images = [load_image(path) for path in files]
    detector = YoloDetector(
        args.model,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz,
        device=args.device,
    )
    detector.detect(images[0], conf=args.conf)  # calentamiento fuera de la medición
    samples: list[float] = []
    detections_total = 0
    for index in range(args.iterations):
        image = images[index % len(images)]
        started = perf_counter()
        detections = detector.detect(image, conf=args.conf)
        samples.append((perf_counter() - started) * 1000.0)
        detections_total += len(detections)
    payload = build_benchmark_payload(
        model_path=str(args.model),
        model_sha256=sha256_file(args.model),
        samples_ms=samples,
        imgsz=args.imgsz,
        conf=args.conf,
        iou=args.iou,
        device=args.device,
        images=len(images),
        iterations=args.iterations,
        seed=args.seed,
        detections_total=detections_total,
    )
    run_name = args.run_name or f"infer-{args.imgsz}-conf{args.conf}"
    with tempfile.TemporaryDirectory(prefix="ppe-bench-") as tmp:
        directory = Path(tmp)
        samples_csv = directory / "latency_samples.csv"
        rows = "\n".join(f"{index},{value:.4f}" for index, value in enumerate(samples, start=1))
        samples_csv.write_text(f"iteration,latency_ms\n{rows}\n", encoding="utf-8")
        summary = directory / "summary.md"
        summary.write_text(
            "# Sesión de inferencia — GPCICD PPE Detection\n\n"
            f"- Referencia del modelo: `{payload.tags['model_reference']}`\n"
            f"- Imágenes: {len(images)} · iteraciones: {args.iterations}\n"
            f"- Configuración: imgsz={args.imgsz}, conf={args.conf}, iou={args.iou}, "
            f"device={args.device}\n"
            f"- Latencia media: {payload.metrics['latency_mean_ms']} ms · "
            f"p95: {payload.metrics['latency_p95_ms']} ms · "
            f"throughput: {payload.metrics['throughput_fps']} fps\n",
            encoding="utf-8",
        )
        payload = replace(payload, artifacts=(samples_csv, summary))
        tracker = MlflowTracker(args.tracking_uri, args.experiment)
        run_id = tracker.log_run(run_name, payload)
    print(f"run_id={run_id}")
    print(f"latency_mean_ms={payload.metrics['latency_mean_ms']}")
    print(f"latency_p95_ms={payload.metrics['latency_p95_ms']}")
    print(f"throughput_fps={payload.metrics['throughput_fps']}")
    return 0


def _run_register(args: argparse.Namespace) -> int:
    """Registra el paquete del modelo y su identidad en el Model Registry."""
    import tempfile

    from ppe_detection.detector_config import sha256_file

    if not args.model.is_file():
        raise TrackingError(f"No existe el artefacto del modelo: {args.model}")
    digest = sha256_file(args.model)
    version = args.version or _default_model_version(args.model)
    identity = {
        "name": args.name,
        "version": version,
        "sha256": digest,
        "artifact": str(args.model),
        "reference": f"sha256:{digest}",
        "run_id": args.run_id,
    }
    tracker = MlflowTracker(args.tracking_uri)
    with tempfile.TemporaryDirectory(prefix="ppe-model-") as tmp:
        bundle = build_model_bundle(
            Path(tmp) / "model",
            identity=identity,
            model_path=args.model,
            model_card=args.model_card,
            include_weights=not args.no_weights,
        )
        tracker.log_artifacts(args.run_id, bundle, "model")
    registered = tracker.register_model_version(
        args.name,
        args.run_id,
        alias=args.alias,
        tags={
            "model_reference": identity["reference"],
            "model_sha256": digest,
            "model_version": version,
        },
    )
    print(f"model={args.name}")
    print(f"version={registered}")
    print(f"alias={args.alias}")
    print(f"model_reference={identity['reference']}")
    return 0


def _run(argv: Sequence[str] | None) -> int:
    args = parse_args(argv)
    if args.command == "log":
        summary = json.loads(args.summary.read_text(encoding="utf-8"))
        if not isinstance(summary, Mapping):
            raise TrackingError("El summary.json debe ser un objeto JSON.")
        artifacts = [args.summary]
        report = args.summary.with_suffix(".md")
        if report.is_file():
            artifacts.append(report)
        artifacts.extend(args.artifact)
        tracker = MlflowTracker(args.tracking_uri, args.experiment)
        run_id = log_evaluation_run(
            summary,
            tracker=tracker,
            run_name=args.run_name,
            dataset_sha256=args.dataset_sha256,
            artifacts=artifacts,
        )
        print(f"run_id={run_id}")
        return 0
    if args.command == "compare":
        tracker = MlflowTracker(args.tracking_uri)
        print(render_comparison(compare_runs(args.run_id, tracker)))
        return 0
    if args.command == "benchmark":
        return _run_benchmark(args)
    if args.command == "register":
        return _run_register(args)
    raise TrackingError(f"Comando no soportado: {args.command}")


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada de la CLI."""
    try:
        return _run(argv)
    except TrackingError as exc:
        print(f"error: {exc}")
        return 1
