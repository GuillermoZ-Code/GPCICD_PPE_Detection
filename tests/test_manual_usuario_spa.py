"""Pruebas estructurales del manual de usuario de la SPA (HU-058, issue #114)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "docs" / "manual" / "README.md"
CAPTURAS = ROOT / "docs" / "manual" / "capturas"
PNG_NAMES = (
    "01-seleccion.png",
    "02-analisis.png",
    "03-resultados.png",
    "04-sin-detecciones.png",
)


def _text() -> str:
    return MANUAL.read_text(encoding="utf-8")


def _png(name: str) -> None:
    path = CAPTURAS / name
    assert path.is_file(), f"falta la captura {name}"
    assert path.stat().st_size > 1_000, f"captura vacía: {name}"
    assert path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", f"no es PNG: {name}"


def test_ac_01_flujo_con_capturas_reales() -> None:
    """AC-01: el manual describe el flujo rediseñado y enlaza sus capturas."""
    # Arrange
    text = _text()

    # Act / Assert
    assert "## 3. Flujo paso a paso" in text
    for step in ("01 Selección", "02 Análisis", "03 Resultados"):
        assert step in text, f"falta el paso {step}"
    for name in PNG_NAMES[:3]:
        assert f"capturas/{name}" in text, f"el manual no enlaza {name}"
        _png(name)


def test_ac_02_sin_detecciones_y_limites_explicitos() -> None:
    """AC-02: el resultado vacío se explica con sus límites."""
    # Arrange
    text = _text()

    # Act / Assert
    assert "## 5. Cuando no hay detecciones" in text
    for phrase in (
        "no significa que no haya EPP",
        "umbral de confianza",
        "filtros",
        "no certifica el cumplimiento",
    ):
        assert phrase in text, f"falta la explicación: {phrase}"
    assert "capturas/04-sin-detecciones.png" in text
    _png("04-sin-detecciones.png")


def test_ac_03_estructura_y_enlaces_del_manual() -> None:
    """AC-03: secciones, enlaces y fecha de verificación están presentes."""
    # Arrange
    text = _text()

    # Act / Assert
    headings = (
        "# Manual de usuario de la SPA",
        "## 1. Qué necesitas",
        "## 2. Qué verás",
        "## 3. Flujo paso a paso",
        "## 4. Leer los resultados",
        "## 5. Cuando no hay detecciones",
        "## 6. Si algo falla",
        "## 7. Verificación",
    )
    positions = [text.find(heading) for heading in headings]
    assert all(position >= 0 for position in positions), "falta una sección obligatoria"
    assert positions == sorted(positions), "las secciones están fuera de orden"
    assert "errores.md" in text
    assert "Fecha de verificación: 2026-11-28" in text
    assert "HU-077" in text and "PR #267" in text


def test_capturas_declaran_origen_local() -> None:
    """AC-01/AC-03: las capturas se declaran como demo local, no validación remota."""
    # Arrange
    text = _text()

    # Act / Assert
    assert "API simulada" in text
    assert "no es una validación del sitio remoto" in text
    assert text.count("![Captura") >= len(PNG_NAMES)
    for name in PNG_NAMES:
        _png(name)
