"""Pruebas de la CLI de inferencia (sin ultralytics)."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pytest

from ppe_detection.contracts import Detection, ImageData
from ppe_detection.detection import predict


def _write_image(path: Path, color: tuple[int, int, int] = (10, 20, 30)) -> Path:
    array = np.full((6, 8, 3), color, dtype=np.uint8)
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

    def detect(self, image: ImageData) -> list[Detection]:
        return [_detection()]


def test_parse_args_requires_model_and_source() -> None:
    # Arrange / Act / Assert
    with pytest.raises(SystemExit):
        predict.parse_args([])


def test_parse_args_defaults() -> None:
    # Arrange / Act
    args = predict.parse_args(["--model", "best.pt", "--source", "imagenes"])

    # Assert
    assert args.conf == predict.DEFAULT_CONF
    assert args.iou == predict.DEFAULT_IOU
    assert args.imgsz == predict.DEFAULT_IMGSZ
    assert args.device == predict.DEFAULT_DEVICE
    assert args.output == predict.DEFAULT_OUTPUT


def test_iter_images_accepts_file_and_folder(tmp_path: Path) -> None:
    # Arrange
    first = _write_image(tmp_path / "a.png")
    second = _write_image(tmp_path / "b.jpg")
    (tmp_path / "nota.txt").write_text("no es imagen", encoding="utf-8")

    # Act
    single = predict.iter_images(first)
    folder = predict.iter_images(tmp_path)

    # Assert
    assert single == [first]
    assert folder == [first, second]


def test_iter_images_rejects_missing_source(tmp_path: Path) -> None:
    # Arrange / Act / Assert
    with pytest.raises(FileNotFoundError):
        predict.iter_images(tmp_path / "missing")


def test_detection_rows_maps_fields() -> None:
    # Arrange / Act
    rows = predict.detection_rows(Path("foto.png"), [_detection()])

    # Assert
    assert rows == [
        {
            "image": "foto.png",
            "class_name": "Gloves",
            "confidence": 0.9,
            "x1": 1.0,
            "y1": 2.0,
            "x2": 3.0,
            "y2": 4.0,
        }
    ]


def test_write_detections_csv(tmp_path: Path) -> None:
    # Arrange
    rows = predict.detection_rows(Path("foto.png"), [_detection()])
    output = tmp_path / "detections.csv"

    # Act
    predict.write_detections_csv(rows, output)

    # Assert
    with output.open(encoding="utf-8", newline="") as file:
        saved = list(csv.DictReader(file))
    assert len(saved) == 1
    assert saved[0]["class_name"] == "Gloves"
    assert saved[0]["confidence"] == "0.9"


def test_format_summary_counts_by_class() -> None:
    # Arrange
    rows = predict.detection_rows(Path("foto.png"), [_detection(), _detection()])

    # Act
    summary = predict.format_summary(rows)

    # Assert
    assert "Total de detecciones: 2" in summary
    assert "Gloves: 2" in summary


def test_run_writes_detections_csv(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    # Arrange
    image = _write_image(tmp_path / "a.png")
    model = tmp_path / "best.pt"
    model.write_bytes(b"pesos simulados")
    output = tmp_path / "out"
    monkeypatch.setattr(predict, "YoloDetector", FakeDetector)
    args = predict.parse_args(
        ["--model", str(model), "--source", str(image), "--output", str(output)]
    )

    # Act
    predict.run(args)

    # Assert
    with (output / "detections.csv").open(encoding="utf-8", newline="") as file:
        saved = list(csv.DictReader(file))
    assert len(saved) == 1
    assert saved[0]["image"] == str(image)
    assert "Total de detecciones: 1" in capsys.readouterr().out


def test_run_rejects_missing_model(tmp_path: Path) -> None:
    # Arrange
    image = _write_image(tmp_path / "a.png")
    args = predict.parse_args(["--model", str(tmp_path / "missing.pt"), "--source", str(image)])

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        predict.run(args)


def test_run_rejects_empty_folder(tmp_path: Path) -> None:
    # Arrange
    folder = tmp_path / "vacia"
    folder.mkdir()
    model = tmp_path / "best.pt"
    model.write_bytes(b"pesos simulados")
    args = predict.parse_args(
        ["--model", str(model), "--source", str(folder), "--output", str(tmp_path / "out")]
    )

    # Act / Assert
    with pytest.raises(FileNotFoundError):
        predict.run(args)
