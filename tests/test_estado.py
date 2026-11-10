"""Pruebas del comando de estado (sin git ni gh reales)."""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

from ppe_detection.tools import estado
from ppe_detection.tools.estado import (
    GENERATED_END,
    GENERATED_START,
    Issue,
    PullRequest,
    Report,
    parse_backlog_sp,
    render,
    replace_block,
    run,
)


def _report() -> Report:
    return Report(
        generated_at=datetime(2026, 11, 9, 12, 0, tzinfo=UTC),
        branch="feature/003-hu-002-deteccion",
        dirty=0,
        ahead=4,
        behind=0,
        develop="54094b6 (2026-11-04)",
        commits=("179187d docs(detection): documentar el manifiesto run.json",),
        prs=(
            PullRequest(
                number=28,
                title="feat(io): cargar y validar imagenes (HU-001)",
                base="develop",
                review="aprobada",
                checks="ok",
                issue=1,
            ),
        ),
        issues=(
            Issue(number=1, title="HU-001 — Cargar una imagen", milestone="M3-S1", sp=1),
            Issue(number=3, title="HU-003 — Visualizar detecciones", milestone="M3-S1", sp=1),
            Issue(number=8, title="HU-008 — Evaluar el modelo", milestone="M3-S2", sp=2),
        ),
        warnings=(),
    )


def _report_without_github() -> Report:
    return Report(
        generated_at=datetime(2026, 11, 9, 12, 0, tzinfo=UTC),
        branch="develop",
        dirty=0,
        ahead=0,
        behind=0,
        develop="f975019 (2026-11-09)",
        commits=(),
        prs=(),
        issues=(),
        warnings=("`gh` no disponible o sin sesión: PRs e issues sin actualizar",),
        github_ok=False,
    )


def test_parse_backlog_sp_reads_points_per_hu() -> None:
    # Arrange
    text = (
        "### HU-001 — Cargar una imagen\n"
        "- **SP:** 1 · **Labels:** `ep-01`.\n"
        "\n"
        "### HU-002 — Detectar EPP\n"
        "- **Depende de:** SPI-01.\n"
        "- **SP:** 3 · **Labels:** `ep-02`.\n"
    )

    # Act
    points = parse_backlog_sp(text)

    # Assert
    assert points == {"HU-001": 1, "HU-002": 3}


def test_parse_backlog_sp_ignores_sections_after_last_hu() -> None:
    # Arrange: la tabla de TA-EDA repite un `**SP:** 3 (propuesto)` después de HU-015.
    text = (
        "### HU-015 — Comprobar el sistema\n"
        "- **SP:** 1 · **Labels:** `ep-05`.\n"
        "\n"
        "## Pendiente de validación (Jesús)\n"
        "\n"
        "### TA-EDA — EDA del dataset (propuesta, no creada)\n"
        "- **SP:** 3 (propuesto).\n"
    )

    # Act
    points = parse_backlog_sp(text)

    # Assert
    assert points == {"HU-015": 1}


def test_parse_backlog_sp_matches_real_backlog() -> None:
    # Arrange
    text = (estado.REPO_ROOT / "docs/curso/backlog.md").read_text(encoding="utf-8")

    # Act
    points = parse_backlog_sp(text)

    # Assert
    assert len(points) == 15
    assert points["HU-015"] == 1
    assert sum(points.values()) == 22


def test_render_summarizes_prs_issues_and_next() -> None:
    # Arrange
    report = _report()

    # Act
    text = render(report)

    # Assert
    assert "Pull requests abiertas (1)" in text
    assert "#28" in text
    assert "revisión: aprobada" in text
    assert "Issues abiertas: 3 · 4 SP" in text
    assert "- M3-S1 (2 SP): #1 #3" in text
    assert "**En revisión:** #1 (PR #28)" in text
    assert "**Siguiente por orden:** #3 HU-003" in text


def test_render_reports_warnings() -> None:
    # Arrange
    report = _report_without_github()

    # Act
    text = render(report)

    # Assert
    assert "**Avisos:**" in text
    assert "`gh` no disponible" in text


def test_write_refuses_without_github(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    target = tmp_path / "ESTADO.md"
    target.write_text(f"{GENERATED_START}\ncontenido previo\n{GENERATED_END}\n", encoding="utf-8")
    monkeypatch.setattr(estado, "ESTADO_PATH", target)
    monkeypatch.setattr(estado, "collect", _report_without_github)

    # Act
    code = estado.main(["--write"])

    # Assert
    assert code == 1
    assert "contenido previo" in target.read_text(encoding="utf-8")


def test_write_updates_when_sources_are_available(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange
    target = tmp_path / "ESTADO.md"
    target.write_text(f"{GENERATED_START}\ncontenido previo\n{GENERATED_END}\n", encoding="utf-8")
    monkeypatch.setattr(estado, "ESTADO_PATH", target)
    monkeypatch.setattr(estado, "collect", _report)

    # Act
    code = estado.main(["--write"])

    # Assert
    assert code == 0
    content = target.read_text(encoding="utf-8")
    assert "contenido previo" not in content
    assert "Pull requests abiertas (1)" in content


def test_replace_block_keeps_the_session_log() -> None:
    # Arrange
    document = (
        "# Estado operativo\n\n"
        f"{GENERATED_START}\n"
        "contenido viejo\n"
        f"{GENERATED_END}\n\n"
        "## Bitácora de sesiones\n\n"
        "### 2026-11-09 · Guillermo\n"
        "- **Hecho:** revisión de #28.\n"
    )

    # Act
    result = replace_block(document, "contenido nuevo")

    # Assert
    assert "contenido nuevo" in result
    assert "contenido viejo" not in result
    assert "## Bitácora de sesiones" in result
    assert "revisión de #28" in result


def test_run_decodes_utf8_output() -> None:
    # Arrange
    code = "import sys; sys.stdout.buffer.write('\\u2014'.encode('utf-8'))"

    # Act
    output = run([sys.executable, "-c", code])

    # Assert
    assert output == "\u2014"
