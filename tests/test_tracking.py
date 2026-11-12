"""Pruebas del registro y comparación de experimentos (HU-009)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import pytest

from ppe_detection.tracking import (
    RunPayload,
    RunView,
    TrackingError,
    build_run_payload,
    compare_runs,
    log_evaluation_run,
    render_comparison,
)

MODEL_SHA = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"
YAML_SHA = "B5EAEEE1DE7DC547E1513E0D3D0F3D902767BD211705A0DC9FE8EF8C99C262C4"
DATASET_SHA = "3D1AE47B7F1401B02A05A997E413765D8F15529FB1944F2A5B1ADF536E909432"


def _summary(*, split: str = "test", map50: float = 0.810) -> dict[str, object]:
    """Resumen mínimo con el contrato que produce HU-008."""
    return {
        "generated_at": "2026-11-11T01:43:51+00:00",
        "model": {"path": "artifacts/models/best.pt", "sha256": MODEL_SHA},
        "dataset": {
            "path": "artifacts/datasets/data_local.yaml",
            "split": split,
            "yaml_sha256": YAML_SHA,
        },
        "config": {"imgsz": 640, "conf": 0.001, "iou": 0.7, "seed": 42, "device": "cpu"},
        "images": 1094,
        "instances": 1905,
        "metrics": {
            "metrics/precision(B)": 0.7998181632540331,
            "metrics/recall(B)": 0.7671586023912447,
            "metrics/mAP50(B)": map50,
            "metrics/mAP50-95(B)": 0.5161625983083129,
        },
        "per_class": {
            "Gloves": {
                "p": 0.5977778032660654,
                "r": 0.6367041198501873,
                "ap50": 0.6133083598036241,
                "ap": 0.4072271520881155,
            },
            "Vest": {
                "p": 0.8825185463763818,
                "r": 0.9048529466517239,
                "ap50": 0.9310186477149945,
                "ap": 0.7124291279096434,
            },
        },
    }


@dataclass
class FakeTracker:
    """Tracker en memoria para probar sin depender de MLflow."""

    runs: dict[str, RunView] = field(default_factory=dict)
    logged: list[tuple[str, RunPayload]] = field(default_factory=list)

    def log_run(self, run_name: str, payload: RunPayload) -> str:
        run_id = f"run-{len(self.logged) + 1}"
        self.logged.append((run_name, payload))
        self.runs[run_id] = RunView(
            run_id=run_id,
            run_name=run_name,
            params=dict(payload.params),
            metrics=dict(payload.metrics),
            tags=dict(payload.tags),
        )
        return run_id

    def get_run(self, run_id: str) -> RunView:
        return self.runs[run_id]


def test_build_run_payload_records_model_partition_and_config() -> None:
    # Arrange
    summary = _summary()

    # Act
    payload = build_run_payload(summary)

    # Assert
    assert payload.params["model_path"] == "artifacts/models/best.pt"
    assert payload.params["model_sha256"] == MODEL_SHA
    assert payload.params["dataset_split"] == "test"
    assert payload.params["imgsz"] == "640"
    assert payload.params["conf"] == "0.001"
    assert payload.params["images"] == "1094"
    assert payload.tags["model_reference"] == f"sha256:{MODEL_SHA}"


def test_build_run_payload_contains_global_and_per_class_metrics() -> None:
    # Arrange
    summary = _summary()

    # Act
    payload = build_run_payload(summary)

    # Assert
    assert payload.metrics["precision"] == pytest.approx(0.7998181632540331)
    assert payload.metrics["recall"] == pytest.approx(0.7671586023912447)
    assert payload.metrics["map50"] == pytest.approx(0.810)
    assert payload.metrics["map50_95"] == pytest.approx(0.5161625983083129)
    assert payload.metrics["Gloves_map50"] == pytest.approx(0.6133083598036241)
    assert payload.metrics["Vest_map50_95"] == pytest.approx(0.7124291279096434)


def test_build_run_payload_records_dataset_sha_when_provided() -> None:
    # Arrange
    summary = _summary()

    # Act
    payload = build_run_payload(summary, dataset_sha256=DATASET_SHA)

    # Assert
    assert payload.tags["dataset_sha256"] == DATASET_SHA
    assert payload.params["dataset_yaml_sha256"] == YAML_SHA


def test_log_evaluation_run_returns_run_id_and_passes_artifacts(tmp_path: Path) -> None:
    # Arrange
    summary_path = tmp_path / "summary.json"
    summary_path.write_text("{}", encoding="utf-8")
    report_path = tmp_path / "summary.md"
    report_path.write_text("# informe", encoding="utf-8")
    tracker = FakeTracker()

    # Act
    run_id = log_evaluation_run(
        _summary(),
        tracker=tracker,
        run_name="test-1094",
        artifacts=[summary_path, report_path],
    )

    # Assert
    assert run_id == "run-1"
    assert tracker.logged[0][0] == "test-1094"
    assert tracker.logged[0][1].artifacts == (summary_path, report_path)


def test_log_evaluation_run_uses_deterministic_default_name() -> None:
    # Arrange
    tracker = FakeTracker()

    # Act
    run_id = log_evaluation_run(_summary(), tracker=tracker)

    # Assert
    assert run_id == "run-1"
    assert tracker.logged[0][0].startswith("eval-test-")


def test_build_run_payload_rejects_weights() -> None:
    # Arrange
    weights = Path("artifacts/models/best.pt")

    # Act / Assert
    with pytest.raises(TrackingError, match="pesos"):
        build_run_payload(_summary(), artifacts=[weights])


def test_build_run_payload_requires_model_sha256() -> None:
    # Arrange
    summary = _summary()
    summary["model"] = {"path": "artifacts/models/best.pt"}

    # Act / Assert
    with pytest.raises(TrackingError, match="sha256"):
        build_run_payload(summary)


def test_log_evaluation_run_rejects_missing_artifact(tmp_path: Path) -> None:
    # Arrange
    missing = tmp_path / "missing.json"

    # Act / Assert
    with pytest.raises(TrackingError, match="no existe"):
        log_evaluation_run(_summary(), tracker=FakeTracker(), artifacts=[missing])


def test_compare_runs_distinguishes_two_runs() -> None:
    # Arrange
    tracker = FakeTracker()
    run_a = log_evaluation_run(
        _summary(split="test_original_sin_fuga", map50=0.726),
        tracker=tracker,
        run_name="eval492",
    )
    run_b = log_evaluation_run(
        _summary(split="test", map50=0.810),
        tracker=tracker,
        run_name="test1094",
    )

    # Act
    text = render_comparison(compare_runs([run_a, run_b], tracker))

    # Assert
    assert "eval492" in text
    assert "test1094" in text
    assert run_a in text
    assert run_b in text
    assert "0.7260" in text
    assert "0.8100" in text
    assert f"sha256:{MODEL_SHA}" in text
    assert text.count("**model_reference**") == 1


def test_compare_runs_requires_two_unique_ids() -> None:
    # Arrange
    tracker = FakeTracker()

    # Act / Assert
    with pytest.raises(TrackingError, match="dos runs"):
        compare_runs(["run-1"], tracker)
    with pytest.raises(TrackingError, match="distintos"):
        compare_runs(["run-1", "run-1"], tracker)


def test_render_comparison_includes_model_reference() -> None:
    # Arrange
    view = RunView(
        run_id="run-1",
        run_name="eval-test",
        params={"model_sha256": MODEL_SHA, "model_path": "artifacts/models/best.pt"},
        metrics={"map50": 0.810},
        tags={
            "model_reference": f"sha256:{MODEL_SHA}",
            "mlflow.runName": "internal",
        },
    )

    # Act
    text = render_comparison((view,))

    # Assert
    assert f"sha256:{MODEL_SHA}" in text
    assert "artifacts/models/best.pt" in text
    assert "mlflow.runName" not in text
