"""Paridad REST/gRPC con el detector simulado común (HU-062, issue #118)."""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from typing import Any

import cv2
import grpc
import numpy as np
import pytest
from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import CLASSES, Detection, Detector, FakeDetector, ImageData
from ppe_detection.detector_config import DetectorNotConfiguredError, ModelIdentity
from ppe_detection.grpc import client, server
from ppe_detection.grpc.protos import ppe_pb2, ppe_pb2_grpc
from ppe_detection.grpc.server import default_options
from ppe_detection.results import NO_DETECTIONS_MESSAGE

IDENTITY = ModelIdentity(
    version="paridad-1.0",
    sha256="B" * 64,
    artifact="modelos/best.onnx",
)


class _CountingDetector:
    """Detector simulado que registra cuántas veces se le invoca."""

    def __init__(self, detections: list[Detection]) -> None:
        self.detections = detections
        self.calls = 0

    def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
        self.calls += 1
        return list(self.detections)


class _UnconfiguredDetector:
    """Detector inyectado que se comporta como modelo no configurado."""

    def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
        raise DetectorNotConfiguredError("No hay un modelo de inferencia configurado.")


def _png(width: int = 12, height: int = 8) -> bytes:
    """PNG RGB determinista compartido por ambos protocolos."""
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[0, 0] = (255, 0, 0)
    ok, buffer = cv2.imencode(".png", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    assert ok
    return buffer.tobytes()


def _jpeg(width: int = 12, height: int = 8) -> bytes:
    """JPEG RGB determinista compartido por ambos protocolos."""
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[1, 1] = (0, 255, 0)
    ok, buffer = cv2.imencode(".jpg", cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
    assert ok
    return buffer.tobytes()


def _detections() -> list[Detection]:
    """Seis detecciones canónicas, una por clase, en orden estable."""
    return [
        Detection(
            class_id=index,
            class_name=CLASSES[index],
            confidence=round(0.55 + 0.05 * index, 2),
            bbox=(float(index), float(index), float(index + 1), float(index + 2)),
            image_width=12,
            image_height=8,
        )
        for index in range(len(CLASSES))
    ]


def _fake_detector() -> FakeDetector:
    """FakeDetector con el catálogo canónico, sin pesos ni GPU."""
    return FakeDetector(_detections())


def _rest(detector: Detector, data: bytes, *, mime: str = "image/png") -> Any:
    """Cliente REST con el detector y la identidad fijos."""
    return TestClient(create_app(detector=detector, model_identity=IDENTITY)).post(
        "/predict", files={"file": ("image.png", data, mime)}
    )


@contextmanager
def _grpc(detector: Detector | None) -> Generator[ppe_pb2_grpc.PpeDetectionStub]:
    """Servidor gRPC efímero en bucle local con el detector inyectado."""
    grpc_server = server.create_server(detector=detector, model_identity=IDENTITY)
    port = grpc_server.add_insecure_port("127.0.0.1:0")
    assert port > 0
    grpc_server.start()
    channel = grpc.insecure_channel(f"127.0.0.1:{port}", options=default_options())
    try:
        yield ppe_pb2_grpc.PpeDetectionStub(channel)
    finally:
        channel.close()
        grpc_server.stop(0)


def _call(stub: ppe_pb2_grpc.PpeDetectionStub, data: bytes) -> Any:
    """Invoca `Detect` con la imagen compartida."""
    return stub.Detect(ppe_pb2.PredictRequest(image=data, source="paridad"), timeout=30)


def _rejected(stub: ppe_pb2_grpc.PpeDetectionStub, data: bytes) -> tuple[str, str]:
    """Devuelve (código, detalle) de una llamada gRPC rechazada."""
    with pytest.raises(grpc.RpcError) as excinfo:
        _call(stub, data)
    return client.call_status(excinfo.value)


# ---------------------------------------------------------------- AC-01


def test_same_png_returns_identical_detections() -> None:
    """AC-01: el mismo PNG produce las mismas detecciones por ambos protocolos."""
    # Arrange
    data = _png()
    detector = _fake_detector()

    # Act
    rest = _rest(detector, data)
    with _grpc(detector) as stub:
        grpc_response = _call(stub, data)

    # Assert
    assert rest.status_code == 200
    rest_detections = rest.json()["detections"]
    assert len(rest_detections) == len(grpc_response.detections) == len(CLASSES)
    for item, proto in zip(rest_detections, grpc_response.detections, strict=True):
        assert item["class_id"] == proto.class_id
        assert item["class_name"] == proto.class_name
        assert item["confidence"] == pytest.approx(proto.confidence)
        assert item["bbox"] == pytest.approx(
            [proto.bbox.x1, proto.bbox.y1, proto.bbox.x2, proto.bbox.y2]
        )


def test_same_jpeg_is_accepted_by_both_protocols() -> None:
    """AC-01: el mismo JPEG se acepta por ambos protocolos."""
    # Arrange
    data = _jpeg()
    detector = _fake_detector()

    # Act
    rest = _rest(detector, data, mime="image/jpeg")
    with _grpc(detector) as stub:
        grpc_response = _call(stub, data)

    # Assert
    assert rest.status_code == 200
    assert rest.json()["image_width"] == grpc_response.image_width == 12
    assert len(rest.json()["detections"]) == len(grpc_response.detections)


def test_empty_result_is_equivalent() -> None:
    """AC-01: un resultado vacío es válido y equivalente."""
    # Arrange
    detector = FakeDetector()
    data = _png()

    # Act
    rest = _rest(detector, data)
    with _grpc(detector) as stub:
        grpc_response = _call(stub, data)

    # Assert
    assert rest.status_code == 200
    assert rest.json()["detections"] == []
    assert list(grpc_response.detections) == []
    assert grpc_response.message == NO_DETECTIONS_MESSAGE


def test_detection_order_and_bbox_are_equivalent() -> None:
    """AC-01: el orden y la semántica xyxy del bbox se conservan."""
    # Arrange
    detector = _fake_detector()
    data = _png()

    # Act
    rest = _rest(detector, data).json()["detections"]
    with _grpc(detector) as stub:
        proto = list(_call(stub, data).detections)

    # Assert
    assert (
        [item["class_name"] for item in rest]
        == [item.class_name for item in proto]
        == list(CLASSES)
    )
    for item, detection in zip(rest, proto, strict=True):
        x1, y1, x2, y2 = item["bbox"]
        assert x1 < x2 and y1 < y2
        assert (x1, y1, x2, y2) == pytest.approx(
            (detection.bbox.x1, detection.bbox.y1, detection.bbox.x2, detection.bbox.y2)
        )


def test_model_identity_is_equivalent() -> None:
    """AC-01: versión, SHA256, artefacto y referencia coinciden."""
    # Arrange
    detector = _fake_detector()
    data = _png()

    # Act
    rest = _rest(detector, data).json()
    with _grpc(detector) as stub:
        grpc_response = _call(stub, data)

    # Assert
    assert rest["model_version"] == grpc_response.model_version == IDENTITY.version
    assert rest["model_sha256"] == grpc_response.model_sha256 == IDENTITY.sha256
    assert rest["model_artifact"] == grpc_response.model_artifact == IDENTITY.artifact
    assert rest["model_reference"] == grpc_response.model_reference == f"sha256:{IDENTITY.sha256}"


def test_both_protocols_report_same_image_dimensions() -> None:
    """AC-01: las dimensiones informadas coinciden con la imagen decodificada."""
    # Arrange
    detector = _fake_detector()
    data = _png(width=20, height=10)

    # Act
    rest = _rest(detector, data).json()
    with _grpc(detector) as stub:
        grpc_response = _call(stub, data)

    # Assert
    assert (rest["image_width"], rest["image_height"]) == (20, 10)
    assert (grpc_response.image_width, grpc_response.image_height) == (20, 10)


# ---------------------------------------------------------------- AC-02


def test_invalid_image_maps_400_to_invalid_argument(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-02: una entrada inválida da 400 e INVALID_ARGUMENT con el mismo detalle."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    data = b"no-es-una-imagen"
    detector = _fake_detector()

    # Act
    rest = _rest(detector, data)
    with _grpc(detector) as stub:
        state, detail = _rejected(stub, data)

    # Assert
    assert rest.status_code == 400
    assert state == "INVALID_ARGUMENT"
    assert rest.json()["detail"] == detail
    assert "JPEG y PNG" in detail


def test_missing_model_maps_503_to_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-02: sin modelo configurado, 503 ↔ UNAVAILABLE."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    data = _png()

    # Act
    rest = TestClient(create_app()).post(
        "/predict", files={"file": ("image.png", data, "image/png")}
    )
    with _grpc(None) as stub:
        state, detail = _rejected(stub, data)

    # Assert
    assert rest.status_code == 503
    assert state == "UNAVAILABLE"
    assert rest.json()["detail"] == detail


def test_detection_time_unconfigured_maps_503_to_unavailable() -> None:
    """AC-02: un detector inyectado sin modelo mapea 503 ↔ UNAVAILABLE."""
    # Arrange
    detector = _UnconfiguredDetector()
    data = _png()

    # Act
    rest = _rest(detector, data)
    with _grpc(detector) as stub:
        state, detail = _rejected(stub, data)

    # Assert
    assert rest.status_code == 503
    assert state == "UNAVAILABLE"
    assert rest.json()["detail"] == detail


def test_service_recovers_after_rejection() -> None:
    """AC-02: tras un rechazo, ambos protocolos siguen atendiendo inferencias."""
    # Arrange
    data = _png()
    detector = _fake_detector()

    # Act
    bad_rest = _rest(detector, b"")
    with _grpc(detector) as stub:
        _rejected(stub, b"")
        recovered_grpc = _call(stub, data)
    recovered_rest = _rest(detector, data)

    # Assert
    assert bad_rest.status_code == 400
    assert recovered_rest.status_code == 200
    assert len(recovered_rest.json()["detections"]) == len(recovered_grpc.detections)


# ---------------------------------------------------------------- AC-03


def test_shared_fake_detector_needs_no_model_weights(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-03: la paridad se prueba sin PPE_MODEL_PATH ni pesos."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    detector = _fake_detector()
    data = _png()

    # Act
    rest = _rest(detector, data)
    with _grpc(detector) as stub:
        grpc_response = _call(stub, data)

    # Assert
    assert rest.status_code == 200
    assert len(grpc_response.detections) == len(CLASSES)


def test_shared_fake_detector_is_called_once_per_protocol() -> None:
    """AC-03: el detector compartido se invoca una vez por cada protocolo."""
    # Arrange
    detector = _CountingDetector(_detections())
    data = _png()

    # Act
    _rest(detector, data)
    with _grpc(detector) as stub:
        _call(stub, data)

    # Assert
    assert detector.calls == 2


def test_shared_fake_detector_confidences_match() -> None:
    """AC-03: las confianzas del detector simulado no se alteran en ningún adaptador."""
    # Arrange
    detector = _fake_detector()
    expected = [item.confidence for item in _detections()]
    data = _png()

    # Act
    rest = _rest(detector, data).json()["detections"]
    with _grpc(detector) as stub:
        proto = list(_call(stub, data).detections)

    # Assert
    assert [item["confidence"] for item in rest] == pytest.approx(expected)
    assert [item.confidence for item in proto] == pytest.approx(expected)
