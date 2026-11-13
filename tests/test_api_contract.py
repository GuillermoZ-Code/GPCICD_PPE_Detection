"""Contrato HTTP de la API REST (HU-006) — frente de Eliana (PLAN-PRUEBAS §4.3).

Complementa `tests/test_api.py`, `tests/test_image_validation.py` y las pruebas
de identidad de `tests/test_model_version.py` sin repetirlos: aquí se fijan los
límites del esquema publicado (OpenAPI), los bordes del umbral `conf`, el
mapeo del adaptador hacia el detector inyectado, la configuración de CORS por
entorno y la semántica del resultado vacío (AC-006.1, AC-006.2, AC-006.3,
AC-004.1/2 y AC-013.1).
"""

from __future__ import annotations

from typing import Any

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import CLASSES, Detection, FakeDetector, ImageData
from ppe_detection.io import MAX_IMAGE_BYTES
from ppe_detection.io.images import PNG_MAGIC

PNG_NAME = "image.png"


def _png_bytes(width: int = 8, height: int = 6) -> bytes:
    """PNG RGB determinista para las peticiones de prueba."""
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[0, 0] = (255, 0, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".png", bgr)
    assert ok
    return buffer.tobytes()


def _jpeg_bytes(width: int = 8, height: int = 6) -> bytes:
    """JPEG RGB determinista: la API también acepta el segundo formato."""
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[1, 1] = (0, 255, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".jpg", bgr)
    assert ok
    return buffer.tobytes()


def _detection(class_id: int, confidence: float) -> Detection:
    """Detección válida de una clase canónica sobre una imagen 8x6."""
    return Detection(
        class_id=class_id,
        class_name=CLASSES[class_id],
        confidence=confidence,
        bbox=(float(class_id), 1.0, float(class_id + 1), 3.0),
        image_width=8,
        image_height=6,
    )


def _client(detector: Any) -> TestClient:
    return TestClient(create_app(detector=detector, model_version="test-1.0"))


def _upload(
    client: TestClient,
    data: bytes,
    filename: str = PNG_NAME,
    mime: str = "image/png",
) -> Any:
    return client.post("/predict", files={"file": (filename, data, mime)})


def _data(conf: str | None) -> dict[str, str]:
    return {} if conf is None else {"conf": conf}


class _CountingDetector:
    """Detector doble: cuenta invocaciones y no devuelve detecciones."""

    def __init__(self) -> None:
        self.calls = 0

    def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
        self.calls += 1
        return []


class _CapturingDetector:
    """Detector doble: guarda la última imagen decodificada que recibió."""

    def __init__(self) -> None:
        self.image: ImageData | None = None

    def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
        self.image = image
        return []


class _RecordingDetector:
    """Detector doble: registra el umbral `conf` que le llegó."""

    def __init__(self) -> None:
        self.conf: float | None = None

    def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
        self.conf = conf
        return []


# ---------------------------------------------------------------- AC-006.3


def test_openapi_documents_conf_parameter_constraints() -> None:
    """AC-006.3: el esquema publicado declara los límites de `conf` (0.01..0.99)."""
    # Arrange
    document = _client(FakeDetector()).get("/openapi.json").json()
    body = document["components"]["schemas"]["Body_predict_predict_post"]

    # Act
    conf = body["properties"]["conf"]["anyOf"][0]

    # Assert
    assert conf["minimum"] == 0.01
    assert conf["maximum"] == 0.99


def test_predict_response_schema_requires_full_contract() -> None:
    """AC-006.1: `PredictResponse` declara obligatorios los ocho campos publicados."""
    # Arrange
    document = _client(FakeDetector()).get("/openapi.json").json()

    # Act
    required = document["components"]["schemas"]["PredictResponse"]["required"]

    # Assert
    assert set(required) == {
        "detections",
        "image_width",
        "image_height",
        "model_version",
        "model_sha256",
        "model_artifact",
        "model_reference",
        "elapsed_ms",
    }


def test_conf_boundaries_are_inclusive_and_forwarded() -> None:
    """AC-006.3: 0.01 y 0.99 son válidos y llegan al detector sin transformación."""
    for value in ("0.01", "0.99"):
        # Arrange
        detector = _RecordingDetector()
        client = _client(detector)

        # Act
        response = client.post(
            "/predict",
            files={"file": (PNG_NAME, _png_bytes(), "image/png")},
            data=_data(value),
        )

        # Assert
        assert response.status_code == 200
        assert detector.conf == float(value)


def test_conf_outside_boundaries_rejected() -> None:
    """AC-006.3: valores justo fuera del rango devuelven 422 de validación."""
    for value in ("0.009", "0.991"):
        # Arrange
        client = _client(FakeDetector())

        # Act
        response = client.post(
            "/predict",
            files={"file": (PNG_NAME, _png_bytes(), "image/png")},
            data=_data(value),
        )

        # Assert
        assert response.status_code == 422


def test_conf_non_numeric_rejected() -> None:
    """AC-006.3: un `conf` no numérico es un error de validación, no un 500."""
    # Arrange
    client = _client(FakeDetector())

    # Act
    response = client.post(
        "/predict",
        files={"file": (PNG_NAME, _png_bytes(), "image/png")},
        data=_data("no-es-numero"),
    )

    # Assert
    assert response.status_code == 422


# ---------------------------------------------------------------- AC-006.2


