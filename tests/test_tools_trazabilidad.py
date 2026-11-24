"""Pruebas de la matriz de trazabilidad (HU-093, issue #149).

AC-01 origenes de datos, AC-02 marcas de faltantes y AC-03 compuerta de CI.
Ninguna prueba invoca `gh` ni usa red.
"""

from __future__ import annotations

import json
from pathlib import Path

from ppe_detection.tools import trazabilidad

ISSUES = {
    "HU-091": {"number": 147, "state": "CLOSED"},
    "HU-092": {"number": 148, "state": "CLOSED"},
    "HU-093": {"number": 149, "state": "OPEN"},
}
ISSUE_TO_HU = {147: "HU-091", 148: "HU-092", 149: "HU-093"}


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _spec(root: Path, name: str, body: str = "# Spec\n") -> None:
    _write(root / "specs" / name / "spec.md", body)


def test_specs_map_hu_to_directory(tmp_path: Path) -> None:
    """AC-01: cada carpeta de spec se asocia a su HU."""
    # Arrange
    _spec(tmp_path, "092-hu-091-plantilla-hu")
    _spec(tmp_path, "093-hu-092-backlog-espejo")
    _spec(tmp_path, "001-ta-contract-first")

    # Act
    mapping = trazabilidad.specs_by_hu(tmp_path)

    # Assert
    assert mapping == {
        "HU-091": "092-hu-091-plantilla-hu",
        "HU-092": "093-hu-092-backlog-espejo",
    }


def test_tests_mentioning_hu_are_detected(tmp_path: Path) -> None:
    """AC-01: una prueba que menciona HU-NNN cuenta para esa HU."""
    # Arrange
    _write(tmp_path / "tests" / "test_a.py", '"""HU-091."""\n')
    _write(tmp_path / "frontend" / "src" / "App.test.tsx", "// HU-007\n")
    _write(tmp_path / "tests" / "test_b.py", '"""sin referencia."""\n')

    # Act
    mapping = trazabilidad.tests_by_hu(tmp_path)

    # Assert
    assert mapping == {"HU-091": {"tests/test_a.py"}, "HU-007": {"App.test.tsx"}}


def test_tests_from_spec_and_mentions_are_merged(tmp_path: Path) -> None:
    """AC-01: las pruebas citadas por la spec se suman a las que mencionan la HU."""
    # Arrange
    _spec(
        tmp_path,
        "092-hu-091-plantilla-hu",
        "| AC | Prueba |\n|---|---|\n| AC-01 | `tests/test_issue_template.py` |\n",
    )
    _write(tmp_path / "tests" / "test_extra.py", '"""HU-091."""\n')
    specs = trazabilidad.specs_by_hu(tmp_path)

    # Act
    cited = trazabilidad.spec_tests(tmp_path, specs)

    # Assert
    assert cited == {"HU-091": {"test_issue_template.py"}}


def test_spec_test_citations_include_pytest_and_vitest(tmp_path: Path) -> None:
    """AC-01: la tabla de aceptación puede citar pytest y Vitest."""
    # Arrange
    _spec(
        tmp_path,
        "005-hu-007-interfaz",
        "| AC | Prueba |\n|---|---|\n"
        "| AC-1 | `tests/test_api.py` |\n"
        "| AC-2 | `src/App.test.tsx` |\n",
    )

    # Act
    cited = trazabilidad.spec_tests(tmp_path, trazabilidad.specs_by_hu(tmp_path))

    # Assert
    assert cited == {"HU-007": {"test_api.py", "App.test.tsx"}}


def test_prs_link_issues_by_closes() -> None:
    """AC-01: una PR se enlaza por Closes #N."""
    # Arrange
    prs = [{"number": 179, "title": "feat: x", "body": "Closes #147", "headRefName": "f"}]

    # Act
    mapping = trazabilidad.prs_by_hu(prs, ISSUE_TO_HU)

    # Assert
    assert mapping == {"HU-091": {179}}


def test_prs_link_by_title_and_branch_slug() -> None:
    """AC-01: también se enlaza por título o por el slug de la rama."""
    # Arrange
    prs = [
        {"number": 1, "title": "docs: HU-092 backlog", "body": "", "headRefName": "x"},
        {"number": 2, "title": "feat: y", "body": "", "headRefName": "feature/094-hu-093-x"},
    ]

    # Act
    mapping = trazabilidad.prs_by_hu(prs, ISSUE_TO_HU)

    # Assert
    assert mapping == {"HU-092": {1}, "HU-093": {2}}


