"""Pruebas del informe comparativo de runs (HU-099, issue #155)."""

from __future__ import annotations

from pathlib import Path

from ppe_detection.tracking import RunView
from ppe_detection.tracking.mlflow_tracker import render_comparison_report

RUNS = (
    RunView(
        run_id="abc123",
        run_name="eval-test-yolo26n",
        params={"model_path": "artifacts/yolo26n/best.pt", "imgsz": "640"},
        metrics={"map50": 0.892, "map50_95": 0.614, "precision": 0.893, "recall": 0.842},
        tags={"model_reference": "sha256:FEFB1F1A"},
    ),
    RunView(
        run_id="def456",
        run_name="eval-test-yolo11s",
        params={"model_path": "artifacts/yolo11s/best.pt", "imgsz": "640"},
        metrics={"map50": 0.810, "map50_95": 0.516, "precision": 0.800, "recall": 0.767},
        tags={"model_reference": "sha256:E51EB080"},
    ),
)


def test_report_has_table() -> None:
    """AC-01: el informe incluye la tabla comparativa."""
    # Act
    report = render_comparison_report(RUNS, tracking_uri="file:./mlruns")

    # Assert
    assert "| Run | mAP50 | mAP50-95 | Precision | Recall | Artefacto | Enlace |" in report


def test_report_has_one_row_per_run() -> None:
    """AC-01: hay una fila por run."""
    # Act
    report = render_comparison_report(RUNS, tracking_uri="file:./mlruns")

    # Assert
    assert report.count("eval-test-yolo26n") >= 1
    assert report.count("eval-test-yolo11s") >= 1


def test_report_links_each_run() -> None:
    """AC-02: cada run enlaza a su vista en MLflow."""
    # Act
    report = render_comparison_report(RUNS, tracking_uri="file:./mlruns")

    # Assert
    assert "file:./mlruns/#/runs/abc123" in report
    assert "file:./mlruns/#/runs/def456" in report


def test_report_shows_artifact_reference() -> None:
    """AC-02: el artefacto y su SHA256 aparecen en la fila."""
    # Act
    report = render_comparison_report(RUNS, tracking_uri="file:./mlruns")

    # Assert
    assert "artifacts/yolo26n/best.pt" in report
    assert "sha256:FEFB1F1A" in report


def test_report_shows_metrics() -> None:
    """AC-01: las metricas del run se muestran formateadas."""
    # Act
    report = render_comparison_report(RUNS, tracking_uri="file:./mlruns")

    # Assert
    assert "0.892" in report
    assert "0.516" in report


def test_report_has_generation_date() -> None:
    """AC-01: el informe declara cuando se genero."""
    # Act
    report = render_comparison_report(
        RUNS, tracking_uri="file:./mlruns", generated_at="2026-11-24 00:00 UTC"
    )

    # Assert
    assert "2026-11-24 00:00 UTC" in report


def test_write_report_creates_file(tmp_path: Path) -> None:
    """AC-03: el informe se escribe en UTF-8."""
    # Arrange
    report = render_comparison_report(RUNS, tracking_uri="file:./mlruns")
    target = tmp_path / "docs" / "evaluation" / "mlflow-comparacion.md"

    # Act
    target.parent.mkdir(parents=True)
    target.write_text(report, encoding="utf-8")

    # Assert
    assert target.read_text(encoding="utf-8").startswith("# Comparación de runs")
