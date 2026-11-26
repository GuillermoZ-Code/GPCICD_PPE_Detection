"""AC-01, AC-02 y AC-03 (HU-085) — ADR de GitLab CI y Droplet.

Pruebas estáticas: leen los ADR, el índice y la constitución; no requieren red.
"""

from __future__ import annotations

import re
from pathlib import Path

ADR_DIR = Path("docs/adr")
ADR_0007 = ADR_DIR / "0007-gitlab-ci-espejo.md"
ADR_0008 = ADR_DIR / "0008-droplet-caddy.md"
INDEX = ADR_DIR / "README.md"
CONSTITUTION = Path("CONSTITUTION.md")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- AC-01 · decisión


def test_adr_0007_decides_gitlab_ci_with_mirror() -> None:
    """AC-01: el ADR 0007 decide GitLab CI con espejo desde GitHub."""
    # Arrange / Act
    adr = _read(ADR_0007)

    # Assert
    assert "GitLab CI/CD con espejo desde GitHub" in adr
    assert "Estado:** Aceptada" in adr
    assert "mirror-gitlab.yml" in adr


def test_adr_0008_decides_droplet_with_caddy() -> None:
    """AC-01: el ADR 0008 decide Droplet con Docker Compose y Caddy."""
    # Arrange / Act
    adr = _read(ADR_0008)

    # Assert
    assert "Droplet" in adr
    assert "Caddy" in adr
    assert "Estado:** Aceptada" in adr
    assert "compose.prod.yml" in adr


# ---------------------------------------------------------------- AC-02 · alternativas


def test_adrs_record_discarded_alternatives() -> None:
    """AC-02: se registran Premium, Render y Hugging Face como descartados."""
    # Arrange
    text = _read(ADR_0007) + _read(ADR_0008)

    # Act / Assert
    for alternative in ("Premium", "Render", "Hugging Face"):
        assert alternative in text, f"falta la alternativa descartada {alternative!r}"


# ---------------------------------------------------------------- AC-03 · enlaces


def test_constitution_links_both_adrs() -> None:
    """AC-03: la constitución enlaza el 0007 y el 0008."""
    # Arrange / Act
    constitution = _read(CONSTITUTION)

    # Assert
    assert "docs/adr/0007-gitlab-ci-espejo.md" in constitution
    assert "docs/adr/0008-droplet-caddy.md" in constitution


def test_adr_index_lists_and_links_the_new_adrs() -> None:
    """AC-03: el índice lista ambos ADR y sus enlaces apuntan a archivos existentes."""
    # Arrange
    index = _read(INDEX)

    # Act
    linked = set(re.findall(r"\]\((000[78]-[^)]+\.md)\)", index))

    # Assert
    assert linked == {ADR_0007.name, ADR_0008.name}
    for name in linked:
        assert (ADR_DIR / name).is_file(), f"el índice enlaza un archivo inexistente: {name}"
