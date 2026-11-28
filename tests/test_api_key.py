"""Pruebas de la clave de API opcional de `/predict` (HU-051, #107)."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from ppe_detection.api import create_app, security
from ppe_detection.contracts import FakeDetector

SECRET = "clave-secreta-051"


def _png_bytes() -> bytes:
    """PNG RGB determinista para las peticiones de prueba."""
    rgb = np.zeros((8, 6, 3), dtype=np.uint8)
    rgb[0, 0] = (255, 0, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".png", bgr)
    assert ok
    return buffer.tobytes()


def _client(monkeypatch: pytest.MonkeyPatch, env: Mapping[str, str] | None = None) -> TestClient:
    """Arrange: aplicación con un detector doble y entorno de claves controlado."""
    for name in ("PPE_API_KEYS", "PPE_API_KEY"):
        monkeypatch.delenv(name, raising=False)
    for name, value in (env or {}).items():
        monkeypatch.setenv(name, value)
    return TestClient(create_app(detector=FakeDetector(), model_version="test-1.0"))


def _post(client: TestClient, key: str | None = None) -> Any:
    headers: dict[str, str] = {}
    if key is not None:
        headers["X-API-Key"] = key
    return client.post(
        "/predict",
        files={"file": ("image.png", _png_bytes(), "image/png")},
        headers=headers,
    )


def test_sin_cabecera_devuelve_401_ac_01(monkeypatch) -> None:
    """AC-01: con claves configuradas, `/predict` exige la cabecera."""
    # Arrange
    client = _client(monkeypatch, {"PPE_API_KEYS": SECRET})

    # Act
    response = _post(client)

    # Assert
    assert response.status_code == 401
    assert "X-API-Key" in response.json()["detail"]
    assert SECRET not in response.json()["detail"]


def test_clave_incorrecta_devuelve_401_ac_01(monkeypatch) -> None:
    """AC-01: una clave no configurada se rechaza con 401."""
    # Arrange
    client = _client(monkeypatch, {"PPE_API_KEYS": SECRET})

    # Act
    response = _post(client, "clave-erronea")

    # Assert
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "ApiKey"


def test_clave_correcta_devuelve_200_ac_01(monkeypatch) -> None:
    """AC-01: la clave configurada permite inferir y no cambia la respuesta."""
    # Arrange
    client = _client(monkeypatch, {"PPE_API_KEYS": SECRET})

    # Act
    response = _post(client, SECRET)

    # Assert
    assert response.status_code == 200
    assert response.json()["model_version"] == "test-1.0"


def test_multiples_claves_separadas_por_coma_ac_01(monkeypatch) -> None:
    """AC-01: se aceptan todas las claves de una lista separada por comas."""
    # Arrange
    client = _client(monkeypatch, {"PPE_API_KEYS": f" primera , {SECRET} , , "})

    # Act / Assert
    assert _post(client, "primera").status_code == 200
    assert _post(client, SECRET).status_code == 200
    assert _post(client, "tercera").status_code == 401


def test_configured_keys_acepta_legacy_y_ignora_vacios_ac_01() -> None:
    """AC-01: se recortan las claves y se conserva `PPE_API_KEY` por compatibilidad."""
    # Arrange / Act
    multiples = security.configured_keys({"PPE_API_KEYS": " a , , b "})
    legacy = security.configured_keys({"PPE_API_KEY": "clave-antigua"})
    sin_claves = security.configured_keys({"PPE_API_KEYS": " , "})

    # Assert
    assert multiples == ("a", "b")
    assert legacy == ("clave-antigua",)
    assert sin_claves == ()


def test_openapi_documenta_401_ac_01(monkeypatch) -> None:
    """AC-01: OpenAPI documenta el 401 sin publicar valores de claves."""
    # Arrange
    client = _client(monkeypatch, {"PPE_API_KEYS": SECRET})

    # Act
    document = client.get("/openapi.json").json()
    respuestas = document["paths"]["/predict"]["post"]["responses"]

    # Assert
    assert "401" in respuestas
    assert "X-API-Key" in respuestas["401"]["description"]
    assert SECRET not in str(document)


def test_sin_variable_no_exige_clave_ac_02(monkeypatch) -> None:
    """AC-02: sin variables de clave, `/predict` sigue público."""
    # Arrange
    client = _client(monkeypatch)

    # Act
    response = _post(client)

    # Assert
    assert response.status_code == 200
    assert response.json()["detections"] == []


def test_variable_vacia_no_exige_clave_ac_02(monkeypatch) -> None:
    """AC-02: una variable vacía equivale a autenticación desactivada."""
    # Arrange
    client = _client(monkeypatch, {"PPE_API_KEYS": ""})

    # Act
    response = _post(client)

    # Assert
    assert response.status_code == 200


def test_solo_predict_esta_protegido_ac_02(monkeypatch) -> None:
    """AC-02: salud y descubrimiento siguen accesibles sin clave."""
    # Arrange
    client = _client(monkeypatch, {"PPE_API_KEYS": SECRET})

    # Act / Assert
    assert client.get("/health").status_code == 200
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").status_code == 200  # detector inyectado
    assert client.get("/openapi.json").status_code == 200
    assert client.get("/docs").status_code == 200


def test_comparacion_no_corta_circuito_ac_03(monkeypatch) -> None:
    """AC-03: se comparan todas las claves, incluso cuando ninguna coincide."""
    # Arrange
    llamadas: list[bool] = []
    original = security.hmac.compare_digest

    def contar(*args: Any, **kwargs: Any) -> bool:
        llamadas.append(True)
        return original(*args, **kwargs)

    monkeypatch.setattr(security.hmac, "compare_digest", contar)

    # Act
    resultado = security.is_authorized("clave-mala", ("a", "b", "c"))

    # Assert
    assert resultado is False
    assert len(llamadas) == 3


def test_clave_correcta_por_digest_ac_03() -> None:
    """AC-03: la comparación usa digests y respeta los casos borde."""
    # Arrange / Act / Assert
    assert security.is_authorized("b", ("a", "b", "c")) is True
    assert security.is_authorized(None, ("a", "b")) is False
    assert security.is_authorized("", ("a", "b")) is False
    assert security.is_authorized("cualquiera", ()) is True


def test_secretos_nunca_se_registran_ac_03(monkeypatch, caplog) -> None:
    """AC-03: ni la clave válida ni la rechazada aparecen en los logs."""
    # Arrange
    caplog.set_level(logging.INFO, logger="ppe_detection.api")
    client = _client(monkeypatch, {"PPE_API_KEYS": SECRET})
    incorrecta = "clave-rechazada-051"

    # Act
    assert _post(client, incorrecta).status_code == 401
    assert _post(client, SECRET).status_code == 200

    # Assert
    assert SECRET not in caplog.text
    assert incorrecta not in caplog.text
    assert "headers" not in caplog.text
