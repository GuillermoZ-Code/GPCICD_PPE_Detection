"""Pruebas del checklist de release v1.0.0 (HU-111, issue #167)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "docs" / "entrega" / "RELEASE-V1.0.0.md"
CHANGELOG = ROOT / "CHANGELOG.md"
SHA = "e36ae555c4dd173817ac7b8dd3054d3426c90e3d"
MODEL_SHA = "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9"


def _text() -> str:
    return RELEASE.read_text(encoding="utf-8")


def test_release_doc_exists() -> None:
    # Act / Assert
    assert RELEASE.is_file()


def test_release_doc_records_tag_and_merge_commit() -> None:
    # Arrange
    text = _text()

    # Act / Assert
    assert "v1.0.0" in text
    assert SHA in text
    assert "2026-11-28" in text
    assert re.search(r"`v1\.0\.0`", text)


def test_release_doc_has_complete_checklist() -> None:
    # Arrange
    text = _text()

    # Act
    done = len(re.findall(r"^- \[x\] ", text, flags=re.MULTILINE))
    pending = len(re.findall(r"^- \[ \] ", text, flags=re.MULTILINE))

    # Assert
    assert done >= 10
    assert pending >= 1


def test_release_doc_declares_test_gap() -> None:
    # Arrange
    text = _text()

    # Act / Assert
    assert "1.168" in text
    assert "1.200" in text


def test_release_doc_associates_image_and_model() -> None:
    # Arrange
    text = _text()

    # Act / Assert
    assert "CI_REGISTRY_IMAGE" in text
    assert MODEL_SHA in text
    assert "yolo26n" in text


def test_release_doc_verifies_health() -> None:
    # Arrange
    text = _text()

    # Act / Assert
    assert "/health/ready" in text
    assert "yolo26n-clean" in text
    assert "model_loaded" in text


def test_release_doc_attributes_license_and_dataset() -> None:
    # Arrange
    text = _text()

    # Act / Assert
    assert "AGPL-3.0" in text
    assert "CC-BY-4.0" in text


def test_release_doc_documents_rollback() -> None:
    # Arrange
    text = _text()

    # Act / Assert
    assert "## 4. Rollback" in text
    assert "make deploy TAG=" in text


def test_release_doc_links_github_release() -> None:
    # Arrange
    text = _text()

    # Act / Assert
    assert "releases/tag/v1.0.0" in text


def test_changelog_has_release_notes() -> None:
    # Arrange
    text = CHANGELOG.read_text(encoding="utf-8")

    # Act / Assert
    assert re.search(r"^## \[1\.0\.0\] - \d{4}-\d{2}-\d{2}$", text, flags=re.MULTILINE)
