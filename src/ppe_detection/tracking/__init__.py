"""Registro y comparación de experimentos en MLflow (HU-009)."""

from ppe_detection.tracking.mlflow_tracker import (
    DEFAULT_EXPERIMENT,
    DEFAULT_TRACKING_URI,
    MlflowTracker,
    RunPayload,
    RunTracker,
    RunView,
    TrackingError,
    build_run_payload,
    compare_runs,
    default_run_name,
    log_evaluation_run,
    main,
    parse_args,
    render_comparison,
)

__all__ = [
    "DEFAULT_EXPERIMENT",
    "DEFAULT_TRACKING_URI",
    "MlflowTracker",
    "RunPayload",
    "RunTracker",
    "RunView",
    "TrackingError",
    "build_run_payload",
    "compare_runs",
    "default_run_name",
    "log_evaluation_run",
    "main",
    "parse_args",
    "render_comparison",
]
