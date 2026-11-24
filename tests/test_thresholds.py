"""Pruebas de calibración de umbrales por clase (HU-029)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ppe_detection.contracts import CLASSES
from ppe_detection.evaluation.thresholds import (
    DEFAULT_THRESHOLD,
    GroundTruth,
    ImageRecord,
    Prediction,
    calibrate_thresholds,
    calibration_payload,
    evaluate_thresholds,
    load_thresholds,
    threshold_map,
    write_thresholds,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _gt(class_name: str, bbox: tuple[float, float, float, float]) -> GroundTruth:
    return GroundTruth(class_name=class_name, bbox=bbox)


def _pred(
    class_name: str, confidence: float, bbox: tuple[float, float, float, float]
) -> Prediction:
    return Prediction(class_name=class_name, confidence=confidence, bbox=bbox)


def _record(
    ground_truth: tuple[GroundTruth, ...] = (),
    predictions: tuple[Prediction, ...] = (),
) -> ImageRecord:
    return ImageRecord(ground_truth=ground_truth, predictions=predictions)


def test_calibrate_maximizes_f1_for_gloves() -> None:
    """AC-01: el umbral elegido elimina el falso positivo y maximiza F1."""

    # Arrange
    record = _record(
        ground_truth=(_gt("Gloves", (0, 0, 10, 10)),),
        predictions=(
            _pred("Gloves", 0.40, (0, 0, 10, 10)),
            _pred("Gloves", 0.10, (50, 50, 60, 60)),
        ),
    )

    # Act
    result = calibrate_thresholds([record], thresholds=(0.05, 0.10, 0.40, 0.50, 0.90))

    # Assert
    assert result["Gloves"].threshold == 0.40
    assert result["Gloves"].f1 == pytest.approx(1.0)
    assert result["Gloves"].tp == 1
    assert result["Gloves"].fp == 0


def test_calibrate_uses_all_validation_records() -> None:
    """AC-01: una predicción débil en otra imagen impide bajar el umbral."""

    # Arrange
    records = [
        _record(
            ground_truth=(_gt("Vest", (0, 0, 10, 10)),),
            predictions=(_pred("Vest", 0.80, (0, 0, 10, 10)),),
        ),
        _record(
            ground_truth=(_gt("Vest", (20, 20, 30, 30)),),
            predictions=(_pred("Vest", 0.20, (40, 40, 50, 50)),),
        ),
    ]

    # Act
    result = calibrate_thresholds(records, thresholds=(0.10, 0.30, 0.50, 0.80, 0.90))

    # Assert
    assert result["Vest"].threshold == 0.80
    assert result["Vest"].tp == 1
    assert result["Vest"].fp == 0
    assert result["Vest"].fn == 1


def test_calibrate_handles_class_without_ground_truth() -> None:
    """AC-01: una clase sin etiquetas conserva el umbral por defecto."""

    # Arrange
    record = _record(predictions=(_pred("mask", 0.90, (0, 0, 10, 10)),))

    # Act
    result = calibrate_thresholds([record], thresholds=(0.10, 0.50, 0.90))

    # Assert
    assert result["mask"].threshold == DEFAULT_THRESHOLD
    assert result["mask"].f1 == 0.0


def test_calibrate_handles_class_without_predictions() -> None:
    """AC-01: una clase sin predicciones conserva el umbral por defecto."""

    # Arrange
    record = _record(ground_truth=(_gt("helmet", (0, 0, 10, 10)),))

    # Act
    result = calibrate_thresholds([record], thresholds=(0.10, 0.50, 0.90))

    # Assert
    assert result["helmet"].threshold == DEFAULT_THRESHOLD
    assert result["helmet"].recall == 0.0


def test_calibrate_ties_prefer_higher_threshold() -> None:
    """AC-01: con el mismo F1 se prefiere el umbral más alto."""

    # Arrange
    record = _record(
        ground_truth=(_gt("goggles", (0, 0, 10, 10)),),
        predictions=(_pred("goggles", 0.50, (0, 0, 10, 10)),),
    )

    # Act
    result = calibrate_thresholds([record], thresholds=(0.30, 0.50, 0.70))

    # Assert
    assert result["goggles"].threshold == 0.50
    assert result["goggles"].f1 == pytest.approx(1.0)


def test_evaluate_thresholds_returns_before_after_counts() -> None:
    """AC-02: la evaluación por umbral devuelve TP, FP, FN y P/R/F1."""

    # Arrange
    record = _record(
        ground_truth=(
            _gt("Gloves", (0, 0, 10, 10)),
            _gt("Vest", (20, 20, 30, 30)),
        ),
        predictions=(
            _pred("Gloves", 0.90, (0, 0, 10, 10)),
            _pred("Gloves", 0.80, (40, 40, 50, 50)),
            _pred("Vest", 0.80, (60, 60, 70, 70)),
        ),
    )

    # Act
    result = evaluate_thresholds([record], dict.fromkeys(CLASSES, 0.50))

    # Assert
    assert (result["Gloves"].tp, result["Gloves"].fp, result["Gloves"].fn) == (1, 1, 0)
    assert result["Gloves"].precision == pytest.approx(0.5)
    assert (result["Vest"].tp, result["Vest"].fp, result["Vest"].fn) == (0, 1, 1)
    assert result["Vest"].f1 == 0.0


def test_threshold_map_has_all_canonical_classes() -> None:
    """AC-03: el mapa exportado cubre las seis clases en orden canónico."""

    # Arrange
    record = _record(
        ground_truth=(_gt("safety_shoe", (0, 0, 10, 10)),),
        predictions=(_pred("safety_shoe", 0.60, (0, 0, 10, 10)),),
    )
    result = calibrate_thresholds([record], thresholds=(0.30, 0.60))

    # Act
    values = threshold_map(result)

    # Assert
    assert tuple(values) == CLASSES
    assert values["safety_shoe"] == 0.60


def test_write_and_load_thresholds_roundtrip(tmp_path: Path) -> None:
    """AC-03: el YAML escrito se puede consumir sin PyYAML."""

    # Arrange
    record = _record(
        ground_truth=(_gt("Gloves", (0, 0, 10, 10)),),
        predictions=(_pred("Gloves", 0.40, (0, 0, 10, 10)),),
    )
    result = calibrate_thresholds([record], thresholds=(0.20, 0.40))
    path = tmp_path / "thresholds.yaml"

    # Act
    write_thresholds(path, result)
    loaded = load_thresholds(path)

    # Assert
    assert set(loaded) == set(CLASSES)
    assert loaded["Gloves"] == 0.40
    assert "version: 1" in path.read_text(encoding="utf-8")


def test_write_thresholds_rejects_missing_class(tmp_path: Path) -> None:
    """AC-03: no se exporta un YAML incompleto."""

    # Arrange
    record = _record()
    result = evaluate_thresholds([record], dict.fromkeys(CLASSES, 0.25))
    incomplete = {key: value for key, value in result.items() if key != "mask"}

    # Act / Assert
    with pytest.raises(ValueError, match="Faltan clases"):
        write_thresholds(tmp_path / "thresholds.yaml", incomplete)


def test_calibration_payload_is_traceable() -> None:
    """AC-02: el resumen conserva split, IoU y métricas por clase."""

    # Arrange
    record = _record(
        ground_truth=(_gt("Vest", (0, 0, 10, 10)),),
        predictions=(_pred("Vest", 0.70, (0, 0, 10, 10)),),
    )
    result = calibrate_thresholds([record], thresholds=(0.50, 0.70))

    # Act
    payload = calibration_payload(result, split="valid")

    # Assert
    assert payload["split"] == "valid"
    assert payload["iou"] == 0.5
    assert payload["metrics"]["Vest"]["tp"] == 1


def test_repository_thresholds_yaml_has_six_classes() -> None:
    """AC-03: el archivo versionado contiene las seis clases."""

    # Act
    values = load_thresholds(REPO_ROOT / "configs" / "thresholds.yaml")

    # Assert
    assert tuple(values) == CLASSES
    assert all(0.0 <= value <= 1.0 for value in values.values())
