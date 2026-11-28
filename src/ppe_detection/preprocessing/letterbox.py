"""Preprocesamiento con letterbox y contrato numérico (HU-035).

La entrada es una imagen RGB ``uint8`` en formato HWC. El letterbox conserva la
relación de aspecto, centra la imagen en un lienzo y devuelve la escala y el padding
necesarios para invertir las coordenadas de las detecciones.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

import cv2
import numpy as np

DEFAULT_SIZE: Final = 640
DEFAULT_PADDING: Final = (114, 114, 114)
DEFAULT_STRIDE: Final = 32


class PreprocessingError(ValueError):
    """La imagen o los parámetros del letterbox no son válidos."""


@dataclass(frozen=True, slots=True)
class LetterboxResult:
    """Imagen transformada y metadatos para invertir las coordenadas."""

    image: np.ndarray
    scale: float
    pad_x: int
    pad_y: int
    original_width: int
    original_height: int
    target_width: int
    target_height: int

    @property
    def padding(self) -> tuple[int, int]:
        """Padding horizontal y vertical aplicado a la imagen."""
        return self.pad_x, self.pad_y


def _validate_image(image: np.ndarray) -> None:
    if not isinstance(image, np.ndarray):
        raise PreprocessingError("image debe ser un numpy.ndarray")
    if image.dtype != np.uint8:
        raise PreprocessingError("image debe ser uint8")
    if image.ndim != 3 or image.shape[2] != 3:
        raise PreprocessingError("image debe tener forma (alto, ancho, 3)")
    if image.shape[0] <= 0 or image.shape[1] <= 0:
        raise PreprocessingError("las dimensiones de la imagen deben ser positivas")


def _target_shape(new_shape: int | tuple[int, int], stride: int) -> tuple[int, int]:
    if isinstance(new_shape, int):
        width = height = new_shape
    elif len(new_shape) == 2:
        height, width = (int(new_shape[0]), int(new_shape[1]))
    else:
        raise PreprocessingError("new_shape debe ser un entero o (alto, ancho)")
    if width <= 0 or height <= 0:
        raise PreprocessingError("new_shape debe ser positivo")
    if stride > 0:
        width = ((width + stride - 1) // stride) * stride
        height = ((height + stride - 1) // stride) * stride
    return width, height


def letterbox(
    image: np.ndarray,
    *,
    new_shape: int | tuple[int, int] = DEFAULT_SIZE,
    color: tuple[int, int, int] = DEFAULT_PADDING,
    scaleup: bool = True,
    stride: int = DEFAULT_STRIDE,
) -> LetterboxResult:
    """Redimensiona con padding centrado y devuelve la transformación inversa."""
    _validate_image(image)
    target_width, target_height = _target_shape(new_shape, stride)
    original_height, original_width = image.shape[:2]
    scale = min(target_width / original_width, target_height / original_height)
    if not scaleup:
        scale = min(scale, 1.0)
    resized_width = max(1, round(original_width * scale))
    resized_height = max(1, round(original_height * scale))
    resized = cv2.resize(image, (resized_width, resized_height), interpolation=cv2.INTER_LINEAR)

    horizontal = target_width - resized_width
    vertical = target_height - resized_height
    pad_x = horizontal // 2
    pad_y = vertical // 2
    padded = cv2.copyMakeBorder(
        resized,
        pad_y,
        vertical - pad_y,
        pad_x,
        horizontal - pad_x,
        cv2.BORDER_CONSTANT,
        value=color,
    )
    return LetterboxResult(
        image=padded,
        scale=scale,
        pad_x=pad_x,
        pad_y=pad_y,
        original_width=original_width,
        original_height=original_height,
        target_width=target_width,
        target_height=target_height,
    )


def inverse_letterbox_boxes(
    boxes: np.ndarray | list[tuple[float, float, float, float]],
    result: LetterboxResult,
) -> list[tuple[float, float, float, float]]:
    """Convierte cajas xyxy del lienzo a la imagen original y las recorta."""
    values = np.asarray(boxes, dtype=np.float32)
    if values.ndim != 2 or values.shape[1] != 4:
        raise PreprocessingError("boxes debe tener forma (N, 4)")
    restored: list[tuple[float, float, float, float]] = []
    for x1, y1, x2, y2 in values:
        left = (float(x1) - result.pad_x) / result.scale
        top = (float(y1) - result.pad_y) / result.scale
        right = (float(x2) - result.pad_x) / result.scale
        bottom = (float(y2) - result.pad_y) / result.scale
        restored.append(
            (
                max(0.0, min(float(result.original_width), left)),
                max(0.0, min(float(result.original_height), top)),
                max(0.0, min(float(result.original_width), right)),
                max(0.0, min(float(result.original_height), bottom)),
            )
        )
    return restored


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Normaliza una imagen RGB uint8 HWC a float32 en ``[0, 1]``."""
    _validate_image(image)
    return image.astype(np.float32) / 255.0


__all__ = [
    "DEFAULT_PADDING",
    "DEFAULT_SIZE",
    "DEFAULT_STRIDE",
    "LetterboxResult",
    "PreprocessingError",
    "inverse_letterbox_boxes",
    "letterbox",
    "normalize_image",
]
