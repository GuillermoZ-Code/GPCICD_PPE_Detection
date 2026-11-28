"""Pruebas del entrenador (HU-017, sin GPU ni ultralytics)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ppe_detection.training.train import (
    _metrics_markdown,
    build_train_kwargs,
    load_data_config,
    main,
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


def _write_train_config(path: Path, *, model: str = "yolo26n.pt", extra: str = "") -> Path:
    config = path / "train.yaml"
    config.write_text(
        "data: /content/data_colab.yaml\n"
        "eval_data: /content/data_eval_colab.yaml\n"
        f"model: {model}\n"
        "epochs: 100\n"
        "imgsz: 640\n"
        "batch: -1\n"
        "device: '0'\n"
        "project: /content/runs/train\n"
        "name: yolo26n_clean\n"
        "seed: 42\n"
        "eval_split: test\n"
        "amp: true\n"
        "cache: false\n"
        f"{extra}",
        encoding="utf-8",
    )
    return config


def test_parse_args_loads_yaml_config(tmp_path: Path) -> None:
    """AC-01: --config carga el YAML versionado."""

    # Arrange
    config = _write_train_config(tmp_path)

    # Act
    parsed = parse_args(["--config", str(config)])

    # Assert
    assert parsed.model == "yolo26n.pt"
    assert parsed.data == Path("/content/data_colab.yaml")
    assert parsed.epochs == 100
    assert parsed.imgsz == 640
    assert parsed.seed == 42


def test_yaml_accepts_yolo26_models(tmp_path: Path) -> None:
    """AC-01: el YAML puede seleccionar yolo26n o yolo26s."""

    # Arrange
    config = _write_train_config(tmp_path, model="yolo26s.pt")

    # Act
    parsed = parse_args(["--config", str(config)])

    # Assert
    assert parsed.model == "yolo26s.pt"


def test_cli_overrides_yaml_config(tmp_path: Path) -> None:
    """FR-003: la CLI gana sobre el YAML."""

    # Arrange
    config = _write_train_config(tmp_path)

    # Act
    parsed = parse_args(["--config", str(config), "--epochs", "2", "--seed", "99"])

    # Assert
    assert parsed.epochs == 2
    assert parsed.seed == 99
    assert parsed.model == "yolo26n.pt"


def test_config_rejects_unknown_key(tmp_path: Path) -> None:
    """FR-004: una clave desconocida no se ignora."""

    # Arrange
    config = _write_train_config(tmp_path, extra="unknown_key: true\n")

    # Act / Assert
    with pytest.raises(ValueError, match="unknown_key"):
        parse_args(["--config", str(config)])


def test_config_requires_data_when_missing(tmp_path: Path) -> None:
    """Una configuración sin data exige --data."""

    # Arrange
    config = tmp_path / "train.yaml"
    config.write_text("model: yolo26n.pt\nepochs: 1\n", encoding="utf-8")

    # Act / Assert
    with pytest.raises(SystemExit):
        parse_args(["--config", str(config)])


def test_config_records_seed_imgsz_epochs_split(tmp_path: Path) -> None:
    """AC-02: la configuración resuelta conserva los campos reproducibles."""

    # Arrange
    config = _write_train_config(tmp_path)

    # Act
    parsed = parse_args(["--config", str(config)])

    # Assert
    assert (parsed.seed, parsed.imgsz, parsed.epochs, parsed.eval_split) == (
        42,
        640,
        100,
        "test",
    )


def test_dry_run_does_not_require_data_or_gpu(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """AC-03: --dry-run imprime la configuración sin validar archivos."""

    # Arrange
    config = _write_train_config(tmp_path)

    # Act
    code = main(["--config", str(config), "--dry-run"])

    # Assert
    assert code == 0
    output = capsys.readouterr().out
    assert '"dry_run": true' in output
    assert '"model": "yolo26n.pt"' in output


def test_versioned_configs_exist() -> None:
    """FR-007: las configuraciones de YOLO26n/s están versionadas."""

    # Arrange / Act
    n_config = parse_args(["--config", "configs/train/yolo26n.yaml"])
    s_config = parse_args(["--config", "configs/train/yolo26s.yaml"])

    # Assert
    assert n_config.model == "yolo26n.pt"
    assert s_config.model == "yolo26s.pt"


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
