"""Pruebas de liveness y readiness de la API (HU-045, issue #101)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import FakeDetector
from ppe_detection.detector_config import ModelIdentity

SHA256 = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"


def _identity() -> ModelIdentity:
    return ModelIdentity(
        version="yolo11s-clean",
        sha256=SHA256,
        artifact="artifacts/drive/yolo11s_clean/weights/best.pt",
    )


def test_live_responds_without_model(monkeypatch) -> None:
    """AC-01: liveness responde aunque no exista detector cargado."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    application = create_app()
    client = TestClient(application)

    # Act
    response = client.get("/health/live")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert application.state.detector is None


def test_live_does_not_build_detector(monkeypatch) -> None:
    """AC-01: liveness no dispara la construcción perezosa del modelo."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    application = create_app()

    # Act
    with TestClient(application) as client:
        response = client.get("/health/live")

    # Assert
    assert response.status_code == 200
    assert application.state.detector is None


def test_ready_returns_503_without_detector(monkeypatch) -> None:
    """AC-01: readiness devuelve 503 hasta que el modelo esté cargado."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    client = TestClient(create_app())

    # Act
    response = client.get("/health/ready")

    # Assert
    assert response.status_code == 503
    assert response.json()["status"] == "not_ready"
    assert response.json()["model_loaded"] is False


def test_ready_returns_200_with_detector() -> None:
    """AC-01: readiness pasa a 200 cuando el detector ya está cargado."""
    # Arrange
    client = TestClient(create_app(detector=FakeDetector([]), model_identity=_identity()))

    # Act
    response = client.get("/health/ready")

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["model_loaded"] is True


def test_ready_reports_model_version_and_sha256() -> None:
    """AC-02: readiness publica versión y SHA256 verificable del modelo."""
    # Arrange
    client = TestClient(create_app(detector=FakeDetector([]), model_identity=_identity()))

    # Act
    body = client.get("/health/ready").json()

    # Assert
    assert body["model_version"] == "yolo11s-clean"
    assert body["model_sha256"] == SHA256
    assert body["model_reference"] == f"sha256:{SHA256}"


def test_ready_reports_unknown_identity_when_not_configured(tmp_path, monkeypatch) -> None:
    """AC-02: sin manifiesto, readiness no inventa versión ni hash."""
    # Arrange
    monkeypatch.setattr(
        "ppe_detection.detector_config.DEFAULT_MANIFEST_PATH",
        tmp_path / "missing-models.lock",
    )
    for name in ("PPE_MODEL_MANIFEST", "PPE_MODEL_VERSION", "PPE_MODEL_SHA256"):
        monkeypatch.delenv(name, raising=False)
    client = TestClient(create_app(detector=FakeDetector([])))

    # Act
    body = client.get("/health/ready").json()

    # Assert
    assert body["model_version"] == "unknown"
    assert body["model_sha256"] is None
    assert body["model_reference"] == "version:unknown"


def test_live_and_ready_are_documented_in_openapi() -> None:
    """AC-03: OpenAPI expone los dos contratos de salud."""
    # Arrange
    client = TestClient(create_app(detector=FakeDetector([])))

    # Act
    schema = client.get("/openapi.json").json()

    # Assert
    assert "/health/live" in schema["paths"]
    assert "/health/ready" in schema["paths"]
    assert "get" in schema["paths"]["/health/live"]
    assert "get" in schema["paths"]["/health/ready"]


def test_openapi_documents_ready_503_contract() -> None:
    """AC-03: el contrato OpenAPI documenta el 503 de readiness."""
    # Arrange
    client = TestClient(create_app(detector=FakeDetector([])))

    # Act
    schema = client.get("/openapi.json").json()
    responses = schema["paths"]["/health/ready"]["get"]["responses"]

    # Assert
    assert "200" in responses
    assert "503" in responses
    for code in ("200", "503"):
        response_schema = responses[code]["content"]["application/json"]["schema"]
        assert response_schema["$ref"] == "#/components/schemas/ReadyResponse"
