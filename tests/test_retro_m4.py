"""Pruebas estructurales de la retrospectiva del M4 (HU-108, issue #164)."""

from __future__ import annotations

import re
from pathlib import Path

RETRO_PATH = Path(__file__).resolve().parents[1] / "docs" / "curso" / "M4" / "RETRO.md"

INTEGRATORS = ("Guillermo Zabala", "Eliana Cardona", "Hernán Estrada", "Jesús Riveros")
SECTIONS = ("### Start", "### Stop", "### Continue")
ACTION_ROW = re.compile(r"^\|\s*(A-\d{2})[^|]*\|(.+)\|\s*$", re.M)
DATE = re.compile(r"\d{2}/\d{2}/\d{4}|\d{4}-\d{2}-\d{2}")


def _text() -> str:
    return RETRO_PATH.read_text(encoding="utf-8")


def _block(name: str) -> str:
    text = _text()
    start = text.index(f"## {name}")
    rest = text[start:]
    end = rest.find("\n## ", 1)
    return rest if end == -1 else rest[:end]


def test_document_has_retro_sections() -> None:
    """AC-03: el documento existe y tiene la tabla de acciones."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "| Acción | Dueño | Fecha |" in text
    assert text.count("### Start") == 4


def test_all_integrators_have_sections() -> None:
    """AC-01: los cuatro integrantes tienen start/stop/continue."""
    # Arrange / Act / Assert
    for name in INTEGRATORS:
        block = _block(name)
        for section in SECTIONS:
            assert section in block, f"{name} sin {section}"


def test_sections_have_items() -> None:
    """AC-01: cada lista tiene al menos un item."""
    # Arrange / Act / Assert
    for name in INTEGRATORS:
        block = _block(name)
        for section in SECTIONS:
            start = block.index(section)
            rest = block[start + len(section) :]
            end = rest.find("\n### ")
            chunk = rest if end == -1 else rest[:end]
            items = [line for line in chunk.splitlines() if line.strip().startswith("- ")]
            assert items, f"{name} {section} sin items"


def test_actions_have_owner_and_date() -> None:
    """AC-02: cada accion tiene dueno y fecha."""
    # Arrange
    text = _text()

    # Act
    rows = [
        (match.group(1), *(cell.strip() for cell in match.group(2).split("|")))
        for match in ACTION_ROW.finditer(text)
    ]

    # Assert
    assert len(rows) >= 4
    for action_id, owner, date in rows:
        assert owner and owner != "—", f"{action_id} sin dueno"
        assert DATE.search(date), f"{action_id} sin fecha valida"
