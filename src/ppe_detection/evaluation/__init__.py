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

__all__ = [
    "ErrorCase",
    "ErrorSummary",
    "EvaluationConfig",
    "EvaluationError",
    "GroundTruthBox",
    "ImageAnnotations",
    "PredictionBox",
    "analyze_errors",
    "build_summary",
    "evaluate",
    "render_error_report",
    "render_markdown",
    "sha256_file",
    "validate_model_names",
]
