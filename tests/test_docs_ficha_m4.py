"""Pruebas de la ficha y el guion de sustentación M4 (HU-057, issue #113)."""

from __future__ import annotations

import re
from pathlib import Path

FICHA = Path(__file__).resolve().parents[1] / "docs" / "entrega" / "FICHA-M4.md"

BLOCKS = (
    "0:00\u20132:00",
    "2:00\u20135:00",
    "5:00\u20138:00",
    "8:00\u201311:00",
    "11:00\u201313:30",
    "13:30\u201315:00",
)
TOPICS = ("CI/CD", "Docker", "mAP", "runbook", "riesgos", "retrospectiva")
CHECKLIST_ITEMS = ("develop", "tablero", "uv sync", "PPE_MODEL_PATH", "Docker", "SPA", "CI")
RESPONSIBLES = ("Eliana", "Hernán", "Guillermo", "Jesús")


def _text() -> str:
    return FICHA.read_text(encoding="utf-8")


def test_ficha_exists_and_has_script() -> None:
    """AC-01: la ficha existe y contiene el guion de sustentación."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "## Guion de la sustentación" in text
    assert "## 1. Datos rápidos" in text


def test_script_has_six_time_blocks() -> None:
    """AC-01: los bloques cubren de 0:00 a 15:00 sin huecos."""
    # Arrange / Act
    text = _text()

    # Assert
    for block in BLOCKS:
        assert block in text, f"falta el bloque {block}"


def test_each_block_has_speaker_and_evidence() -> None:
    """AC-01: cada bloque declara responsable y evidencia mostrada."""
    # Arrange
    text = _text()

    # Act
    blocks = re.findall(
        r"^###\s+(\d{1,2}:\d{2}\u2013\d{1,2}:\d{2})[^\n]*\n(.*?)(?=^###\s|\Z)",
        text,
        flags=re.M | re.S,
    )

    # Assert
    assert len(blocks) == len(BLOCKS)
    for _interval, body in blocks:
        assert "**Responsable:**" in body
        assert "**Evidencia:**" in body


def test_script_covers_required_topics() -> None:
    """AC-01: el guion menciona las evidencias exigidas por la rúbrica."""
    # Arrange / Act
    text = _text()

    # Assert
    for topic in TOPICS:
        assert topic in text, f"falta el tema {topic}"
    for name in RESPONSIBLES:
        assert name in text, f"falta el responsable {name}"


def test_checklist_has_responsible_column() -> None:
    """AC-02: el checklist del entorno tiene responsable por ítem."""
    # Arrange
    text = _text()

    # Act
    section = text.split("## Checklist del entorno (§5.4)", 1)[1].split("\n## ", 1)[0]

    # Assert
    for column in ("Ítem", "Comando", "Criterio", "Responsable"):
        assert column in section, f"falta la columna {column}"
    rows = [line for line in section.splitlines() if line.startswith("| ")]
    assert len(rows) >= 8, "el checklist tiene menos de seis ítems"


def test_checklist_covers_environment_items() -> None:
    """AC-02: el checklist cubre repo, entorno, modelo, contenedor y CI."""
    # Arrange
    text = _text()
    section = text.split("## Checklist del entorno (§5.4)", 1)[1].split("\n## ", 1)[0]

    # Assert
    for item in CHECKLIST_ITEMS:
        assert item in section, f"falta el ítem {item}"


def test_timed_rehearsal_log_exists() -> None:
    """AC-03: existe el registro cronometrado por bloque."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "## Ensayo cronometrado" in text
    assert "Objetivo" in text
    assert "Real" in text
    assert "Estado" in text


def test_rehearsal_rows_have_goal_real_and_status() -> None:
    """AC-03: hay una fila de ensayo por cada bloque del guion."""
    # Arrange
    text = _text()
    section = text.split("## Ensayo cronometrado", 1)[1].split("\n## ", 1)[0]

    # Act
    rows = [line for line in section.splitlines() if re.match(r"^\|\s*\d{1,2}:\d{2}", line)]

    # Assert
    assert len(rows) == len(BLOCKS)
    for row in rows:
        cells = [cell.strip() for cell in row.split("|")]
        assert len(cells) >= 5
        assert cells[2], "falta la duración objetivo"
        assert cells[3], "falta la duración real"
        assert cells[4], "falta el estado"


def test_rehearsal_distinguishes_static_and_team_execution() -> None:
    """AC-03: no se afirma un ensayo real que no se ejecutó."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "Validación estática" in text
    assert "Ensayo del equipo" in text
    assert "Pendiente" in text
