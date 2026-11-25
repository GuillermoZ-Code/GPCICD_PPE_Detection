"""Pruebas estáticas de la imagen optimizada (HU-084, issue #140)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "Dockerfile"
RUNBOOK = ROOT / "docs" / "operacion" / "docker.md"


def _runtime() -> str:
    """Devuelve el bloque de la etapa final `runtime`."""
    texto = DOCKERFILE.read_text(encoding="utf-8")
    return texto.split("FROM python:3.13-slim AS runtime\n", 1)[1].split("\nFROM ", 1)[0]


def _dockerfile() -> str:
    """Devuelve el contenido del Dockerfile."""
    return DOCKERFILE.read_text(encoding="utf-8")


def test_runtime_usa_usuario_no_root_ac_01() -> None:
    """AC-01: la etapa final crea y usa un usuario con UID distinto de cero."""
    # Arrange / Act
    texto = _dockerfile()
    runtime = _runtime()

    # Assert
    assert re.search(r"useradd\s+--uid\s+([1-9]\d*)\b", texto)
    assert "USER appuser" in runtime
    assert "USER root" not in runtime


def test_capas_ordenadas_sin_uv_en_runtime_ac_01() -> None:
    """AC-01: dependencias se construyen antes que el código y uv no va al runtime."""
    # Arrange
    texto = _dockerfile()
    runtime = _runtime()

    # Act
    manifiestos = texto.index("COPY pyproject.toml uv.lock")
    dependencias = texto.index("RUN uv sync --frozen --no-dev --no-install-project")
    codigo = texto.index("COPY src ./src")

    # Assert
    assert manifiestos < dependencias < codigo
    assert "FROM python:3.13-slim AS runtime-deps" in texto
    assert re.search(r"COPY\s+--chown=appuser:appuser\s+--from=runtime-deps\s+/app/\.venv", texto)
    assert "/usr/local/bin/uv" not in runtime


def test_runbook_documenta_tamano_antes_despues_ac_02() -> None:
    """AC-02: el runbook registra MB antes/después y el comando para medirlos."""
    # Arrange / Act
    texto = RUNBOOK.read_text(encoding="utf-8")
    seccion = texto.split("## 9. Tamaño de la imagen (HU-084)", 1)[1]

    # Assert
    assert "Antes (HU-011)" in seccion
    assert "Después (HU-084)" in seccion
    assert re.search(r"\d+(?:\.\d+)?\s*MB", seccion)
    assert "docker image inspect" in seccion


def test_directiva_user_se_verifica_estaticamente_ac_03() -> None:
    """AC-03: la directiva USER se comprueba leyendo el Dockerfile, sin Docker."""
    # Arrange
    runtime = _runtime()
    lineas = [linea.strip() for linea in runtime.splitlines()]

    # Act
    user_lines = [linea for linea in lineas if linea.startswith("USER ")]

    # Assert
    assert user_lines == ["USER appuser"]
    assert lineas.index("USER appuser") < lineas.index("ENTRYPOINT [\"/entrypoint.sh\"]")
