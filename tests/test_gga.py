"""HU-075 — Pruebas del hook opcional de GGA."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from ppe_detection.tools import gga_hook

ROOT = Path(__file__).resolve().parents[1]
GGA = ROOT / ".gga"
PRECOMMIT = ROOT / ".pre-commit-config.yaml"
DOC = ROOT / "docs" / "operacion" / "gga.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_gga_config_uses_opencode_and_the_constitution() -> None:
    """AC-01: el proveedor es local y las reglas salen de CONSTITUTION."""

    # Arrange
    config = _read(GGA)

    # Assert
    assert 'PROVIDER="opencode"' in config
    assert 'RULES_FILE="CONSTITUTION.md"' in config
    assert 'PR_BASE_BRANCH="develop"' in config


def test_gga_config_reviews_code_and_excludes_artifacts() -> None:
    """AC-01: se revisan fuentes y se excluyen dependencias y artefactos."""

    # Arrange
    config = _read(GGA)

    # Assert
    assert "src/*" in config
    assert "frontend/src/*" in config
    assert ".venv/*" in config
    assert "node_modules/*" in config


def test_precommit_declares_the_optional_hook() -> None:
    """AC-02: pre-commit invoca el wrapper opcional, no a GGA directamente."""

    # Arrange
    config = _read(PRECOMMIT)

    # Assert
    assert "gga-optional" in config
    assert "uv run python -m ppe_detection.tools.gga_hook" in config
    assert "pass_filenames: false" in config


def test_hook_is_not_blocking_when_gga_is_absent() -> None:
    """AC-02: sin GGA, el hook devuelve 0 y no ejecuta ningún proceso."""

    # Arrange
    calls: list[object] = []

    def runner(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        calls.append((args, kwargs))
        return subprocess.CompletedProcess(args=[], returncode=1)

    # Act
    code = gga_hook.run_gga(which=lambda _: None, runner=runner)

    # Assert
    assert code == 0
    assert calls == []


def test_hook_propagates_gga_exit_code_when_available() -> None:
    """AC-02: con GGA instalado, el resultado de la revisión se propaga."""

    # Arrange
    calls: list[list[str]] = []

    def runner(command: list[str], *, check: bool) -> subprocess.CompletedProcess[str]:
        calls.append(command)
        assert check is False
        return subprocess.CompletedProcess(args=command, returncode=2)

    # Act
    code = gga_hook.run_gga(
        ("--diff-only",),
        which=lambda _: "C:/bin/gga.exe",
        runner=runner,
    )

    # Assert
    assert code == 2
    assert calls == [["gga", "run", "--diff-only"]]


def test_main_prints_a_skip_message_without_gga(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """AC-02: la ausencia de GGA se informa y no se convierte en error."""

    # Arrange
    monkeypatch.setattr(gga_hook, "gga_available", lambda: False)

    # Act
    code = gga_hook.main([])

    # Assert
    assert code == 0
    assert "no está instalado" in capsys.readouterr().out


def test_runbook_documents_the_optional_behavior() -> None:
    """AC-02: el runbook explica que GGA no bloquea y no sustituye la revisión."""

    # Arrange
    text = _read(DOC)

    # Assert
    assert "opcional y no bloqueante" in text
    assert "no sustituye la revisión humana" in text
    assert "gga run --pr-mode" in text


def test_gga_config_has_no_literal_tokens() -> None:
    """AC-01: la configuración versionada no contiene credenciales."""

    # Arrange
    config = _read(GGA)

    # Assert
    for marker in ("glpat-", "dop_v1_", "dckr_pat_", "ghp_"):
        assert marker not in config
