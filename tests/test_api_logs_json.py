"""Pruebas de logs estructurados con request_id (HU-047, issue #103)."""

from __future__ import annotations

import json
import logging
import uuid
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.api.logging import RequestLoggingMiddleware
from ppe_detection.contracts import FakeDetector

LOGGER = "ppe_detection.api"
REQUIRED_FIELDS = {"event", "method", "path", "status", "duration_ms", "request_id"}


@pytest.fixture(autouse=True)
def _enable_request_logs(caplog: pytest.LogCaptureFixture) -> None:
    caplog.set_level(logging.INFO, logger=LOGGER)


def _client() -> TestClient:
    return TestClient(create_app(detector=FakeDetector([])))


def _entries(caplog: pytest.LogCaptureFixture) -> list[dict[str, Any]]:
    return [json.loads(record.getMessage()) for record in caplog.records if record.name == LOGGER]


def test_logs_method_path_status_latency_and_request_id(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """AC-01: cada petición registra método, ruta, estado, latencia y request_id."""
    # Arrange
    client = _client()

    # Act
    response = client.get("/health")

    # Assert
    entry = _entries(caplog)[0]
    assert entry["method"] == "GET"
    assert entry["path"] == "/health"
    assert entry["status"] == 200
    assert isinstance(entry["duration_ms"], (int, float))
    assert entry["request_id"] == response.headers["x-request-id"]


def test_each_request_emits_one_json_log_record(caplog: pytest.LogCaptureFixture) -> None:
    """AC-01: dos peticiones producen dos registros, uno por cada una."""
    # Arrange
    client = _client()

    # Act
    client.get("/health")
    client.get("/health/live")

    # Assert
    assert len(_entries(caplog)) == 2


def test_generated_request_id_is_present_in_log(caplog: pytest.LogCaptureFixture) -> None:
    """AC-01: el identificador generado aparece en el registro."""
    # Act
    _client().get("/health")

    # Assert
    request_id = _entries(caplog)[0]["request_id"]
    assert uuid.UUID(str(request_id))


def test_log_line_is_valid_json(caplog: pytest.LogCaptureFixture) -> None:
    """AC-01: la línea de log es JSON válido con los campos contractuales."""
    # Act
    _client().get("/health")

    # Assert
    records = [record for record in caplog.records if record.name == LOGGER]
    entry = json.loads(records[0].getMessage())
    assert set(entry) >= REQUIRED_FIELDS


def test_error_responses_are_logged_with_500(caplog: pytest.LogCaptureFixture) -> None:
    """AC-01: un error interno se registra con estado 500 sin filtrar detalles."""
    # Arrange
    app = FastAPI()
    app.add_middleware(RequestLoggingMiddleware)

    @app.get("/boom")
    async def boom() -> None:
        raise RuntimeError("BOOM-SECRETO")

    client = TestClient(app)

    # Act
    response = client.get("/boom")

    # Assert
    assert response.status_code == 500
    entry = _entries(caplog)[0]
    assert entry["status"] == 500
    assert "BOOM-SECRETO" not in caplog.text


def test_authorization_header_is_never_logged(caplog: pytest.LogCaptureFixture) -> None:
    """AC-02: el token Bearer no aparece en el log."""
    # Act
    _client().get("/health", headers={"Authorization": "Bearer token-secreto-123"})

    # Assert
    assert "token-secreto-123" not in caplog.text


def test_api_key_header_is_never_logged(caplog: pytest.LogCaptureFixture) -> None:
    """AC-02: la clave de API de cabecera no aparece en el log."""
    # Act
    _client().get("/health", headers={"X-API-Key": "clave-super-secreta-456"})

    # Assert
    assert "clave-super-secreta-456" not in caplog.text


def test_request_body_is_never_logged(caplog: pytest.LogCaptureFixture) -> None:
    """AC-02: el cuerpo JSON de la petición no se serializa en el log."""
    # Act
    _client().post("/ruta-inexistente", json={"secreto": "cuerpo-super-secreto"})

    # Assert
    assert "cuerpo-super-secreto" not in caplog.text


def test_image_bytes_are_never_logged(caplog: pytest.LogCaptureFixture) -> None:
    """AC-02: los bytes de una imagen de inferencia no se registran."""
    # Act
    _client().post(
        "/predict",
        files={"file": ("sensible.png", b"IMAGEN-SUPER-SECRETA", "image/png")},
    )

    # Assert
    assert "IMAGEN-SUPER-SECRETA" not in caplog.text


def test_request_id_header_is_propagated(caplog: pytest.LogCaptureFixture) -> None:
    """AC-03: el X-Request-ID entrante se devuelve en la respuesta."""
    # Act
    response = _client().get("/health", headers={"X-Request-ID": "req-abc-123"})

    # Assert
    assert response.headers["x-request-id"] == "req-abc-123"
    assert _entries(caplog)[0]["request_id"] == "req-abc-123"


def test_generated_request_id_is_returned(caplog: pytest.LogCaptureFixture) -> None:
    """AC-03: sin cabecera entrante se genera y devuelve un UUID."""
    # Act
    response = _client().get("/health")

    # Assert
    request_id = response.headers["x-request-id"]
    assert uuid.UUID(request_id)
    assert _entries(caplog)[0]["request_id"] == request_id


def test_empty_request_id_header_generates_new_identifier(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """AC-03: una cabecera vacía se reemplaza por un identificador nuevo."""
    # Act
    response = _client().get("/health", headers={"X-Request-ID": ""})

    # Assert
    request_id = response.headers["x-request-id"]
    assert request_id != ""
    assert uuid.UUID(request_id)
    assert _entries(caplog)[0]["request_id"] == request_id
