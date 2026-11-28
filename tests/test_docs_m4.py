"""HU-087 — documentación de gobierno sincronizada con el M4.

Pruebas estáticas: leen `CONSTITUTION.md`, `AGENTS.md`, `README.md` y la
constitución derivada de `.specify/memory/`. No abren red ni dependen del
entorno; solo verifican que la documentación no se quede en el M3.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CONSTITUTION = REPO / "CONSTITUTION.md"
DERIVED = REPO / ".specify" / "memory" / "constitution.md"
AGENTS = REPO / "AGENTS.md"
README = REPO / "README.md"

_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
_SKIP_PREFIXES = ("http://", "https://", "mailto:", "#", "tel:")


def _read(path: Path) -> str:
    """Lee un documento esperado; su ausencia falla con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def _links(text: str) -> list[str]:
    """Devuelve los destinos internos de los enlaces Markdown."""
    found: list[str] = []
    for raw in _LINK.findall(text):
        target = raw.strip()
        if target.startswith(_SKIP_PREFIXES):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if target:
            found.append(target)
    return found


# --------------------------------------------------------------- HU-087 — AC-01


def test_ac01_constitution_documents_m4_stack_roadmap_and_risks() -> None:
    """AC-01: la constitución declara stack, roadmap, riesgos y decisiones M4."""
    # Arrange
    text = _read(CONSTITUTION)

    # Assert
    assert "| **Módulo activo** | M4" in text
    for term in (
        "YOLO26n",
        "ONNX",
        "GitLab CI",
        "Droplet",
        "Caddy",
        "ADR 0009",
        "ADR 0013",
        "1.200",
    ):
        assert term in text, f"falta {term} en CONSTITUTION.md"


# --------------------------------------------------------------- HU-087 — AC-02


def test_ac02_derived_constitution_is_synced_with_m4() -> None:
    """AC-02: la constitución derivada repite los principios y el foco M4."""
    # Arrange
    text = _read(DERIVED)

    # Assert
    assert "DERIVADO, NO FUENTE DE VERDAD" in text
    assert "**Versión:** 1.2" in text
    for term in ("M4", "YOLO26n", "GitLab CI", "Droplet", "Caddy", "1.200"):
        assert term in text, f"falta {term} en la constitución derivada"


# --------------------------------------------------------------- HU-087 — AC-03


def test_ac03_internal_links_in_governance_docs_resolve() -> None:
    """AC-03: los enlaces internos de la documentación de gobierno existen."""
    # Arrange
    broken: list[str] = []

    # Act
    for document in (CONSTITUTION, AGENTS, README):
        base = document.parent
        for target in _links(_read(document)):
            if not (base / target).exists():
                broken.append(f"{document.name} -> {target}")

    # Assert
    assert not broken, "enlaces internos rotos: " + ", ".join(broken)


def test_ac01_readme_reflects_the_m4_model_and_deployment() -> None:
    """AC-01: el README describe el modelo y el despliegue reales del M4."""
    # Arrange
    text = _read(README)

    # Assert
    assert "yolo26n-clean" in text
    assert "https://143.198.10.157.sslip.io" in text
    assert "ONNX" in text
    assert "Caddy" in text
    assert "yolo11s-clean" not in text
