"""HU-070 — operaciones de despliegue con `make` (AC-01 y AC-03).

Pruebas estáticas: leen el Makefile y `deploy/remote.sh` sin conectarse al servidor.
"""

from __future__ import annotations

from pathlib import Path

MAKEFILE = Path("Makefile")
REMOTE = Path("deploy/remote.sh")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-070 · AC-01


def test_make_exposes_the_deploy_workflow() -> None:
    """AC-01: desplegar, verificar y publicar el modelo tienen objetivo propio."""
    # Arrange
    makefile = _read(MAKEFILE)

    # Assert
    for target in ("deploy:", "verify:", "model-publish:"):
        assert target in makefile, f"falta {target}"


def test_deploy_target_requires_a_tag() -> None:
    """AC-01: el objetivo documenta que necesita TAG y el host del Droplet."""
    # Arrange
    makefile = _read(MAKEFILE)

    # Assert
    assert "TAG=<sha>" in makefile
    assert "PPE_DEPLOY_HOST" in makefile


def test_verify_target_documents_the_public_url() -> None:
    """AC-01: la verificación usa la URL pública, no una ruta interna."""
    # Arrange
    makefile = _read(MAKEFILE)

    # Assert
    assert "PPE_PUBLIC_URL" in makefile
    assert "deploy/remote.sh verify" in makefile


# --------------------------------------------------------------- HU-070 · AC-03


def test_remote_script_refuses_to_run_without_a_host() -> None:
    """AC-03: sin servidor el script se detiene antes de tocar nada."""
    # Arrange
    script = _read(REMOTE)

    # Assert
    assert "${PPE_DEPLOY_HOST:?" in script
    assert "exit 64" in script


def test_remote_script_uses_the_public_mirror() -> None:
    """AC-03: el servidor baja las imágenes de Docker Hub, sin credenciales."""
    # Arrange
    script = _read(REMOTE)

    # Assert
    assert "gpcicd-ppe-api" in script
    assert "gpcicd-ppe-web" in script
    assert "gpcicd-ppe-caddy" in script
    assert "docker login" not in script


def test_remote_script_copies_the_versioned_files() -> None:
    """AC-03: el despliegue manual usa los mismos archivos que el pipeline."""
    # Arrange
    script = _read(REMOTE)

    # Assert
    assert "compose.prod.yml docker/Caddyfile deploy/deploy.sh" in script
    assert "sh deploy.sh" in script
