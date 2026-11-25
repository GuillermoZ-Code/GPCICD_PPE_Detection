"""AC-01, AC-02 y AC-03 (HU-046) — HEALTHCHECK de la imagen y de compose.

Pruebas estáticas: leen el Dockerfile, el script y compose sin construir la imagen.
"""

from __future__ import annotations

from pathlib import Path

DOCKERFILE = Path("Dockerfile")
SCRIPT = Path("docker/healthcheck.sh")
COMPOSE = Path("compose.yml")
RUNBOOK = Path("docs/operacion/docker.md")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- AC-01 · /health/ready


def test_dockerfile_declares_healthcheck_with_script() -> None:
    """AC-01: el Dockerfile define HEALTHCHECK y lo delega al script."""
    # Arrange / Act
    dockerfile = _read(DOCKERFILE)

    # Assert
    assert "HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3" in dockerfile
    assert 'CMD ["/healthcheck.sh"]' in dockerfile


def test_healthcheck_queries_ready_endpoint_for_rest() -> None:
    """AC-01: con REST, el healthcheck consulta `/health/ready`."""
    # Arrange / Act
    script = _read(SCRIPT)

    # Assert
    assert "/health/ready" in script
    assert "PPE_SERVICES" in script


def test_healthcheck_covers_grpc_port() -> None:
    """AC-01: con gRPC, el healthcheck comprueba el puerto 9000."""
    # Arrange / Act
    script = _read(SCRIPT)

    # Assert
    assert "9000" in script
    assert "socket.create_connection" in script


# ---------------------------------------------------------------- AC-03 · estáticas


def test_dockerfile_copies_and_chmods_the_script() -> None:
    """AC-03: la imagen copia el script y le da permisos de ejecución."""
    # Arrange / Act
    dockerfile = _read(DOCKERFILE)
    script = _read(SCRIPT)

    # Assert
    assert "COPY docker/healthcheck.sh /healthcheck.sh" in dockerfile
    assert "chmod 0755 /healthcheck.sh" in dockerfile
    assert script.startswith("#!/bin/sh")


# ---------------------------------------------------------------- AC-02 · compose


def test_compose_and_runbook_expose_health_status() -> None:
    """AC-02: compose hereda el healthcheck y el runbook explica `docker inspect`."""
    # Arrange
    compose = _read(COMPOSE)
    runbook = _read(RUNBOOK)

    # Act / Assert
    assert 'test: ["CMD", "/healthcheck.sh"]' in compose
    assert "docker inspect" in runbook
    assert ".State.Health.Status" in runbook
    assert "healthy" in runbook
