"""Configuración del detector desde variables de entorno (HU-006/HU-010).

Componente central compartido: REST y gRPC construyen el detector con la misma
función y las mismas variables (`PPE_MODEL_PATH`, `PPE_CONF`, `PPE_IOU`,
`PPE_IMGSZ`, `PPE_DEVICE` y `PPE_MODEL_VERSION`), de modo que una misma
configuración no requiere detectores independientes (AC-010.2).
"""

from __future__ import annotations

import os
from pathlib import Path

from ppe_detection.contracts import Detector


class DetectorNotConfiguredError(RuntimeError):
    """No hay artefacto configurado para construir el detector."""


def env_float(name: str, default: float) -> float:
    """Lee un número de una variable de entorno; ante un valor inválido, usa el por omisión."""
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def env_int(name: str, default: int) -> int:
    """Lee un entero de una variable de entorno; ante un valor inválido, usa el por omisión."""
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def default_model_version() -> str:
    """Versión del modelo: `PPE_MODEL_VERSION`, o el nombre del artefacto, o `unknown`."""
    explicit = os.getenv("PPE_MODEL_VERSION")
    if explicit:
        return explicit
    model_path = os.getenv("PPE_MODEL_PATH")
    return Path(model_path).stem if model_path else "unknown"


def build_detector() -> Detector:
    """Construye el detector YOLO configurado; perezoso para no cargar torch al importar.

    Raises:
        DetectorNotConfiguredError: si `PPE_MODEL_PATH` no está definida.
    """
    from ppe_detection.detection.yolo import (
        DEFAULT_CONF,
        DEFAULT_DEVICE,
        DEFAULT_IMGSZ,
        DEFAULT_IOU,
        YoloDetector,
    )

    model_path = os.getenv("PPE_MODEL_PATH")
    if not model_path:
        raise DetectorNotConfiguredError("No hay modelo configurado: define PPE_MODEL_PATH.")
    return YoloDetector(
        model_path,
        conf=env_float("PPE_CONF", DEFAULT_CONF),
        iou=env_float("PPE_IOU", DEFAULT_IOU),
        imgsz=env_int("PPE_IMGSZ", DEFAULT_IMGSZ),
        device=os.getenv("PPE_DEVICE", DEFAULT_DEVICE),
    )