def test_matrix_marks_missing_spec() -> None:
    """AC-02: una HU cerrada sin spec queda marcada."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={"HU-091": {"number": 147, "state": "CLOSED"}},
        specs={},
        tests={"HU-091": {"test_a.py"}},
        prs={"HU-091": {179}},
    )

    # Act / Assert
    assert rows[0].missing == ("spec",)


def test_matrix_marks_missing_tests() -> None:
    """AC-02: una HU cerrada sin pruebas queda marcada."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={"HU-091": {"number": 147, "state": "CLOSED"}},
        specs={"HU-091": "092-hu-091"},
        tests={},
        prs={"HU-091": {179}},
    )

    # Act / Assert
    assert rows[0].missing == ("pruebas",)


def test_matrix_marks_complete_hu() -> None:
    """AC-02: con spec y pruebas no hay marca."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={"HU-091": {"number": 147, "state": "CLOSED"}},
        specs={"HU-091": "092-hu-091"},
        tests={"HU-091": {"test_a.py"}},
        prs={"HU-091": {179}},
    )

    # Act / Assert
    assert rows[0].missing == ()


def test_check_fails_on_closed_hu_without_spec() -> None:
    """AC-03: la compuerta falla con una HU cerrada sin spec."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={"HU-091": {"number": 147, "state": "CLOSED"}},
        specs={},
        tests={"HU-091": {"test_a.py"}},
        prs={},
    )

    # Act
    failures = trazabilidad.check(rows, exemptions={})

    # Assert
    assert failures and "HU-091" in failures[0] and "spec" in failures[0]


def test_check_fails_on_closed_hu_without_tests() -> None:
    """AC-03: la compuerta falla con una HU cerrada sin pruebas."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={"HU-091": {"number": 147, "state": "CLOSED"}},
        specs={"HU-091": "092-hu-091"},
        tests={},
        prs={},
    )

    # Act
    failures = trazabilidad.check(rows, exemptions={})

    # Assert
    assert failures and "pruebas" in failures[0]


def test_check_ignores_open_hu() -> None:
    """AC-03: una HU abierta puede no tener spec ni pruebas."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={"HU-149": {"number": 149, "state": "OPEN"}},
        specs={},
        tests={},
        prs={},
    )

    # Act
    failures = trazabilidad.check(rows, exemptions={})

    # Assert
    assert failures == []


def test_check_honors_exemptions() -> None:
    """AC-03: una HU documental exenta no rompe la compuerta."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={"HU-016": {"number": 72, "state": "CLOSED"}},
        specs={"HU-016": "017-hu-016-spike"},
        tests={},
        prs={},
    )

    # Act
    failures = trazabilidad.check(rows, exemptions={"HU-016": "spike documental"})

    # Assert
    assert failures == []


def test_render_has_table_and_totals() -> None:
    """AC-02: el informe es una tabla con totales."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues=ISSUES,
        specs={"HU-091": "092-hu-091", "HU-092": "093-hu-092"},
        tests={"HU-091": {"test_a.py"}},
        prs={"HU-091": {179}, "HU-092": {188}},
    )

    # Act
    report = trazabilidad.render(rows, generated_at="2026-11-23 00:00 UTC")

    # Assert
    assert "| HU | Issue | Estado | Spec | PR | Pruebas | Falta |" in report
    assert "| HU-091 |" in report
    assert "| HU-093 |" in report
    assert "HU-092" in report


def test_render_marks_missing_cells_with_dash() -> None:
    """AC-02: sin spec o pruebas la celda muestra un guion."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={"HU-091": {"number": 147, "state": "CLOSED"}},
        specs={},
        tests={},
        prs={},
    )

    # Act
    report = trazabilidad.render(rows, generated_at="2026-11-23 00:00 UTC")

    # Assert
    assert "| HU-091 | [#147]" in report
    assert "| — | — | — |" in report
    assert "spec, pr, pruebas" in report


def test_render_counts_complete_and_incomplete() -> None:
    """AC-02: el encabezado resume completas e incompletas."""
    # Arrange
    rows = trazabilidad.build_rows(
        issues={
            "HU-091": {"number": 147, "state": "CLOSED"},
            "HU-092": {"number": 148, "state": "CLOSED"},
        },
        specs={"HU-091": "092-hu-091"},
        tests={"HU-091": {"test_a.py"}},
        prs={"HU-091": {179}},
    )

    # Act
    report = trazabilidad.render(rows, generated_at="2026-11-23 00:00 UTC")

    # Assert
    assert "completas: 1" in report
    assert "incompletas: 1" in report


def test_load_issues_parses_gh_output() -> None:
    """AC-01: el JSON de `gh issue list` se convierte en el mapa de issues."""
    # Arrange
    payload = json.dumps(
        [
            {"number": 147, "title": "HU-091 — x", "state": "CLOSED"},
            {"number": 5, "title": "otra cosa", "state": "OPEN"},
        ]
    )

    # Act
    issues = trazabilidad.parse_issues(payload)

    # Assert
    assert issues == {"HU-091": {"number": 147, "state": "CLOSED"}}
