"""Pruebas estructurales de la guía de reproducibilidad (HU-040)."""

from __future__ import annotations

from pathlib import Path

GUIDE = Path(__file__).resolve().parents[1] / "docs" / "evaluation" / "reproducibilidad.md"


def _text() -> str:
    return GUIDE.read_text(encoding="utf-8")


def test_guide_has_required_sections() -> None:
    """AC-03: la guía contiene las secciones estructurales obligatorias."""

    # Act
    text = _text()

    # Assert
    for section in (
        "## 1. Alcance",
        "## 2. Entorno y hardware",
        "## 3. Datos y versiones",
        "## 4. Pasos con `uv`",
        "## 5. Tiempos de referencia",
        "## 6. MLflow",
        "## 7. Paquete y artefacto del modelo",
        "## 8. Verificación",
        "## 9. Límites",
    ):
        assert section in text


def test_guide_documents_uv_versions_seed_hardware_and_time() -> None:
    """AC-01: la guía registra uv, versiones, semilla, hardware y duración."""

    # Act
    text = _text()

    # Assert
    assert "uv sync --all-extras" in text
    assert "Python" in text and "3.13.16" in text
    assert "Ultralytics" in text and "8.4.216" in text
    assert "torch" in text and "2.15.0" in text
    assert "Semilla" in text and "42" in text
    assert "Intel Core i5-1235U" in text
    assert "85 min" in text


def test_guide_links_mlflow_and_model_package() -> None:
    """AC-02: la guía enlaza runs de MLflow y el artefacto del modelo."""

    # Act
    text = _text()

    # Assert
    assert "mlflow-comparacion.md" in text
    assert "../operacion/mlflow.md" in text
    assert "models.lock" in text
    assert "best.pt" in text
    assert "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9" in text


def test_guide_does_not_expose_secrets_or_user_paths() -> None:
    """AC-03: la guía no contiene secretos ni rutas personales."""

    # Act
    text = _text()

    # Assert
    assert "GITLAB_TOKEN" not in text
    assert "C:\\Users\\" not in text
    assert "/content/drive" not in text
    assert "password" not in text.lower()
