"""Contrato de inferencia: ImageData, Detection, Detector y FakeDetector."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, runtime_checkable

import numpy as np

# Orden canónico del data.yaml del dataset. El índice es el class_id.
CLASSES: tuple[str, ...] = (
    "Gloves",
    "Vest",
    "goggles",
    "helmet",
    "mask",
    "safety_shoe",
)

#: Formatos que la carga de imágenes entrega al contrato.
IMAGE_FORMATS: frozenset[str] = frozenset({"jpeg", "png"})


class ContractError(ValueError):
    """Error de validación del contrato de inferencia."""


def _is_int(value: object) -> bool:
    """Indica si el valor es un entero y no un booleano."""
    return isinstance(value, int) and not isinstance(value, bool)


def _is_number(value: object) -> bool:
    """Indica si el valor es un número real y no un booleano."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


@dataclass(frozen=True, slots=True)
class ImageData:
    """Imagen RGB decodificada y sus dimensiones originales."""

    array: np.ndarray
    width: int
    height: int
    format: str
    source: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.array, np.ndarray):
            raise ContractError("array debe ser un numpy.ndarray")
        if self.array.dtype != np.uint8:
            raise ContractError("array debe ser uint8")
        if self.array.ndim != 3 or self.array.shape[2] != 3:
            raise ContractError("array debe tener forma (alto, ancho, 3)")
        height, width = self.array.shape[:2]
        if width <= 0 or height <= 0:
            raise ContractError("las dimensiones de la imagen deben ser positivas")
        if not _is_int(self.width) or not _is_int(self.height):
            raise ContractError("width y height deben ser enteros")
        if (self.width, self.height) != (width, height):
            raise ContractError(
                f"width/height ({self.width}x{self.height}) no coinciden con el array "
                f"({width}x{height})"
            )
        if self.format not in IMAGE_FORMATS:
            raise ContractError(f"format debe ser uno de {sorted(IMAGE_FORMATS)}")


@dataclass(frozen=True, slots=True)
class Detection:
    """Detección validada: clase, confianza y caja xyxy en píxeles."""

    class_id: int
    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float]
    image_width: int
    image_height: int

    def __post_init__(self) -> None:
        if not _is_int(self.class_id):
            raise ContractError("class_id debe ser un entero")
        if not 0 <= self.class_id < len(CLASSES):
            raise ContractError(f"class_id fuera de rango: {self.class_id}")
        if not isinstance(self.class_name, str) or self.class_name != CLASSES[self.class_id]:
            raise ContractError(
                f"class_name {self.class_name!r} no corresponde a class_id {self.class_id}"
            )
        if (
            not _is_number(self.confidence)
            or not math.isfinite(self.confidence)
            or not 0.0 <= self.confidence <= 1.0
        ):
            raise ContractError("confidence debe ser finita y estar en [0, 1]")
        if not _is_int(self.image_width) or not _is_int(self.image_height):
            raise ContractError("las dimensiones de la imagen deben ser enteras")
        if self.image_width <= 0 or self.image_height <= 0:
            raise ContractError("las dimensiones de la imagen deben ser positivas")
        if len(self.bbox) != 4:
            raise ContractError("bbox debe tener cuatro valores xyxy")
        if not all(_is_number(value) for value in self.bbox):
            raise ContractError("bbox debe contener números")
        x1, y1, x2, y2 = (float(value) for value in self.bbox)
        if not all(math.isfinite(value) for value in (x1, y1, x2, y2)):
            raise ContractError("bbox debe contener valores finitos")
        if x1 >= x2 or y1 >= y2:
            raise ContractError("bbox inválida: se requiere x1 < x2 y y1 < y2")
        if x1 < 0 or y1 < 0 or x2 > self.image_width or y2 > self.image_height:
            raise ContractError("bbox fuera de los límites de la imagen")


@runtime_checkable
class Detector(Protocol):
    """Protocolo de inferencia que deben cumplir el fake y el detector real."""

    def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
        """Devuelve las detecciones de la imagen."""
        ...


class FakeDetector:
    """Detector determinista para pruebas y desarrollo sin YOLO."""

    def __init__(self, detections: Sequence[Detection] | None = None) -> None:
        self._detections = tuple(detections or ())

    def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
        """Devuelve las detecciones fijas configuradas."""
        return list(self._detections)
