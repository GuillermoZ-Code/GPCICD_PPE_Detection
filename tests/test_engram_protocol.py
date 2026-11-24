"""Pruebas del protocolo de memoria de agentes (HU-102, issue #158)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADR = ROOT / "docs" / "adr" / "0011-memoria-agentes.md"
ADR_INDEX = ROOT / "docs" / "adr" / "README.md"
AGENTS = ROOT / "AGENTS.md"


def _adr() -> str:
    return ADR.read_text(encoding="utf-8")


def test_adr_exists_with_decision() -> None:
    """AC-02: el ADR 0011 existe y tiene decisión."""
    # Act
    text = _adr()

    # Assert
    assert "## Decisión" in text
    assert "## Consecuencias" in text


def test_adr_says_what_is_stored() -> None:
    """AC-01: el protocolo define qué se guarda."""
    # Act
    text = _adr()

    # Assert
    assert "Qué se guarda" in text
    assert "decisiones" in text
    assert "hallazgos" in text


def test_adr_forbids_secrets_and_personal_data() -> None:
    """AC-01: el protocolo prohíbe secretos y datos personales."""
    # Act
    text = _adr()

    # Assert
    assert "Qué no se guarda" in text
    assert "credenciales" in text
    assert "datos personales" in text


def test_adr_documents_sync_and_export() -> None:
    """AC-01: el protocolo explica sincronización y exportación."""
    # Act
    text = _adr()

    # Assert
    assert "Sincronización" in text
    assert "local a cada equipo" in text
    assert "Exportación" in text


def test_adr_is_subordinate_to_repository() -> None:
    """AC-02: la memoria queda subordinada a la constitución y los ADR."""
    # Act
    text = _adr()

    # Assert
    assert "manda el repositorio" in text
    assert "CONSTITUTION.md" in text


def test_agents_links_the_adr() -> None:
    """AC-03: AGENTS.md referencia el ADR 0011."""
    # Act
    text = AGENTS.read_text(encoding="utf-8")

    # Assert
    assert "ADR 0011" in text


def test_adr_index_lists_0011() -> None:
    """AC-02: el índice de ADR incluye el 0011."""
    # Act
    text = ADR_INDEX.read_text(encoding="utf-8")

    # Assert
    assert "0011-memoria-agentes.md" in text
