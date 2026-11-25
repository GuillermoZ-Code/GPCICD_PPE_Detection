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
    "GroundTruthBox",
    "ImageAnnotations",
    "PredictionBox",
    "analyze_errors",
    "GroundTruth",
    "ImageRecord",
    "Prediction",
    "ThresholdMetrics",
    "build_summary",
    "calibrate_thresholds",
    "calibration_payload",
    "evaluate",
    "render_error_report",
    "evaluate_thresholds",
    "load_thresholds",
    "render_markdown",
    "sha256_file",
    "threshold_map",
    "validate_model_names",
    "write_thresholds",
]
