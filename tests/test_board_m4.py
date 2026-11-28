"""Pruebas del tablero del M4 (HU-090, issue #146)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "docs" / "curso" / "backlog.md"
BOARD = ROOT / "docs" / "curso" / "M4" / "TABLERO.md"
FIBONACCI = {1, 2, 3, 5, 8}
SIZE = {1: "XS", 2: "S", 3: "M", 5: "L", 8: "XL"}
EPICS = {f"ep-{number:02d}" for number in range(5, 16)}
OWNERS = ("Guillermo Zabala", "Eliana Cardona", "Hernán Estrada", "Jesús Riveros")


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _backlog_rows(text: str) -> list[list[str]]:
    rows = [_cells(line) for line in text.splitlines() if line.strip().startswith("| HU-")]
    return [cells for cells in rows if len(cells) > 1 and re.search(r"\[#\d+\]", cells[1])]


def _m4_rows(text: str) -> list[list[str]]:
    return [cells for cells in _backlog_rows(text) if len(cells) >= 9]


def _text() -> str:
    return BACKLOG.read_text(encoding="utf-8")


def test_m4_has_one_hundred_hus() -> None:
    # Act
    rows = _m4_rows(_text())

    # Assert
    assert len(rows) == 100


def test_m4_issue_numbers_are_unique() -> None:
    # Arrange
    rows = _m4_rows(_text())

    # Act
    numbers = [match.group(1) for cells in rows if (match := re.search(r"#(\d+)", cells[1]))]

    # Assert
    assert len(set(numbers)) == 100


def test_backlog_totals_match_official() -> None:
    # Arrange
    rows = _backlog_rows(_text())

    # Act
    total_sp = sum(int(cells[4] if len(cells) >= 9 else cells[3]) for cells in rows)

    # Assert
    assert len(rows) == 113
    assert total_sp == 219


def test_each_integrator_sums_fifty_sp() -> None:
    # Arrange
    owner: str | None = None
    totals: dict[str, int] = {}

    # Act
    for line in _text().splitlines():
        heading = re.match(r"^### (.+?) \(", line)
        if heading:
            owner = heading.group(1)
            continue
        if owner not in OWNERS or not line.strip().startswith("| HU-"):
            continue
        cells = _cells(line)
        if len(cells) < 9 or not re.search(r"\[#\d+\]", cells[1]):
            continue
        totals[owner] = totals.get(owner, 0) + int(cells[4])

    # Assert
    assert totals == dict.fromkeys(OWNERS, 50)


def test_estimates_are_fibonacci() -> None:
    # Arrange
    estimates = [int(cells[4]) for cells in _m4_rows(_text())]

    # Act / Assert
    assert set(estimates) <= FIBONACCI


def test_size_mapping_is_coherent() -> None:
    # Arrange
    text = BOARD.read_text(encoding="utf-8")
    parsed = {
        int(match.group(1)): match.group(2)
        for match in re.finditer(r"^\| (\d) \| (XS|S|M|L|XL) \|$", text, re.MULTILINE)
    }

    # Act / Assert
    assert parsed == SIZE


def test_waves_are_valid() -> None:
    # Arrange
    waves = {cells[6] for cells in _m4_rows(_text())}

    # Act / Assert
    assert waves == {"1", "2", "3"}


def test_epics_are_valid() -> None:
    # Arrange
    epics = {cells[3].strip("`") for cells in _m4_rows(_text())}

    # Act / Assert
    assert epics <= EPICS


def test_priorities_are_valid() -> None:
    # Arrange
    priorities = {cells[5] for cells in _m4_rows(_text())}

    # Act / Assert
    assert priorities <= {"P0", "P1", "P2"}


def test_every_m4_hu_has_spec() -> None:
    # Arrange
    specs = [cells[7] for cells in _m4_rows(_text())]

    # Act / Assert
    assert all(re.search(r"\d{3}", spec) for spec in specs)


def test_board_doc_lists_required_views() -> None:
    # Arrange
    text = BOARD.read_text(encoding="utf-8")

    # Act / Assert
    for view in ("Por integrante", "Por ola", "Por épica"):
        assert view in text


def test_board_doc_explains_burndown() -> None:
    # Arrange
    text = BOARD.read_text(encoding="utf-8").lower()

    # Act / Assert
    assert "burndown" in text
    assert "insights" in text
