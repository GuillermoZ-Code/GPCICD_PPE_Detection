"""Pruebas del comando de calidad (HU-012)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from ppe_detection.tools import calidad


def _result(name: str = "pruebas", returncode: int = 0, output: str = "ok") -> calidad.Result:
    return calidad.Result(
        check=calidad.Check(name=name, command=("pytest", "-q")),
        returncode=returncode,
        output=output,
    )


def test_main_returns_zero_when_all_checks_pass(monkeypatch, capsys) -> None:
    """AC-01: la suite informa y devuelve 0 cuando todo pasa."""
    # Arrange
    monkeypatch.setattr(calidad, "run_all", lambda *args, **kwargs: [_result()])

    # Act
    code = calidad.main([])

    # Assert
    assert code == 0
    assert "OK" in capsys.readouterr().out


def test_deliberate_regression_makes_main_fail(monkeypatch, capsys) -> None:
    """AC-02: una verificación fallida devuelve un código distinto de cero."""
    # Arrange
    monkeypatch.setattr(
        calidad,
        "run_all",
        lambda *args, **kwargs: [_result(returncode=1, output="1 failed")],
    )

    # Act
    code = calidad.main([])

    # Assert
    assert code == 1
    assert "FALLO" in capsys.readouterr().out


def test_render_report_marks_failure() -> None:
    """FR-002/FR-003: el informe distingue OK de FALLO y resume el total."""
    # Act
    text = calidad.render_report([_result("ruff"), _result("pruebas", 1)])

    # Assert
    assert "[OK] ruff" in text
    assert "[FALLO] pruebas" in text
    assert "1/2" in text


def test_ruff_reports_configured_violation(tmp_path: Path) -> None:
    """AC-03: Ruff detecta un import sin usar con la configuración del proyecto."""
    # Arrange
    path = tmp_path / "violacion.py"
    path.write_text("import os\n", encoding="utf-8")

    # Act
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    # Assert
    assert result.returncode != 0
    assert "F401" in result.stdout


def test_default_checks_do_not_require_gpu_or_dataset() -> None:
    """AC-04: la suite por defecto no depende de GPU ni del dataset completo."""
    # Act
    commands = " ".join(" ".join(check.command) for check in calidad.DEFAULT_CHECKS)

    # Assert
    assert "cuda" not in commands.lower()
    assert "dataset" not in commands.lower()
    assert "artifacts" not in commands.lower()
