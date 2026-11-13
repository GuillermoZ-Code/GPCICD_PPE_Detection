"""Registro de evaluaciones y comparación de runs en MLflow (HU-009).

El módulo no importa MLflow hasta que se usa ``MlflowTracker``. El paquete base y
las pruebas unitarias funcionan con un tracker inyectado; MLflow vive en el extra
``tracking``.
"""

from __future__ import annotations

import argparse
import importlib
import json
import math
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

DEFAULT_TRACKING_URI = "sqlite:///mlflow.db"
DEFAULT_EXPERIMENT = "ppe-detection-eval"

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
    return parser


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parsea los argumentos de la CLI."""
    return build_parser().parse_args(argv)


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
    raise TrackingError(f"Comando no soportado: {args.command}")


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada de la CLI."""
    try:
        return _run(argv)
    except TrackingError as exc:
        print(f"error: {exc}")
        return 1
