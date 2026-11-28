"""Pruebas del espejo del backlog (HU-092, issue #148).

AC-01 las 113 HU con SP, dueño, ola y spec; AC-02 totales que cuadran; AC-03 el
espejo coincide con las specs del repositorio.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "docs" / "curso" / "backlog.md"
SPECS = ROOT / "specs"

HU_ROW = re.compile(r"^\| (HU-\d{3}) \| \[#\d+\]", re.M)
M4_ROW = re.compile(
    r"^\| (HU-\d{3}) \| \[#\d+\]\([^)]*\) \| .+? \| `ep-\d{2}` \| (\d+) \| P\d \| (\d) \| ",
    re.M,
)
SPEC_LINK = re.compile(r"\]\(\.\./\.\./specs/([^)/]+)/?\)")
FIBONACCI = {1, 2, 3, 5, 8, 13}
DASH = "\u2013"


def _backlog() -> str:
    return BACKLOG.read_text(encoding="utf-8")


def _owner_rows(text: str, name: str) -> int:
    start = text.index(f"### {name} (")
    rest = text[start:]
    ends = [index for index in (rest.find("\n### "), rest.find("\n## ")) if index != -1]
    block = rest if not ends else rest[: min(ends)]
    return len(HU_ROW.findall(block))


def test_backlog_lists_all_113_hus() -> None:
    """AC-01: las 113 HU aparecen una sola vez."""
    # Arrange
    text = _backlog()

    # Act
    hus = HU_ROW.findall(text)

    # Assert
    assert len(hus) == 113, f"se esperaban 113 HU, hay {len(hus)}"
    assert len(set(hus)) == 113, "hay HU repetidas"
    assert hus[0] == "HU-001" and "HU-113" in hus


def test_backlog_m4_rows_have_epic_sp_wave_and_spec() -> None:
    """AC-01: cada HU del M4 trae epica, SP Fibonacci, ola y spec."""
    # Arrange
    text = _backlog()

    # Act
    rows = M4_ROW.findall(text)

    # Assert
    assert len(rows) == 100, f"se esperaban 100 HU del M4, hay {len(rows)}"
    for hu, sp, wave in rows:
        assert int(sp) in FIBONACCI, f"{hu} tiene SP fuera de Fibonacci: {sp}"
        assert int(wave) in {1, 2, 3}, f"{hu} tiene ola invalida: {wave}"
    counts = {
        name: _owner_rows(text, name)
        for name in ("Guillermo Zabala", "Eliana Cardona", "Hernán Estrada", "Jesús Riveros")
    }
    assert counts == {
        "Guillermo Zabala": 24,
        "Eliana Cardona": 26,
        "Hernán Estrada": 25,
        "Jesús Riveros": 25,
    }


def test_backlog_totals_match_rows() -> None:
    """AC-02: los totales por sprint e integrante cuadran."""
    # Arrange
    text = _backlog()

    # Act / Assert
    assert f"| M3-S1 | 31/10{DASH}07/11/2026 | 7 | 11 |" in text
    assert f"| M3-S2 | 08/11{DASH}14/11/2026 | 6 | 8 |" in text
    assert f"| M4-S3 | 15/11{DASH}28/11/2026 | 100 | 200 |" in text
    assert "| **Total** | | **113** | **219** |" in text
    for name, github, hus, sp in (
        ("Guillermo Zabala", "GuillermoZ-Code", 24, 50),
        ("Eliana Cardona", "ElianaCardona", 26, 50),
        ("Hernán Estrada", "HestradaUAO", 25, 50),
        ("Jesús Riveros", "jesusriverosUAO", 25, 50),
    ):
        assert f"| {name} | `{github}` | {hus} | {sp} | 192 |" in text


def test_backlog_specs_match_repository() -> None:
    """AC-03: cada spec enlazada existe; el espejo es una instantanea, no un indice vivo."""
    # Arrange
    text = _backlog()

    # Act
    linked = set(SPEC_LINK.findall(text))

    # Assert
    missing = sorted(name for name in linked if not (SPECS / name).is_dir())
    assert not missing, f"specs enlazadas que no existen: {missing}"
    assert len(linked) >= 20, f"el espejo solo enlaza {len(linked)} specs"
