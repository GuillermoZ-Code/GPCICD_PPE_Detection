"""Evaluación reproducible del detector de EPP."""

from ppe_detection.evaluation.errors import (
    ErrorCase,
    ErrorSummary,
    GroundTruthBox,
    ImageAnnotations,
    PredictionBox,
    analyze_errors,
    render_error_report,
)
from ppe_detection.evaluation.evaluate import (
    EvaluationConfig,
    EvaluationError,
    build_summary,
    evaluate,
    render_markdown,
    sha256_file,
    validate_model_names,
)
from ppe_detection.evaluation.thresholds import (
    GroundTruth,
    ImageRecord,
    Prediction,
    ThresholdMetrics,
    calibrate_thresholds,
    calibration_payload,
    evaluate_thresholds,
    load_thresholds,
    threshold_map,
    write_thresholds,
)

__all__ = [
    "ErrorCase",
    "ErrorSummary",
    "EvaluationConfig",
    "EvaluationError",
    "GroundTruth",
    "GroundTruthBox",
    "ImageAnnotations",
    "ImageRecord",
    "Prediction",
    "PredictionBox",
    "ThresholdMetrics",
    "analyze_errors",
    "build_summary",
    "calibrate_thresholds",
    "calibration_payload",
    "evaluate",
    "evaluate_thresholds",
    "load_thresholds",
    "render_error_report",
    "render_markdown",
    "sha256_file",
    "threshold_map",
    "validate_model_names",
    "write_thresholds",
]
