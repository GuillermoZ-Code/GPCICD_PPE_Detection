"""Configuración del detector desde variables de entorno (HU-006/HU-010).

Componente central compartido: REST y gRPC construyen el detector con la misma
función y las mismas variables (`PPE_MODEL_PATH`, `PPE_CONF`, `PPE_IOU`,
`PPE_IMGSZ`, `PPE_DEVICE` y `PPE_MODEL_VERSION`), de modo que una misma
configuración no requiere detectores independientes (AC-010.2).
"""

from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path

from ppe_detection.contracts import Detector

SHA256_PATTERN = re.compile(r"[0-9A-Fa-f]{64}")


class DetectorNotConfiguredError(RuntimeError):
    """No hay artefacto configurado para construir el detector."""


@dataclass(frozen=True, slots=True)
class ModelIdentity:
    """Identidad verificable del artefacto que produjo una inferencia."""

    version: str
    sha256: str | None = None
    artifact: str | None = None

    @property
    def reference(self) -> str:
        """Referencia estable; usa `sha256:<hash>` cuando el hash está disponible."""
        if self.sha256:
            return f"sha256:{self.sha256}"
        if self.artifact:
            return f"artifact:{self.artifact}"
        return f"version:{self.version}"


def sha256_file(path: Path) -> str:
    """Calcula el SHA256 de un archivo por bloques, en hexadecimal mayúscula."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def default_model_identity() -> ModelIdentity:
    """Construye la identidad desde el entorno y, si hace falta, calcula el SHA256."""
    version = default_model_version()
    model_path = os.getenv("PPE_MODEL_PATH")
    artifact = model_path or None
    explicit = os.getenv("PPE_MODEL_SHA256")
    if explicit:
        if not SHA256_PATTERN.fullmatch(explicit):
            raise ValueError("PPE_MODEL_SHA256 debe ser un SHA256 hexadecimal de 64 caracteres.")
        digest: str | None = explicit.upper()
    elif model_path and Path(model_path).is_file():
        digest = sha256_file(Path(model_path))
    else:
        digest = None
    return ModelIdentity(version=version, sha256=digest, artifact=artifact)


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
