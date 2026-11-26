"""Pruebas de CODEOWNERS y checks obligatorios (HU-082, issue #138)."""

from __future__ import annotations

from pathlib import Path

from ppe_detection.tools.ownership import load_manifest, render_codeowners

ROOT = Path(__file__).resolve().parents[1]
ADR = ROOT / "docs" / "adr" / "0012-codeowners-checks-obligatorios.md"
CODEOWNERS = ROOT / ".github" / "CODEOWNERS"
CHECKS = (
    "Asignar revisor",
    "Calidad",
    "Frontend",
    "Matriz",
    "Plantilla",
    "Propiedad",
    "Specs",
)


def test_codeowners_refleja_el_manifiesto_ac_01() -> None:
    """AC-01: CODEOWNERS es exactamente la proyección del manifiesto."""
    # Arrange
    manifest = load_manifest()

    # Act
    generado = render_codeowners(manifest)
    versionado = CODEOWNERS.read_text(encoding="utf-8")

    # Assert
    assert versionado == generado


def test_codeowners_cubre_duenos_y_bloqueos_ac_01() -> None:
    """AC-01: dueños y rutas de un solo escritor aparecen en CODEOWNERS."""
    # Arrange
    manifest = load_manifest()
    lineas = CODEOWNERS.read_text(encoding="utf-8").splitlines()

    # Act
    reglas = [linea for linea in lineas if linea and not linea.startswith("#")]

    # Assert
    for dueno in manifest.owners:
        assert any(linea.endswith(f"@{dueno}") for linea in reglas)
    for ruta, dueno in manifest.locked.items():
        assert f"{ruta} @{dueno}" in reglas


def test_adr_lista_checks_requeridos_ac_02() -> None:
    """AC-02: el ADR enumera los siete checks y no activa protección técnica."""
    # Arrange / Act
    texto = ADR.read_text(encoding="utf-8")

    # Assert
    for check in CHECKS:
        assert check in texto
    assert "protección escrita" in texto
    assert "pendiente de aprobación" in texto


def test_adr_actualiza_proteccion_escrita_ac_03() -> None:
    """AC-03: el ADR 0012 actualiza al 0004 sin reescribirlo y queda indexado."""
    # Arrange
    anterior = ROOT / "docs" / "adr" / "0004-gitflow-spec-kit-merge.md"
    indice = ROOT / "docs" / "adr" / "README.md"

    # Act
    texto = ADR.read_text(encoding="utf-8")

    # Assert
    assert "ADR 0004" in texto
    assert "regla escrita" in anterior.read_text(encoding="utf-8")
    assert "[0012](0012-codeowners-checks-obligatorios.md)" in indice.read_text(encoding="utf-8")
