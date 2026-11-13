"""Pruebas de validación de imágenes recibidas (HU-005)."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from ppe_detection.contracts import FakeDetector
from ppe_detection.io import MAX_IMAGE_BYTES, load_image, load_image_bytes, validate_image_bytes
from ppe_detection.io.images import InvalidImageError


def _png_bytes(width: int = 8, height: int = 6) -> bytes:
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[0, 0] = (255, 0, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".png", bgr)
    assert ok
    return buffer.tobytes()


def test_corrupt_upload_is_rejected_without_detector(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC-01: un archivo corrupto se rechaza y el detector no se ejecuta."""
    # Arrange
    monkeypatch.setattr(FakeDetector, "detect", lambda *_: pytest.fail("detector invocado"))

    # Act / Assert
    with pytest.raises(InvalidImageError, match="Formato no admitido"):
        validate_image_bytes(b"no es una imagen")


def test_empty_upload_is_rejected() -> None:
    """AC-02: un archivo vacío se rechaza con un mensaje comprensible."""
    # Act / Assert
    with pytest.raises(InvalidImageError, match="vac"):
        validate_image_bytes(b"")


def test_valid_upload_returns_image_for_preprocessing() -> None:
    """AC-03: una imagen JPEG/PNG válida se entrega al preprocesamiento."""
    # Arrange
    data = _png_bytes(width=13, height=7)

    # Act
    image = validate_image_bytes(data, source="upload")

    # Assert
    assert image.source == "upload"
    assert image.format == "png"
    assert image.array.shape == (7, 13, 3)
    assert image.array.dtype == np.uint8


def test_oversized_upload_is_rejected() -> None:
    """FR-002: un archivo mayor de 10 MB se rechaza antes de decodificar."""
    # Arrange
    data = b"\xff\xd8\xff" + b"0" * MAX_IMAGE_BYTES

    # Act / Assert
    with pytest.raises(InvalidImageError, match="10 MB"):
        validate_image_bytes(data)


def test_unsupported_format_is_rejected() -> None:
    """FR-002: un formato distinto de JPEG/PNG se rechaza por su contenido."""
    # Act / Assert
    with pytest.raises(InvalidImageError, match="Formato no admitido"):
        validate_image_bytes(b"GIF89a" + b"\x00" * 16)


def test_load_image_bytes_uses_the_same_limit() -> None:
    """FR-004: la carga desde bytes comparte el límite de la validación."""
    # Arrange
    data = b"\xff\xd8\xff" + b"0" * MAX_IMAGE_BYTES

    # Act / Assert
    with pytest.raises(InvalidImageError, match="10 MB"):
        load_image_bytes(data)


def test_load_image_rejects_an_oversized_file(tmp_path: Path) -> None:
    """FR-004: la carga desde disco rechaza archivos mayores de 10 MB."""
    # Arrange
    path = tmp_path / "grande.jpg"
    path.write_bytes(b"\xff\xd8\xff" + b"0" * MAX_IMAGE_BYTES)

    # Act / Assert
    with pytest.raises(InvalidImageError, match="10 MB"):
        load_image(path)
