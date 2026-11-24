"""Pruebas del contador de pruebas (HU-094, issue #150).

AC-01 suma pytest y Vitest, AC-02 tabla por archivo e integrante y AC-03 salidas
simuladas. Ninguna prueba lanza pytest ni Vitest.
"""

from __future__ import annotations

import json
from pathlib import Path

from ppe_detection.tools import pruebas
from ppe_detection.tools.ownership import Manifest

PYTEST_DOUBLE_QUIET = "tests/test_api.py: 2\ntests/test_metrics.py: 35\n\n"
PYTEST_IDS = "tests/test_api.py::test_a\ntests/test_api.py::test_b\ntests/test_zzz.py::test_c\n"
VITEST_JSON = json.dumps(
    [
        {"name": "a", "file": "C:/repo/frontend/src/App.test.tsx"},
        {"name": "b", "file": "C:/repo/frontend/src/App.test.tsx"},
    ]
)


def _manifest() -> Manifest:
    return Manifest(
        owners={
            "ElianaCardona": ("tests/test_api*.py",),
            "GuillermoZ-Code": ("frontend/",),
        },
        locked={},
        names={
            "ElianaCardona": "Eliana Cardona",
            "GuillermoZ-Code": "Guillermo Zabala",
        },
    )


def test_pytest_counter_accepts_both_formats() -> None:
    """AC-01: el parser de pytest acepta doble quiet e ids de prueba."""
    # Arrange
    expected = {"tests/test_api.py": 2, "tests/test_metrics.py": 35}

    # Act
    from_quiet = pruebas.count_pytest(PYTEST_DOUBLE_QUIET)
    from_ids = pruebas.count_pytest(PYTEST_IDS)

    # Assert
    assert from_quiet == expected
    assert from_ids == {"tests/test_api.py": 2, "tests/test_zzz.py": 1}


def test_vitest_counter_reads_json() -> None:
    """AC-01: el parser de Vitest lee el JSON y normaliza la ruta."""
    # Act
    counts = pruebas.count_vitest(VITEST_JSON)

    # Assert
    assert counts == {"frontend/src/App.test.tsx": 2}


def test_report_maps_owner_from_manifest() -> None:
    """AC-02: cada archivo aparece con el dueno declarado en el manifiesto."""
    # Arrange
    pytest_counts = pruebas.count_pytest(PYTEST_DOUBLE_QUIET)
    vitest_counts = pruebas.count_vitest(VITEST_JSON)

    # Act
    rows = pruebas.build_rows(pytest_counts, vitest_counts, _manifest())

    # Assert
    owners = {row.path: row.owner for row in rows}
    assert owners["tests/test_api.py"] == "Eliana Cardona"
    assert owners["tests/test_metrics.py"] == "sin dueño"
    assert owners["frontend/src/App.test.tsx"] == "Guillermo Zabala"


def test_report_has_suite_and_owner_totals() -> None:
    """AC-02: el informe resume por suite y por integrante."""
    # Arrange
    pytest_counts = pruebas.count_pytest(PYTEST_DOUBLE_QUIET)
    vitest_counts = pruebas.count_vitest(VITEST_JSON)
    rows = pruebas.build_rows(pytest_counts, vitest_counts, _manifest())

    # Act
    report = pruebas.render_report(rows, generated_at="2026-11-23 00:00 UTC")

    # Assert
    assert "## 1. Resumen" in report
    assert "| Backend | pytest | 2 | 37 |" in report
    assert "| Frontend | Vitest | 1 | 2 |" in report
    assert "| **Total** | | **3** | **39** |" in report
    assert "| tests/test_api.py | pytest | 2 | Eliana Cardona |" in report
    assert "| Eliana Cardona | 2 | 0 | 2 |" in report
    assert "| Guillermo Zabala | 0 | 2 | 2 |" in report
    assert "2026-11-23 00:00 UTC" in report


def test_report_writes_markdown_to_target(tmp_path: Path) -> None:
    """AC-03: el informe se escribe en UTF-8 con salto de linea final."""
    # Arrange
    rows = pruebas.build_rows(
        pruebas.count_pytest(PYTEST_IDS),
        pruebas.count_vitest(VITEST_JSON),
        _manifest(),
    )
    content = pruebas.render_report(rows, generated_at="2026-11-23 00:00 UTC")
    target = tmp_path / "reporte-de-prueba.md"

    # Act
    written = pruebas.write_report(target, content)

    # Assert
    assert written == target
    text = target.read_text(encoding="utf-8")
    assert text.endswith("\n")
    assert "## 2. Desglose por archivo" in text


def test_report_renders_unowned_files_explicitly() -> None:
    """AC-02: un archivo sin dueno se muestra como 'sin dueno', no se inventa."""
    # Arrange
    rows = pruebas.build_rows({"tests/test_zzz.py": 1}, {}, _manifest())

    # Act
    report = pruebas.render_report(rows, generated_at="2026-11-23 00:00 UTC")

    # Assert
    assert "| tests/test_zzz.py | pytest | 1 | sin dueño |" in report
    assert "| sin dueño | 1 | 0 | 1 |" in report