def test_oversized_upload_rejected_before_detector_and_server_stays_up() -> None:
    """AC-006.2: un archivo mayor de 10 MB da 400, no llama al detector y la
    siguiente petición se atiende con la misma instancia inyectada."""
    # Arrange
    spy = _CountingDetector()
    client = _client(spy)
    oversized = b"\xff\xd8\xff" + b"0" * MAX_IMAGE_BYTES

    # Act
    rejected = _upload(client, oversized)

    # Assert: rechazo antes del detector, sin tumba del servidor.
    assert rejected.status_code == 400
    assert "10 MB" in rejected.json()["detail"]
    assert spy.calls == 0
    accepted = _upload(client, _png_bytes())
    assert accepted.status_code == 200
    assert spy.calls == 1  # el detector inyectado se reutiliza entre peticiones


def test_png_magic_with_corrupt_payload_returns_client_error() -> None:
    """AC-006.2: bytes con firma PNG pero contenido corrupto son un 4xx de
    decodificación, sin invocar el detector y sin tumbar el servidor."""
    # Arrange
    spy = _CountingDetector()
    client = _client(spy)

    # Act
    rejected = _upload(client, PNG_MAGIC + b"contenido que no decodifica")

    # Assert
    assert rejected.status_code == 400
    assert "No se pudo decodificar" in rejected.json()["detail"]
    assert spy.calls == 0
    accepted = _upload(client, _png_bytes())
    assert accepted.status_code == 200


def test_get_predict_is_method_not_allowed() -> None:
    """AC-006.3: el contrato publicado solo define POST; GET devuelve 405."""
    # Act
    response = _client(FakeDetector()).get("/predict")

    # Assert
    assert response.status_code == 405


# ---------------------------------------------------------------- CORS


def test_cors_origins_configurable_via_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CORS: `PPE_CORS_ORIGINS` define los orígenes permitidos en el despliegue."""
    # Arrange
    monkeypatch.setenv("PPE_CORS_ORIGINS", "http://localhost:8080")
    client = _client(FakeDetector())
    preflight = {
        "Access-Control-Request-Method": "POST",
        "Origin": "http://localhost:8080",
    }

    # Act
    allowed = client.options("/predict", headers=preflight)
    denied = client.options(
        "/predict",
        headers={"Access-Control-Request-Method": "POST", "Origin": "http://localhost:5173"},
    )

    # Assert
    assert allowed.status_code == 200
    assert allowed.headers["access-control-allow-origin"] == "http://localhost:8080"
    assert "access-control-allow-origin" not in denied.headers


def test_actual_post_cors_response_carries_allow_origin() -> None:
    """CORS: una petición real con origen permitido recibe la cabecera de vuelta."""
    # Arrange
    client = _client(FakeDetector())

    # Act
    response = client.post(
        "/predict",
        files={"file": (PNG_NAME, _png_bytes(), "image/png")},
        headers={"Origin": "http://localhost:5173"},
    )

    # Assert
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


# ---------------------------------------------------------------- AC-006.1


def test_jpeg_upload_accepted_and_format_forwarded() -> None:
    """AC-006.1: un JPEG válido se acepta y llega al detector como formato `jpeg`."""
    # Arrange
    spy = _CapturingDetector()
    client = _client(spy)

    # Act
    response = _upload(client, _jpeg_bytes(), filename="obra.jpeg", mime="image/jpeg")

    # Assert
    assert response.status_code == 200
    assert spy.image is not None
    assert spy.image.format == "jpeg"
    assert (spy.image.width, spy.image.height) == (8, 6)


def test_detector_receives_source_and_original_dimensions() -> None:
    """AC-006.1: el adaptador entrega al detector el nombre de archivo como
    fuente y las dimensiones originales de la imagen decodificada."""
    # Arrange
    spy = _CapturingDetector()
    client = _client(spy)

    # Act
    response = _upload(client, _png_bytes(), filename="reporte de obra.png")

    # Assert
    assert response.status_code == 200
    assert spy.image is not None
    assert spy.image.source == "reporte de obra.png"
    assert (spy.image.width, spy.image.height) == (8, 6)


def test_multiple_detections_preserve_order_and_full_schema() -> None:
    """AC-006.1: varias detecciones conservan el orden del detector y cada campo."""
    # Arrange
    detections = [
        _detection(class_id, 0.9 - 0.1 * index) for index, class_id in enumerate((0, 3, 5))
    ]
    client = _client(FakeDetector(detections))

    # Act
    response = _upload(client, _png_bytes())

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert [item["class_name"] for item in body["detections"]] == [
        "Gloves",
        "helmet",
        "safety_shoe",
    ]
    for position, detection in enumerate(body["detections"]):
        expected = detections[position]
        assert detection == {
            "class_id": expected.class_id,
            "class_name": expected.class_name,
            "confidence": expected.confidence,
            "bbox": list(expected.bbox),
            "image_width": expected.image_width,
            "image_height": expected.image_height,
        }


def test_empty_result_is_valid_contract_response() -> None:
    """AC-004.1/AC-004.2: el resultado vacío es 200 con el contrato completo,
    sin `detail` de error y conservando dimensiones e identidad del modelo."""
    # Arrange
    client = _client(FakeDetector())

    # Act
    response = _upload(client, _png_bytes())

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["detections"] == []
    assert "detail" not in body
    assert (body["image_width"], body["image_height"]) == (8, 6)
    assert body["model_version"] == "test-1.0"


def test_explicit_model_version_wins_over_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """AC-013.1: la versión explícita de la app prevalece sobre `PPE_MODEL_VERSION`."""
    # Arrange
    monkeypatch.setenv("PPE_MODEL_VERSION", "env-1.2")
    client = _client(FakeDetector([_detection(3, 0.9)]))

    # Act
    response = _upload(client, _png_bytes())

    # Assert
    assert response.status_code == 200
    assert response.json()["model_version"] == "test-1.0"
