"""HU-024 — publicación del modelo en el Generic Package Registry (AC-01 a AC-03).

Pruebas estáticas: leen el script de publicación y el pipeline, sin subir nada ni
llamar a GitLab.
"""

from __future__ import annotations

from pathlib import Path

PUBLISH = Path("deploy/model/publish.sh")
PIPELINE = Path(".gitlab-ci.yml")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-024 · AC-01


def test_publish_targets_the_generic_package_registry() -> None:
    """AC-01: el artefacto va al endpoint de paquetes genéricos del proyecto."""
    # Arrange
    script = _read(PUBLISH)

    # Assert
    assert "/packages/generic/" in script
    assert "${project}/packages/generic/${package}/${version}/${name}" in script


def test_publish_uses_a_token_and_never_hardcodes_it() -> None:
    """AC-01: el token llega por entorno y no aparece en el archivo."""
    # Arrange
    script = _read(PUBLISH)

    # Assert
    assert "PRIVATE-TOKEN: $GITLAB_TOKEN" in script
    assert "${GITLAB_TOKEN:?" in script
    assert "glpat-" not in script


def test_publish_requires_file_and_version() -> None:
    """AC-01: sin archivo o versión el script se detiene con código distinto de cero."""
    # Arrange
    script = _read(PUBLISH)

    # Assert
    assert "uso: publish.sh <archivo> <version>" in script
    assert "exit 64" in script
    assert "exit 66" in script


# --------------------------------------------------------------- HU-024 · AC-02


def test_publish_verifies_the_uploaded_blob() -> None:
    """AC-02: se descarga lo publicado y se compara el SHA256."""
    # Arrange
    script = _read(PUBLISH)

    # Assert
    assert "sha256sum" in script
    assert "local_sum" in script and "remote_sum" in script
    assert "no coincide" in script


def test_publish_prints_the_models_lock_snippet() -> None:
    """AC-02: el resultado se pega en `models.lock` sin transcribir a mano."""
    # Arrange
    script = _read(PUBLISH)

    # Assert
    assert "models.lock:" in script
    assert "url =" in script
    assert "sha256 =" in script


# --------------------------------------------------------------- HU-024 · AC-03


def test_deploy_downloads_the_model_from_the_registry() -> None:
    """AC-03: el despliegue baja el peso del paquete, no de una ruta local."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "packages/generic/$PPE_MODEL_PACKAGE/$PPE_MODEL_VERSION" in pipeline
    assert "JOB-TOKEN: $CI_JOB_TOKEN" in pipeline


def test_deploy_verifies_the_model_checksum() -> None:
    """AC-03: el peso montado en el servidor se verifica antes de arrancar."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "sha256sum -c -" in pipeline


def test_model_version_and_checksum_are_declared() -> None:
    """AC-03: la versión y el SHA256 viven en el pipeline, no en la prosa."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "PPE_MODEL_PACKAGE:" in pipeline
    assert "PPE_MODEL_VERSION:" in pipeline
    assert "PPE_MODEL_SHA256:" in pipeline
