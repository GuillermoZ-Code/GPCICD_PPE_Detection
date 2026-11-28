"""Pruebas del pipeline de GitLab en `make estado` (HU-106, issue #162)."""

from __future__ import annotations

import json
from datetime import UTC, datetime

import pytest

from ppe_detection.tools import estado
from ppe_detection.tools.estado import GITLAB_BRANCH, Pipeline, Report, parse_pipeline, render

PIPELINES = json.dumps(
    [
        {
            "id": 10,
            "status": "success",
            "sha": "899e87e1234567890",
            "web_url": "https://gitlab.com/educacional-group/GPCICD_PPE_Detection/-/pipelines/10",
        },
        {
            "id": 9,
            "status": "failed",
            "sha": "abcdef0",
            "web_url": "https://gitlab.com/x/-/pipelines/9",
        },
    ]
)


def _report(pipeline: Pipeline | None = None, note: str | None = None) -> Report:
    return Report(
        generated_at=datetime(2026, 11, 27, tzinfo=UTC),
        branch="develop",
        dirty=0,
        ahead=0,
        behind=0,
        develop="899e87e",
        commits=("899e87e feat: algo",),
        prs=(),
        issues=(),
        warnings=(),
        pipeline=pipeline,
        gitlab_note=note,
    )


def test_parse_pipeline_reads_first_run() -> None:
    """AC-03: se toma el pipeline más reciente de la respuesta."""
    # Act
    pipeline = parse_pipeline(PIPELINES)

    # Assert
    assert pipeline == Pipeline(
        status="success",
        sha="899e87e1234567890",
        web_url="https://gitlab.com/educacional-group/GPCICD_PPE_Detection/-/pipelines/10",
    )


def test_parse_pipeline_accepts_single_object() -> None:
    """AC-03: una respuesta con un solo objeto también es válida."""
    # Arrange
    payload = json.dumps(
        {"status": "running", "sha": "abc1234", "web_url": "https://gitlab.com/x/-/pipelines/1"}
    )

    # Act
    pipeline = parse_pipeline(payload)

    # Assert
    assert pipeline is not None
    assert pipeline.status == "running"


def test_parse_pipeline_rejects_empty_list() -> None:
    """AC-03: sin pipelines no hay datos."""
    # Act / Assert
    assert parse_pipeline("[]") is None


def test_parse_pipeline_rejects_missing_fields() -> None:
    """AC-03: falta un campo obligatorio."""
    # Arrange
    payload = json.dumps([{"status": "success", "sha": "abc"}])

    # Act / Assert
    assert parse_pipeline(payload) is None


def test_parse_pipeline_rejects_invalid_json() -> None:
    """AC-03: una salida que no es JSON no rompe el estado."""
    # Act / Assert
    assert parse_pipeline("no es json") is None


def test_render_shows_pipeline() -> None:
    """AC-02: el estado muestra estado y URL del pipeline."""
    # Arrange
    pipeline = Pipeline(status="success", sha="899e87e1234567890", web_url="https://gitlab.com/x/1")

    # Act
    text = render(_report(pipeline))

    # Assert
    assert "**GitLab:**" in text
    assert "success" in text
    assert "https://gitlab.com/x/1" in text


def test_render_shows_short_sha() -> None:
    """AC-02: el SHA se muestra corto."""
    # Arrange
    pipeline = Pipeline(status="failed", sha="899e87e1234567890", web_url="https://gitlab.com/x/1")

    # Act
    text = render(_report(pipeline))

    # Assert
    assert "`899e87e`" in text


def test_render_without_pipeline_shows_note() -> None:
    """AC-01: sin glab se indica, no se falla."""
    # Act
    text = render(_report(None, "glab no está instalado"))

    # Assert
    assert "no disponible" in text
    assert "glab no está instalado" in text


def test_collect_gitlab_without_glab_returns_note(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-01: si glab no está, devuelve nota y no falla."""
    # Arrange
    monkeypatch.setattr(estado.shutil, "which", lambda _: None)
    warnings: list[str] = []

    # Act
    pipeline, note = estado._collect_gitlab(warnings)

    # Assert
    assert pipeline is None
    assert note == "glab no está instalado"
    assert warnings


def test_collect_gitlab_with_glab_parses(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-01: con glab disponible, consulta y parsea."""
    # Arrange
    monkeypatch.setattr(estado.shutil, "which", lambda _: "glab")
    monkeypatch.setattr(estado, "run", lambda command: PIPELINES)

    # Act
    pipeline, note = estado._collect_gitlab([])

    # Assert
    assert note is None
    assert pipeline is not None and pipeline.status == "success"


def test_collect_gitlab_reports_failed_command(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-01: si glab falla, se avisa sin romper."""
    # Arrange
    monkeypatch.setattr(estado.shutil, "which", lambda _: "glab")
    monkeypatch.setattr(estado, "run", lambda command: None)
    warnings: list[str] = []

    # Act
    pipeline, note = estado._collect_gitlab(warnings)

    # Assert
    assert pipeline is None
    assert note == "no se pudo consultar el pipeline de GitLab"


def test_gitlab_branch_is_develop() -> None:
    """AC-02: el pipeline consultado es el de la rama de integración."""
    # Assert
    assert GITLAB_BRANCH == "develop"
