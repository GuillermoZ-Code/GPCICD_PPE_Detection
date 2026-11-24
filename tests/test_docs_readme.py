"""Pruebas del mapa de documentación (HU-112, issue #168)."""

from __future__ import annotations

import re
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "docs" / "README.md"

LINK = re.compile(r"\]\(([^)]+)\)")
AREAS = ("Gobierno", "Curso", "Operación", "Datos y modelo", "Arquitectura", "Specs")
TERMS = ("MaaS", "SDD", "DinD", "mAP", "NMS", "AGPL", "Droplet", "ONNX")


def _text() -> str:
    return README.read_text(encoding="utf-8")


def test_readme_exists() -> None:
    """AC-01: el mapa existe y tiene tabla por tema."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "| Tema |" in text
    assert "## Glosario" in text


def test_map_covers_key_areas() -> None:
    """AC-01: el mapa cubre las areas clave."""
    # Arrange / Act
    text = _text()

    # Assert
    for area in AREAS:
        assert area in text, f"falta el area {area}"


def test_glossary_has_required_terms() -> None:
    """AC-02: el glosario define los terminos obligatorios."""
    # Arrange / Act
    text = _text().replace("**", "")

    # Assert
    for term in TERMS:
        assert f"| {term} |" in text, f"falta el termino {term}"


def test_relative_links_resolve() -> None:
    """AC-03: cada enlace relativo apunta a un archivo o carpeta existente."""
    # Arrange
    links = LINK.findall(_text())

    # Act
    broken = [
        link
        for link in links
        if not link.startswith(("http://", "https://", "#", "mailto:"))
        and not (README.parent / link.split("#")[0]).resolve().exists()
    ]

    # Assert
    assert links, "el documento no tiene enlaces"
    assert not broken, f"enlaces rotos: {broken}"
