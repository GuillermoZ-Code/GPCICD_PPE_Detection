"""Casos borde de módulos puros para el cierre del M4 (frente de pruebas).

Cubre geometría, contrato de resultado, letterbox y umbrales por clase sin modificar
el código de producción. Cada prueba sigue el patrón AAA.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, cast

import numpy as np
import pytest

from ppe_detection.contracts import CLASSES, Detection
from ppe_detection.geometry import (
    clip_xyxy,
    is_degenerate,
    letterbox_box,
    letterbox_params,
    scale_xyxy,
    xywh_to_xyxy,
    xyxy_to_xywh,
)
from ppe_detection.postprocessing.thresholds import (
    ThresholdConfig,
    ThresholdConfigError,
    apply_thresholds,
    load_threshold_config,
)
from ppe_detection.preprocessing.letterbox import (
    PreprocessingError,
    inverse_letterbox_boxes,
    letterbox,
    normalize_image,
)
from ppe_detection.results import (
    NO_DETECTIONS_MESSAGE,
    build_error_result,
    build_inference_result,
)


def _detection(
    class_id: int = 0,
    confidence: float = 0.5,
    bbox: tuple[float, float, float, float] = (1.0, 1.0, 10.0, 10.0),
) -> Detection:
    """Detección válida para las pruebas."""
    return Detection(
        class_id=class_id,
        class_name=CLASSES[class_id],
        confidence=confidence,
        bbox=bbox,
        image_width=100,
        image_height=100,
    )


# --- geometría ---------------------------------------------------------------


def test_xyxy_to_xywh_converts() -> None:
    # Act
    box = xyxy_to_xywh((2.0, 4.0, 12.0, 20.0))

    # Assert
    assert box == (2.0, 4.0, 10.0, 16.0)


def test_xywh_round_trip_restores_box() -> None:
    # Arrange
    original = (1.5, 2.5, 30.0, 40.0)

    # Act
    restored = xywh_to_xyxy(xyxy_to_xywh(original))

    # Assert
    assert restored == original


def test_box_rejects_wrong_length() -> None:
    # Act / Assert
    with pytest.raises(ValueError, match="cuatro"):
        xyxy_to_xywh(cast("Any", (1.0, 2.0, 3.0)))


def test_box_rejects_non_finite() -> None:
    # Act / Assert
    with pytest.raises(ValueError, match="finitos"):
        xyxy_to_xywh((0.0, 0.0, math.inf, 10.0))


def test_clip_clamps_negative_coordinates() -> None:
    # Act
    box = clip_xyxy((-5.0, -2.0, 10.0, 20.0), 100, 50)

    # Assert
    assert box == (0.0, 0.0, 10.0, 20.0)


def test_clip_clamps_overflow() -> None:
    # Act
    box = clip_xyxy((90.0, 40.0, 400.0, 500.0), 100, 50)

    # Assert
    assert box == (90.0, 40.0, 100.0, 50.0)


def test_clip_rejects_zero_width() -> None:
    # Act / Assert
    with pytest.raises(ValueError, match="positivos"):
        clip_xyxy((0.0, 0.0, 1.0, 1.0), 0, 50)


def test_is_degenerate_detects_zero_width() -> None:
    # Act / Assert
    assert is_degenerate((5.0, 5.0, 5.0, 20.0)) is True


def test_is_degenerate_honors_min_size() -> None:
    # Arrange
    box = (0.0, 0.0, 4.0, 4.0)

    # Act / Assert
    assert is_degenerate(box, min_size=5.0) is True
    assert is_degenerate(box, min_size=3.0) is False


def test_scale_scales_both_axes() -> None:
    # Act
    box = scale_xyxy((1.0, 2.0, 3.0, 4.0), 2.0, 0.5)

    # Assert
    assert box == (2.0, 1.0, 6.0, 2.0)


@pytest.mark.parametrize(("scale_x", "scale_y"), [(0.0, 1.0), (1.0, -1.0), (math.inf, 1.0)])
def test_scale_rejects_non_positive_or_infinite(scale_x: float, scale_y: float) -> None:
    # Act / Assert
    with pytest.raises(ValueError, match="positivos"):
        scale_xyxy((0.0, 0.0, 1.0, 1.0), scale_x, scale_y)


def test_letterbox_params_landscape_pads_vertically() -> None:
    # Act
    scale, pad_x, pad_y = letterbox_params(1280, 720, 640)

    # Assert
    assert scale == 0.5
    assert pad_x == 0.0
    assert pad_y == 140.0


def test_letterbox_params_portrait_pads_horizontally() -> None:
    # Act
    scale, pad_x, pad_y = letterbox_params(720, 1280, 640)

    # Assert
    assert scale == 0.5
    assert pad_x == 140.0
    assert pad_y == 0.0


def test_letterbox_params_rejects_zero() -> None:
    # Act / Assert
    with pytest.raises(ValueError, match="positivos"):
        letterbox_params(0, 720, 640)


def test_letterbox_box_matches_params() -> None:
    # Act
    box = letterbox_box((128.0, 72.0, 256.0, 144.0), 1280, 720, 640)

    # Assert
    assert box == (64.0, 176.0, 128.0, 212.0)


# --- contrato de resultado ---------------------------------------------------


def test_result_none_is_error() -> None:
    # Act
    result = build_inference_result(None)

    # Assert
    assert result.is_error is True
    assert result.is_empty is False
    assert result.detections == ()


def test_result_empty_is_not_error() -> None:
    # Act
    result = build_inference_result([])

    # Assert
    assert result.is_error is False
    assert result.is_empty is True
    assert result.message == NO_DETECTIONS_MESSAGE


def test_result_single_message() -> None:
    # Act
    result = build_inference_result([_detection(class_id=3)])

    # Assert
    assert result.message == "Se detectó 1 objeto EPP: helmet (x1)."


def test_result_plural_message() -> None:
    # Arrange
    detections = [_detection(class_id=1), _detection(class_id=1)]

    # Act
    result = build_inference_result(detections)

    # Assert
    assert result.message == "Se detectaron 2 objetos EPP: Vest (x2)."


def test_result_orders_by_canonical_class() -> None:
    # Arrange: Vest (1) y Gloves (0), en orden inverso al catálogo
    detections = [_detection(class_id=1), _detection(class_id=0)]

    # Act
    result = build_inference_result(detections)

    # Assert
    assert result.message == "Se detectaron 2 objetos EPP: Gloves (x1), Vest (x1)."


def test_result_counts_repeated_class() -> None:
    # Arrange
    detections = [_detection(class_id=0), _detection(class_id=0), _detection(class_id=5)]

    # Act
    result = build_inference_result(detections)

    # Assert
    assert "Gloves (x2)" in result.message
    assert "safety_shoe (x1)" in result.message


def test_error_result_uses_exception_name() -> None:
    # Act
    result = build_error_result(FileNotFoundError("sin modelo"))

    # Assert
    assert result.is_error is True
    assert "FileNotFoundError" in result.message


def test_result_preserves_detections() -> None:
    # Arrange
    detections = [_detection(), _detection(class_id=4)]

    # Act
    result = build_inference_result(detections)

    # Assert
    assert result.detections == tuple(detections)


# --- letterbox ----------------------------------------------------------------


def test_letterbox_square_has_no_padding() -> None:
    # Arrange
    image = np.zeros((640, 640, 3), dtype=np.uint8)

    # Act
    result = letterbox(image)

    # Assert
    assert result.image.shape == (640, 640, 3)
    assert result.scale == 1.0
    assert result.padding == (0, 0)


def test_letterbox_landscape_pads_vertically() -> None:
    # Arrange
    image = np.zeros((720, 1280, 3), dtype=np.uint8)

    # Act
    result = letterbox(image)

    # Assert
    assert result.image.shape == (640, 640, 3)
    assert result.scale == 0.5
    assert result.padding == (0, 140)


def test_letterbox_portrait_pads_horizontally() -> None:
    # Arrange
    image = np.zeros((1280, 720, 3), dtype=np.uint8)

    # Act
    result = letterbox(image)

    # Assert
    assert result.image.shape == (640, 640, 3)
    assert result.padding == (140, 0)


def test_letterbox_without_scaleup_keeps_size() -> None:
    # Arrange
    image = np.zeros((240, 320, 3), dtype=np.uint8)

    # Act
    result = letterbox(image, scaleup=False)

    # Assert
    assert result.scale == 1.0
    assert result.image.shape == (640, 640, 3)
    assert result.padding == (160, 200)


def test_letterbox_rounds_target_to_stride() -> None:
    # Arrange
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Act
    result = letterbox(image, new_shape=300)

    # Assert
    assert result.target_width == 320
    assert result.target_height == 320
    assert result.image.shape == (320, 320, 3)


def test_letterbox_accepts_height_width_tuple() -> None:
    # Arrange
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Act
    result = letterbox(image, new_shape=(320, 480))

    # Assert
    assert result.image.shape == (320, 480, 3)
    assert result.target_width == 480
    assert result.target_height == 320


def test_letterbox_rejects_float_image() -> None:
    # Arrange
    image = np.zeros((10, 10, 3), dtype=np.float32)

    # Act / Assert
    with pytest.raises(PreprocessingError, match="uint8"):
        letterbox(image)


def test_letterbox_rejects_two_dimensional_image() -> None:
    # Arrange
    image = np.zeros((10, 10), dtype=np.uint8)

    # Act / Assert
    with pytest.raises(PreprocessingError, match="forma"):
        letterbox(image)


def test_normalize_image_dtype_and_range() -> None:
    # Arrange
    image = np.full((2, 2, 3), 255, dtype=np.uint8)

    # Act
    normalized = normalize_image(image)

    # Assert
    assert normalized.dtype == np.float32
    assert float(normalized.max()) == 1.0
    assert float(normalized.min()) == 1.0


def test_inverse_boxes_restore_positions() -> None:
    # Arrange
    image = np.zeros((200, 100, 3), dtype=np.uint8)
    result = letterbox(image)

    # Act
    boxes = inverse_letterbox_boxes([(160.0, 0.0, 480.0, 640.0)], result)

    # Assert
    assert boxes == [(0.0, 0.0, 100.0, 200.0)]


def test_inverse_boxes_clip_out_of_bounds() -> None:
    # Arrange
    image = np.zeros((200, 100, 3), dtype=np.uint8)
    result = letterbox(image)

    # Act
    boxes = inverse_letterbox_boxes([(-100.0, -100.0, 1000.0, 1000.0)], result)

    # Assert
    assert boxes == [(0.0, 0.0, 100.0, 200.0)]


def test_inverse_boxes_reject_bad_shape() -> None:
    # Arrange
    image = np.zeros((200, 100, 3), dtype=np.uint8)
    result = letterbox(image)

    # Act / Assert
    with pytest.raises(PreprocessingError, match="N, 4"):
        inverse_letterbox_boxes(cast("Any", [(1.0, 2.0, 3.0)]), result)


# --- umbrales por clase -------------------------------------------------------


def test_threshold_config_rejects_missing_class() -> None:
    # Arrange
    thresholds = dict.fromkeys(CLASSES[1:], 0.25)

    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="faltan"):
        ThresholdConfig(thresholds)


def test_threshold_config_rejects_extra_class() -> None:
    # Arrange
    thresholds = {**dict.fromkeys(CLASSES, 0.25), "person": 0.25}

    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="sobran"):
        ThresholdConfig(thresholds)


def test_threshold_config_rejects_out_of_range() -> None:
    # Arrange
    thresholds = dict.fromkeys(CLASSES, 0.25)
    thresholds["helmet"] = 1.5

    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="Umbral inválido"):
        ThresholdConfig(thresholds)


def test_threshold_config_rejects_bool() -> None:
    # Arrange
    thresholds = dict.fromkeys(CLASSES, 0.25)
    thresholds["helmet"] = True

    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="Umbral inválido"):
        ThresholdConfig(thresholds)


def test_threshold_config_default_is_quarter() -> None:
    # Act
    config = ThresholdConfig.default()

    # Assert
    assert set(config.thresholds) == set(CLASSES)
    assert all(value == 0.25 for value in config.thresholds.values())


def test_load_explicit_missing_file_raises(tmp_path: Path) -> None:
    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="No existe"):
        load_threshold_config(tmp_path / "no-existe.yaml")


def test_apply_thresholds_filters_low_confidence() -> None:
    # Arrange
    config = ThresholdConfig(dict.fromkeys(CLASSES, 0.5))
    low = _detection(confidence=0.4)
    high = _detection(confidence=0.6)

    # Act
    kept = apply_thresholds([low, high], config)

    # Assert
    assert kept == [high]


def test_apply_thresholds_keeps_on_boundary() -> None:
    # Arrange
    config = ThresholdConfig(dict.fromkeys(CLASSES, 0.5))
    detection = _detection(confidence=0.5)

    # Act
    kept = apply_thresholds([detection], config)

    # Assert
    assert kept == [detection]


def test_apply_thresholds_preserves_order() -> None:
    # Arrange
    config = ThresholdConfig(dict.fromkeys(CLASSES, 0.1))
    first = _detection(confidence=0.9)
    second = _detection(class_id=1, confidence=0.7)

    # Act
    kept = apply_thresholds([first, second], config)

    # Assert
    assert kept == [first, second]


def test_apply_thresholds_empty_sequence() -> None:
    # Arrange
    config = ThresholdConfig.default()

    # Act / Assert
    assert apply_thresholds([], config) == []


def test_threshold_config_accepts_valid_map() -> None:
    # Arrange
    thresholds = dict.fromkeys(CLASSES, 0.3)

    # Act
    config = ThresholdConfig(thresholds)

    # Assert
    assert config.thresholds["mask"] == 0.3
