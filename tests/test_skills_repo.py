"""AC-01, AC-02 y AC-03 (HU-074) — skills versionadas en el repositorio.

Pruebas estáticas: comprueban la estructura de `.agents/skills/` y la tabla de
`AGENTS.md`, sin red ni agentes.
"""

from __future__ import annotations

from pathlib import Path

SKILLS = Path(".agents/skills")
AGENTS = Path("AGENTS.md")
GLAB = SKILLS / "glab" / "SKILL.md"
FRONTEND_DESIGN = SKILLS / "frontend-design" / "SKILL.md"
LICENSE = SKILLS / "frontend-design" / "LICENSE.txt"
README = SKILLS / "README.md"


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    """Devuelve el bloque YAML entre los dos primeros separadores `---`."""
    assert text.startswith("---"), "el SKILL.md no empieza con frontmatter YAML"
    _, frontmatter, _ = text.split("---", 2)
    return frontmatter


# ---------------------------------------------------------------- AC-01 · instalación


def test_glab_skill_is_versioned_in_the_repository() -> None:
    """AC-01: la skill oficial de `glab` vive en `.agents/skills/glab/`."""
    # Arrange / Act
    frontmatter = _frontmatter(_read(GLAB))

    # Assert
    assert "name: glab" in frontmatter


def test_frontend_design_skill_is_versioned_with_its_license() -> None:
    """AC-01: `frontend-design` se versiona con su licencia Apache-2.0."""
    # Arrange / Act
    frontmatter = _frontmatter(_read(FRONTEND_DESIGN))
    license_text = _read(LICENSE)

    # Assert
    assert "name: frontend-design" in frontmatter
    assert "Apache License" in license_text


# ---------------------------------------------------------------- AC-02 · AGENTS.md


def test_agents_table_lists_both_skills() -> None:
    """AC-02: la tabla de `AGENTS.md` documenta `glab` y `frontend-design`."""
    # Arrange / Act
    agents = _read(AGENTS)

    # Assert
    assert "`frontend-design`" in agents
    assert "`glab`" in agents
    assert ".agents/skills/" in agents


# ---------------------------------------------------------------- AC-03 · descubrimiento


def test_skills_have_name_and_description_for_discovery() -> None:
    """AC-03: cada skill expone `name` y `description`, que es lo que el agente lista."""
    # Arrange
    skills = {
        "glab": _frontmatter(_read(GLAB)),
        "frontend-design": _frontmatter(_read(FRONTEND_DESIGN)),
    }

    # Act / Assert
    for name, frontmatter in skills.items():
        assert f"name: {name}" in frontmatter
        assert "description:" in frontmatter


def test_skills_readme_documents_origin_and_update() -> None:
    """AC-03: el README explica origen, actualización y alcance de cada skill."""
    # Arrange / Act
    readme = _read(README)

    # Assert
    assert "`glab`" in readme
    assert "`frontend-design`" in readme
    assert "glab skills install" in readme
    assert "npx skills add" in readme


def test_user_level_skills_are_not_duplicated() -> None:
    """AC-03: las skills pesadas o personales no se copian al repositorio."""
    # Arrange / Act
    versioned = {path.name for path in SKILLS.iterdir() if path.is_dir()}

    # Assert
    assert "archify" not in versioned
    assert "jan-project-standard" not in versioned
