"""Pruebas de inferencia por lotes con JSON por imagen (HU-039)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pytest

from ppe_detection.contracts import Detection, ImageData
from ppe_detection.detection import predict


def _write_image(path: Path) -> Path:
    array = np.zeros((6, 8, 3), dtype=np.uint8)
    ok, buffer = cv2.imencode(path.suffix, cv2.cvtColor(array, cv2.COLOR_RGB2BGR))
    assert ok
    path.write_bytes(buffer.tobytes())
    return path


def _detection() -> Detection:
    return Detection(
        class_id=0,
        class_name="Gloves",
        confidence=0.9,
        bbox=(1.0, 2.0, 3.0, 4.0),
        image_width=8,
        image_height=6,
    )


class FakeDetector:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def detect(self, image: ImageData, **_kwargs: Any) -> list[Detection]:
        return [_detection()]


class EmptyDetector:
    def __init__(self, *_args: Any, **_kwargs: Any) -> None:
        pass

    def detect(self, image: ImageData, **_kwargs: Any) -> list[Detection]:
        return []


def test_parse_args_accepts_dir_alias() -> None:
    """AC-01: `--dir` es alias de entrada por carpeta."""

    # Act
    args = predict.parse_args(["--model", "best.pt", "--dir", "imagenes"])

    # Assert
    assert args.source == Path("imagenes")


def test_image_json_records_identity_and_parameters() -> None:
    """AC-02: el JSON incluye versión, imgsz y umbrales."""

    # Arrange
    args = predict.parse_args(
        [
            "--model",
            "best.pt",
            "--dir",
            "imagenes",
            "--conf",
            "0.4",
            "--iou",
            "0.5",
            "--imgsz",
            "320",
            "--seed",
            "7",
        ]
    )
    image = ImageData(
        array=np.zeros((6, 8, 3), dtype=np.uint8),
        width=8,
        height=6,
        format="png",
        source="a.png",
    )

    # Act
    payload = predict.image_json_payload(Path("a.png"), image, [_detection()], args, "ABC123")

    # Assert
    assert payload["model"] == {"path": "best.pt", "version": "best", "sha256": "ABC123"}
    assert payload["parameters"] == {
        "conf": 0.4,
        "iou": 0.5,
        "imgsz": 320,
        "device": "cpu",
        "seed": 7,
    }
    assert payload["detections"][0]["class_name"] == "Gloves"


def test_run_writes_one_json_per_image(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-01: la carpeta produce un JSON por imagen."""

    # Arrange
    first = _write_image(tmp_path / "a.png")
    _write_image(tmp_path / "b.jpg")
    model = tmp_path / "best.pt"
    model.write_bytes(b"pesos")
    output = tmp_path / "out"
    monkeypatch.setattr(predict, "YoloDetector", FakeDetector)
    args = predict.parse_args(
        ["--model", str(model), "--dir", str(tmp_path), "--output", str(output)]
    )

    # Act
    predict.run(args)

    # Assert
    first_payload = json.loads((output / "json" / "a.png.json").read_text(encoding="utf-8"))
    second_payload = json.loads((output / "json" / "b.jpg.json").read_text(encoding="utf-8"))
    assert first_payload["image"] == str(first)
    assert first_payload["model"]["version"] == "best"
    assert first_payload["parameters"]["imgsz"] == predict.DEFAULT_IMGSZ
    assert second_payload["detections"][0]["bbox"] == [1.0, 2.0, 3.0, 4.0]


def test_run_json_handles_empty_detections(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-03: un detector simulado vacío produce un JSON válido."""

    # Arrange
    image = _write_image(tmp_path / "a.png")
    model = tmp_path / "best.pt"
    model.write_bytes(b"pesos")
    output = tmp_path / "out"
    monkeypatch.setattr(predict, "YoloDetector", EmptyDetector)
    args = predict.parse_args(
        ["--model", str(model), "--dir", str(tmp_path), "--output", str(output)]
    )

    # Act
    predict.run(args)

    # Assert
    payload = json.loads((output / "json" / "a.png.json").read_text(encoding="utf-8"))
    assert payload["image"] == str(image)
    assert payload["detections"] == []
    assert payload["message"] == predict.NO_DETECTIONS_MESSAGE
