"""Pruebas de límites de carga en REST (HU-048, issue #104)."""

from __future__ import annotations

import cv2
import numpy as np
from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import FakeDetector


def _image_bytes(extension: str) -> bytes:
    ok, buffer = cv2.imencode(extension, np.zeros((8, 8, 3), dtype=np.uint8))
    assert ok
    return buffer.tobytes()


def _client() -> TestClient:
    return TestClient(create_app(detector=FakeDetector([])))


def _upload(client: TestClient, data: bytes, mime: str = "image/png", name: str = "image.png"):
    return client.post("/predict", files={"file": (name, data, mime)})


def test_file_above_configured_limit_returns_413(monkeypatch) -> None:
    """AC-01: superar PPE_MAX_UPLOAD_MB responde 413 con el límite configurado."""
    # Arrange
    monkeypatch.setenv("PPE_MAX_UPLOAD_MB", "0.001")
    client = _client()

    # Act
    response = _upload(client, b"x" * 2048)

    # Assert
    assert response.status_code == 413
    assert "0.001" in response.json()["detail"]


def test_default_limit_allows_small_image(monkeypatch) -> None:
    """AC-01: sin configuración, una imagen pequeña se acepta con el límite de 10 MB."""
    # Arrange
    monkeypatch.delenv("PPE_MAX_UPLOAD_MB", raising=False)
    client = _client()

    # Act
    response = _upload(client, _image_bytes(".png"))

    # Assert
    assert response.status_code == 200


def test_disallowed_mime_returns_415() -> None:
    """AC-02: un MIME distinto de PNG/JPEG responde 415."""
    # Act
    response = _upload(_client(), _image_bytes(".png"), mime="application/pdf")

    # Assert
    assert response.status_code == 415


def test_mime_with_parameters_is_accepted() -> None:
    """AC-02: un MIME PNG con parámetros se normaliza y se acepta."""
    # Act
    response = _upload(_client(), _image_bytes(".png"), mime="image/png; charset=binary")

    # Assert
    assert response.status_code == 200


def test_415_message_names_allowed_types() -> None:
    """AC-02: el error 415 indica los tipos permitidos."""
    # Act
    response = _upload(_client(), _image_bytes(".png"), mime="application/pdf")

    # Assert
    detail = response.json()["detail"]
    assert "image/png" in detail
    assert "image/jpeg" in detail


def test_valid_jpeg_is_still_accepted() -> None:
    """AC-02: JPEG con MIME y firma correctos sigue siendo válido."""
    # Act
    response = _upload(_client(), _image_bytes(".jpg"), mime="image/jpeg", name="obra.jpg")

    # Assert
    assert response.status_code == 200


def test_service_responds_after_rejection(monkeypatch) -> None:
    """AC-03: tras un 413 el servicio sigue disponible."""
    # Arrange
    monkeypatch.setenv("PPE_MAX_UPLOAD_MB", "0.001")
    client = _client()
    _upload(client, b"x" * 2048)

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200


def test_valid_prediction_after_rejection() -> None:
    """AC-03: tras un 415 una inferencia válida no queda corrompida."""
    # Arrange
    client = _client()
    _upload(client, _image_bytes(".png"), mime="application/pdf")

    # Act
    response = _upload(client, _image_bytes(".png"))

    # Assert
    assert response.status_code == 200
    assert "detections" in response.json()
