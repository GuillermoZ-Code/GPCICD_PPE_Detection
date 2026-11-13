"""Pruebas ampliadas de MLflow, tracking y CLI (HU-009).

Cubre AC-009.1/2/3 y FR-002/003/007: payload, referencia del artefacto,
comparación de runs, tracker MLflow y CLI.
"""

from __future__ import annotations

import json
import sys
import types
from dataclasses import dataclass, field
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from ppe_detection.tracking import (
    RunPayload,
    RunView,
    TrackingError,
    build_run_payload,
    compare_runs,
    default_run_name,
    parse_args,
    render_comparison,
)
from ppe_detection.tracking import mlflow_tracker as module

MODEL_SHA = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"
YAML_SHA = "B5EAEEE1DE7DC547E1513E0D3D0F3D902767BD211705A0DC9FE8EF8C99C262C4"


def _summary(*, split: str = "test") -> dict[str, Any]:
    return {
        "generated_at": "2026-11-12T00:00:00+00:00",
        "model": {"path": "artifacts/models/best.pt", "sha256": MODEL_SHA},
        "dataset": {
            "path": "artifacts/datasets/data.yaml",
            "split": split,
            "yaml_sha256": YAML_SHA,
        },
        "config": {"imgsz": 640, "conf": 0.001, "iou": 0.7, "seed": 42, "device": "cpu"},
        "images": 10,
        "instances": 20,
        "metrics": {
            "metrics/precision(B)": 0.5,
            "metrics/recall(B)": 0.6,
            "metrics/mAP50(B)": 0.7,
            "metrics/mAP50-95(B)": 0.4,
        },
        "per_class": {
            "helmet": {"p": 0.5, "r": 0.6, "ap50": 0.7, "ap": 0.4},
        },
    }


@dataclass
class FakeTracker:
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


def _view(run_id: str, name: str, **overrides: Any) -> RunView:
    values: dict[str, Any] = {
        "run_id": run_id,
        "run_name": name,
        "params": {"dataset_split": "test"},
        "metrics": {"map50": 0.5},
        "tags": {"model_reference": f"sha256:{MODEL_SHA}"},
    }
    values.update(overrides)
    return RunView(**values)


class _RunContext:
    def __enter__(self) -> Any:
        return SimpleNamespace(info=SimpleNamespace(run_id="run-1"))

    def __exit__(self, *args: object) -> bool:
        return False


class _FakeClient:
    def __init__(self, tracking_uri: str | None = None) -> None:
        self.tracking_uri = tracking_uri

    def get_run(self, run_id: str) -> Any:
        if run_id == "missing":
            raise RuntimeError("run inexistente")
        return SimpleNamespace(
            info=SimpleNamespace(run_id=run_id, run_name="demo"),
            data=SimpleNamespace(
                params={"a": "1"},
                metrics={"m": 0.5},
                tags={"t": "v"},
            ),
        )


def _fake_mlflow(monkeypatch: pytest.MonkeyPatch) -> Any:
    mlflow: Any = types.ModuleType("mlflow")
    mlflow.tracking_uri = None
    mlflow.experiment = None
    mlflow.run_name = None
    mlflow.logged = {"params": {}, "metrics": {}, "tags": {}, "artifacts": []}
    mlflow.set_tracking_uri = lambda uri: setattr(mlflow, "tracking_uri", uri)
    mlflow.set_experiment = lambda name: setattr(mlflow, "experiment", name)
    mlflow.start_run = lambda run_name: _record_run(mlflow, run_name)
    mlflow.log_params = lambda params: mlflow.logged["params"].update(params)
    mlflow.log_metrics = lambda metrics: mlflow.logged["metrics"].update(metrics)
    mlflow.set_tags = lambda tags: mlflow.logged["tags"].update(tags)
    mlflow.log_artifact = lambda path: mlflow.logged["artifacts"].append(path)
    tracking: Any = types.ModuleType("mlflow.tracking")
    tracking.MlflowClient = _FakeClient
    monkeypatch.setitem(sys.modules, "mlflow", mlflow)
    monkeypatch.setitem(sys.modules, "mlflow.tracking", tracking)
    return mlflow


