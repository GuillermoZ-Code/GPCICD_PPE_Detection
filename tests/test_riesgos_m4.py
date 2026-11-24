"""Pruebas estructurales del registro de riesgos del M4 (HU-104, issue #160)."""

from __future__ import annotations

import re
from pathlib import Path

RISKS_PATH = Path(__file__).resolve().parents[1] / "docs" / "curso" / "M4" / "RIESGOS.md"

ROW = re.compile(r"^\|\s*(R-\d{2})\s*\|(.+)\|\s*$", re.M)
CATEGORIES = {"infraestructura", "ci", "modelo", "equipo"}


def _rows() -> list[list[str]]:
    text = RISKS_PATH.read_text(encoding="utf-8")
    return [[cell.strip() for cell in match.group(2).split("|")] for match in ROW.finditer(text)]


def test_file_exists() -> None:
    """AC-01: el registro existe y tiene la tabla."""
    # Arrange / Act
    text = RISKS_PATH.read_text(encoding="utf-8")

    # Assert
    assert "| ID | Riesgo |" in text
    assert _rows()


def test_all_categories_present() -> None:
    """AC-01: cubre infraestructura, CI, modelo y equipo."""
    # Arrange
    rows = _rows()

    # Act
    found = {row[1] for row in rows}

    # Assert
    assert found >= CATEGORIES, f"faltan categorias: {CATEGORIES - found}"


def test_every_risk_has_owner_and_trigger() -> None:
    """AC-02: cada riesgo declara dueno y disparador."""
    # Arrange
    rows = _rows()

    # Act / Assert
    for row in rows:
        risk_id, owner, trigger = row[0], row[4], row[5]
        assert owner and owner != "—", f"{risk_id} sin dueno"
        assert trigger and trigger != "—", f"{risk_id} sin disparador"


def test_minimum_number_of_risks() -> None:
    """AC-03: hay al menos ocho riesgos registrados."""
    # Arrange / Act
    rows = _rows()

    # Assert
    assert len(rows) >= 8, f"solo hay {len(rows)} riesgos"
