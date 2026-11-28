"""Pruebas del informe de sprint y del burndown (HU-103, issue #159)."""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path

import pytest

from ppe_detection.tools.sprint import Closed, SprintError, burndown, deviation, velocity_by_person

ROOT = Path(__file__).resolve().parents[1]
SPRINT = ROOT / "docs" / "curso" / "M4" / "SPRINT.md"
BACKLOG = ROOT / "docs" / "curso" / "backlog.md"


def test_burndown_with_simulated_data() -> None:
    # Arrange
    closed = [
        Closed(day=date(2026, 11, 24), sp=5, owner="a"),
        Closed(day=date(2026, 11, 24), sp=3, owner="b"),
        Closed(day=date(2026, 11, 25), sp=2, owner="a"),
    ]

    # Act
    points = burndown(closed, total_sp=20)

    # Assert
    assert [(point.closed_sp, point.remaining_sp) for point in points] == [(8, 12), (2, 10)]


def test_burndown_without_closures_is_empty() -> None:
    # Act / Assert
    assert burndown([], total_sp=20) == []


def test_burndown_rejects_invalid_total() -> None:
    # Act / Assert
    with pytest.raises(SprintError, match="positivo"):
        burndown([], total_sp=0)


def test_burndown_rejects_closures_over_total() -> None:
    # Arrange
    closed = [Closed(day=date(2026, 11, 24), sp=21)]

    # Act / Assert
    with pytest.raises(SprintError, match="superan"):
        burndown(closed, total_sp=20)


def test_velocity_by_person_sums_sp() -> None:
    # Arrange
    closed = [
        Closed(day=date(2026, 11, 24), sp=5, owner="Guillermo"),
        Closed(day=date(2026, 11, 25), sp=3, owner="Guillermo"),
        Closed(day=date(2026, 11, 25), sp=2, owner="Eliana"),
        Closed(day=date(2026, 11, 25), sp=1, owner=None),
    ]

    # Act
    velocity = velocity_by_person(closed)

    # Assert
    assert velocity == {"Eliana": 2, "Guillermo": 8}


def test_deviation_signs() -> None:
    # Act / Assert
    assert deviation(planned=50, delivered=45) == -10.0
    assert deviation(planned=50, delivered=60) == 20.0
    assert deviation(planned=50, delivered=50) == 0.0


def test_deviation_rejects_zero_plan() -> None:
    # Act / Assert
    with pytest.raises(SprintError, match="positivo"):
        deviation(planned=0, delivered=10)


def test_doc_burndown_is_monotonic() -> None:
    # Arrange
    text = SPRINT.read_text(encoding="utf-8")
    rows = [
        (int(sp), int(remaining))
        for sp, remaining in re.findall(r"^\| \d{2}/11 \| \d+ \| (\d+) \| (\d+) \|$", text, re.M)
    ]

    # Act
    remaining = [200]
    for closed_sp, _value in rows[1:]:
        remaining.append(remaining[-1] - closed_sp)

    # Assert
    assert rows[0] == (0, 200)
    assert [value for _, value in rows] == remaining


def test_doc_remaining_equals_open_hus() -> None:
    # Arrange
    text = SPRINT.read_text(encoding="utf-8")
    last_remaining = int(re.findall(r"^\| \d{2}/11 \| \d+ \| \d+ \| (\d+) \|$", text, re.M)[-1])
    open_sp = sum(int(sp) for sp in re.findall(r"^\| HU-\d{3} \| #\d+ \| (\d+) \|", text, re.M))

    # Act / Assert
    assert last_remaining == open_sp == 20


def test_backlog_has_hundred_m4_hus() -> None:
    # Arrange
    rows = [
        [cell.strip() for cell in line.strip().strip("|").split("|")]
        for line in BACKLOG.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("| HU-")
    ]
    m4 = [cells for cells in rows if len(cells) >= 9 and re.search(r"\[#\d+\]", cells[1])]

    # Act / Assert
    assert len(m4) == 100
    assert sum(int(cells[4]) for cells in m4) == 200
