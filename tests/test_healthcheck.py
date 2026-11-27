"""HU-046 — HEALTHCHECK de la imagen (AC-01, AC-02 y AC-03).

Pruebas estáticas: leen el script y el Dockerfile sin construir la imagen ni
levantar contenedores.
"""

from __future__ import annotations

import re
from pathlib import Path

SCRIPT = Path("docker/healthcheck.sh")
DOCKERFILE = Path("Dockerfile")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def test_rest_mode_checks_health_ready() -> None:
    """AC-01: en modo REST el healthcheck consulta `/health/ready`."""
    # Arrange
    script = _read(SCRIPT)

    # Assert
    assert "/health/ready" in script
    assert "127.0.0.1:8000" in script


def test_grpc_mode_checks_the_rpc_port() -> None:
    """AC-02: en modo gRPC no hay HTTP; se comprueba el puerto 9000."""
    # Arrange
    script = _read(SCRIPT)

    # Assert
    assert "PPE_SERVICES" in script
    assert "9000" in script
    assert "connect_ex" in script


def test_healthcheck_does_not_need_curl() -> None:
    """AC-01: la imagen runtime no trae curl; el script usa python del entorno."""
    # Arrange
    script = _read(SCRIPT)

    # Act
    calls_curl = re.search(r"^\s*curl\b", script, re.MULTILINE)

    # Assert
    assert calls_curl is None
    assert "python -c" in script


def test_healthcheck_exits_non_zero_on_failure() -> None:
    """AC-01: un fallo tiene que devolver código distinto de cero."""
    # Arrange
    script = _read(SCRIPT)

    # Assert
    assert "sys.exit(0 if" in script
    assert "set -eu" in script


def test_dockerfile_declares_healthcheck_with_margins() -> None:
    """AC-03: la imagen declara HEALTHCHECK con intervalo, timeout y reintentos."""
    # Arrange
    dockerfile = _read(DOCKERFILE)

    # Assert
    assert "HEALTHCHECK --interval=30s --timeout=5s" in dockerfile
    assert "--start-period=90s" in dockerfile
    assert "--retries=3" in dockerfile


def test_dockerfile_copies_the_healthcheck_script() -> None:
    """AC-03: el script viaja en la imagen y se ejecuta como CMD."""
    # Arrange
    dockerfile = _read(DOCKERFILE)

    # Assert
    assert "docker/healthcheck.sh /healthcheck.sh" in dockerfile
    assert 'CMD ["/healthcheck.sh"]' in dockerfile


def test_web_image_is_healthy_before_caddy_publishes_it() -> None:
    """AC-02: nginx responde antes de que Caddy lo ponga detrás del dominio."""
    # Arrange
    dockerfile = _read(DOCKERFILE)

    # Assert
    assert "wget -q --spider http://127.0.0.1/" in dockerfile
