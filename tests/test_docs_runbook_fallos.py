"""Pruebas del runbook de diagnóstico de fallos (HU-056, issue #112)."""

from __future__ import annotations

import re
from pathlib import Path

RUNBOOK = Path(__file__).resolve().parents[1] / "docs" / "operacion" / "fallos.md"

STAGES = ("pipeline", "registry", "SSH", "contenedor", "proxy", "modelo")
COMMANDS = ("glab", "docker logs", "docker inspect", "curl")
DRILL_IDS = ("F1", "F2", "F3")
DRILL_FIELDS = ("Síntoma", "Verificación", "Acción", "Resultado esperado")


def _text() -> str:
    return RUNBOOK.read_text(encoding="utf-8")


def test_runbook_has_six_stage_decision_tree() -> None:
    """AC-01: el árbol cubre las seis etapas del despliegue."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "## Árbol de decisión" in text
    for stage in STAGES:
        assert stage in text, f"falta la etapa {stage}"


def test_each_stage_has_symptom_and_action() -> None:
    """AC-01: cada etapa define qué observar y qué hacer."""
    # Arrange
    text = _text()

    # Act
    sections = re.findall(r"^###\s+(.*)$", text, flags=re.M)

    # Assert
    assert len(STAGES) <= len(sections)
    assert text.count("Síntoma") >= len(STAGES)
    assert text.count("Acción") >= len(STAGES)


def test_required_commands_are_documented() -> None:
    """AC-02: están las cuatro herramientas de diagnóstico exigidas."""
    # Arrange / Act
    text = _text()

    # Assert
    for command in COMMANDS:
        assert command in text, f"falta el comando {command}"


def test_commands_have_expected_interpretation() -> None:
    """AC-02: cada comando indica cómo interpretar su salida."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "## Recetario de comandos" in text
    assert text.count("Interpretación") >= len(COMMANDS)


def test_three_drills_are_documented() -> None:
    """AC-03: hay tres fallos simulados con los cuatro campos obligatorios."""
    # Arrange
    text = _text()

    # Act
    blocks = re.findall(r"^###\s+(F[123][^\n]*)\n(.*?)(?=^###\s|\Z)", text, flags=re.M | re.S)

    # Assert
    assert {block[0][:2] for block in blocks} >= set(DRILL_IDS)
    assert len(blocks) == 3
    for _title, body in blocks:
        for field in DRILL_FIELDS:
            assert field in body, f"falta el campo {field} en el fallo simulado"


def test_drill_log_distinguishes_static_and_team_validation() -> None:
    """AC-03: el registro no confunde revisión documental con ensayo del equipo."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "## Registro de ensayos" in text
    assert "Validación estática" in text
    assert "Ensayo del equipo" in text
    assert "Pendiente" in text
