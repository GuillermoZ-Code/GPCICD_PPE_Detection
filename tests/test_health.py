"""Pruebas del healthcheck de la API (AC-015.1, rúbrica M3)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import Detection, FakeDetector
from ppe_detection.detector_config import ModelIdentity

SHA256 = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"


def _detection() -> Detection:
    return Detection(
        class_id=3,
        class_name="helmet",
        confidence=0.9,
        bbox=(1.0, 2.0, 5.0, 6.0),
        image_width=8,
        image_height=6,
    )


def _identity() -> ModelIdentity:
    return ModelIdentity(
        version="yolo11s-clean",
        sha256=SHA256,
        artifact="artifacts/drive/yolo11s_clean/weights/best.pt",
    )


def test_health_reports_ok_when_detector_is_loaded() -> None:
    """AC-015.1: el healthcheck responde el estado del componente."""
    # Arrange
    client = TestClient(
        create_app(
            detector=FakeDetector([_detection()]),
            model_identity=_identity(),
        )
    )

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True
    assert body["api_version"] == "0.1.0"


def test_health_reports_degraded_without_detector(monkeypatch) -> None:
    """AC-015.1: sin modelo cargado el estado es `degraded`, no un error."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    client = TestClient(create_app())

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "degraded"
    assert response.json()["model_loaded"] is False


def test_health_exposes_the_published_model_identity() -> None:
    """AC-015.1: el contrato publica la identidad verificable del modelo."""
    # Arrange
    client = TestClient(create_app(detector=FakeDetector([]), model_identity=_identity()))

    # Act
    body = client.get("/health").json()

    # Assert
    assert body["model_version"] == "yolo11s-clean"
    assert body["model_sha256"] == SHA256
    assert body["model_reference"] == f"sha256:{SHA256}"
    assert body["model_artifact"].endswith("best.pt")


def test_health_default_identity_is_explicitly_unknown(monkeypatch) -> None:
    """AC-015.1: sin configuración la referencia no inventa un artefacto."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    monkeypatch.delenv("PPE_MODEL_VERSION", raising=False)
    monkeypatch.delenv("PPE_MODEL_SHA256", raising=False)
    client = TestClient(create_app(detector=FakeDetector([])))

    # Act
    body = client.get("/health").json()

    # Assert
    assert body["model_version"] == "unknown"
    assert body["model_reference"] == "version:unknown"
    assert body["model_sha256"] is None
    assert body["model_artifact"] is None


def test_health_does_not_build_the_detector(monkeypatch) -> None:
    """AC-015.1: el chequeo es barato y no carga el modelo por su cuenta."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    application = create_app()

    # Act
    with TestClient(application) as client:
        client.get("/health")
        loaded_after = application.state.detector

    # Assert
    assert loaded_after is None


def test_health_is_documented_in_openapi() -> None:
    """AC-006.3: el contrato OpenAPI documenta también el healthcheck."""
    # Arrange
    client = TestClient(create_app(detector=FakeDetector([])))

    # Act
    schema = client.get("/openapi.json").json()

    # Assert
    assert "/health" in schema["paths"]
    assert "get" in schema["paths"]["/health"]
