"""Pruebas de la API REST de inferencia (HU-006)."""

from __future__ import annotations

import importlib
from typing import Any

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import Detection, Detector, FakeDetector, ImageData


def _png_bytes(width: int = 8, height: int = 6) -> bytes:
    rgb = np.zeros((height, width, 3), dtype=np.uint8)
    rgb[0, 0] = (255, 0, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".png", bgr)
    assert ok
    return buffer.tobytes()


def _detection() -> Detection:
    return Detection(
        class_id=3,
        class_name="helmet",
        confidence=0.9,
        bbox=(1.0, 2.0, 5.0, 6.0),
        image_width=8,
        image_height=6,
    )


def _client(detector: Detector | None = None) -> TestClient:
    return TestClient(
        create_app(
            detector=detector if detector is not None else FakeDetector([_detection()]),
            model_version="test-1.0",
        )
    )


def _upload(client: TestClient, data: bytes) -> Any:
    return client.post(
        "/predict",
        files={"file": ("image.png", data, "image/png")},
    )


def test_predict_returns_detections() -> None:
    """AC-01: una imagen compatible devuelve el esquema publicado."""
    # Arrange
    client = _client()

    # Act
    response = _upload(client, _png_bytes())

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["model_version"] == "test-1.0"
    assert body["image_width"] == 8
    assert body["image_height"] == 6
    assert body["elapsed_ms"] >= 0
    assert body["detections"] == [
        {
            "class_id": 3,
            "class_name": "helmet",
            "confidence": 0.9,
            "bbox": [1.0, 2.0, 5.0, 6.0],
            "image_width": 8,
            "image_height": 6,
        }
    ]


def test_empty_detections_returns_empty_list() -> None:
    """AC-01: un detector sin cajas produce una lista vacía válida."""
    # Arrange
    client = _client(FakeDetector())

    # Act
    response = _upload(client, _png_bytes())

    # Assert
    assert response.status_code == 200
    assert response.json()["detections"] == []


def test_invalid_file_returns_400_and_server_stays_up() -> None:
    """AC-02: un archivo inválido no tumba el servidor."""
    # Arrange
    client = _client()

    # Act
    invalid = _upload(client, b"no es una imagen")
    valid = _upload(client, _png_bytes())

    # Assert
    assert invalid.status_code == 400
    assert "Formato" in invalid.json()["detail"]
    assert valid.status_code == 200


def test_invalid_file_does_not_invoke_detector() -> None:
    """AC-02/FR-004: la validación ocurre antes de llamar al detector."""

    # Arrange
    class SpyDetector:
        def __init__(self) -> None:
            self.called = False

        def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
            self.called = True
            return []

    spy = SpyDetector()
    client = _client(spy)

    # Act
    response = _upload(client, b"no es una imagen")

    # Assert
    assert response.status_code == 400
    assert spy.called is False


def test_empty_file_returns_400() -> None:
    """AC-02: un archivo vacío devuelve un error de cliente."""
    # Act
    response = _upload(_client(), b"")

    # Assert
    assert response.status_code == 400
    assert "vac" in response.json()["detail"]


def test_missing_file_returns_422() -> None:
    """El campo `file` es obligatorio en el contrato multipart."""
    # Act
    response = _client().post("/predict")

    # Assert
    assert response.status_code == 422


def test_openapi_documents_predict() -> None:
    """AC-03: OpenAPI documenta la operación, la entrada y la respuesta."""
    # Act
    response = _client().get("/openapi.json")

    # Assert
    assert response.status_code == 200
    document = response.json()
    operation = document["paths"]["/predict"]["post"]
    assert "requestBody" in operation
    assert "PredictResponse" in document["components"]["schemas"]


def test_without_model_returns_503(monkeypatch: pytest.MonkeyPatch) -> None:
    """Sin artefacto configurado la API responde 503, no 500."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    client = TestClient(create_app())

    # Act
    response = _upload(client, _png_bytes())

    # Assert
    assert response.status_code == 503
    assert "modelo" in response.json()["detail"].lower()


def test_lifespan_preloads_model(monkeypatch: pytest.MonkeyPatch) -> None:
    """Con PPE_MODEL_PATH, el modelo se carga al arrancar y no en la primera petición."""
    # Arrange
    module = importlib.import_module("ppe_detection.api.app")
    fake = FakeDetector([_detection()])
    monkeypatch.setenv("PPE_MODEL_PATH", "modelo.pt")
    monkeypatch.setattr(module, "_build_detector", lambda: fake)
    application = create_app()

    # Act
    with TestClient(application) as client:
        response = client.get("/openapi.json")

    # Assert
    assert response.status_code == 200
    assert application.state.detector is fake


def test_predict_passes_conf_override() -> None:
    """El umbral de confianza se puede fijar por petición."""

    # Arrange
    class RecordingDetector:
        def __init__(self) -> None:
            self.conf: float | None = None

        def detect(self, image: ImageData, *, conf: float | None = None) -> list[Detection]:
            self.conf = conf
            return []

    detector = RecordingDetector()
    client = TestClient(create_app(detector=detector, model_version="test-1.0"))

    # Act
    response = client.post(
        "/predict",
        files={"file": ("image.png", _png_bytes(), "image/png")},
        data={"conf": "0.5"},
    )

    # Assert
    assert response.status_code == 200
    assert detector.conf == 0.5


def test_predict_rejects_out_of_range_conf() -> None:
    """Un conf fuera de [0.01, 0.99] devuelve 422, no 500."""
    # Act
    response = _client().post(
        "/predict",
        files={"file": ("image.png", _png_bytes(), "image/png")},
        data={"conf": "1.5"},
    )

    # Assert
    assert response.status_code == 422


def test_cors_allows_frontend_origin() -> None:
    """El frontend de desarrollo puede llamar a la API desde Vite."""
    # Act
    response = _client().options(
        "/predict",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    # Assert
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
