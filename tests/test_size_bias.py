"""Pruebas del sesgo de tamaño por clase (HU-037)."""

from __future__ import annotations

import pytest

from ppe_detection.contracts import CLASSES
from ppe_detection.evaluation.errors import (
    GroundTruthBox,
    ImageAnnotations,
    PredictionBox,
)
from ppe_detection.evaluation.size_bias import (
    SizeBiasError,
    average_precision_by_size,
    evaluate_size_bias,
    size_bucket,
)


def _record(
    ground_truth: tuple[GroundTruthBox, ...] = (),
    predictions: tuple[PredictionBox, ...] = (),
) -> ImageAnnotations:
    return ImageAnnotations(
        image="sample.jpg",
        width=100,
        height=100,
        ground_truth=ground_truth,
        predictions=predictions,
    )


def _gt(class_name: str, bbox: tuple[float, float, float, float]) -> GroundTruthBox:
    return GroundTruthBox(class_name=class_name, bbox=bbox)


def _pred(
    class_name: str, confidence: float, bbox: tuple[float, float, float, float]
) -> PredictionBox:
    return PredictionBox(class_name=class_name, confidence=confidence, bbox=bbox)


def test_size_bucket_classifies_relative_area() -> None:
    """AC-01: las cajas se clasifican por área relativa documentada."""

    # Act / Assert
    assert size_bucket((0, 0, 10, 5), 100, 100) == "small"
    assert size_bucket((0, 0, 20, 10), 100, 100) == "medium"
    assert size_bucket((0, 0, 20, 20), 100, 100) == "large"


def test_size_bucket_rejects_invalid_parameters() -> None:
    """AC-03: dimensiones o umbrales inválidos fallan explícitamente."""

    # Act / Assert
    with pytest.raises(SizeBiasError, match="positivos"):
        size_bucket((0, 0, 1, 1), 0, 100)
    with pytest.raises(SizeBiasError, match="small_max"):
        size_bucket((0, 0, 1, 1), 100, 100, small_max=0.1, medium_max=0.05)


def test_perfect_detection_has_ap_one() -> None:
    """AC-02: una detección perfecta en un bucket produce AP 1."""

    # Arrange
    record = _record(
        (_gt("Gloves", (0, 0, 20, 20)),),
        (_pred("Gloves", 0.9, (0, 0, 20, 20)),),
    )

    # Act
    result = average_precision_by_size([record], "Gloves", "large")

    # Assert
    assert result.gt_count == 1
    assert result.average_precision == pytest.approx(1.0)
    assert result.recall == 1.0


def test_missed_detection_has_zero_ap() -> None:
    """AC-02: un objeto sin predicción en su bucket produce AP 0."""

    # Arrange
    record = _record((_gt("Gloves", (0, 0, 20, 20)),))

    # Act
    result = average_precision_by_size([record], "Gloves", "large")

    # Assert
    assert result.gt_count == 1
    assert result.predictions == 0
    assert result.average_precision == 0.0


def test_evaluate_size_bias_covers_all_classes_and_buckets() -> None:
    """AC-02: la tabla cubre las seis clases y tres buckets."""

    # Act
    table = evaluate_size_bias([_record()])

    # Assert
    assert tuple(table) == CLASSES
    assert set(table["Gloves"]) == {"small", "medium", "large"}
