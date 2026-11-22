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
import tomllib
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


DEFAULT_MANIFEST_PATH = Path(__file__).resolve().parents[2] / "models.lock"


class ModelManifestError(ValueError):
    """El manifiesto del modelo no existe, no es TOML válido o está incompleto."""


@dataclass(frozen=True, slots=True)
class ModelManifest:
    """Manifiesto canónico del artefacto que se despliega."""

    name: str
    version: str
    sha256: str
    url: str

    @property
    def identity(self) -> ModelIdentity:
        """Identidad compatible con REST, gRPC, `/health` y MLflow."""
        return ModelIdentity(version=self.version, sha256=self.sha256, artifact=self.url)


def _resolve_manifest_path(path: str | Path | None = None) -> Path | None:
    """Resuelve la ruta del manifiesto; una ruta explícita debe existir."""
    if path is not None:
        candidate = Path(path)
        if not candidate.is_file():
            raise ModelManifestError(f"No existe el manifiesto del modelo: {candidate}")
        return candidate

    explicit = os.getenv("PPE_MODEL_MANIFEST")
    if explicit:
        candidate = Path(explicit)
        if not candidate.is_file():
            raise ModelManifestError(f"No existe el manifiesto del modelo: {candidate}")
        return candidate

    return DEFAULT_MANIFEST_PATH if DEFAULT_MANIFEST_PATH.is_file() else None


def _parse_manifest(path: Path) -> ModelManifest:
    """Lee y valida un manifiesto TOML."""
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise ModelManifestError(f"El manifiesto {path} no es TOML válido: {exc}") from exc

    values: dict[str, str] = {}
    for field in ("name", "version", "sha256", "url"):
        value = raw.get(field)
        if not isinstance(value, str) or not value.strip():
            raise ModelManifestError(
                f"El manifiesto {path} no define el campo obligatorio '{field}'."
            )
        values[field] = value.strip()

    if not SHA256_PATTERN.fullmatch(values["sha256"]):
        raise ModelManifestError(
            f"El SHA256 del manifiesto {path} debe tener 64 caracteres hexadecimales."
        )

    return ModelManifest(
        name=values["name"],
        version=values["version"],
        sha256=values["sha256"].upper(),
        url=values["url"],
    )


def load_model_manifest(path: str | Path | None = None) -> ModelManifest:
    """Carga el manifiesto indicado o el canónico del repositorio."""
    resolved = _resolve_manifest_path(path)
    if resolved is None:
        raise ModelManifestError(f"No existe el manifiesto del modelo en {DEFAULT_MANIFEST_PATH}.")
    return _parse_manifest(resolved)


def _optional_model_manifest() -> ModelManifest | None:
    """Carga el manifiesto si existe; una ruta explícita inexistente es un error."""
    resolved = _resolve_manifest_path()
    return _parse_manifest(resolved) if resolved is not None else None


def sha256_file(path: Path) -> str:
    """Calcula el SHA256 de un archivo por bloques, en hexadecimal mayúscula."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def default_model_identity() -> ModelIdentity:
    """Construye la identidad desde overrides, el manifiesto o el artefacto."""
    explicit_version = os.getenv("PPE_MODEL_VERSION")
    explicit_sha = os.getenv("PPE_MODEL_SHA256")
    if explicit_sha and not SHA256_PATTERN.fullmatch(explicit_sha):
        raise ValueError("PPE_MODEL_SHA256 debe ser un SHA256 hexadecimal de 64 caracteres.")

    manifest = None
    if not explicit_version or not explicit_sha:
        manifest = _optional_model_manifest()

    model_path = os.getenv("PPE_MODEL_PATH")
    version = explicit_version or (manifest.version if manifest else None)
    if version is None:
        version = Path(model_path).stem if model_path else "unknown"
    artifact = model_path or (manifest.url if manifest else None)

    if explicit_sha:
        digest: str | None = explicit_sha.upper()
    elif model_path and Path(model_path).is_file():
        digest = sha256_file(Path(model_path))
    elif manifest is not None:
        digest = manifest.sha256
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
    """Versión del modelo: override, manifiesto, nombre del artefacto o `unknown`."""
    explicit = os.getenv("PPE_MODEL_VERSION")
    if explicit:
        return explicit
    manifest = _optional_model_manifest()
    if manifest is not None:
        return manifest.version
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
