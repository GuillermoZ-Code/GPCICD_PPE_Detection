"""Pruebas del plan de pruebas hacia 1.200 (HU-095, issue #151).

AC-01 baseline y objetivo unicos, AC-02 reparto que cuadra y AC-03 fecha y comando.
"""

from __future__ import annotations

import re
from pathlib import Path

PLAN_PATH = Path(__file__).resolve().parents[1] / "docs" / "curso" / "PLAN-PRUEBAS.md"

BASELINE = 533
TARGET = 1200
GAP = TARGET - BASELINE
BY_INTEGRATOR = {
    "Guillermo Zabala": 192,
    "Hernán Estrada": 112,
    "Eliana Cardona": 192,
    "Jesús Riveros": 171,
}


def _plan() -> str:
    return PLAN_PATH.read_text(encoding="utf-8")


def test_plan_has_one_baseline_and_target() -> None:
    """AC-01: el plan declara un baseline, un objetivo y una brecha que cuadran."""
    # Arrange
    plan = _plan()

    # Act / Assert
    assert f"| **Punto de partida** | **{BASELINE}**" in plan
    assert f"| **Objetivo** | **{TARGET:,}**".replace(",", ".") in plan
    assert f"| **Brecha** | **{GAP}**" in plan
    assert BASELINE + GAP == TARGET


def test_plan_splits_remaining_tests_by_integrator() -> None:
    """AC-02: el reparto por integrante suma exactamente la brecha."""
    # Arrange
    plan = _plan()

    # Act
    missing = [name for name in BY_INTEGRATOR if f"| {name} |" not in plan]
    total = sum(BY_INTEGRATOR.values())

    # Assert
    assert not missing, f"faltan integrantes en el reparto: {missing}"
    assert total == GAP, f"el reparto suma {total}, se esperaban {GAP}"
    assert "| **Total** | **768** | **104** | **664** | **+3** | **667** |" in plan


def test_plan_documents_counting_command_and_date() -> None:
    """AC-03: el plan dice como se cuenta y cuando se midio."""
    # Arrange
    plan = _plan()

    # Act / Assert
    assert "make pruebas-write" in plan
    assert re.search(r"2026-11-\d{2}", plan), "falta la fecha de medicion"


def test_plan_keeps_correction_history() -> None:
    """AC-01: las cifras anteriores quedan como historial, no como baseline."""
    # Arrange
    plan = _plan()
    history = plan.split("## 5. Historial de correcciones", maxsplit=1)[-1]

    # Act / Assert
    assert "375" in history
    assert "451" in history
    assert "| **Punto de partida** | **451**" not in plan
