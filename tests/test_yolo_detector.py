"""Pruebas del adaptador YOLO con modelo falso (sin ultralytics)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pytest

from ppe_detection.contracts import CLASSES, ImageData
from ppe_detection.detection.yolo import YoloDetector

NAMES = dict(enumerate(CLASSES))


class FakeTensor:
    def __init__(self, value: Any) -> None:
        self._value = value

    def item(self) -> Any:
        return self._value

    def tolist(self) -> Any:
        return self._value


class FakeBox:
    def __init__(self, class_id: int, confidence: float, xyxy: list[float]) -> None:
        self.cls = FakeTensor(class_id)
        self.conf = FakeTensor(confidence)
        self.xyxy = [FakeTensor(xyxy)]


class FakeResult:
    def __init__(self, boxes: list[FakeBox] | None) -> None:
        self.boxes = boxes


class FakeModel:
    def __init__(self, results: list[FakeResult], names: dict[int, str] | None = None) -> None:
        self._results = results
        self.names = NAMES if names is None else names
        self.calls: list[dict[str, Any]] = []
        self.source: Any = None

    def predict(self, source: Any, **kwargs: Any) -> list[FakeResult]:
        self.source = source
        self.calls.append(kwargs)
        return self._results


def _image(width: int = 8, height: int = 6) -> ImageData:
    array = np.zeros((height, width, 3), dtype=np.uint8)
    array[0, 0] = (255, 0, 0)
    return ImageData(array=array, width=width, height=height, format="png", source="test")


def _detector(model: FakeModel, **kwargs: Any) -> YoloDetector:
    return YoloDetector(model_path="best.pt", model=model, **kwargs)


def test_detector_maps_boxes_to_detections() -> None:
    # Arrange
    model = FakeModel([FakeResult([FakeBox(3, 0.82, [1.0, 2.0, 5.0, 6.0])])])
    detector = _detector(model)

    # Act
    detections = detector.detect(_image())

    # Assert
    assert len(detections) == 1
    assert detections[0].class_name == "helmet"
    assert detections[0].confidence == 0.82
    assert detections[0].bbox == (1.0, 2.0, 5.0, 6.0)
    assert (detections[0].image_width, detections[0].image_height) == (8, 6)


def test_detector_uses_canonical_catalog() -> None:
    # Arrange / Act
    detector = _detector(FakeModel([]))

    # Assert
    assert detector.classes == CLASSES


def test_detector_converts_rgb_to_bgr() -> None:
    # Arrange
    model = FakeModel([])
    detector = _detector(model)

    # Act
    detector.detect(_image())

    # Assert: el píxel rojo RGB (255, 0, 0) llega al modelo como BGR (0, 0, 255).
    assert model.source[0, 0].tolist() == [0, 0, 255]


def test_detector_returns_empty_list_without_boxes() -> None:
    # Arrange
    detector = _detector(FakeModel([FakeResult(None)]))

    # Act
    detections = detector.detect(_image())

    # Assert
    assert detections == []


def test_detector_returns_empty_list_with_empty_boxes() -> None:
    # Arrange
    detector = _detector(FakeModel([FakeResult([])]))

    # Act / Assert
    assert detector.detect(_image()) == []


def test_detector_returns_empty_list_without_results() -> None:
    # Arrange
    detector = _detector(FakeModel([]))

    # Act / Assert
    assert detector.detect(_image()) == []


def test_detector_clips_boxes_to_image() -> None:
    # Arrange
    model = FakeModel([FakeResult([FakeBox(0, 0.5, [-5.0, -5.0, 100.0, 100.0])])])
    detector = _detector(model)

    # Act
    detections = detector.detect(_image(width=8, height=6))

    # Assert
    assert detections[0].bbox == (0.0, 0.0, 8.0, 6.0)


def test_detector_skips_degenerate_boxes() -> None:
    # Arrange
    boxes = [FakeBox(0, 0.5, [4.0, 4.0, 4.0, 4.0]), FakeBox(0, 0.5, [6.0, 1.0, 3.0, 2.0])]
    detector = _detector(FakeModel([FakeResult(boxes)]))

    # Act
    detections = detector.detect(_image())

    # Assert
    assert detections == []


def test_detector_skips_invalid_confidence() -> None:
    # Arrange: una caja válida entre confianzas no finitas o fuera de rango.
    boxes = [
        FakeBox(0, 0.5, [1.0, 1.0, 4.0, 4.0]),
        FakeBox(1, math.nan, [1.0, 1.0, 4.0, 4.0]),
        FakeBox(1, math.inf, [1.0, 1.0, 4.0, 4.0]),
        FakeBox(1, -0.2, [1.0, 1.0, 4.0, 4.0]),
        FakeBox(1, 1.4, [1.0, 1.0, 4.0, 4.0]),
    ]
    detector = _detector(FakeModel([FakeResult(boxes)]))

    # Act
    detections = detector.detect(_image())

    # Assert
    assert [detection.class_name for detection in detections] == ["Gloves"]


def test_detector_rejects_wrong_catalog() -> None:
    # Arrange
    names = dict(enumerate(("Helmet", "Vest", "Gloves", "Goggles", "Mask", "Safety Shoe")))

    # Act / Assert
    with pytest.raises(ValueError):
        _detector(FakeModel([], names=names))


def test_detector_rejects_coco_catalog() -> None:
    # Arrange
    names = {0: "person", 1: "bicycle", 2: "car"}

    # Act / Assert
    with pytest.raises(ValueError):
        _detector(FakeModel([], names=names))


def test_detector_rejects_out_of_range_class() -> None:
    # Arrange
    model = FakeModel([FakeResult([FakeBox(6, 0.9, [1.0, 1.0, 2.0, 2.0])])])
    detector = _detector(model)

    # Act / Assert
    with pytest.raises(ValueError):
        detector.detect(_image())


def test_detector_passes_thresholds_to_model() -> None:
    # Arrange
    model = FakeModel([])
    detector = _detector(model, conf=0.3, iou=0.5, imgsz=1280, device="cpu")

    # Act
    detector.detect(_image())

    # Assert
    assert model.calls == [
        {"conf": 0.3, "iou": 0.5, "imgsz": 1280, "device": "cpu", "verbose": False}
    ]


def test_detector_requires_model_or_path() -> None:
    # Arrange / Act / Assert
    with pytest.raises(ValueError):
        YoloDetector()


@pytest.mark.skipif(not Path("artifacts/models").is_dir(), reason="sin artefactos locales")
def test_real_weights_smoke() -> None:
    # Arrange
    pytest.importorskip("ultralytics")
    weights = next(Path("artifacts/models").glob("*/weights/best.pt"), None)
    samples_dir = Path("artifacts/samples")
    samples = sorted(samples_dir.glob("*")) if samples_dir.is_dir() else []
    sample = next(
        (path for path in samples if path.suffix.lower() in {".jpg", ".jpeg", ".png"}),
        None,
    )
    if weights is None or sample is None:
        pytest.skip("faltan pesos o muestra local")

    # Act
    from ppe_detection.io import load_image

    detector = YoloDetector(weights, conf=0.25, imgsz=640, device="cpu")
    detections = detector.detect(load_image(sample))

    # Assert
    assert isinstance(detections, list)
    assert all(detection.class_name in CLASSES for detection in detections)
