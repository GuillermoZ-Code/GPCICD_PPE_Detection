"""Pruebas del servicio gRPC de inferencia (HU-010)."""

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
from ppe_detection.grpc import client, server
from ppe_detection.grpc.protos import ppe_pb2, ppe_pb2_grpc
from ppe_detection.grpc.server import default_options
from ppe_detection.io import MAX_IMAGE_BYTES
from ppe_detection.results import NO_DETECTIONS_MESSAGE, build_inference_result

MODEL_VERSION = "test-1.0"


def _png_bytes(width: int = 12, height: int = 8) -> bytes:
    """Imagen PNG RGB mínima, determinista, para las pruebas."""
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[0, 0] = (255, 0, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".png", bgr)
    assert ok
    return buffer.tobytes()


def _detection(class_id: int, width: int = 12, height: int = 8) -> Detection:
    """Detección válida del catálogo canónico para una imagen 12x8."""
    x2 = class_id + 1.0
    y2 = class_id + 2.0
    return Detection(
        class_id=class_id,
        class_name=CLASSES[class_id],
        confidence=round(0.5 + 0.1 * class_id, 2),
        bbox=(float(class_id), float(class_id), x2, y2),
        image_width=width,
        image_height=height,
    )


def _six_catalog_detector() -> FakeDetector:
    """FakeDetector con una detección por cada clase canónica."""
    return FakeDetector([_detection(class_id) for class_id in range(len(CLASSES))])


@contextmanager
def _grpc_stub(
    detector: Detector | None,
) -> Generator[ppe_pb2_grpc.PpeDetectionStub]:
    """Servidor gRPC real en bucle local y stub de cliente para una sesión."""
    grpc_server = server.create_server(detector=detector, model_version=MODEL_VERSION)
    port = grpc_server.add_insecure_port("127.0.0.1:0")
    assert port > 0, "no se pudo abrir el puerto efímero de pruebas"
    grpc_server.start()
    channel = grpc.insecure_channel(f"127.0.0.1:{port}", options=default_options())
    stub = ppe_pb2_grpc.PpeDetectionStub(channel)
    try:
        yield stub
    finally:
        channel.close()
        grpc_server.stop(0)


def _call(stub: ppe_pb2_grpc.PpeDetectionStub, data: bytes) -> Any:
    """Invoca Detect con imagen y fuente de prueba."""
    request = ppe_pb2.PredictRequest(image=data, source="pruebas")
    return stub.Detect(request, timeout=30)


def _rest_response_body(detector: Detector, data: bytes) -> dict[str, Any]:
    """Ejecuta la misma inferencia vía la API REST (HU-006)."""
    http = TestClient(create_app(detector=detector, model_version=MODEL_VERSION))
    response = http.post("/predict", files={"file": ("image.png", data, "image/png")})
    assert response.status_code == 200
    return response.json()


# ---------------------------------------------------------------- AC-010.1


def test_detect_returns_structured_response_with_canonical_catalog() -> None:
    """AC-010.1: respuesta estructurada con el catálogo de seis clases."""
    # Arrange
    detector = _six_catalog_detector()
    expected_message = build_inference_result(
        [_detection(class_id) for class_id in range(len(CLASSES))]
    ).message

    # Act
    with _grpc_stub(detector) as stub:
        response = _call(stub, _png_bytes())

    # Assert
    assert len(response.detections) == 6
    assert [d.class_name for d in response.detections] == list(CLASSES)
    assert response.image_width == 12
    assert response.image_height == 8
    assert response.model_version == MODEL_VERSION
    assert response.elapsed_ms >= 0
    for detection in response.detections:
        assert detection.class_id == CLASSES.index(detection.class_name)
        assert 0.0 <= detection.confidence <= 1.0
        assert 0 <= detection.bbox.x1 < detection.bbox.x2 <= 12
        assert 0 <= detection.bbox.y1 < detection.bbox.y2 <= 8
        assert detection.image_width == 12
        assert detection.image_height == 8
    assert response.message == expected_message


def test_grpc_rest_equivalence_same_image_and_detector() -> None:
    """AC-010.2: REST y gRPC comparten convenciones con el mismo detector."""
    # Arrange
    detector = _six_catalog_detector()
    data = _png_bytes()

    # Act
    with _grpc_stub(detector) as stub:
        grpc_response = _call(stub, data)
    rest_body = _rest_response_body(detector, data)

    # Assert: convenciones semánticas (clase y confianza) y espaciales (bbox xyxy)
    rest_detections = rest_body["detections"]
    assert len(rest_detections) == len(grpc_response.detections)
    for rest, grpc_detection in zip(rest_detections, grpc_response.detections, strict=True):
        assert rest["class_id"] == grpc_detection.class_id
        assert rest["class_name"] == grpc_detection.class_name
        assert rest["confidence"] == pytest.approx(grpc_detection.confidence)
        assert rest["bbox"] == pytest.approx(
            [
                grpc_detection.bbox.x1,
                grpc_detection.bbox.y1,
                grpc_detection.bbox.x2,
                grpc_detection.bbox.y2,
            ]
        )
        assert rest["image_width"] == grpc_detection.image_width
        assert rest["image_height"] == grpc_detection.image_height
    assert rest_body["image_width"] == grpc_response.image_width
    assert rest_body["image_height"] == grpc_response.image_height
    assert rest_body["model_version"] == grpc_response.model_version
    assert rest_body["elapsed_ms"] >= 0
    assert grpc_response.elapsed_ms >= 0