def _record_run(mlflow: Any, run_name: str) -> _RunContext:
    mlflow.run_name = run_name
    return _RunContext()


def test_build_run_payload_deduplicates_artifacts(tmp_path: Path) -> None:
    # Arrange
    artifact = tmp_path / "summary.json"

    # Act
    payload = build_run_payload(_summary(), artifacts=[artifact, artifact])

    # Assert
    assert payload.artifacts == (artifact,)


def test_build_run_payload_rejects_pth_artifacts() -> None:
    with pytest.raises(TrackingError, match="pesos"):
        build_run_payload(_summary(), artifacts=[Path("model.pth")])


def test_build_run_payload_rejects_onnx_artifacts() -> None:
    with pytest.raises(TrackingError, match="pesos"):
        build_run_payload(_summary(), artifacts=[Path("model.onnx")])


def test_build_run_payload_rejects_zip_artifacts() -> None:
    with pytest.raises(TrackingError, match="datasets"):
        build_run_payload(_summary(), artifacts=[Path("dataset.zip")])


def test_build_run_payload_requires_metrics_section() -> None:
    # Arrange
    summary = _summary()
    del summary["metrics"]

    # Act / Assert
    with pytest.raises(TrackingError, match="metrics"):
        build_run_payload(summary)


def test_build_run_payload_requires_per_class() -> None:
    # Arrange
    summary = _summary()
    summary["per_class"] = {}

    # Act / Assert
    with pytest.raises(TrackingError, match="per_class"):
        build_run_payload(summary)


def test_build_run_payload_rejects_non_finite_metric() -> None:
    # Arrange
    summary = _summary()
    summary["metrics"]["metrics/mAP50(B)"] = float("nan")

    # Act / Assert
    with pytest.raises(TrackingError, match="finito"):
        build_run_payload(summary)


def test_build_run_payload_rejects_invalid_dataset_sha() -> None:
    with pytest.raises(TrackingError, match="dataset_sha256"):
        build_run_payload(_summary(), dataset_sha256="no-es-un-sha")


def test_build_run_payload_omits_missing_yaml_sha() -> None:
    # Arrange
    summary = _summary()
    summary["dataset"].pop("yaml_sha256")

    # Act
    payload = build_run_payload(summary)

    # Assert
    assert "dataset_yaml_sha256" not in payload.params
    assert "dataset_yaml_sha256" not in payload.tags


def test_default_run_name_uses_lowercase_sha_prefix() -> None:
    # Act
    name = default_run_name(_summary())

    # Assert
    assert name == f"eval-test-{MODEL_SHA[:12].lower()}"


def test_compare_runs_rejects_empty_id() -> None:
    with pytest.raises(TrackingError, match="vacíos"):
        compare_runs(["", "run-1"], FakeTracker())


def test_render_comparison_rejects_no_runs() -> None:
    with pytest.raises(TrackingError, match="No hay runs"):
        render_comparison([])


def test_render_comparison_escapes_pipes_and_newlines() -> None:
    # Arrange
    view = _view("run-1", "demo", params={"note": "a|b\nc"}, metrics={}, tags={})

    # Act
    text = render_comparison((view,))

    # Assert
    assert "a\\|b c" in text


def test_render_comparison_uses_dash_for_missing_values() -> None:
    # Arrange
    first = _view("run-1", "uno", params={"a": "1"}, metrics={}, tags={})
    second = _view("run-2", "dos", params={"b": "2"}, metrics={}, tags={})

    # Act
    text = render_comparison((first, second))

    # Assert
    assert "| **a** | 1 | — |" in text
    assert "| **b** | — | 2 |" in text


def test_render_comparison_formats_metrics_with_four_decimals() -> None:
    # Arrange
    view = _view("run-1", "demo", params={}, metrics={"map50": 0.5}, tags={})

    # Act
    text = render_comparison((view,))

    # Assert
    assert "0.5000" in text


def test_render_comparison_uses_run_name_and_short_id() -> None:
    # Arrange
    view = _view("run-123456789", "demo", params={}, metrics={}, tags={})

    # Act
    text = render_comparison((view,))

    # Assert
    assert "demo (run-1234)" in text


