"""Pruebas del contrato ImageData / Detection / Detector (TA-11)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import cast

import numpy as np
import pytest

from ppe_detection.contracts import CLASSES, Detection, FakeDetector, ImageData


def _image(width: int = 8, height: int = 6) -> ImageData:
    array = np.zeros((height, width, 3), dtype=np.uint8)
    return ImageData(array=array, width=width, height=height, format="png", source="test")


def test_classes_match_data_yaml_order() -> None:
    # Arrange / Act / Assert
    assert CLASSES == ("Gloves", "Vest", "goggles", "helmet", "mask", "safety_shoe")


def test_fake_detector_returns_list() -> None:
    # Arrange
    detection = Detection(
        class_id=0,
        class_name="Gloves",
        confidence=0.9,
        bbox=(1.0, 2.0, 3.0, 4.0),
        image_width=8,
        image_height=6,
    )
    detector = FakeDetector([detection])

    # Act
    result = detector.detect(_image())

    # Assert
    assert result == [detection]
    assert isinstance(result, list)


def test_empty_detections_returns_empty_list() -> None:
    # Arrange
    detector = FakeDetector()

    # Act
    result = detector.detect(_image())

    # Assert
    assert result == []
    assert isinstance(result, list)


def test_fake_detector_is_deterministic() -> None:
    # Arrange
    detector = FakeDetector()
    image = _image()

    # Act
    first = detector.detect(image)
    second = detector.detect(image)

    # Assert
    assert first == second


def test_detection_accepts_valid_values() -> None:
    # Arrange / Act
    detection = Detection(
        class_id=3,
        class_name="helmet",
        confidence=0.5,
        bbox=(0.0, 0.0, 8.0, 6.0),
        image_width=8,
        image_height=6,
    )

    # Assert
    assert detection.class_name == "helmet"
    assert detection.confidence == 0.5


@pytest.mark.parametrize("confidence", [-0.1, 1.1, math.nan, math.inf])
def test_detection_rejects_invalid_confidence(confidence: float) -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        Detection(
            class_id=0,
            class_name="Gloves",
            confidence=confidence,
            bbox=(1.0, 2.0, 3.0, 4.0),
            image_width=8,
            image_height=6,
        )


def test_detection_rejects_unknown_class() -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        Detection(
            class_id=0,
            class_name="Boots",
            confidence=0.9,
            bbox=(1.0, 2.0, 3.0, 4.0),
            image_width=8,
            image_height=6,
        )


def test_detection_rejects_class_id_name_mismatch() -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        Detection(
            class_id=0,
            class_name="Vest",
            confidence=0.9,
            bbox=(1.0, 2.0, 3.0, 4.0),
            image_width=8,
            image_height=6,
        )


def test_detection_rejects_inverted_bbox() -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        Detection(
            class_id=0,
            class_name="Gloves",
            confidence=0.9,
            bbox=(3.0, 2.0, 1.0, 4.0),
            image_width=8,
            image_height=6,
        )


def test_detection_rejects_bbox_outside_image() -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        Detection(
            class_id=0,
            class_name="Gloves",
            confidence=0.9,
            bbox=(0.0, 0.0, 9.0, 4.0),
            image_width=8,
            image_height=6,
        )


@pytest.mark.parametrize(
    "array",
    [
        np.zeros((6, 8, 3), dtype=np.float32),
        np.zeros((6, 8), dtype=np.uint8),
        np.zeros((6, 8, 4), dtype=np.uint8),
        np.zeros((0, 8, 3), dtype=np.uint8),
    ],
)
def test_image_data_rejects_invalid_arrays(array: np.ndarray) -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        ImageData(array=array, width=8, height=6, format="png", source="test")


def test_image_data_rejects_dimension_mismatch() -> None:
    # Arrange
    array = np.zeros((6, 8, 3), dtype=np.uint8)

    # Act / Assert
    with pytest.raises(ValueError):
        ImageData(array=array, width=9, height=6, format="png", source="test")


def test_image_data_rejects_non_int_dimensions() -> None:
    # Arrange
    array = np.zeros((6, 8, 3), dtype=np.uint8)

    # Act / Assert
    with pytest.raises(ValueError):
        ImageData(
            array=array,
            width=cast("int", 8.0),
            height=6,
            format="png",
            source="test",
        )


@pytest.mark.parametrize("image_format", ["gif", "bmp", "pdf", ""])
def test_image_data_rejects_unsupported_format(image_format: str) -> None:
    # Arrange
    array = np.zeros((6, 8, 3), dtype=np.uint8)

    # Act / Assert
    with pytest.raises(ValueError):
        ImageData(array=array, width=8, height=6, format=image_format, source="test")


def test_image_data_accepts_supported_formats() -> None:
    # Arrange
    array = np.zeros((6, 8, 3), dtype=np.uint8)

    # Act
    jpeg = ImageData(array=array, width=8, height=6, format="jpeg", source="test")
    png = ImageData(array=array, width=8, height=6, format="png", source="test")

    # Assert
    assert (jpeg.format, png.format) == ("jpeg", "png")


def test_detection_rejects_non_int_image_dimensions() -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        Detection(
            class_id=0,
            class_name="Gloves",
            confidence=0.9,
            bbox=(1.0, 2.0, 3.0, 4.0),
            image_width=cast("int", 8.5),
            image_height=6,
        )


@pytest.mark.parametrize("confidence", [True, False])
def test_detection_rejects_bool_confidence(confidence: bool) -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        Detection(
            class_id=0,
            class_name="Gloves",
            confidence=confidence,
            bbox=(1.0, 2.0, 3.0, 4.0),
            image_width=8,
            image_height=6,
        )


def test_contract_is_documented() -> None:
    # Arrange
    document = Path("docs/architecture/contracts.md")

    # Act / Assert
    assert document.exists()
    content = document.read_text(encoding="utf-8")
    assert "ImageData" in content
    assert "Detection" in content
