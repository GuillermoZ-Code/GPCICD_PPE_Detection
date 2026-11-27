"""HU-024 — manifiesto del modelo publicado en el registry (AC-01 a AC-03).

Pruebas estáticas: leen `models.lock` y el pipeline; no descargan el peso.
"""

from __future__ import annotations

import re
from pathlib import Path

MANIFEST = Path("models.lock")
PIPELINE = Path(".gitlab-ci.yml")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def _field(name: str) -> str:
    """Extrae un campo `nombre = "valor"` del manifiesto."""
    match = re.search(rf'^{name}\s*=\s*"([^"]+)"', _read(MANIFEST), re.MULTILINE)
    assert match, f"falta {name} en models.lock"
    return match.group(1)


# --------------------------------------------------------------- HU-024 · AC-01


def test_manifest_points_to_the_generic_package_registry() -> None:
    """AC-01: el artefacto se descarga del paquete genérico del proyecto."""
    # Arrange / Act
    url = _field("url")

    # Assert
    assert url.startswith("https://gitlab.com/api/v4/projects/89281003/packages/generic/")
    assert url.endswith("/best.pt")


def test_package_name_is_the_documented_one() -> None:
    """AC-01: el paquete se llama `ppe-detection-models`."""
    # Arrange / Act
    url = _field("url")

    # Assert
    assert "/packages/generic/ppe-detection-models/" in url


# --------------------------------------------------------------- HU-024 · AC-02


def test_checksum_is_a_full_uppercase_sha256() -> None:
    """AC-02: el SHA256 tiene 64 caracteres hexadecimales en mayúsculas."""
    # Arrange / Act
    sha = _field("sha256")

    # Assert
    assert re.fullmatch(r"[0-9A-F]{64}", sha)


def test_manifest_version_matches_the_package_url() -> None:
    """AC-02: la versión del manifiesto es la de la URL publicada."""
    # Arrange
    version = _field("version")

    # Act
    url = _field("url")

    # Assert
    assert f"/{version}/" in url


def test_manifest_identifies_the_model() -> None:
    """AC-02: el manifiesto declara nombre y versión del modelo."""
    # Arrange
    manifest = _read(MANIFEST)

    # Assert
    assert 'name = "ppe-detection"' in manifest
    assert 'version = "yolo26n-clean"' in manifest


# --------------------------------------------------------------- HU-024 · AC-03


def test_deploy_downloads_from_the_registry_with_the_job_token() -> None:
    """AC-03: el pipeline baja el peso del paquete, no de una ruta local."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "packages/generic/$PPE_MODEL_PACKAGE/$PPE_MODEL_VERSION" in pipeline
    assert "JOB-TOKEN: $CI_JOB_TOKEN" in pipeline
    assert "sha256sum -c -" in pipeline


def test_model_is_not_versioned_and_is_mounted_read_only() -> None:
    """AC-03: el peso no vive en Git y el contenedor lo monta `:ro`."""
    # Arrange
    ignore = Path(".gitignore").read_text(encoding="utf-8")
    compose = Path("compose.prod.yml").read_text(encoding="utf-8")

    # Assert
    assert "*.pt" in ignore
    assert "/models:ro" in compose
