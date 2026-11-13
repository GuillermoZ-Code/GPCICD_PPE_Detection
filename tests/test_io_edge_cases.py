"""Casos límite de carga de imágenes (HU-005)."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from ppe_detection.io import load_image, load_image_bytes
from ppe_detection.io.images import InvalidImageError


def _encode(array: np.ndarray, extension: str) -> bytes:
    ok, buffer = cv2.imencode(extension, array)
    assert ok
    return buffer.tobytes()


def test_grayscale_png_is_converted_to_rgb() -> None:
    """AC-005.1: una imagen de un canal se entrega con tres canales."""
    gray = np.full((6, 8), 128, dtype=np.uint8)
    image = load_image_bytes(_encode(gray, ".png"))

    assert image.array.shape == (6, 8, 3)
    assert image.format == "png"


def test_rgba_png_drops_alpha() -> None:
    """AC-005.1: el canal alfa no llega al contrato RGB."""
    rgba = np.zeros((6, 8, 4), dtype=np.uint8)
    rgba[..., 3] = 255
    image = load_image_bytes(_encode(rgba, ".png"))

    assert image.array.shape == (6, 8, 3)


def test_uppercase_extension_is_supported(tmp_path: Path) -> None:
    """AC-005.1: la extensión no distingue mayúsculas."""
    rgb = np.zeros((6, 8, 3), dtype=np.uint8)
    path = tmp_path / "IMAGEN.PNG"
    path.write_bytes(_encode(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), ".png"))

    image = load_image(path)

    assert image.format == "png"


def test_file_without_extension_is_detected_by_content(tmp_path: Path) -> None:
    """AC-005.1: el contenido manda sobre el nombre del archivo."""
    rgb = np.zeros((6, 8, 3), dtype=np.uint8)
    path = tmp_path / "upload"
    path.write_bytes(_encode(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), ".png"))

    image = load_image(path)

    assert image.format == "png"


def test_truncated_png_is_rejected() -> None:
    """AC-005.1: una cabecera válida sin cuerpo no se acepta."""
    rgb = np.zeros((6, 8, 3), dtype=np.uint8)
    data = _encode(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), ".png")[:20]

    with pytest.raises(InvalidImageError):
        load_image_bytes(data)


def test_path_with_spaces_is_supported(tmp_path: Path) -> None:
    """AC-005.3: las rutas con espacios se cargan correctamente."""
    rgb = np.zeros((6, 8, 3), dtype=np.uint8)
    path = tmp_path / "foto con espacios.png"
    path.write_bytes(_encode(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), ".png"))

    image = load_image(path)

    assert image.width == 8


def test_path_and_bytes_produce_the_same_array(tmp_path: Path) -> None:
    """AC-005.1: la ruta y los bytes comparten la misma decodificación."""
    rgb = np.zeros((6, 8, 3), dtype=np.uint8)
    rgb[0, 0] = (1, 2, 3)
    data = _encode(cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR), ".png")
    path = tmp_path / "image.png"
    path.write_bytes(data)

    from_path = load_image(path)
    from_bytes = load_image_bytes(data, source="bytes")

    assert np.array_equal(from_path.array, from_bytes.array)
    assert from_path.source == str(path)
    assert from_bytes.source == "bytes"


def test_gif_is_rejected() -> None:
    """AC-005.1: GIF no pertenece al contrato JPEG/PNG."""
    with pytest.raises(InvalidImageError, match="Formato"):
        load_image_bytes(b"GIF89a" + b"\x00" * 32)


def test_bmp_is_rejected() -> None:
    """AC-005.1: BMP no pertenece al contrato JPEG/PNG."""
    with pytest.raises(InvalidImageError, match="Formato"):
        load_image_bytes(b"BM" + b"\x00" * 32)


def test_tiny_image_is_supported() -> None:
    """AC-005.1: una imagen de 1x1 sigue siendo válida."""
    pixel = np.array([[[255, 0, 0]]], dtype=np.uint8)
    image = load_image_bytes(_encode(cv2.cvtColor(pixel, cv2.COLOR_RGB2BGR), ".png"))

    assert (image.width, image.height) == (1, 1)
