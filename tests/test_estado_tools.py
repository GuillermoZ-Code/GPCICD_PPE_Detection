"""Pruebas ampliadas de las herramientas de estado (sin git ni gh reales).

Cubre los FR de `ppe_detection.tools.estado`: parser de SP, render por
milestone, revisión/CI, bloque generado y salida por consola.
"""

from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from typing import Any

import pytest

from ppe_detection.tools import estado
from ppe_detection.tools.estado import (
    Issue,
    Report,
    main,
    parse_backlog_sp,
    render,
    render_summary,
    replace_block,
    summarize_checks,
    summarize_review,
)


def _report(**overrides: Any) -> Report:
    base = Report(
        generated_at=datetime(2026, 11, 12, 12, 0, tzinfo=UTC),
        branch="develop",
        dirty=0,
        ahead=0,
        behind=0,
        develop="6496621 (2026-11-12)",
        commits=("6496621 Merge pull request #54",),
        prs=(),
        issues=(),
        warnings=(),
    )
    return replace(base, **overrides)


def test_parse_backlog_sp_skips_hu_without_sp() -> None:
    # Arrange
    text = (
        "### HU-001 — Uno\n"
        "- **SP:** 1\n"
        "\n"
        "### HU-002 — Dos\n"
        "- **Labels:** `ep-01`\n"
        "\n"
        "### HU-003 — Tres\n"
        "- **SP:** 3\n"
    )

    # Act
    points = parse_backlog_sp(text)

    # Assert
    assert points == {"HU-001": 1, "HU-003": 3}


def test_parse_backlog_sp_ignores_sp_before_first_hu() -> None:
    # Arrange
    text = "**SP:** 99\n\n### HU-001 — Uno\n- **SP:** 1\n"

    # Act
    points = parse_backlog_sp(text)

    # Assert
    assert points == {"HU-001": 1}


def test_summarize_review_maps_states() -> None:
    # Act / Assert
    assert summarize_review("APPROVED") == "aprobada"
    assert summarize_review("CHANGES_REQUESTED") == "cambios"
    assert summarize_review("review_required") == "pendiente"
    assert summarize_review("") == "—"
    assert summarize_review("OTHER") == "other"


def test_summarize_checks_maps_states() -> None:
    # Act / Assert
    assert summarize_checks(None) == "—"
    assert summarize_checks([]) == "—"
    assert summarize_checks([{"conclusion": "SUCCESS"}]) == "ok"
    assert summarize_checks([{"conclusion": "FAILURE"}]) == "fallo"
    assert summarize_checks([{"state": "IN_PROGRESS"}]) == "en curso"
    assert summarize_checks([{"conclusion": "SUCCESS"}, {"state": "QUEUED"}]) == "en curso"
    assert summarize_checks([{"conclusion": "FAILURE"}, {"state": "IN_PROGRESS"}]) == "fallo"


def test_render_without_prs_or_issues() -> None:
    # Arrange
    report = _report(commits=(), prs=(), issues=())

    # Act
    text = render(report)

    # Assert
    assert "- (sin commits)" in text
    assert "**Pull requests abiertas (0):**" in text
    assert "- ninguna" in text
    assert "**Issues abiertas: 0 · 0 SP**" in text
    assert "**En revisión:** ninguna" in text
    assert "**Siguiente por orden:** sin issues abiertas" in text


def test_render_groups_issues_by_milestone() -> None:
    # Arrange
    report = _report(
        issues=(
            Issue(number=1, title="HU-001 — Uno", milestone="M3-S1", sp=1),
            Issue(number=3, title="HU-003 — Tres", milestone="M3-S1", sp=1),
            Issue(number=8, title="HU-008 — Ocho", milestone="M3-S2", sp=2),
            Issue(number=14, title="HU-014 — Catorce", milestone="M4-S3", sp=2),
        )
    )

    # Act
    text = render(report)

    # Assert
    assert "**Issues abiertas: 4 · 6 SP**" in text
    assert "- M3-S1 (2 SP): #1 #3" in text
    assert "- M3-S2 (2 SP): #8" in text
    assert "- M4-S3 (2 SP): #14" in text


def test_render_reports_dirty_and_divergence() -> None:
    # Arrange
    report = _report(dirty=2, ahead=3, behind=1)

    # Act
    text = render(report)

    # Assert
    assert "2 archivo(s) sin commit" in text
    assert "+3/-1 vs `origin/develop`" in text


def test_render_summary_without_issues() -> None:
    # Arrange
    report = _report(commits=(), prs=(), issues=())

    # Act
    text = render_summary(report)

    # Assert
    assert "**Issues abiertas:** 0 · 0 SP" in text
    assert "**En vuelo:** ninguna" in text
    assert "**Siguiente:** sin issues abiertas" in text


def test_replace_block_requires_markers() -> None:
    # Act / Assert
    with pytest.raises(ValueError, match="marcadores"):
        replace_block("documento sin marcadores", "bloque")


def test_main_without_write_prints_report(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Arrange
    monkeypatch.setattr(estado, "collect", lambda: _report())

    # Act
    code = main([])

    # Assert
    assert code == 0
    output = capsys.readouterr().out
    assert "**Pull requests abiertas (0):**" in output
    assert "**Issues abiertas: 0 · 0 SP**" in output
