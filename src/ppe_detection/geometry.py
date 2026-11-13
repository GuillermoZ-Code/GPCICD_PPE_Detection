"""Geometría de cajas para detección (HU-003/HU-008)."""

from __future__ import annotations

from math import isfinite

type Box = tuple[float, float, float, float]


def _box(box: tuple[float, float, float, float]) -> Box:
    values = tuple(float(value) for value in box)
    if len(values) != 4:
        raise ValueError("La caja debe tener cuatro valores.")
    if not all(isfinite(value) for value in values):
        raise ValueError("La caja debe contener números finitos.")
    return (values[0], values[1], values[2], values[3])


def xyxy_to_xywh(box: Box) -> Box:
    """Convierte ``x1, y1, x2, y2`` a ``x, y, ancho, alto``."""
    x1, y1, x2, y2 = _box(box)
    return (x1, y1, x2 - x1, y2 - y1)


def xywh_to_xyxy(box: Box) -> Box:
    """Convierte ``x, y, ancho, alto`` a ``x1, y1, x2, y2``."""
    x, y, width, height = _box(box)
    return (x, y, x + width, y + height)


def clip_xyxy(box: Box, width: int, height: int) -> Box:
    """Recorta una caja a los límites de la imagen."""
    if width <= 0 or height <= 0:
        raise ValueError("width y height deben ser positivos.")
    x1, y1, x2, y2 = _box(box)
    x1 = min(max(x1, 0.0), float(width))
    y1 = min(max(y1, 0.0), float(height))
    x2 = min(max(x2, 0.0), float(width))
    y2 = min(max(y2, 0.0), float(height))
    return (x1, y1, x2, y2)


def is_degenerate(box: Box, *, min_size: float = 0.0) -> bool:
    """Indica si la caja no tiene área suficiente."""
    x1, y1, x2, y2 = _box(box)
    return (x2 - x1) <= min_size or (y2 - y1) <= min_size


def scale_xyxy(box: Box, scale_x: float, scale_y: float) -> Box:
    """Escala una caja por eje; los factores deben ser positivos y finitos."""
    if not isfinite(scale_x) or not isfinite(scale_y) or scale_x <= 0 or scale_y <= 0:
        raise ValueError("Los factores de escala deben ser positivos y finitos.")
    x1, y1, x2, y2 = _box(box)
    return (x1 * scale_x, y1 * scale_y, x2 * scale_x, y2 * scale_y)


def letterbox_params(width: int, height: int, target: int) -> tuple[float, float, float]:
    """Devuelve escala y relleno para llevar una imagen a un lienzo cuadrado."""
    if width <= 0 or height <= 0 or target <= 0:
        raise ValueError("width, height y target deben ser positivos.")
    scale = min(target / width, target / height)
    new_width = round(width * scale)
    new_height = round(height * scale)
    return scale, (target - new_width) / 2, (target - new_height) / 2


def letterbox_box(box: Box, width: int, height: int, target: int) -> Box:
    """Aplica escala y relleno letterbox a una caja."""
    scale, pad_x, pad_y = letterbox_params(width, height, target)
    x1, y1, x2, y2 = _box(box)
    return (
        x1 * scale + pad_x,
        y1 * scale + pad_y,
        x2 * scale + pad_x,
        y2 * scale + pad_y,
    )


__all__ = [
    "Box",
    "clip_xyxy",
    "is_degenerate",
    "letterbox_box",
    "letterbox_params",
    "scale_xyxy",
    "xywh_to_xyxy",
    "xyxy_to_xywh",
]