def test_mlflow_tracker_logs_params_metrics_tags_and_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange
    mlflow = _fake_mlflow(monkeypatch)
    artifact = tmp_path / "summary.json"
    tracker = module.MlflowTracker("sqlite:///test.db", "ppe-test")
    payload = RunPayload(
        params={"a": "1"},
        metrics={"m": 0.5},
        tags={"t": "v"},
        artifacts=(artifact,),
    )

    # Act
    run_id = tracker.log_run("demo", payload)

    # Assert
    assert run_id == "run-1"
    assert mlflow.run_name == "demo"
    assert mlflow.logged["params"] == {"a": "1"}
    assert mlflow.logged["metrics"] == {"m": 0.5}
    assert mlflow.logged["tags"] == {"t": "v"}
    assert mlflow.logged["artifacts"] == [str(artifact)]


def test_mlflow_tracker_get_run_maps_mlflow_data(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    _fake_mlflow(monkeypatch)
    tracker = module.MlflowTracker("sqlite:///test.db")

    # Act
    run = tracker.get_run("run-9")

    # Assert
    assert run.run_id == "run-9"
    assert run.run_name == "demo"
    assert run.params == {"a": "1"}
    assert run.metrics == {"m": 0.5}
    assert run.tags == {"t": "v"}


def test_mlflow_tracker_get_run_wraps_error(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    _fake_mlflow(monkeypatch)
    tracker = module.MlflowTracker("sqlite:///test.db")

    # Act / Assert
    with pytest.raises(TrackingError, match="missing"):
        tracker.get_run("missing")


def test_mlflow_tracker_requires_mlflow(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setitem(sys.modules, "mlflow", None)

    # Act / Assert
    with pytest.raises(TrackingError, match="Falta mlflow"):
        module.MlflowTracker()


def test_mlflow_tracker_sets_tracking_uri_and_experiment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    mlflow = _fake_mlflow(monkeypatch)

    # Act
    module.MlflowTracker("sqlite:///test.db", "ppe-test")

    # Assert
    assert mlflow.tracking_uri == "sqlite:///test.db"
    assert mlflow.experiment == "ppe-test"


def test_parse_args_supports_log_and_compare() -> None:
    # Arrange / Act
    log_args = parse_args(["log", "--summary", "s.json", "--artifact", "a.png"])
    compare_args = parse_args(["compare", "--run-id", "a", "--run-id", "b"])

    # Assert
    assert log_args.command == "log"
    assert log_args.summary == Path("s.json")
    assert log_args.artifact == [Path("a.png")]
    assert compare_args.command == "compare"
    assert compare_args.run_id == ["a", "b"]


def test_main_log_prints_run_id(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Arrange
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(json.dumps(_summary()), encoding="utf-8")
    tracker = FakeTracker()
    monkeypatch.setattr(module, "MlflowTracker", lambda *args, **kwargs: tracker)

    # Act
    code = module.main(["log", "--summary", str(summary_path), "--run-name", "demo"])

    # Assert
    assert code == 0
    assert "run_id=run-1" in capsys.readouterr().out


def test_main_compare_prints_comparison(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Arrange
    tracker = FakeTracker()
    tracker.runs["run-1"] = _view("run-1", "uno")
    tracker.runs["run-2"] = _view("run-2", "dos")
    monkeypatch.setattr(module, "MlflowTracker", lambda *args, **kwargs: tracker)

    # Act
    code = module.main(["compare", "--run-id", "run-1", "--run-id", "run-2"])

    # Assert
    assert code == 0
    assert "Comparación de runs" in capsys.readouterr().out


def test_main_returns_error_on_tracking_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Arrange
    def fail(*args: object, **kwargs: object) -> None:
        raise TrackingError("sin mlflow")

    monkeypatch.setattr(module, "MlflowTracker", fail)

    # Act
    code = module.main(["compare", "--run-id", "a", "--run-id", "b"])

    # Assert
    assert code == 1
    assert "error: sin mlflow" in capsys.readouterr().out
