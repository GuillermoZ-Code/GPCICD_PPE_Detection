"""Contrato gRPC `ppe.v1` (HU-010) — frente de Eliana (PLAN-PRUEBAS §4.3).

Complementa `tests/test_grpc.py` y las pruebas de identidad de
`tests/test_model_version.py` sin repetirlos: aquí se fijan el contrato
declarado en `ppe.proto` y sus stubs generados, la semántica xyxy del bbox
serializado, el resumen de HU-004 con clases repetidas, el error INTERNAL de
un detector que falla, el límite de recepción por encima del default de gRPC,
la equivalencia de metadatos REST/gRPC y la disponibilidad tras reconectar
(AC-010.1, AC-010.2, AC-010.3, FR-008 y AC-013.2).
"""

from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import cv2
import grpc
import numpy as np
import pytest
from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import CLASSES, Detection, Detector, FakeDetector, ImageData
from ppe_detection.detector_config import ModelIdentity
from ppe_detection.grpc import client, server
from ppe_detection.grpc.protos import ppe_pb2, ppe_pb2_grpc
from ppe_detection.grpc.server import default_options
from ppe_detection.io.images import MAX_IMAGE_BYTES, PNG_MAGIC
from ppe_detection.results import NO_DETECTIONS_MESSAGE

MODEL_VERSION = "test-1.0"
PROTO_FILE = Path("src/ppe_detection/grpc/protos/ppe.proto")


def _png_bytes(width: int = 12, height: int = 8) -> bytes:
    """PNG RGB determinista para las llamadas de prueba."""
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[0, 0] = (255, 0, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".png", bgr)
    assert ok
    return buffer.tobytes()


def _jpeg_bytes(width: int = 12, height: int = 8) -> bytes:
    """JPEG RGB determinista: el contrato también admite JPEG."""
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[1, 1] = (0, 255, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".jpg", bgr)
    assert ok
    return buffer.tobytes()


def _detection(class_id: int, confidence: float) -> Detection:
    """Detección válida de una clase canónica sobre una imagen 12x8."""
    return Detection(
        class_id=class_id,
        class_name=CLASSES[class_id],
        confidence=confidence,
        bbox=(float(class_id), float(class_id), float(class_id + 1), float(class_id + 2)),
        image_width=12,
        image_height=8,
    )


def _six_catalog_detector() -> FakeDetector:
    """FakeDetector con una detección por cada clase canónica."""
    return FakeDetector([_detection(class_id, 0.9) for class_id in range(len(CLASSES))])


@contextmanager
def _grpc_stub(
    detector: Detector | None,
    model_identity: ModelIdentity | None = None,
) -> Generator[ppe_pb2_grpc.PpeDetectionStub]:
    """Servidor gRPC real en bucle local y stub de cliente para una sesión."""
    kwargs: dict[str, Any] = {"detector": detector}
    # La versión explícita se omite cuando la prueba fija la identidad completa.
    if model_identity is not None:
        kwargs["model_identity"] = model_identity
    else:
        kwargs["model_version"] = MODEL_VERSION
    grpc_server = server.create_server(**kwargs)
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


def _rejected(stub: ppe_pb2_grpc.PpeDetectionStub, data: bytes) -> tuple[str, str]:
    """Ejecuta una llamada que debe fallar y devuelve (estado, detalle)."""
    with pytest.raises(grpc.RpcError) as excinfo:
        _call(stub, data)
    return client.call_status(excinfo.value)


def _rest_body(detector: Detector, identity: ModelIdentity) -> dict[str, Any]:
    """Ejecuta una inferencia REST con el detector e identidad dados."""
    http = TestClient(create_app(detector=detector, model_identity=identity))
    response = http.post("/predict", files={"file": ("image.png", _png_bytes(), "image/png")})
    assert response.status_code == 200
    return response.json()


# ---------------------------------------------------------------- AC-010.1


def test_proto_declares_ppe_v1_service_contract() -> None:
    """AC-010.1: `ppe.proto` declara el paquete `ppe.v1` y el RPC `Detect`."""
    # Arrange / Act
    proto = PROTO_FILE.read_text(encoding="utf-8")

    # Assert
    assert "package ppe.v1;" in proto
    assert "service PpeDetection" in proto
    assert "rpc Detect(PredictRequest) returns (PredictResponse)" in proto


