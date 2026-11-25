"""Pruebas de configuración por entorno de la API (HU-044, issue #100)."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from ppe_detection.api import create_app
from ppe_detection.api.settings import SettingsError, load_settings, validate_environment

ROOT = Path(__file__).resolve().parents[1]
SHA256 = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"


def _valid_environment() -> dict[str, str]:
    return {
        "PPE_MODEL_PATH": "/models/best.pt",
        "PPE_MODEL_SHA256": SHA256,
        "PPE_MODEL_FORMAT": "onnx",
        "PPE_CONF": "0.4",
        "PPE_IOU": "0.6",
        "PPE_IMGSZ": "320",
        "PPE_DEVICE": "cpu",
        "PPE_CORS_ORIGINS": "http://localhost:5173,https://app.example.com",
        "PPE_API_HOST": "127.0.0.1",
        "PPE_API_PORT": "8001",
        "PPE_GRPC_HOST": "127.0.0.1",
        "PPE_GRPC_PORT": "9001",
        "PPE_GRPC_TARGET": "localhost:9001",
        "PPE_API_KEY": "clave-de-prueba",
    }


def test_env_example_documents_every_ppe_variable() -> None:
    """AC-01: `.env.example` documenta todas las variables PPE_* del código."""
    # Arrange
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "src" / "ppe_detection").rglob("*.py")
    )
    used = set(re.findall(r"\bPPE_[A-Z0-9_]+\b", source))
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    documented = set(re.findall(r"^\s*(?:export\s+)?(PPE_[A-Z0-9_]+)=", example, re.M))

    # Act / Assert
    assert used, "no se encontraron variables PPE_* en el código"
    assert used <= documented, f"Variables sin documentar: {sorted(used - documented)}"


def test_valid_environment_is_accepted() -> None:
    """AC-02: los valores válidos se convierten a sus tipos y límites."""
    # Act
    settings = load_settings(_valid_environment())

    # Assert
    assert settings.conf == 0.4
    assert settings.iou == 0.6
    assert settings.imgsz == 320
    assert settings.api_port == 8001
    assert settings.cors_origins == ("http://localhost:5173", "https://app.example.com")
    assert settings.model_sha256 == SHA256
    assert settings.model_format == "onnx"


def test_invalid_conf_reports_variable_and_reason() -> None:
    """AC-02: un umbral no numérico nombra la variable y explica el error."""
    # Act
    errors = validate_environment({"PPE_CONF": "abc"})

    # Assert
    message = " ".join(errors)
    assert "PPE_CONF" in message
    assert "número" in message


def test_invalid_port_reports_range() -> None:
    """AC-02: un puerto fuera de rango indica el límite válido."""
    # Act
    errors = validate_environment({"PPE_API_PORT": "70000"})

    # Assert
    message = " ".join(errors)
    assert "PPE_API_PORT" in message
    assert "65535" in message


def test_invalid_sha256_reports_length() -> None:
    """AC-02: un SHA256 incompleto explica los 64 caracteres requeridos."""
    # Act
    errors = validate_environment({"PPE_MODEL_SHA256": "abc"})

    # Assert
    message = " ".join(errors)
    assert "PPE_MODEL_SHA256" in message
    assert "64" in message


def test_invalid_cors_origin_is_rejected() -> None:
    """AC-02: un origen CORS sin esquema http/https se rechaza."""
    # Act
    errors = validate_environment({"PPE_CORS_ORIGINS": "ftp://ejemplo"})

    # Assert
    message = " ".join(errors)
    assert "PPE_CORS_ORIGINS" in message
    assert "http" in message.lower()


def test_create_app_fails_early_on_invalid_environment(monkeypatch) -> None:
    """AC-02: la API valida la configuración antes de registrar rutas."""
    # Arrange
    monkeypatch.setenv("PPE_CONF", "abc")

    # Act / Assert
    with pytest.raises(SettingsError, match="PPE_CONF"):
        create_app()


def test_cli_fails_without_leaking_secret() -> None:
    """AC-03: el CLI falla con código 1 y nunca imprime el valor secreto."""
    # Arrange
    env = {key: value for key, value in os.environ.items() if not key.startswith("PPE_")}
    env["PPE_CONF"] = "abc"
    env["PPE_API_KEY"] = "super-secreto-no-imprimir"

    # Act
    process = subprocess.run(
        [sys.executable, "-m", "ppe_detection.api.settings"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    # Assert
    assert process.returncode == 1
    assert "PPE_CONF" in process.stderr
    assert "super-secreto-no-imprimir" not in process.stdout + process.stderr
    assert process.stdout == ""