def test_grpc_rest_equivalence_empty_result() -> None:
    """AC-010.2 + HU-004: vacío es un resultado válido equivalente en ambos."""
    # Arrange
    detector = FakeDetector()

    # Act
    with _grpc_stub(detector) as stub:
        grpc_response = _call(stub, _png_bytes())
    rest_body = _rest_response_body(detector, _png_bytes())

    # Assert
    assert rest_body["detections"] == []
    assert len(grpc_response.detections) == 0
    # gRPC no aclara "vacío como error": no hubo RpcError y el mensaje es del contrato.
    assert grpc_response.message == NO_DETECTIONS_MESSAGE


def test_empty_result_message_matches_hu_004_contract() -> None:
    """HU-004: la inferencia vacía usa el mensaje exacto del contrato de resultado."""
    # Act
    with _grpc_stub(FakeDetector()) as stub:
        response = _call(stub, _png_bytes())

    # Assert: no afirma incumplimiento ni ausencia real de EPP.
    assert response.message == NO_DETECTIONS_MESSAGE
    assert len(response.detections) == 0


# ---------------------------------------------------------------- AC-010.3


def _rejected(data: bytes, stub: ppe_pb2_grpc.PpeDetectionStub) -> grpc.RpcError:
    with pytest.raises(grpc.RpcError) as excinfo:
        stub.Detect(ppe_pb2.PredictRequest(image=data, source="pruebas"), timeout=30)
    return excinfo.value


def test_empty_image_returns_invalid_argument_and_server_stays_up() -> None:
    """AC-010.3: bytes vacíos → INVALID_ARGUMENT y la siguiente solicitud se atiende."""
    # Act / Assert
    with _grpc_stub(_six_catalog_detector()) as stub:
        error = _rejected(b"", stub)
        assert client.call_status(error)[0] == "INVALID_ARGUMENT"
        response = _call(stub, _png_bytes())
        assert response.image_width == 12


def test_corrupt_image_returns_invalid_argument_without_detector() -> None:
    """AC-010.3: bytes corruptos → INVALID_ARGUMENT y el detector no se invoca."""
    # Arrange
    calls: list[ImageData] = []

    class SpyDetector:
        def detect(self, image: ImageData) -> list[Detection]:
            calls.append(image)
            return []

    # Act / Assert
    with _grpc_stub(SpyDetector()) as stub:
        error = _rejected(b"no es una imagen", stub)
        assert client.call_status(error)[0] == "INVALID_ARGUMENT"
        assert "Formato" in client.call_status(error)[1]
        assert calls == []


def test_oversized_image_returns_invalid_argument() -> None:
    """AC-010.3: una imagen mayor de 10 MB se rechaza antes de decodificar."""
    # Arrange
    oversized = b"\xff\xd8\xff" + b"0" * MAX_IMAGE_BYTES

    # Act / Assert
    with _grpc_stub(_six_catalog_detector()) as stub:
        error = _rejected(oversized, stub)
        assert client.call_status(error)[0] == "INVALID_ARGUMENT"
        assert "10 MB" in client.call_status(error)[1]
        assert _call(stub, _png_bytes()).image_width == 12


def test_without_model_returns_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    """FR-006: sin artefacto configurado el estado es UNAVAILABLE, no INTERNAL."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)

    # Act / Assert
    with _grpc_stub(None) as stub:
        error = _rejected(_png_bytes(), stub)
        state, detail = client.call_status(error)
        assert state == "UNAVAILABLE"
        assert "modelo" in detail.lower()
        assert "PPE_MODEL_PATH" in detail


def test_client_detects_against_running_server() -> None:
    """FR-008: el cliente de prueba consume el servidor real con una imagen válida."""
    # Arrange
    grpc_server = server.create_server(
        detector=_six_catalog_detector(), model_version=MODEL_VERSION
    )
    port = grpc_server.add_insecure_port("127.0.0.1:0")
    assert port > 0
    grpc_server.start()
    try:
        # Act
        response = client.detect(f"127.0.0.1:{port}", _png_bytes(), timeout=30)

        # Assert
        assert [d.class_name for d in response.detections] == list(CLASSES)
        assert response.image_width == 12
    finally:
        grpc_server.stop(0)
