"""Artefactos gráficos estables de una evaluación (HU-031).

Ultralytics genera ``confusion_matrix.png``, ``BoxPR_curve.png`` y otras figuras en
el directorio del run. Este módulo las copia a nombres estables que incluyen la
versión y el SHA256 del modelo, de modo que un run de MLflow pueda referenciarlas.
"""

from __future__ import annotations

import re
import shutil
from collections.abc import Mapping
from pathlib import Path

FIGURES: Mapping[str, str] = {
    "confusion_matrix.png": "confusion_matrix",
    "confusion_matrix_normalized.png": "confusion_matrix_normalized",
    "BoxPR_curve.png": "pr_curve",
    "PR_curve.png": "pr_curve",
    "BoxF1_curve.png": "f1_curve",
    "BoxP_curve.png": "precision_curve",
    "BoxR_curve.png": "recall_curve",
}
SHA256_PATTERN = re.compile(r"[0-9A-Fa-f]{64}")


def artifact_slug(model_version: str, sha256: str) -> str:
    """Devuelve el identificador estable ``version-sha12`` del modelo."""
    if not isinstance(model_version, str) or not model_version.strip():
        raise ValueError("model_version no puede estar vacío")
    if not SHA256_PATTERN.fullmatch(sha256):
        raise ValueError("sha256 debe tener 64 caracteres hexadecimales")
    version = re.sub(r"[^a-z0-9]+", "-", model_version.lower()).strip("-") or "model"
    return f"{version}-{sha256[:12].lower()}"


def stable_artifact_name(source_name: str, model_version: str, sha256: str) -> str:
    """Nombre estable para una figura conocida; falla si no es una figura de evaluación."""
    source = Path(source_name)
    stem = FIGURES.get(source.name)
    if stem is None:
        raise ValueError(f"Figura de evaluación desconocida: {source_name!r}")
    return f"{stem}_{artifact_slug(model_version, sha256)}{source.suffix.lower()}"


def collect_evaluation_artifacts(
    source_dir: Path,
    destination_dir: Path,
    *,
    model_version: str,
    model_sha256: str,
) -> tuple[Path, ...]:
    """Copia las figuras presentes con nombres estables por modelo.

    No falla si el run no generó figuras: devuelve una tupla vacía. El destino se
    crea cuando hay al menos una figura.
    """
    source = Path(source_dir)
    destination = Path(destination_dir)
    if not source.is_dir():
        return ()
    copied: list[Path] = []
    for source_name in FIGURES:
        source_path = source / source_name
        if not source_path.is_file():
            continue
        destination.mkdir(parents=True, exist_ok=True)
        target = destination / stable_artifact_name(source_name, model_version, model_sha256)
        shutil.copy2(source_path, target)
        copied.append(target)
    return tuple(copied)


__all__ = [
    "FIGURES",
    "artifact_slug",
    "collect_evaluation_artifacts",
    "stable_artifact_name",
]
