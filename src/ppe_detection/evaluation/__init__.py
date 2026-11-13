"""Evaluación reproducible del detector de EPP."""

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
    "EvaluationConfig",
    "EvaluationError",
    "build_summary",
    "evaluate",
    "render_markdown",
    "sha256_file",
    "validate_model_names",
]
