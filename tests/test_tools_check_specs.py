"""Pruebas del validador de specs (HU-096, issue #152).

AC-01 archivos y AC sin evidencia, AC-02 local/CI y AC-03 specs de ejemplo en tmp_path.
"""

from __future__ import annotations

from pathlib import Path

from ppe_detection.tools import check_specs

VALID = """# Feature Specification: HU-099

## User Scenarios & Testing

1. **AC-01**: dado algo.

## Requirements

- **FR-001**: algo.

## Success Criteria

- **SC-001**: algo.

## Acceptance → Test

| AC | Evidencia |
|---|---|
| AC-01 | `tests/test_demo.py` |
"""


def _spec(
    root: Path,
    name: str = "099-hu-099-demo",
    *,
    body: str = VALID,
    plan: bool = True,
    tasks: bool = True,
    spec_file: bool = True,
) -> Path:
    directory = root / "specs" / name
    directory.mkdir(parents=True, exist_ok=True)
    if spec_file:
        (directory / "spec.md").write_text(body, encoding="utf-8")
    if plan:
        (directory / "plan.md").write_text("# Plan\n", encoding="utf-8")
    if tasks:
        (directory / "tasks.md").write_text("# Tasks\n", encoding="utf-8")
    return directory


def _test_file(
    root: Path,
    name: str = "test_demo.py",
    body: str = "def test_algo():\n    pass\n",
) -> None:
    path = root / "tests" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_missing_spec_file_fails(tmp_path: Path) -> None:
    """AC-01: sin spec.md el validador falla."""
    # Arrange
    _spec(tmp_path, spec_file=False)

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert any("spec.md" in error for error in errors)


def test_missing_plan_file_fails(tmp_path: Path) -> None:
    """AC-01: sin plan.md el validador falla."""
    # Arrange
    _spec(tmp_path, plan=False)

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert any("plan.md" in error for error in errors)


def test_missing_tasks_file_fails(tmp_path: Path) -> None:
    """AC-01: sin tasks.md el validador falla."""
    # Arrange
    _spec(tmp_path, tasks=False)

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert any("tasks.md" in error for error in errors)


def test_missing_section_fails(tmp_path: Path) -> None:
    """AC-01: una spec sin las secciones obligatorias falla."""
    # Arrange
    body = VALID.replace("## Success Criteria", "## Otra cosa")
    _spec(tmp_path, body=body)
    _test_file(tmp_path)

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert any("Success Criteria" in error for error in errors)


def test_declared_ac_without_row_fails(tmp_path: Path) -> None:
    """AC-01: un AC declarado sin fila de evidencia falla."""
    # Arrange
    body = VALID.replace("1. **AC-01**: dado algo.", "1. **AC-01**: uno.\n2. **AC-02**: dos.")
    _spec(tmp_path, body=body)
    _test_file(tmp_path)

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert any("AC-02" in error for error in errors)


def test_broken_test_reference_fails(tmp_path: Path) -> None:
    """AC-01: una prueba citada que no existe falla."""
    # Arrange
    body = VALID.replace("`tests/test_demo.py`", "`tests/test_fantasma.py`")
    _spec(tmp_path, body=body)
    _test_file(tmp_path)

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert any("test_fantasma" in error for error in errors)


def test_bare_test_name_resolves(tmp_path: Path) -> None:
    """AC-01: un nombre de prueba suelto se busca en tests/."""
    # Arrange
    body = VALID.replace("`tests/test_demo.py`", "`test_algo`")
    _spec(tmp_path, body=body)
    _test_file(tmp_path)

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert errors == []


def test_frontend_test_reference_resolves(tmp_path: Path) -> None:
    """AC-01: una prueba de Vitest se resuelve bajo frontend/."""
    # Arrange
    body = VALID.replace("`tests/test_demo.py`", "`App.test.tsx`")
    _spec(tmp_path, body=body)
    frontend = tmp_path / "frontend" / "src" / "App.test.tsx"
    frontend.parent.mkdir(parents=True)
    frontend.write_text("// test\n", encoding="utf-8")

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert errors == []


def test_document_evidence_is_accepted(tmp_path: Path) -> None:
    """AC-01: un documento existente es evidencia valida."""
    # Arrange
    body = VALID.replace("`tests/test_demo.py`", "`docs/evaluation/HU-099.md`")
    _spec(tmp_path, body=body)
    evidence = tmp_path / "docs" / "evaluation" / "HU-099.md"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("# Informe\n", encoding="utf-8")

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert errors == []


def test_legacy_spec_only_checks_files(tmp_path: Path) -> None:
    """AC-03: una spec anterior a 092 solo exige los tres archivos."""
    # Arrange
    _spec(tmp_path, name="010-hu-008-evaluacion", body="# Spec vieja\n")

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert errors == []


def test_validate_reports_all_problems(tmp_path: Path) -> None:
    """AC-03: el validador acumula los problemas de varias specs."""
    # Arrange
    _spec(tmp_path, name="099-hu-099-uno", plan=False)
    _spec(tmp_path, name="100-hu-100-dos", tasks=False)

    # Act
    errors = check_specs.validate(tmp_path)

    # Assert
    assert len(errors) >= 2


def test_main_returns_nonzero_with_problems(tmp_path: Path) -> None:
    """AC-02: el comando devuelve codigo distinto de cero con problemas."""
    # Arrange
    _spec(tmp_path, spec_file=False)

    # Act
    code = check_specs.main(["--check", "--root", str(tmp_path)])

    # Assert
    assert code == 1


def test_main_returns_zero_without_problems(tmp_path: Path) -> None:
    """AC-02: el comando devuelve cero cuando todo esta bien."""
    # Arrange
    _spec(tmp_path)
    _test_file(tmp_path)

    # Act
    code = check_specs.main(["--check", "--root", str(tmp_path)])

    # Assert
    assert code == 0
