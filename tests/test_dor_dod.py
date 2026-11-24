"""Pruebas de la DoR y la DoD del M4 (HU-107, issue #163).

AC-01 criterios de entrada, AC-02 criterios de salida y AC-03 guia actualizada.
Las pruebas son autocontenidas: no dependen de otras ramas ni de red.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRIBUTING_PATH = ROOT / "CONTRIBUTING.md"

HEADING = re.compile(r"^#{2,3} ")
CHECKBOX = re.compile(r"^- \[ \] .+")


def _contributing() -> str:
    return CONTRIBUTING_PATH.read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    """Minúsculas, sin backticks y con espacios colapsados."""
    return re.sub(r"\s+", " ", text.replace("`", "")).strip().casefold()


def _section(text: str, heading: str) -> str:
    """Devuelve el cuerpo de un encabezado de nivel 3 hasta el próximo encabezado."""
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == f"### {heading}":
            body: list[str] = []
            for following in lines[index + 1 :]:
                if HEADING.match(following):
                    break
                body.append(following)
            return "\n".join(body)
    raise AssertionError(f"falta la seccion {heading!r} en CONTRIBUTING.md")


def _checkboxes(section: str) -> list[str]:
    return [line for line in section.splitlines() if CHECKBOX.match(line.strip())]


def test_dor_lists_entry_criteria() -> None:
    """AC-01: la DoR exige spec, AC, SP, dueno y dependencias."""
    # Arrange
    text = _contributing()

    # Act
    dor = _section(text, "Definition of Ready (DoR)")
    dor_text = _normalize(dor)

    # Assert
    for keyword in ("spec", "criterios de aceptación", "story points", "dueño", "dependencias"):
        assert keyword in dor_text, f"la DoR no menciona {keyword!r}"
    assert len(_checkboxes(dor)) >= 5, "la DoR debe tener al menos cinco items"


def test_dod_lists_exit_criteria() -> None:
    """AC-02: la DoD exige pruebas, make check, PR, issue cerrada y conteo."""
    # Arrange
    text = _contributing()

    # Act
    dod = _section(text, "Definition of Done (DoD)")
    dod_text = _normalize(dod)

    # Assert
    for keyword in ("prueba", "make check", "aprobación", "issue", "conteo"):
        assert keyword in dod_text, f"la DoD no menciona {keyword!r}"
    assert "docs/curso/pruebas.md" in dod_text
    assert len(_checkboxes(dod)) >= 5, "la DoD debe tener al menos cinco items"


def test_contributing_has_dor_dod_sections() -> None:
    """AC-03: la guia tiene la seccion y la enlaza desde la tabla de contenidos."""
    # Arrange
    text = _contributing()

    # Act
    has_heading = "Criterios de entrada y salida (DoR / DoD)" in text
    has_toc_link = "criterios-de-entrada-y-salida" in text
    has_ready = "### Definition of Ready (DoR)" in text
    has_done = "### Definition of Done (DoD)" in text

    # Assert
    assert has_heading, "falta la seccion de criterios de entrada y salida"
    assert has_toc_link, "la tabla de contenidos no enlaza la seccion nueva"
    assert has_ready and has_done, "faltan los encabezados de DoR y DoD"


def test_dor_and_dod_items_are_checkboxes() -> None:
    """AC-03: cada criterio es una casilla marcable, no un parrafo suelto."""
    # Arrange
    text = _contributing()

    # Act
    sections = {
        "DoR": _section(text, "Definition of Ready (DoR)"),
        "DoD": _section(text, "Definition of Done (DoD)"),
    }

    # Assert
    for name, section in sections.items():
        bullets = [line for line in section.splitlines() if line.strip().startswith("- ")]
        boxes = _checkboxes(section)
        assert bullets, f"{name} no tiene criterios"
        assert len(boxes) == len(bullets), f"{name} tiene criterios que no son casillas"
