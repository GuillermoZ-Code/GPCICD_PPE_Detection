"""Pruebas de capacidad y velocidad real (HU-109, issue #165)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from ppe_detection.tools.sprint import SprintError, capacity, deviation

CAPACIDAD = Path(__file__).resolve().parents[1] / "docs" / "curso" / "M4" / "CAPACIDAD.md"
ROW = re.compile(
    r"^\| ([A-Za-zÁÉÍÓÚáéíóúñ ]+) \| (\d+) \| (\d+) \| (-?\d+,\d) % \| ([\d,]+) \|$",
    re.MULTILINE,
)


def _rows() -> list[tuple[str, int, int, float, float]]:
    text = CAPACIDAD.read_text(encoding="utf-8")
    return [
        (name, int(plan), int(done), float(dev.replace(",", ".")), float(rate.replace(",", ".")))
        for name, plan, done, dev, rate in ROW.findall(text)
    ]


def test_capacity_per_person_day() -> None:
    # Act / Assert
    assert capacity(delivered_sp=184, people=4, days=10) == 4.6


@pytest.mark.parametrize(("people", "days"), [(0, 10), (4, 0), (-1, 10)])
def test_capacity_rejects_invalid_inputs(people: int, days: int) -> None:
    # Act / Assert
    with pytest.raises(SprintError, match="positivos"):
        capacity(delivered_sp=184, people=people, days=days)


def test_deviation_against_plan() -> None:
    # Act / Assert
    assert deviation(planned=50, delivered=45) == -10.0
    assert deviation(planned=50, delivered=47) == -6.0
    assert deviation(planned=50, delivered=50) == 0.0
    assert deviation(planned=50, delivered=42) == -16.0


def test_doc_table_sums_to_total() -> None:
    # Arrange
    rows = _rows()

    # Act
    planned = sum(row[1] for row in rows)
    delivered = sum(row[2] for row in rows)

    # Assert
    assert (planned, delivered) == (200, 184)
    assert len(rows) == 4


def test_doc_deviation_matches_numbers() -> None:
    # Act / Assert
    for _name, planned, delivered, stated, _rate in _rows():
        assert deviation(planned=planned, delivered=delivered) == stated


def test_doc_capacity_matches_numbers() -> None:
    # Act / Assert
    for _name, _plan, delivered, _dev, stated in _rows():
        assert capacity(delivered_sp=delivered, people=1, days=10) == stated


def test_doc_states_one_to_one_ratio() -> None:
    # Arrange
    text = CAPACIDAD.read_text(encoding="utf-8")

    # Act / Assert
    assert "1 SP ≈ 1 día" in text
    assert "5 veces" in text


def test_doc_remaining_matches_open_hus() -> None:
    # Arrange
    text = CAPACIDAD.read_text(encoding="utf-8")

    # Act / Assert
    assert "16 SP" in text
    for issue in ("#111", "#114", "#136", "#144", "#165", "#166", "#167"):
        assert issue in text
