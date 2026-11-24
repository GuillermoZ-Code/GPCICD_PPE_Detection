"""Pruebas del informe de rúbrica (HU-113, issue #169)."""

from __future__ import annotations

from pathlib import Path

from ppe_detection.tools import rubrica

ITEM = rubrica.RubricItem("R-99", "Área", "Criterio", "docs/x.md", "Jesús")


def test_validate_items_accepts_complete() -> None:
    """AC-03: un ítem completo es válido."""
    # Arrange / Act
    errors = rubrica.validate_items([ITEM])

    # Assert
    assert errors == []


def test_validate_items_rejects_missing_owner() -> None:
    """AC-03: un ítem sin responsable no es válido."""
    # Arrange
    bad = rubrica.RubricItem("R-98", "Área", "Criterio", "docs/x.md", "")

    # Act
    errors = rubrica.validate_items([bad])

    # Assert
    assert errors and "R-98" in errors[0]


def test_build_rows_marks_existing_evidence(tmp_path: Path) -> None:
    """AC-01: la evidencia existente se marca."""
    # Arrange
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "x.md").write_text("# x\n", encoding="utf-8")

    # Act
    rows = rubrica.build_rows(tmp_path, [ITEM])

    # Assert
    assert rows[0].exists is True


def test_build_rows_marks_missing_evidence(tmp_path: Path) -> None:
    """AC-02: la evidencia ausente se marca como pendiente."""
    # Act
    rows = rubrica.build_rows(tmp_path, [ITEM])

    # Assert
    assert rows[0].exists is False


def test_render_lists_all_items() -> None:
    """AC-01: el informe lista cada ítem."""
    # Arrange
    rows = rubrica.build_rows(Path("."), [ITEM])

    # Act
    report = rubrica.render(rows, generated_at="2026-11-23 00:00 UTC")

    # Assert
    assert "R-99" in report
    assert "| ID | Área | Criterio | Evidencia | Responsable | Estado |" in report


def test_render_marks_ok_and_pending() -> None:
    """AC-02: usa ✔ y ✘ según la evidencia."""
    # Arrange
    rows = [rubrica.ReportRow(ITEM, True), rubrica.ReportRow(ITEM, False)]

    # Act
    report = rubrica.render(rows, generated_at="2026-11-23 00:00 UTC")

    # Assert
    assert "✔" in report
    assert "✘" in report
    assert "cumplidos: 1" in report
    assert "27/11/2026" in report


def test_write_report_creates_file(tmp_path: Path) -> None:
    """AC-03: el informe se escribe en UTF-8."""
    # Arrange
    content = rubrica.render([rubrica.ReportRow(ITEM, True)], generated_at="2026-11-23")
    target = tmp_path / "docs" / "entrega" / "RUBRICA-M4.md"

    # Act
    written = rubrica.write_report(target, content)

    # Assert
    assert written == target
    assert target.read_text(encoding="utf-8").endswith("\n")


def test_main_check_passes_with_real_rubric() -> None:
    """AC-03: el comando valida la rúbrica real sin fallar."""
    # Act
    code = rubrica.main(["--check"])

    # Assert
    assert code == 0
