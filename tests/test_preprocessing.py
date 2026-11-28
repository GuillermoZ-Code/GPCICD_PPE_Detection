"""Pruebas del letterbox y la transformación inversa (HU-035)."""

from __future__ import annotations

import numpy as np
import pytest

from ppe_detection.preprocessing import (
    DEFAULT_PADDING,
    PreprocessingError,
    inverse_letterbox_boxes,
    letterbox,
    normalize_image,
)


def _image(height: int = 50, width: int = 100) -> np.ndarray:
    return np.zeros((height, width, 3), dtype=np.uint8)


def test_letterbox_preserves_aspect_ratio_and_shape() -> None:
    """AC-01: una imagen 100x50 se escala a 640x640 con padding vertical."""

    # Act
    result = letterbox(_image(), new_shape=640)

    # Assert
    assert result.image.shape == (640, 640, 3)
    assert result.scale == pytest.approx(6.4)
    assert result.padding == (0, 160)
    assert result.original_width == 100
    assert result.original_height == 50


def test_letterbox_uses_configured_padding_color() -> None:
    """AC-01: el padding usa el color solicitado."""

    # Act
    result = letterbox(_image(32, 64), new_shape=640, color=(7, 8, 9))

    # Assert
    assert tuple(result.image[0, 0]) == (7, 8, 9)
    assert result.image.shape == (640, 640, 3)


def test_letterbox_can_disable_scaleup() -> None:
    """AC-03: una imagen pequeña no se amplía si scaleup=False."""

    # Act
    result = letterbox(_image(16, 32), new_shape=640, scaleup=False)

    # Assert
    assert result.scale == 1.0
    assert result.image.shape == (640, 640, 3)
    assert result.image[320, 320].tolist() == [0, 0, 0]


def test_letterbox_rejects_invalid_image() -> None:
    """AC-01: una imagen que no es uint8 HWC falla explícitamente."""

    # Act / Assert
    with pytest.raises(PreprocessingError, match="uint8"):
        letterbox(np.zeros((10, 10, 3), dtype=np.float32))


def test_inverse_letterbox_restores_original_coordinates() -> None:
    """AC-02: una caja en el lienzo vuelve a las coordenadas originales."""

    # Arrange
    result = letterbox(_image(), new_shape=640)
    padded_box = [(64.0, 192.0, 128.0, 256.0)]

    # Act
    restored = inverse_letterbox_boxes(padded_box, result)

    # Assert
    assert restored[0] == pytest.approx((10.0, 5.0, 20.0, 15.0))


def test_inverse_letterbox_clips_to_original_image() -> None:
    """AC-02: una caja fuera del lienzo se recorta a la imagen original."""

    # Arrange
    result = letterbox(_image(), new_shape=640)

    # Act
    restored = inverse_letterbox_boxes([(-100.0, -100.0, 1000.0, 1000.0)], result)

    # Assert
    assert restored == [(0.0, 0.0, 100.0, 50.0)]


def test_normalize_image_returns_float32_in_unit_range() -> None:
    """AC-01: la normalización conserva HWC y devuelve float32 en [0,1]."""

    # Arrange
    image = _image(2, 3)
    image[0, 0] = (255, 128, 0)

    # Act
    normalized = normalize_image(image)

    # Assert
    assert normalized.shape == (2, 3, 3)
    assert normalized.dtype == np.float32
    assert normalized.min() == 0.0
    assert normalized.max() == 1.0
    assert normalized[0, 0].tolist() == pytest.approx([1.0, 128 / 255, 0.0])


def test_non_square_target_centers_padding() -> None:
    """AC-03: un destino no cuadrado mantiene padding centrado."""

    # Act
    result = letterbox(_image(), new_shape=(640, 320), stride=32)

    # Assert
    assert result.image.shape == (640, 320, 3)
    assert result.scale == pytest.approx(3.2)
    assert result.padding == (0, 240)
    assert tuple(result.image[0, 0]) == DEFAULT_PADDING
