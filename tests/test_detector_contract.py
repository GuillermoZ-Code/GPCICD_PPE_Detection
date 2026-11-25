"""Pruebas de contrato del detector con salida estilo YOLO26 (HU-034).

La suite no carga Ultralytics, GPU ni dataset: usa un modelo falso con la misma
forma de salida que ``YOLO.predict`` y verifica el contrato público del detector.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pytest

from ppe_detection.contracts import CLASSES, ImageData
from ppe_detection.detection.yolo import YoloDetector

NAMES = dict(enumerate(CLASSES))


class FakeTensor:
    """Tensor mínimo que imita ``item()`` y ``tolist()`` de Ultralytics."""

    def __init__(self, value: Any) -> None:
        self._value = value

    def item(self) -> Any:
        return self._value

    def tolist(self) -> Any:
        return self._value


class FakeBox:
    """Caja mínima con la forma que devuelve ``Results.boxes``."""

    def __init__(self, class_id: int, confidence: float, xyxy: list[float]) -> None:
        self.cls = FakeTensor(class_id)
        self.conf = FakeTensor(confidence)
        self.xyxy = [FakeTensor(xyxy)]


class FakeResult:
    """Resultado mínimo de Ultralytics."""

    def __init__(self, boxes: list[FakeBox] | None) -> None:
        self.boxes = boxes


class FakeModel:
    """Modelo falso con nombres canónicos y una lista de resultados."""

    def __init__(self, results: list[FakeResult], names: dict[int, str] | None = None) -> None:
        self._results = results
        self.names = NAMES if names is None else names
        self.calls: list[dict[str, Any]] = []

    def predict(self, source: Any, **kwargs: Any) -> list[FakeResult]:
        self.calls.append(kwargs)
        return self._results


def _image(width: int = 8, height: int = 6) -> ImageData:
    array = np.zeros((height, width, 3), dtype=np.uint8)
    return ImageData(array=array, width=width, height=height, format="png", source="contract")


def _detector(
    results: list[FakeResult],
    *,
    names: dict[int, str] | None = None,
    **kwargs: Any,
) -> YoloDetector:
    return YoloDetector(model_path="yolo26n.pt", model=FakeModel(results, names=names), **kwargs)


def test_contract_catalog_matches_yaml_order() -> None:
    """AC-01: las seis clases se conservan en el orden canónico del data.yaml."""

    # Arrange
    expected = ("Gloves", "Vest", "goggles", "helmet", "mask", "safety_shoe")
    detector = _detector([FakeResult([])])

    # Act / Assert
    assert expected == CLASSES
    assert detector.classes == expected


def test_contract_confidence_stays_in_closed_range() -> None:
    """AC-02: las confianzas fuera de [0,1] se descartan y las válidas se conservan."""

    # Arrange
    boxes = [
        FakeBox(0, 0.0, [1, 1, 4, 4]),
        FakeBox(1, 1.0, [1, 1, 4, 4]),
        FakeBox(2, -0.01, [1, 1, 4, 4]),
        FakeBox(3, 1.01, [1, 1, 4, 4]),
        FakeBox(4, math.nan, [1, 1, 4, 4]),
        FakeBox(5, math.inf, [1, 1, 4, 4]),
    ]
    detector = _detector([FakeResult(boxes)])

    # Act
    detections = detector.detect(_image())

    # Assert
    assert [item.class_name for item in detections] == ["Gloves", "Vest"]
    assert all(0.0 <= item.confidence <= 1.0 for item in detections)


def test_contract_boxes_stay_inside_image() -> None:
    """AC-02: las cajas se recortan a los límites de la imagen."""

    # Arrange
    boxes = [
        FakeBox(0, 0.8, [-5, -5, 100, 100]),
        FakeBox(1, 0.9, [7, 5, 9, 7]),
    ]
    detector = _detector([FakeResult(boxes)])

    # Act
    detections = detector.detect(_image(width=8, height=6))

    # Assert
    assert [item.bbox for item in detections] == [(0.0, 0.0, 8.0, 6.0), (7.0, 5.0, 8.0, 6.0)]
    assert all(0 <= item.bbox[0] < item.bbox[2] <= 8 for item in detections)
    assert all(0 <= item.bbox[1] < item.bbox[3] <= 6 for item in detections)


def test_contract_fake_yolo26_output_maps_all_classes() -> None:
    """AC-03: una salida simulada de YOLO26 se convierte en detecciones tipadas."""

    # Arrange
    boxes = [FakeBox(index, 0.5 + index / 100, [1, 1, 4, 4]) for index in range(len(CLASSES))]
    model = FakeModel([FakeResult(boxes)])
    detector = YoloDetector(model_path="yolo26n.pt", model=model, nms=False)

    # Act
    detections = detector.detect(_image())

    # Assert
    assert [item.class_name for item in detections] == list(CLASSES)
    assert all(item.class_id == index for index, item in enumerate(detections))
    assert model.calls[0]["nms"] is False


@pytest.mark.parametrize("class_id", [6, -1, 99])
def test_contract_rejects_class_outside_catalog(class_id: int) -> None:
    """AC-01: un class_id fuera del catálogo falla de forma explícita."""

    # Arrange
    detector = _detector([FakeResult([FakeBox(class_id, 0.8, [1, 1, 4, 4])])])

    # Act / Assert
    with pytest.raises(ValueError, match="class_id"):
        detector.detect(_image())


def test_contract_rejects_catalog_outside_epp() -> None:
    """AC-01: un modelo con clases ajenas al catálogo EPP no se acepta."""

    # Arrange
    names = {0: "person", 1: "bicycle"}

    # Act / Assert
    with pytest.raises(ValueError):
        _detector([FakeResult([])], names=names)
