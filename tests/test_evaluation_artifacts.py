"""Pruebas de artefactos gráficos de evaluación (HU-031)."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, ClassVar

import numpy as np
import pytest

from ppe_detection.contracts import CLASSES
from ppe_detection.evaluation import (
    EvaluationConfig,
    artifact_slug,
    collect_evaluation_artifacts,
    stable_artifact_name,
)
from ppe_detection.evaluation.evaluate import evaluate

SHA = "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9"


class _Box:
    ap_class_index: ClassVar[list[int]] = [0]
    p: ClassVar[list[float]] = [0.8]
    r: ClassVar[list[float]] = [0.7]
    ap50: ClassVar[list[float]] = [0.75]
    ap: ClassVar[list[float]] = [0.5]


class _Confusion:
    matrix: ClassVar[Any] = np.array([[1.0, 0.0], [0.0, 1.0]])


class _FakeMetrics:
    results_dict: ClassVar[dict[str, float]] = {
        "metrics/precision(B)": 0.8,
        "metrics/recall(B)": 0.7,
        "metrics/mAP50(B)": 0.75,
        "metrics/mAP50-95(B)": 0.5,
    }
    box = _Box()
    nt_per_class: ClassVar[list[int]] = [1]
    confusion_matrix = _Confusion()
    speed: ClassVar[dict[str, float]] = {"inference": 1.0}

    def __init__(self, save_dir: Path) -> None:
        self.save_dir = save_dir


class _FakeYolo:
    names: ClassVar[dict[int, str]] = dict(enumerate(CLASSES))

    def __init__(self, save_dir: Path) -> None:
        self.save_dir = save_dir
        self.plot_calls: list[bool] = []

    def val(self, **kwargs: object) -> _FakeMetrics:
        self.plot_calls.append(bool(kwargs.get("plots")))
        return _FakeMetrics(self.save_dir)


def _config(tmp_path: Path) -> EvaluationConfig:
    model = tmp_path / "best.pt"
    data = tmp_path / "data.yaml"
    model.write_bytes(b"fake-weights")
    data.write_text("path: .\n", encoding="utf-8")
    return EvaluationConfig(model=model, data=data, output=tmp_path / "eval", name="unit")


def _source(tmp_path: Path) -> Path:
    source = tmp_path / "source"
    source.mkdir()
    (source / "confusion_matrix.png").write_bytes(b"confusion")
    (source / "BoxPR_curve.png").write_bytes(b"pr")
    (source / "BoxF1_curve.png").write_bytes(b"f1")
    (source / "notes.txt").write_text("no es una figura", encoding="utf-8")
    return source


def test_artifact_slug_is_stable_and_safe() -> None:
    """AC-02: la versión y el SHA generan un identificador estable y seguro."""

    # Act
    slug = artifact_slug("YOLO26n clean", SHA)
    name = stable_artifact_name("confusion_matrix.png", "YOLO26n clean", SHA)

    # Assert
    assert slug == "yolo26n-clean-fefb1f1a120f"
    assert name == "confusion_matrix_yolo26n-clean-fefb1f1a120f.png"
    assert artifact_slug("YOLO26n clean", SHA) == slug


def test_collect_copies_confusion_and_pr_curves(tmp_path: Path) -> None:
    """AC-01: las figuras se copian por código y conservan su contenido."""

    # Arrange
    source = _source(tmp_path)
    destination = tmp_path / "artifacts"

    # Act
    copied = collect_evaluation_artifacts(
        source,
        destination,
        model_version="yolo26n-clean",
        model_sha256=SHA,
    )

    # Assert
    names = {path.name for path in copied}
    assert names == {
        "confusion_matrix_yolo26n-clean-fefb1f1a120f.png",
        "pr_curve_yolo26n-clean-fefb1f1a120f.png",
        "f1_curve_yolo26n-clean-fefb1f1a120f.png",
    }
    assert (destination / "pr_curve_yolo26n-clean-fefb1f1a120f.png").read_bytes() == b"pr"
    assert not (destination / "notes.txt").exists()


def test_collect_returns_empty_without_plots(tmp_path: Path) -> None:
    """AC-01: un run sin figuras no inventa archivos."""

    # Arrange
    source = tmp_path / "empty"
    source.mkdir()
    destination = tmp_path / "artifacts"

    # Act
    copied = collect_evaluation_artifacts(
        source,
        destination,
        model_version="yolo26n-clean",
        model_sha256=SHA,
    )

    # Assert
    assert copied == ()
    assert not destination.exists()


def test_collect_rejects_unknown_figure() -> None:
    """AC-02: una figura ajena al contrato no recibe un nombre estable."""

    # Act / Assert
    with pytest.raises(ValueError, match="desconocida"):
        stable_artifact_name("notes.txt", "yolo26n-clean", SHA)


def test_evaluate_adds_stable_artifacts_to_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-03: `evaluate` copia las figuras y las registra en el summary."""

    # Arrange
    config = _config(tmp_path)
    source = _source(tmp_path)
    module = importlib.import_module("ppe_detection.evaluation.evaluate")
    fake_yolo = _FakeYolo(source)
    monkeypatch.setattr(module, "_load_yolo", lambda: lambda _path: fake_yolo)

    # Act
    summary = evaluate(config)

    # Assert
    slug = artifact_slug("best", summary["model"]["sha256"])
    artifacts = {Path(path).name for path in summary["artifacts"]}
    assert artifacts == {
        f"confusion_matrix_{slug}.png",
        f"pr_curve_{slug}.png",
        f"f1_curve_{slug}.png",
    }
    assert fake_yolo.plot_calls == [True]
    assert (config.output / config.name / "summary.json").is_file()
    assert (config.output / config.name / "summary.md").is_file()
