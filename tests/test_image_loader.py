"""Pruebas de carga y validación de imágenes (HU-001)."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from ppe_detection.contracts import FakeDetector
from ppe_detection.io.images import InvalidImageError, load_image, load_image_bytes


def _encode(array_rgb: np.ndarray, extension: str, params: list[int] | None = None) -> bytes:
    bgr = cv2.cvtColor(array_rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(extension, bgr, params or [])
    assert ok
    return buffer.tobytes()


def _write(path: Path, data: bytes) -> Path:
    path.write_bytes(data)
    return path


def _rgb(width: int = 8, height: int = 6) -> np.ndarray:
    array = np.zeros((height, width, 3), dtype=np.uint8)
    array[0, 0] = (255, 0, 0)
    array[0, 1] = (0, 255, 0)
    array[0, 2] = (0, 0, 255)
    return array


def test_load_png_returns_rgb_image_data(tmp_path: Path) -> None:
    # Arrange
    path = _write(tmp_path / "image.png", _encode(_rgb(), ".png"))

    # Act
    image = load_image(path)

    # Assert
    assert image.array.shape == (6, 8, 3)
    assert image.array.dtype == np.uint8
    assert image.format == "png"
    assert image.source == str(path)
    assert image.array[0, 0].tolist() == [255, 0, 0]
    assert image.array[0, 2].tolist() == [0, 0, 255]


def test_load_jpeg_returns_rgb_image_data(tmp_path: Path) -> None:
    # Arrange
    color = np.full((6, 8, 3), (10, 120, 200), dtype=np.uint8)
    path = _write(tmp_path / "image.jpg", _encode(color, ".jpg"))

    # Act
    image = load_image(path)

    # Assert
    assert image.array.shape == (6, 8, 3)
    assert image.format == "jpeg"
    assert np.allclose(image.array[0, 0], (10, 120, 200), atol=10)


def test_preserves_original_dimensions(tmp_path: Path) -> None:
    # Arrange
    path = _write(tmp_path / "image.png", _encode(_rgb(width=13, height=7), ".png"))

    # Act
    image = load_image(path)

    # Assert
    assert (image.width, image.height) == (13, 7)


def test_load_bytes_uses_source_label() -> None:
    # Arrange
    data = _encode(_rgb(), ".png")

    # Act
    image = load_image_bytes(data, source="upload")

    # Assert
    assert image.source == "upload"
    assert image.format == "png"


def test_format_is_detected_by_content_not_extension(tmp_path: Path) -> None:
    # Arrange
    path = _write(tmp_path / "image.jpg", _encode(_rgb(), ".png"))

    # Act
    image = load_image(path)

    # Assert
    assert image.format == "png"


def test_empty_file_is_rejected(tmp_path: Path) -> None:
    # Arrange
    path = _write(tmp_path / "empty.png", b"")

    # Act / Assert
    with pytest.raises(InvalidImageError):
        load_image(path)


def test_corrupt_file_is_rejected(tmp_path: Path) -> None:
    # Arrange
    path = _write(tmp_path / "corrupt.png", b"no es una imagen")

    # Act / Assert
    with pytest.raises(InvalidImageError):
        load_image(path)


def test_unsupported_format_is_rejected(tmp_path: Path) -> None:
    # Arrange
    path = _write(tmp_path / "image.bmp", _encode(_rgb(), ".bmp"))

    # Act / Assert
    with pytest.raises(InvalidImageError):
        load_image(path)


def test_missing_file_is_rejected(tmp_path: Path) -> None:
    # Arrange
    path = tmp_path / "missing.png"

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        load_image(path)


def test_directory_is_rejected(tmp_path: Path) -> None:
    # Arrange
    directory = tmp_path / "carpeta"
    directory.mkdir()

    # Act / Assert
    with pytest.raises(InvalidImageError):
        load_image(directory)


def test_loading_does_not_invoke_detector(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    path = _write(tmp_path / "image.png", _encode(_rgb(), ".png"))

    def _boom(self: FakeDetector, *_args: object, **_kwargs: object) -> None:
        raise AssertionError("la carga no debe ejecutar inferencia")

    monkeypatch.setattr(FakeDetector, "detect", _boom)

    # Act
    image = load_image(path)

    # Assert
    assert image.width == 8
