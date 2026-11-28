"""Pruebas del postprocesamiento con umbrales por clase (HU-036)."""

from __future__ import annotations

from pathlib import Path

import pytest

from ppe_detection.contracts import CLASSES, Detection
from ppe_detection.postprocessing import (
    DEFAULT_CONFIG_PATH,
    ThresholdConfig,
    ThresholdConfigError,
    apply_thresholds,
    load_threshold_config,
)

CONFIG_VALUES = {
    "Gloves": 0.45,
    "Vest": 0.51,
    "goggles": 0.30,
    "helmet": 0.49,
    "mask": 0.40,
    "safety_shoe": 0.32,
}


def _detection(class_id: int, confidence: float) -> Detection:
    return Detection(
        class_id=class_id,
        class_name=CLASSES[class_id],
        confidence=confidence,
        bbox=(1.0, 1.0, 5.0, 5.0),
        image_width=10,
        image_height=10,
    )


def _config(**overrides: float) -> ThresholdConfig:
    values = dict(CONFIG_VALUES)
    values.update(overrides)
    return ThresholdConfig(values)


def _write_config(path: Path, values: dict[str, float]) -> None:
    lines = ["version: 1", "iou: 0.50", "thresholds:"]
    lines.extend(f"  {class_name}: {value}" for class_name, value in values.items())
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_loads_repository_thresholds() -> None:
    """AC-01: el YAML versionado se lee y conserva sus valores calibrados."""

    # Act
    config = load_threshold_config()

    # Assert
    assert config.source == DEFAULT_CONFIG_PATH
    assert config.thresholds["Gloves"] == 0.45
    assert config.thresholds["Vest"] == 0.51


def test_missing_default_config_uses_safe_defaults(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-01: sin archivo por defecto se usa 0,25 en las seis clases."""

    # Arrange
    module = __import__("ppe_detection.postprocessing.thresholds", fromlist=["x"])
    monkeypatch.setattr(module, "DEFAULT_CONFIG_PATH", tmp_path / "missing.yaml")

    # Act
    config = load_threshold_config()

    # Assert
    assert config.source is None
    assert config.thresholds == dict.fromkeys(CLASSES, 0.25)


def test_explicit_missing_config_fails(tmp_path: Path) -> None:
    """AC-03: una ruta explícita inexistente no se sustituye silenciosamente."""

    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="No existe"):
        load_threshold_config(tmp_path / "missing.yaml")


def test_invalid_threshold_fails(tmp_path: Path) -> None:
    """AC-03: un umbral fuera de [0,1] produce un error de arranque."""

    # Arrange
    path = tmp_path / "thresholds.yaml"
    _write_config(path, {**CONFIG_VALUES, "Gloves": 1.5})

    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="inválida"):
        load_threshold_config(path)


def test_missing_class_fails(tmp_path: Path) -> None:
    """AC-03: un YAML incompleto no se acepta."""

    # Arrange
    path = tmp_path / "thresholds.yaml"
    _write_config(path, {key: value for key, value in CONFIG_VALUES.items() if key != "mask"})

    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="inválida"):
        load_threshold_config(path)


def test_threshold_config_rejects_foreign_class() -> None:
    """AC-03: una clase ajena al catálogo EPP se rechaza."""

    # Act / Assert
    with pytest.raises(ThresholdConfigError, match="sobran"):
        ThresholdConfig({**CONFIG_VALUES, "person": 0.5})


def test_apply_filters_each_class_with_its_threshold() -> None:
    """AC-02: cada clase usa su propio umbral y conserva las que lo alcanzan."""

    # Arrange
    detections = [
        _detection(1, 0.50),  # Vest: cae
        _detection(1, 0.60),  # Vest: queda
        _detection(0, 0.44),  # Gloves: cae
        _detection(0, 0.45),  # Gloves: queda
        _detection(2, 0.30),  # goggles: queda
        _detection(5, 0.31),  # safety_shoe: cae
    ]

    # Act
    result = apply_thresholds(detections, _config())

    # Assert
    assert [item.class_name for item in result] == ["Vest", "Gloves", "goggles"]


def test_apply_preserves_order_and_does_not_mutate() -> None:
    """AC-02: el filtro no reordena ni modifica la lista de entrada."""

    # Arrange
    original = [_detection(3, 0.49), _detection(4, 0.40), _detection(0, 0.90)]
    snapshot = list(original)

    # Act
    result = apply_thresholds(original, _config())

    # Assert
    assert result == original
    assert original == snapshot


def test_apply_empty_list() -> None:
    """AC-02: una lista vacía devuelve una lista vacía."""

    # Act / Assert
    assert apply_thresholds([], _config()) == []


def test_default_apply_uses_repository_config() -> None:
    """AC-02: sin configuración explícita se usa el YAML del repositorio."""

    # Arrange
    below = _detection(0, 0.20)
    above = _detection(0, 0.90)

    # Act
    result = apply_thresholds([below, above])

    # Assert
    assert result == [above]
