"""Carga y validación de imágenes JPEG/PNG."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from ppe_detection.contracts import ImageData

JPEG_MAGIC = b"\xff\xd8\xff"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SUPPORTED_SUFFIXES = frozenset({".jpg", ".jpeg", ".png"})

#: Límite de entrada alineado con `MAX_BYTES` del frontend (10 MB).
MAX_IMAGE_BYTES = 10 * 1024 * 1024


class InvalidImageError(ValueError):
    """La entrada no es una imagen JPEG/PNG válida."""


def _detect_format(data: bytes) -> str:
    if data.startswith(JPEG_MAGIC):
        return "jpeg"
    if data.startswith(PNG_MAGIC):
        return "png"
    raise InvalidImageError("Formato no admitido: se aceptan JPEG y PNG.")


def _check_size(size: int, max_bytes: int = MAX_IMAGE_BYTES) -> None:
    """Rechaza entradas vacías o mayores que el límite configurado."""
    if size == 0:
        raise InvalidImageError("El archivo está vacío.")
    if size > max_bytes:
        limit = max_bytes // (1024 * 1024)
        raise InvalidImageError(f"La imagen supera el límite de {limit} MB.")


def _decode(data: bytes, source: str) -> ImageData:
    _check_size(len(data))
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
    _check_size(file_path.stat().st_size)
    return _decode(file_path.read_bytes(), str(file_path))


def validate_image_bytes(
    data: bytes,
    source: str = "upload",
    max_bytes: int = MAX_IMAGE_BYTES,
) -> ImageData:
    """Valida y decodifica una imagen recibida (JPEG/PNG, hasta 10 MB).

    No importa ni ejecuta el detector: solo comprueba el tamaño, el formato por
    contenido y la decodificación.
    """
    _check_size(len(data), max_bytes)
    return _decode(data, source)


def load_image_bytes(data: bytes, source: str = "bytes") -> ImageData:
    """Carga una imagen JPEG/PNG desde bytes (API o interfaz)."""
    return validate_image_bytes(data, source=source)


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
