"""Pruebas del informe reproducible de evaluación (HU-008)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar

import numpy as np

from ppe_detection.contracts import CLASSES
from ppe_detection.evaluation.evaluate import (
    EvaluationConfig,
    build_summary,
    render_markdown,
    sha256_file,
)


class _Box:
    ap_class_index: ClassVar[list[int]] = list(range(6))
    p: ClassVar[list[float]] = [0.5, 0.6, 0.7, 0.8, 0.9, 0.4]
    r: ClassVar[list[float]] = [0.4, 0.5, 0.6, 0.7, 0.8, 0.3]
    ap50: ClassVar[list[float]] = [0.55, 0.65, 0.75, 0.85, 0.95, 0.45]
    ap: ClassVar[list[float]] = [0.35, 0.45, 0.55, 0.65, 0.75, 0.25]


class _Confusion:
    matrix: ClassVar[Any] = np.array([[1.0, 0.0], [0.0, 2.0]])


class _Metrics:
    results_dict: ClassVar[dict[str, float]] = {
        "metrics/precision(B)": 0.8,
        "metrics/recall(B)": 0.7,
        "metrics/mAP50(B)": 0.75,
        "metrics/mAP50-95(B)": 0.5,
    }
    box = _Box()
    nt_per_class: ClassVar[list[int]] = [1, 1, 1, 1, 1, 1]
    confusion_matrix = _Confusion()
    speed: ClassVar[dict[str, float]] = {"inference": 1.5, "preprocess": 0.5}


def _config(tmp_path: Path) -> EvaluationConfig:
    model = tmp_path / "best.pt"
    data = tmp_path / "data.yaml"
    model.write_bytes(b"fake-weights")
    data.write_text("path: .\ntest: test/images\n", encoding="utf-8")
    return EvaluationConfig(model=model, data=data, split="test", output=tmp_path / "eval")


def _summary(tmp_path: Path) -> dict[str, Any]:
    return build_summary(_config(tmp_path), _Metrics(), CLASSES, "ABC123", images=9)


def test_summary_records_model_path_and_sha(tmp_path: Path) -> None:
    """AC-008.1: el informe identifica el artefacto y su SHA256."""
    summary = _summary(tmp_path)
    assert summary["model"]["path"].endswith("best.pt")
    assert summary["model"]["sha256"] == "ABC123"


def test_summary_records_dataset_split_and_yaml_hash(tmp_path: Path) -> None:
    """AC-008.1: la partición y el hash del YAML quedan registrados."""
    summary = _summary(tmp_path)
    assert summary["dataset"]["split"] == "test"
    assert summary["dataset"]["yaml_sha256"] == sha256_file(_config(tmp_path).data)


def test_summary_records_reproducible_config(tmp_path: Path) -> None:
    """AC-008.1: imgsz, conf, iou, seed y device son parte del resumen."""
    summary = _summary(tmp_path)
    assert summary["config"] == {
        "imgsz": 640,
        "conf": 0.001,
        "iou": 0.7,
        "seed": 42,
        "device": "cpu",
    }


def test_summary_counts_images_and_instances(tmp_path: Path) -> None:
    """AC-008.1: el informe informa imágenes y objetos evaluados."""
    summary = _summary(tmp_path)
    assert summary["images"] == 9
    assert summary["instances"] == 6


def test_summary_includes_all_six_classes(tmp_path: Path) -> None:
    """AC-008.2: el desglose por clase cubre las seis categorías."""
    summary = _summary(tmp_path)
    assert set(summary["per_class"]) == set(CLASSES)


def test_summary_includes_global_metrics(tmp_path: Path) -> None:
    """AC-008.2: las métricas globales se conservan."""
    summary = _summary(tmp_path)
    assert summary["metrics"]["metrics/mAP50(B)"] == 0.75
    assert summary["metrics"]["metrics/mAP50-95(B)"] == 0.5


def test_summary_serializes_confusion_matrix(tmp_path: Path) -> None:
    """AC-008.1: la matriz de confusión es JSON serializable."""
    summary = _summary(tmp_path)
    assert summary["confusion_matrix"] == [[1.0, 0.0], [0.0, 2.0]]


def test_summary_includes_speed(tmp_path: Path) -> None:
    """AC-008.1: los tiempos por etapa quedan en el manifiesto."""
    summary = _summary(tmp_path)
    assert summary["speed_ms_per_image"]["inference"] == 1.5


def test_markdown_contains_all_classes_and_global_metrics(tmp_path: Path) -> None:
    """AC-008.2: el Markdown presenta la tabla global y las seis clases."""
    markdown = render_markdown(_summary(tmp_path))
    assert "| **all** |" in markdown
    for class_name in CLASSES:
        assert class_name in markdown


def test_summary_is_json_serializable(tmp_path: Path) -> None:
    """AC-008.1: el informe se puede escribir como JSON sin tipos numpy."""
    payload = json.dumps(_summary(tmp_path), ensure_ascii=False)
    assert '"model"' in payload
    assert '"confusion_matrix"' in payload
