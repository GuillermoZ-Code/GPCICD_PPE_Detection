"""Evaluación reproducible del detector de EPP."""

from ppe_detection.evaluation.artifacts import (
    artifact_slug,
    collect_evaluation_artifacts,
    stable_artifact_name,
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
    "EvaluationConfig",
    "EvaluationError",
    "artifact_slug",
    "build_summary",
    "collect_evaluation_artifacts",
    "evaluate",
    "render_markdown",
    "sha256_file",
    "stable_artifact_name",
    "validate_model_names",
]
