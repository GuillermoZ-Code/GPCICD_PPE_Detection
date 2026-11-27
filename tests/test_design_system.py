"""HU-076 — sistema de diseño de la SPA (AC-01, AC-02 y AC-03).

Pruebas estáticas: leen `design.css`, `main.tsx` e `index.html`. El aspecto real se
comprueba con `npm run test` y abriendo la SPA; aquí se fija el contrato del sistema.
"""

from __future__ import annotations

from pathlib import Path

DESIGN = Path("frontend/src/design.css")
MAIN = Path("frontend/src/main.tsx")
INDEX = Path("frontend/index.html")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-076 · AC-01


def test_dark_theme_declares_the_six_tokens() -> None:
    """AC-01: la paleta oscura declara fondo, panel, tinta, secundario, regla y señal."""
    # Arrange
    css = _read(DESIGN)

    # Assert
    for token in ("--bg:", "--panel-solid:", "--text:", "--muted:", "--line:", "--accent:"):
        assert token in css, f"falta {token}"


def test_light_theme_overrides_paper_and_ink() -> None:
    """AC-01: el tema claro es papel frío con tinta casi negra."""
    # Arrange
    css = _read(DESIGN)

    # Assert
    assert ":root[data-theme='light']" in css
    assert "--bg: #edefe9" in css
    assert "--text: #14170f" in css


def test_only_one_loud_accent_colour() -> None:
    """AC-01: el amarillo de señal es el único color fuerte de la paleta."""
    # Arrange
    css = _read(DESIGN)

    # Assert
    assert css.count("--accent: #f5c400") >= 2  # tema oscuro y claro
    assert "--on-accent: #14170f" in css


# --------------------------------------------------------------- HU-076 · AC-02


def test_panels_are_flat_with_small_radius() -> None:
    """AC-02: reglas de 1 px y radio 0-2 px, sin sombras de tarjeta."""
    # Arrange
    css = _read(DESIGN)

    # Assert
    assert "--radius: 2px" in css
    assert "--shadow: none" in css
    assert "border-radius: 0" in css


def test_typography_is_one_superfamily_with_a_condensed_display() -> None:
    """AC-02: Barlow Condensed para titulares y Barlow para texto, con respaldo."""
    # Arrange
    css = _read(DESIGN)

    # Assert
    assert "--font-display: 'Barlow Condensed'" in css
    assert "--font-body: 'Barlow'" in css
    assert "system-ui" in css


def test_result_numbers_are_tabular() -> None:
    """AC-02: las cifras del reporte se alinean en columna."""
    # Arrange
    css = _read(DESIGN)

    # Assert
    assert "font-variant-numeric: tabular-nums" in css


# --------------------------------------------------------------- HU-076 · AC-03


def test_design_file_loads_after_the_base_styles() -> None:
    """AC-03: el sistema se aplica después del CSS existente, sin reescribirlo."""
    # Arrange
    main = _read(MAIN)

    # Act
    base = main.index("styles.css")
    design = main.index("design.css")

    # Assert
    assert base < design


def test_motion_is_opt_out_and_focus_is_visible() -> None:
    """AC-03: se respeta `prefers-reduced-motion` y el foco de teclado se ve."""
    # Arrange
    css = _read(DESIGN)

    # Assert
    assert "@media (prefers-reduced-motion: reduce)" in css
    assert ":focus-visible" in css


def test_fonts_and_theme_colour_are_declared_in_the_document() -> None:
    """AC-03: el documento carga las fuentes y declara el color de la barra."""
    # Arrange
    html = _read(INDEX)

    # Assert
    assert "Barlow+Condensed" in html
    assert 'name="theme-color"' in html
