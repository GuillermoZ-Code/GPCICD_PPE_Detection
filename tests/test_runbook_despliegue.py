"""Pruebas estructurales del runbook de despliegue (HU-055, issue #111)."""

from __future__ import annotations

from pathlib import Path

RUNBOOK = Path("docs/operacion/despliegue.md")


def _text() -> str:
    assert RUNBOOK.is_file(), "falta docs/operacion/despliegue.md"
    return RUNBOOK.read_text(encoding="utf-8")


def test_runbook_covers_hu_055() -> None:
    # Act
    text = _text()

    # Assert
    assert "HU-055" in text


def test_runbook_has_all_sections() -> None:
    # Act
    text = _text()

    # Assert
    for section in (
        "## 1. Arquitectura desplegada",
        "## 3. Despliegue normal",
        "## 4. Despliegue manual",
        "## 5. Rollback",
        "## 6. Diagnóstico",
        "## 7. Aprovisionamiento",
        "## 8. Apagado",
    ):
        assert section in text


def test_pipeline_deploy_is_documented() -> None:
    # Act
    text = _text()

    # Assert
    assert "build_image" in text
    assert "deploy.sh" in text
    assert "healthchecks" in text


def test_manual_deploy_has_exact_commands() -> None:
    # Act
    text = _text()

    # Assert
    assert "ssh -i" in text
    assert "deploy.sh <tag>" in text
    assert "8 caracteres" in text


def test_rollback_documents_previous_tag() -> None:
    # Act
    text = _text()

    # Assert
    assert ".deployed_env" in text
    assert "<tag-anterior>" in text
    assert "Automático" in text


def test_diagnostics_section_has_commands() -> None:
    # Act
    text = _text()

    # Assert
    assert "docker compose -f compose.prod.yml logs" in text
    assert "sha256sum /opt/ppe/models/best.pt" in text
    assert "curl -fsS" in text


def test_provisioning_is_idempotent() -> None:
    # Act
    text = _text()

    # Assert
    assert "provision.sh" in text
    assert "idempotente" in text
    assert "UFW" in text


def test_model_is_mounted_read_only() -> None:
    # Act
    text = _text()

    # Assert
    assert ":ro" in text
    assert "SHA256" in text


def test_runbook_has_no_secrets() -> None:
    # Act
    text = _text()

    # Assert
    for marker in ("$2a$", "$2b$", "$2y$"):
        assert marker not in text
    assert "BEGIN " + "OPENSSH PRIVATE KEY" not in text


def test_documented_domain_is_current() -> None:
    # Act
    text = _text()

    # Assert
    assert "143.198.10.157.sslip.io" in text