def test_generated_messages_live_in_ppe_v1_package() -> None:
    """AC-010.1: los stubs generados pertenecen al paquete `ppe.v1` declarado."""
    # Arrange: el descriptor tipado de PredictResponse abre el archivo .proto.
    file_descriptor = ppe_pb2.PredictResponse.DESCRIPTOR.file

    # Act / Assert
    assert ppe_pb2.PredictResponse.DESCRIPTOR.full_name == "ppe.v1.PredictResponse"
    for message in ("BoundingBox", "Detection", "PredictRequest"):
        descriptor = file_descriptor.message_types_by_name[message]
        assert descriptor.full_name == f"ppe.v1.{message}"
    service = file_descriptor.services_by_name["PpeDetection"]
    assert service.full_name == "ppe.v1.PpeDetection"


def test_message_summary_counts_repeated_class() -> None:
    """AC-010.1 + HU-004: dos cascos producen el resumen `helmet (x2)`."""
    # Arrange
    detector = FakeDetector([_detection(3, 0.8), _detection(3, 0.6)])

    # Act
    with _grpc_stub(detector) as stub:
        response = _call(stub, _png_bytes())

    # Assert
    assert len(response.detections) == 2
    assert response.message == "Se detectaron 2 objetos EPP: helmet (x2)."


def test_grpc_accepts_jpeg_image() -> None:
    """AC-010.1: un JPEG válido produce la respuesta estructurada con dimensiones."""
    # Act
    with _grpc_stub(_six_catalog_detector()) as stub:
        response = _call(stub, _jpeg_bytes())

    # Assert
    assert (response.image_width, response.image_height) == (12, 8)
    assert response.model_version == MODEL_VERSION


# ---------------------------------------------------------------- AC-010.2


def test_bbox_xyxy_semantics_survive_serialization() -> None:
    """AC-010.2: la caja xyxy llega a protobuf sin intercambio de ejes."""
    # Arrange
    detection = Detection(
        class_id=3,
        class_name="helmet",
        confidence=0.75,
        bbox=(2.5, 1.0, 7.5, 4.0),
        image_width=10,
        image_height=6,
    )

    # Act
    with _grpc_stub(FakeDetector([detection])) as stub:
        response = _call(stub, _png_bytes(width=10, height=6))

    # Assert
    bbox = response.detections[0].bbox
    assert bbox.x1 == 2.5  # borde izquierdo, primer componente de la tupla
    assert bbox.y1 == 1.0  # borde superior
    assert bbox.x2 == 7.5  # borde derecho
    assert bbox.y2 == 4.0  # borde inferior
    assert bbox.x1 < bbox.x2 and bbox.y1 < bbox.y2


def test_rest_grpc_model_identity_metadata_equivalent() -> None:
    """AC-010.2 + AC-013.2: REST y gRPC exponen la misma identidad del modelo."""
    # Arrange
    identity = ModelIdentity(version="eq-1.0", sha256="A" * 64, artifact="modelos/best.pt")
    detector = _six_catalog_detector()

    # Act
    rest = _rest_body(detector, identity)
    with _grpc_stub(detector, model_identity=identity) as stub:
        response = _call(stub, _png_bytes())

    # Assert
    assert rest["model_version"] == response.model_version == "eq-1.0"
    assert rest["model_sha256"] == response.model_sha256 == "A" * 64
    assert rest["model_artifact"] == response.model_artifact == "modelos/best.pt"
    assert rest["model_reference"] == response.model_reference == f"sha256:{'A' * 64}"


