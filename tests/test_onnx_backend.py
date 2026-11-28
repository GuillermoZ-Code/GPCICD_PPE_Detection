"""Pruebas de exportación ONNX y selección de backend (HU-022)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from ppe_detection.contracts import Detection
from ppe_detection.detection import onnx as onnx_module
from ppe_detection.detection.onnx import (
    OnnxError,
    compare_detections,
    export_onnx,
    resolve_backend_path,
)


class FakeModel:
    """Exportador falso que escribe un ONNX mínimo."""

    def __init__(self, weights: str) -> None:
        self.weights = Path(weights)
        self.calls: list[dict[str, Any]] = []

    def export(self, **kwargs: Any) -> str:
        self.calls.append(kwargs)
        target = self.weights.with_suffix(".onnx")
        target.write_bytes(b"onnx-de-prueba")
        return str(target)


def _detection(
    *,
    class_name: str = "helmet",
    confidence: float = 0.8,
    bbox: tuple[float, float, float, float] = (1.0, 2.0, 5.0, 6.0),
) -> Detection:
    return Detection(
        class_id=3,
        class_name=class_name,
        confidence=confidence,
        bbox=bbox,
        image_width=8,
        image_height=6,
    )


def test_resolve_backend_defaults_to_pt(tmp_path: Path) -> None:
    """AC-03: sin formato explícito se usa el .pt."""

    weights = tmp_path / "best.pt"
    weights.write_bytes(b"pt")

    assert resolve_backend_path(weights) == weights


def test_resolve_backend_prefers_onnx(tmp_path: Path) -> None:
    """AC-03: PPE_MODEL_FORMAT=onnx selecciona el hermano .onnx."""

    weights = tmp_path / "best.pt"
    weights.write_bytes(b"pt")
    onnx = tmp_path / "best.onnx"
    onnx.write_bytes(b"onnx")

    assert resolve_backend_path(weights, "onnx") == onnx


def test_resolve_backend_rejects_unknown_format(tmp_path: Path) -> None:
    """Un formato distinto de pt/onnx falla explícitamente."""

    weights = tmp_path / "best.pt"
    weights.write_bytes(b"pt")

    with pytest.raises(OnnxError, match="Formato"):
        resolve_backend_path(weights, "tflite")


def test_resolve_backend_requires_existing_onnx(tmp_path: Path) -> None:
    """No hay fallback silencioso si falta el .onnx."""

    weights = tmp_path / "best.pt"
    weights.write_bytes(b"pt")

    with pytest.raises(OnnxError, match="No existe"):
        resolve_backend_path(weights, "onnx")


def test_export_onnx_writes_manifest(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-01: la exportación registra opset, imgsz y hashes."""

    weights = tmp_path / "best.pt"
    weights.write_bytes(b"pesos")
    fake_model = FakeModel(str(weights))
    monkeypatch.setattr(onnx_module, "_load_yolo", lambda: lambda _path: fake_model)
    monkeypatch.setattr(onnx_module, "_export_dependencies_available", lambda: True)

    result = export_onnx(weights, imgsz=480, opset=18)

    assert result.onnx.is_file()
    assert result.imgsz == 480
    assert result.opset == 18
    manifest = json.loads(result.manifest.read_text(encoding="utf-8"))
    assert manifest["imgsz"] == 480
    assert manifest["opset"] == 18
    assert manifest["weights_sha256"] == result.weights_sha256
    assert manifest["onnx_sha256"] == result.onnx_sha256


def test_export_onnx_requires_optional_dependencies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La exportación explica qué falta si no hay onnx/onnxslim."""

    weights = tmp_path / "best.pt"
    weights.write_bytes(b"pesos")
    monkeypatch.setattr(onnx_module, "_export_dependencies_available", lambda: False)

    with pytest.raises(OnnxError, match="onnx"):
        export_onnx(weights)


def test_compare_detections_within_tolerance() -> None:
    """AC-02: detecciones equivalentes no reportan diferencias."""

    reference = [_detection()]
    candidate = [_detection(confidence=0.80001, bbox=(1.0001, 2.0, 5.0, 6.0))]

    assert compare_detections(reference, candidate) == []


def test_compare_detections_reports_difference() -> None:
    """AC-02: una diferencia de clase, confianza o caja se reporta."""

    reference = [_detection()]
    candidate = [_detection(confidence=0.5, bbox=(0, 0, 1, 1))]

    differences = compare_detections(reference, candidate)

    assert len(differences) == 1
    assert "confianza" in differences[0]
    assert "bbox" in differences[0]


def test_build_detector_uses_onnx(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-03: build_detector resuelve el backend ONNX por entorno."""

    weights = tmp_path / "best.pt"
    weights.write_bytes(b"pt")
    onnx = tmp_path / "best.onnx"
    onnx.write_bytes(b"onnx")
    captured: dict[str, Path] = {}

    class FakeDetector:
        def __init__(self, path: Path, **kwargs: Any) -> None:
            captured["path"] = Path(path)

    monkeypatch.setattr("ppe_detection.detection.yolo.YoloDetector", FakeDetector)
    monkeypatch.setenv("PPE_MODEL_PATH", str(weights))
    monkeypatch.setenv("PPE_MODEL_FORMAT", "onnx")

    from ppe_detection.detector_config import build_detector

    build_detector()

    assert captured["path"] == onnx
