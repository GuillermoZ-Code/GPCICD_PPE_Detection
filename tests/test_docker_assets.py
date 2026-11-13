"""Activos del contenedor Docker CPU (HU-011) — frente de Eliana (PLAN-PRUEBAS §4.3).

Complementa `tests/test_docker.py` sin repetirlo: allí se cubren `uv sync
--frozen`, librerías del sistema, el bloqueo de pesos y el runbook; aquí se
fijan la estructura multietapa del `Dockerfile`, la imagen base del runtime,
el builder del frontend, la selección de servicios del entrypoint, la
separación de servicios y puertos en `compose.yml`, la higiene del contexto
(`.dockerignore`) y el servidor nginx de la SPA (AC-011.1, AC-011.3, AC-011.4).

Todas son estáticas: no requieren Docker ni red.
"""

from __future__ import annotations

import re
from pathlib import Path

DOCKERFILE = Path("Dockerfile")
COMPOSE_FILE = Path("compose.yml")
DOCKERIGNORE = Path(".dockerignore")
ENTRYPOINT = Path("docker/entrypoint.sh")
NGINX_CONF = Path("docker/nginx.conf")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- AC-011.1


def test_dockerfile_declares_three_build_stages() -> None:
    """AC-011.1: el `Dockerfile` es multietapa (builder, runtime y web)."""
    # Arrange / Act
    dockerfile = _read(DOCKERFILE)

    # Assert
    for stage in ("frontend-builder", "runtime", "web"):
        assert re.search(rf"^FROM\s+\S+\s+AS\s+{stage}\s*$", dockerfile, re.MULTILINE), (
            f"falta la etapa {stage}"
        )


def test_runtime_stage_pins_python313_without_uv_downloads() -> None:
    """AC-011.1: el runtime es Python 3.13 slim y uv no descarga intérpretes."""
    # Arrange / Act
    dockerfile = _read(DOCKERFILE)

    # Assert
    assert "FROM python:3.13-slim AS runtime" in dockerfile
    assert "UV_PYTHON_DOWNLOADS=never" in dockerfile


def test_frontend_builder_uses_node24_npm_ci_and_baked_api_url() -> None:
    """AC-011.1: la SPA se construye con Node 24, `npm ci` y `VITE_API_URL`."""
    # Arrange / Act
    dockerfile = _read(DOCKERFILE)

    # Assert
    assert "FROM node:24-alpine AS frontend-builder" in dockerfile
    assert "npm ci" in dockerfile
    assert "ARG VITE_API_URL" in dockerfile
    assert "npm run build" in dockerfile


def test_web_stage_serves_spa_from_nginx() -> None:
    """AC-011.1: la etapa `web` copia el build de la SPA al html de nginx."""
    # Arrange / Act
    dockerfile = _read(DOCKERFILE)

    # Assert
    assert "FROM nginx:1.29-alpine AS web" in dockerfile
    assert "COPY --from=frontend-builder /app/dist /usr/share/nginx/html" in dockerfile


def test_uv_binary_comes_from_pinned_official_image() -> None:
    """AC-011.1: el binario de uv proviene de la imagen oficial con versión fijada."""
    # Arrange / Act
    dockerfile = _read(DOCKERFILE)

    # Assert
    assert re.search(r"COPY --from=ghcr\.io/astral-sh/uv:\d+\.\d+\.\d+ /uv", dockerfile), (
        "la imagen de uv debe estar versionada"
    )


def test_expose_declares_backend_and_web_ports() -> None:
    """AC-011.1: las etapas publican sus puertos (API 8000, gRPC 9000, web 80)."""
    # Arrange / Act
    lines = {line.strip() for line in _read(DOCKERFILE).splitlines()}

    # Assert
    assert "EXPOSE 8000 9000" in lines
    assert "EXPOSE 80" in lines


def test_entrypoint_selects_rest_grpc_or_both() -> None:
    """AC-011.1: `PPE_SERVICES` decide ejecutar REST, gRPC o ambos procesos."""
    # Arrange / Act
    entrypoint = _read(ENTRYPOINT)

    # Assert
    assert "rest) exec python -m ppe_detection.api ;;" in entrypoint
    assert "grpc) exec python -m ppe_detection.grpc ;;" in entrypoint
    assert "rest,grpc | both)" in entrypoint
    assert "python -m ppe_detection.api &" in entrypoint
    assert "python -m ppe_detection.grpc &" in entrypoint


# ---------------------------------------------------------------- AC-011.4


def test_entrypoint_warns_when_artifact_is_missing() -> None:
    """AC-011.4: si `PPE_MODEL_PATH` apunta a un archivo ausente, el arranque
    lo advierte y explica el efecto (503/UNAVAILABLE) en vez de fallar mudo."""
    # Arrange / Act
    entrypoint = _read(ENTRYPOINT)

    # Assert
    assert '[ ! -f "$model" ]' in entrypoint
    assert "ADVERTENCIA" in entrypoint
    assert "PPE_MODEL_PATH" in entrypoint


def test_entrypoint_rejects_unknown_service_value() -> None:
    """AC-011.4: un valor de `PPE_SERVICES` no reconocido falla rápido con código 64."""
    # Arrange / Act
    entrypoint = _read(ENTRYPOINT)

    # Assert
    assert "no válido" in entrypoint
    assert "exit 64" in entrypoint


def test_compose_runs_rest_and_grpc_as_separate_services() -> None:
    """AC-011.4: compose separa la API REST del servicio gRPC y la SPA en el
    target `web` (mismo backend, distinta exposición)."""
    # Arrange / Act
    compose = _read(COMPOSE_FILE)

    # Assert
    assert "PPE_SERVICES: rest" in compose
    assert "PPE_SERVICES: grpc" in compose
    assert "target: web" in compose


def test_compose_publishes_overridable_default_ports() -> None:
    """AC-011.4: los puertos de compose tienen valores por omisión y se
    pueden reasignar con variables de entorno."""
    # Arrange / Act
    compose = _read(COMPOSE_FILE)

    # Assert
    for mapping in (
        "${PPE_API_PORT:-8000}:8000",
        "${PPE_GRPC_PORT:-9000}:9000",
        "${PPE_WEB_PORT:-8080}:80",
    ):
        assert mapping in compose, f"falta el mapeo {mapping!r}"


# ---------------------------------------------------------------- AC-011.3


def test_dockerignore_excludes_virtualenvs_caches_and_tests() -> None:
    """AC-011.3: el contexto de construcción no lleva entornos, cachés ni pruebas."""
    # Arrange
    patterns = {
        line.strip()
        for line in _read(DOCKERIGNORE).splitlines()
        if line.strip() and not line.startswith("#")
    }

    # Act / Assert
    for pattern in (".venv/", "venv/", "node_modules/", "__pycache__/", ".pytest_cache/", "tests/"):
        assert pattern in patterns, f"falta {pattern!r} en {DOCKERIGNORE}"


# ---------------------------------------------------------------- SPA en nginx


def test_nginx_serves_spa_fallback_and_caches_hashed_assets() -> None:
    """AC-011.1: nginx sirve la SPA con fallback a `index.html` y cachea los
    assets con hash (rutas del lado del cliente resuelven a la aplicación)."""
    # Arrange / Act
    conf = _read(NGINX_CONF)

    # Assert
    assert "root /usr/share/nginx/html;" in conf
    assert "index index.html;" in conf
    assert "try_files $uri $uri/ /index.html;" in conf
    assert "location /assets/" in conf
    assert "immutable" in conf
