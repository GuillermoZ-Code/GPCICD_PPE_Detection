"""AC-01, AC-02 y AC-03 (HU-073) — MCP de GitLab y `glab` documentados.

Pruebas estáticas: leen `opencode.json` y el runbook; no abren sesión contra GitLab.
"""

from __future__ import annotations

import json
from pathlib import Path

CONFIG = Path("opencode.json")
RUNBOOK = Path("docs/operacion/herramientas-agente.md")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def _config() -> dict:
    """Carga la configuración de OpenCode; un JSON inválido falla la prueba."""
    return json.loads(_read(CONFIG))


# ---------------------------------------------------------------- AC-01 · MCP


def test_gitlab_mcp_is_declared_as_remote_server() -> None:
    """AC-01: el MCP de GitLab se declara remoto contra la URL oficial."""
    # Arrange / Act
    gitlab = _config()["mcp"]["gitlab"]

    # Assert
    assert gitlab["type"] == "remote"
    assert gitlab["url"] == "https://gitlab.com/api/v4/mcp"
    assert gitlab["enabled"] is True


def test_engram_server_is_preserved() -> None:
    """AC-01: la configuración previa de Engram sigue intacta."""
    # Arrange / Act
    mcp = _config()["mcp"]

    # Assert
    assert mcp["engram"]["type"] == "local"
    assert "engram" in mcp["engram"]["command"]


# ---------------------------------------------------------------- AC-03 · sin tokens


def test_configuration_has_no_tokens() -> None:
    """AC-03: no hay tokens en la configuración versionada."""
    # Arrange / Act
    text = _read(CONFIG)

    # Assert
    assert "glpat-" not in text
    assert "PRIVATE-TOKEN" not in text
    assert "GITLAB_TOKEN" not in text


# ---------------------------------------------------------------- AC-02 · verificación


def test_runbook_documents_glab_and_mcp_checks() -> None:
    """AC-02: el runbook explica cómo verificar `glab` y el MCP."""
    # Arrange / Act
    runbook = _read(RUNBOOK)

    # Assert
    assert "glab auth status" in runbook
    assert "glab api user" in runbook
    assert "opencode mcp list" in runbook
    assert "https://gitlab.com/api/v4/mcp" in runbook


def test_runbook_explains_name_and_oauth() -> None:
    """AC-02: documenta el nombre canónico y que la conexión es OAuth."""
    # Arrange / Act
    runbook = _read(RUNBOOK)

    # Assert
    assert "gitlab-mcp" in runbook
    assert "OAuth" in runbook
    assert "keyring" in runbook
