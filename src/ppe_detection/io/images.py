"""Carga y validación de imágenes JPEG/PNG."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from ppe_detection.contracts import ImageData

JPEG_MAGIC = b"\xff\xd8\xff"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SUPPORTED_SUFFIXES = frozenset({".jpg", ".jpeg", ".png"})


class InvalidImageError(ValueError):
    """La entrada no es una imagen JPEG/PNG válida."""


def _detect_format(data: bytes) -> str:
    if data.startswith(JPEG_MAGIC):
        return "jpeg"
    if data.startswith(PNG_MAGIC):
        return "png"
    raise InvalidImageError("Formato no admitido: se aceptan JPEG y PNG.")


def _decode(data: bytes, source: str) -> ImageData:
    if not data:
        raise InvalidImageError("El archivo está vacío.")
    image_format = _detect_format(data)
    buffer = np.frombuffer(data, dtype=np.uint8)
    decoded = cv2.imdecode(buffer, cv2.IMREAD_COLOR)
    if decoded is None or decoded.size == 0:
        raise InvalidImageError("No se pudo decodificar la imagen.")
    rgb = cv2.cvtColor(decoded, cv2.COLOR_BGR2RGB)
    height, width = rgb.shape[:2]
    return ImageData(
        array=rgb,
        width=width,
        height=height,
        format=image_format,
        source=source,
    )


def load_image(path: str | Path) -> ImageData:
    """Carga una imagen JPEG/PNG desde una ruta sin ejecutar inferencia."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"No existe la imagen: {file_path}")
    if not file_path.is_file():
        raise InvalidImageError(f"La ruta no es un archivo: {file_path}")
    return _decode(file_path.read_bytes(), str(file_path))


def load_image_bytes(data: bytes, source: str = "bytes") -> ImageData:
    """Carga una imagen JPEG/PNG desde bytes (API o interfaz)."""
    return _decode(data, source)


def write_image(image: ImageData, path: str | Path) -> Path:
    """Guarda una ``ImageData`` en JPEG o PNG según la extensión del archivo."""
    file_path = Path(path)
    if file_path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise InvalidImageError("Extensión no admitida: usa .jpg, .jpeg o .png.")
    file_path.parent.mkdir(parents=True, exist_ok=True)
    encoded = cv2.cvtColor(image.array, cv2.COLOR_RGB2BGR)
    if not cv2.imwrite(str(file_path), encoded):
        raise InvalidImageError(f"No se pudo guardar la imagen: {file_path}")
    return file_path
