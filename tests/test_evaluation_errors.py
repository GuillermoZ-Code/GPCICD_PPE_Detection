"""Pruebas del análisis de falsos positivos y negativos (HU-030)."""

from __future__ import annotations

from ppe_detection.evaluation.errors import (
    GroundTruthBox,
    ImageAnnotations,
    PredictionBox,
    analyze_errors,
    render_error_report,
)

SHA = "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9"


def _record(
    ground_truth: tuple[GroundTruthBox, ...] = (),
    predictions: tuple[PredictionBox, ...] = (),
    *,
    image: str = "sample.jpg",
) -> ImageAnnotations:
    return ImageAnnotations(
        image=image,
        width=100,
        height=100,
        ground_truth=ground_truth,
        predictions=predictions,
    )


def test_matched_box_counts_as_true_positive() -> None:
    """AC-01: una caja de la misma clase con IoU suficiente es TP."""

    # Arrange
    record = _record(
        (_gt("Gloves", (0, 0, 20, 20)),),
        (_pred("Gloves", 0.9, (0, 0, 20, 20)),),
    )

    # Act
    summary = analyze_errors([record], confidence=0.25)

    # Assert
    assert (summary.tp, summary.fp, summary.fn) == (1, 0, 0)
    assert summary.per_class["Gloves"]["tp"] == 1
    assert summary.precision == 1.0
    assert summary.recall == 1.0


def test_class_confusion_appears_in_fp_and_fn() -> None:
    """AC-02: una caja de otra clase se clasifica como confusión de clase."""

    # Arrange
    record = _record(
        (_gt("Vest", (0, 0, 20, 20)),),
        (_pred("Gloves", 0.9, (0, 0, 20, 20)),),
    )

    # Act
    summary = analyze_errors([record], confidence=0.25)

    # Assert
    assert summary.false_positives[0].category == "class_confusion"
    assert summary.false_negatives[0].category == "class_confusion"
    assert summary.category_counts["class_confusion"] == 2


def test_localization_error_has_partial_overlap() -> None:
    """AC-02: una caja desplazada se clasifica como localización."""

    # Arrange
    record = _record(
        (_gt("Gloves", (0, 0, 20, 20)),),
        (_pred("Gloves", 0.8, (5, 5, 25, 25)),),
    )

    # Act
    summary = analyze_errors([record], confidence=0.25, iou_threshold=0.5)

    # Assert
    assert summary.false_positives[0].category == "localization"
    assert summary.false_positives[0].overlap == 0.391304347826087


def test_small_object_fn_uses_area_ratio() -> None:
    """AC-02: un objeto menor al 1 % de la imagen se marca como pequeño."""

    # Arrange
    record = _record((_gt("safety_shoe", (0, 0, 5, 5)),))

    # Act
    summary = analyze_errors([record], confidence=0.25, small_area_ratio=0.01)

    # Assert
    assert summary.fn == 1
    assert summary.false_negatives[0].category == "small_object"
    assert summary.false_negatives[0].area_ratio == 0.0025


def test_background_fp_without_relevant_overlap() -> None:
    """AC-01: un FP sin solapamiento ni objeto pequeño es background."""

    # Arrange
    record = _record(
        (_gt("Vest", (0, 0, 20, 20)),),
        (_pred("Gloves", 0.8, (60, 60, 90, 90)),),
    )

    # Act
    summary = analyze_errors([record], confidence=0.25)

    # Assert
    assert summary.false_positives[0].category == "background"
    assert summary.false_positives[0].overlap == 0.0


def test_low_confidence_prediction_is_ignored() -> None:
    """AC-01: una predicción bajo el umbral no cuenta como FP."""

    # Arrange
    record = _record(
        (_gt("Gloves", (0, 0, 20, 20)),),
        (_pred("Gloves", 0.1, (0, 0, 20, 20)),),
    )

    # Act
    summary = analyze_errors([record], confidence=0.25)

    # Assert
    assert (summary.tp, summary.fp, summary.fn) == (0, 0, 1)


def test_analysis_is_deterministic() -> None:
    """AC-01: el mismo conjunto produce el mismo resumen dos veces."""

    # Arrange
    record = _record(
        (_gt("helmet", (0, 0, 20, 20)),),
        (_pred("helmet", 0.9, (0, 0, 20, 20)),),
    )

    # Act
    first = analyze_errors([record])
    second = analyze_errors([record])

    # Assert
    assert first == second


def test_report_has_categories_and_no_embedded_images() -> None:
    """AC-03: el informe usa texto y no incrusta imágenes."""

    # Arrange
    record = _record(
        (_gt("Gloves", (0, 0, 20, 20)),),
        (_pred("Gloves", 0.8, (5, 5, 25, 25)),),
    )
    summary = analyze_errors([record])

    # Act
    report = render_error_report(
        summary,
        model_version="yolo26n-clean",
        model_sha256=SHA,
        split="test",
    )

    # Assert
    assert "localization" in report
    assert "No se publican imágenes" in report
    assert "![" not in report
    assert "yolo26n-clean" in report


def _gt(class_name: str, bbox: tuple[float, float, float, float]) -> GroundTruthBox:
    return GroundTruthBox(class_name=class_name, bbox=bbox)


def _pred(
    class_name: str, confidence: float, bbox: tuple[float, float, float, float]
) -> PredictionBox:
    return PredictionBox(class_name=class_name, confidence=confidence, bbox=bbox)
