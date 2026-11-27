"""Estadísticas de entrada para detectar deriva (HU-038).

Calcula tamaño, relación de aspecto y brillo a partir de `ImageData` sin guardar la
imagen ni datos personales. Las funciones son puras y no conocen el modelo.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

import numpy as np

from ppe_detection.contracts import ImageData

# Coeficientes de luminancia ITU-R BT.601 para RGB.
_RED: Final = 0.299
_GREEN: Final = 0.587
_BLUE: Final = 0.114


class InputStatsError(ValueError):
    """Entrada inválida para el cálculo de estadísticas."""


@dataclass(frozen=True, slots=True)
class ImageStats:
    """Números agregados de una imagen; nunca contiene el arreglo de píxeles."""

    width: int
    height: int
    aspect_ratio: float
    brightness_mean: float
    brightness_std: float


@dataclass(frozen=True, slots=True)
class StatsSummary:
    """Resumen de un lote de imágenes para comparar contra una línea base."""

    count: int
    mean_width: float
    mean_height: float
    mean_aspect_ratio: float
    mean_brightness: float
    min_brightness: float
    max_brightness: float


def image_statistics(image: ImageData) -> ImageStats:
    """Calcula tamaño, aspecto y luminancia media/desviación de una imagen."""
    if not isinstance(image, ImageData):
        raise InputStatsError("image debe ser ImageData")
    array = image.array
    if array.dtype != np.uint8 or array.ndim != 3 or array.shape[2] != 3:
        raise InputStatsError("la imagen debe ser RGB uint8 con forma (H, W, 3)")
    rgb = array.astype(np.float64)
    luminance = _RED * rgb[:, :, 0] + _GREEN * rgb[:, :, 1] + _BLUE * rgb[:, :, 2]
    return ImageStats(
        width=image.width,
        height=image.height,
        aspect_ratio=image.width / image.height,
        brightness_mean=float(luminance.mean()),
        brightness_std=float(luminance.std()),
    )


def summarize_statistics(records: Sequence[ImageStats]) -> StatsSummary:
    """Agrega las estadísticas de un lote; no recibe ni guarda imágenes."""
    if not records:
        raise InputStatsError("se requiere al menos una imagen para resumir")
    brightness = [record.brightness_mean for record in records]
    return StatsSummary(
        count=len(records),
        mean_width=float(np.mean([record.width for record in records])),
        mean_height=float(np.mean([record.height for record in records])),
        mean_aspect_ratio=float(np.mean([record.aspect_ratio for record in records])),
        mean_brightness=float(np.mean(brightness)),
        min_brightness=float(min(brightness)),
        max_brightness=float(max(brightness)),
    )


__all__ = [
    "ImageStats",
    "InputStatsError",
    "StatsSummary",
    "image_statistics",
    "summarize_statistics",
]
