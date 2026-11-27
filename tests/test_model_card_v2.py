"""HU-027 — Model Card v2 (AC-01, AC-02 y AC-03).

Pruebas estáticas: leen `docs/model-card.md` sin red ni pesos. El contenido numérico
vive en el informe de evaluación; aquí se comprueba que la tarjeta lo declare y lo
enlace.
"""

from __future__ import annotations

from pathlib import Path

CARD = Path(__file__).resolve().parents[1] / "docs" / "model-card.md"


def _text() -> str:
    """Devuelve el contenido de la Model Card."""
    return CARD.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-027 · AC-01


def test_model_card_selects_yolo26n_and_links_the_adr() -> None:
    """AC-01: la ficha declara YOLO26n y enlaza el ADR 0009."""
    # Arrange
    text = _text()

    # Assert
    assert "YOLO26n" in text
    assert "yolo26n-clean" in text
    assert "adr/0009-modelo-productivo.md" in text


def test_model_card_distinguishes_selected_from_deployed() -> None:
    """AC-01: el modelo seleccionado y el desplegado no se confunden."""
    # Arrange
    text = _text()

    # Assert
    assert "YOLO11s" in text
    assert "seleccionado" in text.lower()


def test_model_card_compares_with_the_full_test_metrics() -> None:
    """AC-01: la comparación usa mAP del test completo."""
    # Arrange
    text = _text()

    # Assert
    assert "mAP50-95" in text
    assert "0.516" in text
    assert "0.614" in text


# --------------------------------------------------------------- HU-027 · AC-02


def test_model_card_documents_the_weak_classes() -> None:
    """AC-02: `safety_shoe` y `Gloves` tienen análisis propio."""
    # Arrange
    text = _text()

    # Assert
    assert "safety_shoe" in text
    assert "Gloves" in text
    assert "sesgo" in text.lower()


def test_model_card_states_the_limits_of_the_intended_use() -> None:
    """AC-02: el sistema reporta EPP; no certifica cumplimiento."""
    # Arrange
    text = _text()

    # Assert
    assert "Limitaciones" in text
    assert "cumplimiento" in text.lower()


# --------------------------------------------------------------- HU-027 · AC-03


def test_model_card_links_the_manifest_and_checksum() -> None:
    """AC-03: el artefacto se identifica por `models.lock` y su SHA256."""
    # Arrange
    text = _text()

    # Assert
    assert "models.lock" in text
    assert "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9" in text


def test_model_card_links_mlflow_and_the_evaluation_report() -> None:
    """AC-03: la evidencia vive en MLflow y en el informe de evaluación."""
    # Arrange
    text = _text()

    # Assert
    assert "MLflow" in text
    assert "evaluation/YOLO26.md" in text
