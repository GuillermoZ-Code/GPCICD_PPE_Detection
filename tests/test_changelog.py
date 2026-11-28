"""Pruebas de formato del CHANGELOG y las notas v1.0.0 (HU-064, issue #120)."""

from __future__ import annotations

import re
from pathlib import Path

CHANGELOG = Path(__file__).resolve().parents[1] / "CHANGELOG.md"

CATEGORIES = ("### Added", "### Changed", "### Fixed")
REPO = "https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection"


def _text() -> str:
    return CHANGELOG.read_text(encoding="utf-8")


def test_keep_a_changelog_header_is_present() -> None:
    """AC-01: el archivo declara el estándar Keep a Changelog y SemVer."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "# Changelog" in text
    assert "Keep a Changelog" in text
    assert "Semantic Versioning" in text


def test_unreleased_precedes_release_section() -> None:
    """AC-01: Unreleased aparece antes que la versión 1.0.0."""
    # Arrange / Act
    text = _text()

    # Assert
    assert "## [Unreleased]" in text
    assert re.search(r"^## \[1\.0\.0\] - \d{4}-\d{2}-\d{2}$", text, flags=re.M)
    assert text.index("## [Unreleased]") < text.index("## [1.0.0]")


def test_release_notes_link_real_hus_and_prs() -> None:
    """AC-02: las notas de v1.0.0 enlazan HUs y PRs del repositorio."""
    # Arrange
    text = _text()

    # Act
    notes = text.split("## [1.0.0]", 1)[1].split("\n## ", 1)[0]
    issues = re.findall(rf"{REPO}/issues/\d+", notes)
    pulls = re.findall(rf"{REPO}/pull/\d+", notes)

    # Assert
    assert len(issues) >= 4, f"faltan HUs enlazadas: {issues}"
    assert len(pulls) >= 4, f"faltan PRs enlazados: {pulls}"
    assert "v1.0.0" in notes


def test_categories_and_iso_date_are_valid() -> None:
    """AC-03: las categorías canónicas y las viñetas están presentes."""
    # Arrange / Act
    text = _text()
    notes = text.split("## [1.0.0]", 1)[1].split("\n## ", 1)[0]

    # Assert
    for category in CATEGORIES:
        assert category in notes, f"falta la categoría {category}"
        section = notes.split(category, 1)[1].split("\n### ", 1)[0]
        assert re.search(r"^- \[.+\]\(.+\) — ", section, flags=re.M), (
            f"las entradas de {category} no usan viñetas con enlace"
        )
