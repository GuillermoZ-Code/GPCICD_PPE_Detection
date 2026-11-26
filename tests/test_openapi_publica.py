"""Pruebas de la documentación pública de la API MaaS (HU-052, #108)."""

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from ppe_detection.api import create_app

ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "maas" / "README.md"


def _document() -> dict:
    """Arrange: documento OpenAPI de una aplicación sin modelo."""
    return TestClient(create_app()).get("/openapi.json").json()


def _conf_schema(document: dict) -> dict:
    """Extrae la propiedad `conf` del cuerpo multipart de `/predict`."""
    body = document["components"]["schemas"]["Body_predict_predict_post"]
    return body["properties"]["conf"]


def test_predict_summary_y_descripcion_ac_01() -> None:
    """AC-01: `/predict` publica resumen y descripción útiles al consumidor."""
    # Arrange / Act
    operation = _document()["paths"]["/predict"]["post"]

    # Assert
    assert operation["summary"].strip()
    assert operation["description"].strip()
    assert "imagen" in operation["description"].lower()
    assert "EPP" in operation["description"]


def test_predict_codigos_de_error_ac_01() -> None:
    """AC-01: `/predict` documenta 200, 400 y 503 con su significado."""
    # Arrange / Act
    responses = _document()["paths"]["/predict"]["post"]["responses"]

    # Assert
    assert {"200", "400", "503"} <= set(responses)
    assert "imagen" in responses["400"]["description"].lower()
    assert "modelo" in responses["503"]["description"].lower()


def test_health_summary_y_descripcion_ac_01() -> None:
    """AC-01: `/health` publica resumen y descripción del healthcheck."""
    # Arrange / Act
    operation = _document()["paths"]["/health"]["get"]

    # Assert
    assert operation["summary"].strip()
    assert operation["description"].strip()
    assert "modelo" in operation["description"].lower()


def test_conf_documented_limits_ac_01() -> None:
    """AC-01: `conf` conserva sus límites y añade descripción y ejemplo."""
    # Arrange / Act
    conf = _conf_schema(_document())

    # Assert: el contrato existente no se debilita
    numerico = conf["anyOf"][0]
    assert numerico["minimum"] == 0.01
    assert numerico["maximum"] == 0.99
    # Assert: documentación nueva
    assert conf["description"].strip()
    assert 0.25 in conf["examples"]


def test_guia_incluye_url_y_ejemplos_ac_02() -> None:
    """AC-02: la guía pública incluye URL configurable, curl y Python."""
    # Arrange / Act
    guia = GUIDE.read_text(encoding="utf-8")

    # Assert
    assert "PPE_MAAS_URL" in guia
    assert "<URL_PUBLICA>" in guia
    assert "curl" in guia
    assert "python" in guia.lower()
    assert "/predict" in guia
    assert "/health" in guia


def test_guia_documenta_limites_ac_02() -> None:
    """AC-02: la guía declara formatos, tamaño, umbrales y errores reales."""
    # Arrange / Act
    guia = GUIDE.read_text(encoding="utf-8")

    # Assert
    for dato in ("JPEG", "PNG", "10 MB", "0.01", "0.99", "400", "503"):
        assert dato in guia, f"falta documentar {dato}"
    assert "HU-051" in guia
    assert "HU-053" in guia
    assert "HU-054" in guia


def test_openapi_ejemplo_de_respuesta_ac_03() -> None:
    """AC-03: la respuesta 200 de `/predict` incluye un ejemplo completo."""
    # Arrange / Act
    respuesta = _document()["paths"]["/predict"]["post"]["responses"]["200"]
    ejemplo = respuesta["content"]["application/json"]["example"]

    # Assert
    assert "detections" in ejemplo
    assert "model_version" in ejemplo
    assert "elapsed_ms" in ejemplo
    assert isinstance(ejemplo["detections"], list)


def test_info_y_swagger_ac_03() -> None:
    """AC-03: la descripción global y `/docs` presentan la API como MaaS."""
    # Arrange
    client = TestClient(create_app())

    # Act
    info = client.get("/openapi.json").json()["info"]
    docs = client.get("/docs")

    # Assert
    assert "MaaS" in info["description"]
    assert "EPP" in info["description"]
    assert docs.status_code == 200
    assert "swagger-ui" in docs.text.lower()