def test_grpc_reference_falls_back_to_artifact_identity() -> None:
    """AC-013.2: sin hash pero con artefacto, la referencia es `artifact:<ruta>`."""
    # Arrange
    identity = ModelIdentity(version="v-test", sha256=None, artifact="ruta/artefacto.pt")
    grpc_server = server.create_server(detector=_six_catalog_detector(), model_identity=identity)
    port = grpc_server.add_insecure_port("127.0.0.1:0")
    grpc_server.start()
    try:
        channel = grpc.insecure_channel(f"127.0.0.1:{port}", options=default_options())
        artifact_stub = ppe_pb2_grpc.PpeDetectionStub(channel)
        response = artifact_stub.Detect(
            ppe_pb2.PredictRequest(image=_png_bytes(), source="pruebas"), timeout=30
        )
        channel.close()
    finally:
        grpc_server.stop(0)

    # Assert
    assert response.model_sha256 == ""
    assert response.model_artifact == "ruta/artefacto.pt"
    assert response.model_reference == "artifact:ruta/artefacto.pt"


# ---------------------------------------------------------------- AC-010.3


def test_undecodable_png_magic_returns_invalid_argument() -> None:
    """AC-010.3: firma PNG con contenido corrupto → INVALID_ARGUMENT de decodificación."""
    # Act
    with _grpc_stub(_six_catalog_detector()) as stub:
        state, detail = _rejected(stub, PNG_MAGIC + b"contenido que no decodifica")

    # Assert
    assert state == "INVALID_ARGUMENT"
    assert "No se pudo decodificar" in detail


def test_detector_failure_maps_to_internal_and_server_stays_up() -> None:
    """AC-010.3: un fallo del detector es INTERNAL y la siguiente llamada se atiende."""

    # Arrange
    class _FailsOnceDetector:
        def __init__(self) -> None:
            self.calls = 0

        def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
            self.calls += 1
            if self.calls == 1:
                raise RuntimeError("fallo simulado")
            return []

    detector = _FailsOnceDetector()

    # Act / Assert
    with _grpc_stub(detector) as stub:
        state, detail = _rejected(stub, _png_bytes())
        assert state == "INTERNAL"
        assert "RuntimeError" in detail
        response = _call(stub, _png_bytes())
        assert response.message == NO_DETECTIONS_MESSAGE
        assert detector.calls == 2


def test_payload_above_grpc_default_reaches_app_validation() -> None:
    """AC-010.3: un mensaje de poco más de 10 MB cruza el default de 4 MiB de
    gRPC y es la validación de la app la que responde INVALID_ARGUMENT (no el
    transporte con RESOURCE_EXHAUSTED)."""
    # Arrange
    payload = b"\xff\xd8\xff" + b"0" * (MAX_IMAGE_BYTES - 2)

    # Act
    with _grpc_stub(_six_catalog_detector()) as stub:
        state, detail = _rejected(stub, payload)

    # Assert
    assert state == "INVALID_ARGUMENT"
    assert "10 MB" in detail


def test_new_channel_connects_after_invalid_request() -> None:
    """AC-010.3: tras un error de entrada, un cliente nuevo conecta y se atiende."""
    # Arrange
    grpc_server = server.create_server(
        detector=_six_catalog_detector(), model_version=MODEL_VERSION
    )
    port = grpc_server.add_insecure_port("127.0.0.1:0")
    assert port > 0
    grpc_server.start()
    try:
        first_channel = grpc.insecure_channel(f"127.0.0.1:{port}", options=default_options())
        first_stub = ppe_pb2_grpc.PpeDetectionStub(first_channel)
        with pytest.raises(grpc.RpcError):
            first_stub.Detect(ppe_pb2.PredictRequest(image=b""), timeout=30)
        first_channel.close()

        # Act: un canal nuevo contra el mismo servidor sigue atendiendo.
        second_channel = grpc.insecure_channel(f"127.0.0.1:{port}", options=default_options())
        second_stub = ppe_pb2_grpc.PpeDetectionStub(second_channel)
        response = _call(second_stub, _png_bytes())
        second_channel.close()
    finally:
        grpc_server.stop(0)

    # Assert
    assert len(response.detections) == len(CLASSES)


# ---------------------------------------------------------------- FR-008


def test_call_status_names_error_without_grpc_code() -> None:
    """FR-008: un error sin código gRPC se reporta como UNKNOWN con su mensaje."""
    # Act
    state, detail = client.call_status(RuntimeError("boom"))

    # Assert
    assert state == "UNKNOWN"
    assert detail == "boom"
