"""Pruebas del dibujo de detecciones sobre la imagen (HU-003)."""

from __future__ import annotations

import numpy as np

from ppe_detection.contracts import CLASSES, Detection, ImageData
from ppe_detection.visualization.overlay import (
    COLORS,
    DISPLAY_NAMES,
    draw_detections,
    format_label,
)


def _image(width: int = 100, height: int = 100) -> ImageData:
    return ImageData(
        array=np.zeros((height, width, 3), dtype=np.uint8),
        width=width,
        height=height,
        format="png",
        source="test",
    )


def _detection(
    bbox: tuple[float, float, float, float] = (10.0, 50.0, 30.0, 70.0),
    *,
    class_id: int = 3,
    class_name: str = "helmet",
    confidence: float = 0.87,
    image_width: int = 100,
    image_height: int = 100,
) -> Detection:
    return Detection(
        class_id=class_id,
        class_name=class_name,
        confidence=confidence,
        bbox=bbox,
        image_width=image_width,
        image_height=image_height,
    )


def test_every_class_has_a_display_name() -> None:
    # Arrange / Act / Assert
    assert set(CLASSES) == set(DISPLAY_NAMES)
    assert set(CLASSES) == set(COLORS)


def test_empty_detections_return_unchanged_image() -> None:
    # Arrange
    image = _image()

    # Act
    result = draw_detections(image, [])

    # Assert
    assert result is not image
    assert np.array_equal(result.array, image.array)
    assert (result.width, result.height, result.format) == (100, 100, "png")


def test_draws_box_at_expected_pixels() -> None:
    # Arrange
    image = _image()
    detection = _detection()

    # Act
    result = draw_detections(image, [detection])

    # Assert: la esquina superior izquierda de la caja cae en (x=10, y=50).
    assert result.array[50, 10].tolist() == list(COLORS["helmet"])
    assert result.array[60, 25].tolist() == [0, 0, 0]


def test_scales_when_canvas_differs() -> None:
    # Arrange: la detección se midió en 100x100 y se dibuja sobre 200x200.
    image = _image(width=200, height=200)
    detection = _detection(bbox=(10.0, 20.0, 30.0, 40.0))

    # Act
    result = draw_detections(image, [detection])

    # Assert: la caja se duplica y su esquina cae en (x=20, y=40).
    assert result.array[40, 20].tolist() == list(COLORS["helmet"])


def test_format_label() -> None:
    # Arrange
    detection = _detection()

    # Act
    label = format_label(detection)

    # Assert
    assert label == "Casco 0.87"


def test_does_not_modify_input() -> None:
    # Arrange
    image = _image()
    before = image.array.copy()

    # Act
    draw_detections(image, [_detection()])

    # Assert
    assert np.array_equal(image.array, before)


def test_tiny_image_is_supported() -> None:
    # Arrange
    image = _image(width=1, height=1)
    detection = _detection(bbox=(0.0, 0.0, 1.0, 1.0), image_width=1, image_height=1)

    # Act
    result = draw_detections(image, [detection])

    # Assert
    assert result.array.shape == (1, 1, 3)
