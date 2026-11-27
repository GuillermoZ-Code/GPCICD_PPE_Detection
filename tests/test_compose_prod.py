"""HU-071 — `compose.prod.yml` (AC-01, AC-02 y AC-03).

Pruebas estáticas: leen el compose de producción sin levantar contenedores.
"""

from __future__ import annotations

from pathlib import Path

COMPOSE = Path("compose.prod.yml")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def test_production_compose_exposes_the_four_services() -> None:
    """AC-01: api, grpc, web y caddy arrancan juntos."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    for service in ("api:", "grpc:", "web:", "caddy:"):
        assert service in compose


def test_images_come_from_variables_with_a_clear_error() -> None:
    """AC-01: el tag llega por variable y el compose falla si falta."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    assert "${PPE_API_IMAGE:?" in compose
    assert "${PPE_WEB_IMAGE:?" in compose


def test_services_restart_unless_stopped() -> None:
    """AC-02: un reinicio del servidor devuelve los servicios solos."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    # `api` y `grpc` heredan del bloque común, así que la política aparece tres
    # veces: el ancla YAML, `web` y `caddy`.
    assert compose.count("restart: unless-stopped") >= 3


def test_model_is_mounted_read_only() -> None:
    """AC-03: el artefacto vive en el host y no viaja en la imagen."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    assert "${PPE_MODELS_DIR:-/opt/ppe/models}:/models:ro" in compose
    assert "PPE_MODEL_PATH" in compose or "/models/best.pt" in Path("compose.yml").read_text(
        encoding="utf-8"
    )


def test_variables_come_from_the_server_env_file() -> None:
    """AC-03: el `.env` del servidor define dominio, CORS y rutas."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    assert "env_file:" in compose
    assert "- .env" in compose


def test_backend_ports_are_not_published_to_the_internet() -> None:
    """AC-01: API y gRPC quedan en la red interna; Caddy publica 80 y 443."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    assert "8000:8000" not in compose
    assert "9000:9000" not in compose
    assert '"80:80"' in compose
    assert '"443:443"' in compose


def test_production_compose_does_not_build_images() -> None:
    """AC-01: en producción se baja la imagen publicada, no se construye."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    assert "build:" not in compose


def test_caddy_receives_the_domain_from_the_environment() -> None:
    """AC-03: el dominio no está escrito en el compose."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    assert "PPE_DOMAIN" in compose
    assert "example.com" not in compose
