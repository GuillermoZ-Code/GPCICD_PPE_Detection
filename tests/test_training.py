"""Pruebas del entrenador (sin GPU ni ultralytics)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ppe_detection.training.train import (
    _metrics_markdown,
    build_train_kwargs,
    load_data_config,
    parse_args,
    verify_class_order,
)


def _write_data_yaml(path: Path, names: str = "[Helmet, Vest]") -> Path:
    data = path / "data.yaml"
    data.write_text(
        f"train: train/images\nval: valid/images\ntest: test/images\nnc: 2\nnames: {names}\n",
        encoding="utf-8",
    )
    return data


def test_parse_args_exige_data() -> None:
    # Arrange / Act / Assert
    with pytest.raises(SystemExit):
        parse_args([])


def test_parse_args_deriva_eval_si_existe(tmp_path: Path) -> None:
    # Arrange
    data = _write_data_yaml(tmp_path)
    eval_data = tmp_path / "data_eval_preentrenados.yaml"
    eval_data.write_text(
        "train: eval/images\nval: eval/images\ntest: eval/images\n", encoding="utf-8"
    )

    # Act
    config = parse_args(["--data", str(data), "--epochs", "1"])

    # Assert
    assert config.eval_data == eval_data
    assert config.epochs == 1


def test_load_data_config_normaliza_names(tmp_path: Path) -> None:
    # Arrange
    data = _write_data_yaml(tmp_path, "{1: Vest, 0: Helmet}")

    # Act
    config = load_data_config(data)

    # Assert
    assert config["names"] == ["Helmet", "Vest"]
    assert config["nc"] == 2


def test_verify_class_order_acepta_variantes_de_nombre() -> None:
    # Arrange / Act / Assert
    verify_class_order(["Gloves", "Safety Shoe"], {0: "gloves", 1: "safety_shoe"})


def test_verify_class_order_falla_si_cambia_el_orden() -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="orden"):
        verify_class_order(["Gloves", "Vest"], {0: "Vest", 1: "Gloves"})


def test_build_train_kwargs_es_reproducible(tmp_path: Path) -> None:
    # Arrange
    data = _write_data_yaml(tmp_path)
    config = parse_args(["--data", str(data), "--project", str(tmp_path / "runs"), "--epochs", "3"])

    # Act
    kwargs = build_train_kwargs(config)

    # Assert
    assert kwargs["seed"] == 42
    assert kwargs["deterministic"] is True
    assert kwargs["epochs"] == 3
    assert Path(kwargs["project"]).is_absolute()


def test_metrics_markdown_incluye_clases() -> None:
    # Arrange
    summary: dict[str, Any] = {
        "data": "data.yaml",
        "split": "test",
        "imgsz": 640,
        "conf": 0.001,
        "iou": 0.7,
        "seed": 42,
        "results_dict": {
            "metrics/precision(B)": 0.5,
            "metrics/recall(B)": 0.6,
            "metrics/mAP50(B)": 0.7,
            "metrics/mAP50-95(B)": 0.4,
        },
        "per_class": {"Gloves": {"p": 0.5, "r": 0.6, "ap50": 0.7, "ap": 0.4}},
    }

    # Act
    markdown = _metrics_markdown(summary)

    # Assert
    assert "Gloves" in markdown
    assert "mAP50" in markdown
