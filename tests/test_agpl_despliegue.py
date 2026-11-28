"""Pruebas del cumplimiento AGPL y CC-BY en el despliegue (HU-060, #116)."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from ppe_detection.api import create_app

ROOT = Path(__file__).resolve().parents[1]
APP_TSX = ROOT / "frontend" / "src" / "App.tsx"
RUNBOOK = ROOT / "docs" / "operacion" / "licencias-despliegue.md"
DEFAULT_SOURCE_URL = "https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection"
DATASET_URL = "https://huggingface.co/datasets/51ddhesh/PPE_Detection"


def test_health_publica_url_del_codigo_ac_01(monkeypatch) -> None:
    """AC-01: `/health` publica la URL pública del código (AGPL)."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    monkeypatch.delenv("PPE_SOURCE_URL", raising=False)

    # Act
    body = TestClient(create_app()).get("/health").json()

    # Assert
    assert body["source_url"] == DEFAULT_SOURCE_URL

    # Act: la URL puede sustituirse en el despliegue
    monkeypatch.setenv("PPE_SOURCE_URL", "https://example.org/ppe-fork")

    # Assert
    assert TestClient(create_app()).get("/health").json()["source_url"] == (
        "https://example.org/ppe-fork"
    )


def test_health_publica_commit_desplegado_ac_01(monkeypatch) -> None:
    """AC-01: `/health` publica el commit desplegado, o `null` si no se declaró."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    monkeypatch.delenv("PPE_DEPLOY_COMMIT", raising=False)

    # Act
    body = TestClient(create_app()).get("/health").json()

    # Assert
    assert body["commit"] is None

    # Act: el despliegue inyecta el SHA de la imagen publicada
    monkeypatch.setenv("PPE_DEPLOY_COMMIT", "  abc1234  ")

    # Assert
    assert TestClient(create_app()).get("/health").json()["commit"] == "abc1234"


def test_ui_muestra_atribucion_cc_by_ac_02() -> None:
    """AC-02: la SPA atribuye el dataset CC-BY y el runbook lo documenta."""
    # Arrange / Act
    ui = APP_TSX.read_text(encoding="utf-8")
    runbook = RUNBOOK.read_text(encoding="utf-8")

    # Assert
    assert DATASET_URL in ui
    assert "CC-BY-4.0" in ui
    assert DATASET_URL in runbook
    assert "CC-BY-4.0" in runbook


def test_openapi_y_respuesta_incluyen_campos_ac_03(monkeypatch) -> None:
    """AC-03: el schema de `/health` documenta `source_url` y `commit`."""
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    client = TestClient(create_app())

    # Act
    schema = client.get("/openapi.json").json()
    body = client.get("/health").json()

    # Assert
    properties = schema["components"]["schemas"]["HealthResponse"]["properties"]
    assert "source_url" in properties
    assert "commit" in properties
    assert "source_url" in body
    assert "commit" in body
    assert "source_url" not in schema["components"]["schemas"]["ReadyResponse"]["properties"]
