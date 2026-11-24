"""Pruebas de la configuracion de Engram (HU-101, issue #157).

AC-01 MCP registrado y runbook, AC-02 guardar/recuperar y AC-03 base fuera de Git.
No ejecutan Engram ni necesitan red.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "opencode.json"
RUNBOOK_PATH = ROOT / "docs" / "operacion" / "engram.md"
GITIGNORE_PATH = ROOT / ".gitignore"


def _config() -> dict[str, object]:
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def _mcp_engram(data: dict[str, object]) -> dict[str, object]:
    mcp = data.get("mcp")
    assert isinstance(mcp, dict), "opencode.json no declara mcp"
    engram = mcp.get("engram")
    assert isinstance(engram, dict), "mcp.engram no existe"
    return engram


def _runbook() -> str:
    return RUNBOOK_PATH.read_text(encoding="utf-8")


def test_opencode_json_is_valid_json() -> None:
    """AC-01: opencode.json es JSON valido."""
    # Arrange / Act
    data = _config()

    # Assert
    assert "$schema" in data


def test_opencode_declares_engram_mcp() -> None:
    """AC-01: el MCP engram esta declarado con un comando portable."""
    # Arrange
    data = _config()

    # Act
    mcp = data.get("mcp")

    # Assert
    assert isinstance(mcp, dict), "opencode.json no declara mcp"
    engram = mcp.get("engram")
    assert isinstance(engram, dict), "mcp.engram no existe"
    command = engram.get("command")
    assert isinstance(command, list), "mcp.engram.command debe ser una lista"
    assert command[0] == "engram", "el comando debe usar el binario del PATH"
    assert "mcp" in command


def test_opencode_engram_is_enabled() -> None:
    """AC-01: el servidor arranca habilitado por defecto."""
    # Arrange
    data = _config()

    # Act
    engram = _mcp_engram(data)

    # Assert
    assert engram.get("enabled") is True
    assert engram.get("type") == "local"


def test_runbook_documents_installation() -> None:
    """AC-01: el runbook explica como instalarlo y registrarlo."""
    # Arrange
    runbook = _runbook()

    # Act / Assert
    assert "engram setup" in runbook
    assert "opencode mcp list" in runbook


def test_runbook_documents_how_to_disable() -> None:
    """AC-01: el runbook explica como deshabilitarlo en un equipo sin Engram."""
    # Arrange
    runbook = _runbook()

    # Act / Assert
    assert '"enabled": false' in runbook


def test_runbook_documents_save_and_search() -> None:
    """AC-02: el runbook muestra guardar y recuperar una memoria."""
    # Arrange
    runbook = _runbook()

    # Act / Assert
    assert "mem_save" in runbook
    assert "mem_search" in runbook
    assert "Evidencia" in runbook


def test_runbook_documents_local_database() -> None:
    """AC-03: la base local vive fuera del repositorio."""
    # Arrange
    runbook = _runbook()

    # Act / Assert
    assert ".engram/engram.db" in runbook
    assert "fuera de Git" in runbook


def test_gitignore_covers_engram_database() -> None:
    """AC-03: .gitignore excluye las bases SQLite."""
    # Arrange
    patterns = GITIGNORE_PATH.read_text(encoding="utf-8").splitlines()

    # Act / Assert
    assert "*.db" in patterns
    assert "*.sqlite" in patterns
