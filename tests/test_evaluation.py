"""Pruebas del evaluador reproducible (sin GPU, dataset ni ultralytics)."""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any, ClassVar

import numpy as np
import pytest

from ppe_detection.contracts import CLASSES
from ppe_detection.evaluation.evaluate import (
    EvaluationConfig,
    EvaluationError,
    _count_images,
    build_summary,
    evaluate,
    parse_args,
    render_markdown,
    sha256_file,
    validate_model_names,
)


class _FakeBox:
    ap_class_index: ClassVar[list[int]] = [0, 1]
    p: ClassVar[list[float]] = [0.5, 0.7]
    r: ClassVar[list[float]] = [0.6, 0.8]
    ap50: ClassVar[list[float]] = [0.65, 0.85]
    ap: ClassVar[list[float]] = [0.4, 0.6]


class _FakeConfusion:
    matrix: ClassVar[Any] = np.array([[1.0, 0.0], [0.0, 2.0]])


class _FakeMetrics:
    results_dict: ClassVar[dict[str, float]] = {
        "metrics/precision(B)": 0.8,
        "metrics/recall(B)": 0.7,
        "metrics/mAP50(B)": 0.75,
        "metrics/mAP50-95(B)": 0.5,
    }
    box = _FakeBox()
    nt_per_class: ClassVar[list[int]] = [2, 1, 0, 0, 0, 0]
    nt_per_image: ClassVar[list[int]] = [1, 1, 0]
    confusion_matrix = _FakeConfusion()
    speed: ClassVar[dict[str, float]] = {"inference": 1.2}


class _FakeYolo:
    names: ClassVar[dict[int, str]] = dict(enumerate(CLASSES))

    def __init__(self, model_path: str) -> None:
        self.model_path = model_path

    def val(self, **kwargs: object) -> _FakeMetrics:
        assert kwargs["data"]
        return _FakeMetrics()


def _config(tmp_path: Path) -> EvaluationConfig:
    model = tmp_path / "best.pt"
    data = tmp_path / "data.yaml"
    model.write_bytes(b"fake-weights")
    data.write_text("path: .\n", encoding="utf-8")
    return EvaluationConfig(
        model=model,
        data=data,
        output=tmp_path / "eval",
        name="unit",
        plots=False,
    )


def test_default_config_is_deterministic() -> None:
    config = parse_args(["--model", "best.pt", "--data", "data.yaml"])

    assert config.imgsz == 640
    assert config.conf == 0.001
    assert config.iou == 0.7
    assert config.seed == 42
    assert config.device == "cpu"


def test_sha256_file_returns_hex_digest(tmp_path: Path) -> None:
    path = tmp_path / "artifact.bin"
    path.write_bytes(b"contenido")

    digest = sha256_file(path)

    assert len(digest) == 64
    assert digest == digest.upper()


def test_count_images_uses_declared_split(tmp_path: Path) -> None:
    images = tmp_path / "test" / "images"
    images.mkdir(parents=True)
    (images / "a.jpg").write_bytes(b"a")
    (images / "b.png").write_bytes(b"b")
    (images / "not-an-image.txt").write_text("x", encoding="utf-8")
    data = tmp_path / "data.yaml"
    data.write_text("path: .\ntest: test/images\n", encoding="utf-8")

    assert _count_images(data, "test") == 2


def test_validate_model_names_accepts_canonical_catalog() -> None:
    result = validate_model_names(dict(enumerate(CLASSES)))

    assert result[0] == "Gloves"
    assert result[5] == "safety_shoe"


def test_validate_model_names_rejects_wrong_catalog() -> None:
    with pytest.raises(EvaluationError, match="catálogo"):
        validate_model_names(["person", "vest"])


def test_build_summary_contains_global_and_per_class_metrics(tmp_path: Path) -> None:
    config = _config(tmp_path)

    summary = build_summary(config, _FakeMetrics(), CLASSES, "ABC123", images=3)

    assert summary["metrics"]["metrics/mAP50(B)"] == 0.75
    assert summary["per_class"]["Gloves"]["ap50"] == 0.65
    assert summary["per_class"]["Vest"]["r"] == 0.8
    assert summary["instances"] == 3
    assert summary["images"] == 3
    assert summary["model"]["sha256"] == "ABC123"


def test_render_markdown_includes_global_and_classes(tmp_path: Path) -> None:
    summary = build_summary(_config(tmp_path), _FakeMetrics(), CLASSES, "ABC123", images=3)

    markdown = render_markdown(summary)

    assert "| **all** |" in markdown
    assert "Gloves" in markdown
    assert "Vest" in markdown
    assert "SHA256" in markdown


def test_evaluate_writes_summary_and_does_not_train(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = _config(tmp_path)
    module = importlib.import_module("ppe_detection.evaluation.evaluate")
    monkeypatch.setattr(module, "_load_yolo", lambda: _FakeYolo)

    summary = evaluate(config)

    assert (config.output / config.name / "summary.json").is_file()
    assert (config.output / config.name / "summary.md").is_file()
    assert summary["metrics"]["metrics/mAP50-95(B)"] == 0.5


def test_evaluate_rejects_missing_model(tmp_path: Path) -> None:
    config = _config(tmp_path)
    config = EvaluationConfig(model=tmp_path / "missing.pt", data=config.data)

    with pytest.raises(FileNotFoundError, match="modelo"):
        evaluate(config)
