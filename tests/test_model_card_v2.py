"""HU-027 — Model Card v2 (AC-01, AC-02 y AC-03).

Pruebas estáticas: leen `docs/model-card.md` sin red ni pesos. El contenido numérico
vive en el informe de evaluación; aquí se comprueba que la tarjeta lo declare y lo
enlace.
"""

from __future__ import annotations

from pathlib import Path

MODEL_CARD = Path("docs/model-card.md")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-027 · AC-01


def test_card_declares_selected_and_deployed_models() -> None:
    """AC-01: distingue el modelo seleccionado del que está desplegado."""
    # Arrange
    card = _read(MODEL_CARD)

    # Assert
    assert "yolo26n-clean" in card
    assert "YOLO26n" in card
    assert "YOLO11s" in card
    assert "seleccionado" in card.lower()


def test_card_compares_yolo11s_and_yolo26() -> None:
    """AC-01: la comparación existe con las métricas del test completo."""
    # Arrange
    card = _read(MODEL_CARD)

    # Assert
    assert "mAP50-95" in card
    assert "0.516" in card  # YOLO11s
    assert "0.614" in card  # YOLO26n


def test_card_cites_the_productive_model_adr() -> None:
    """AC-01: la decisión remite al ADR 0009."""
    # Arrange
    card = _read(MODEL_CARD)

    # Assert
    assert "0009-modelo-productivo" in card


# --------------------------------------------------------------- HU-027 · AC-02


def test_card_documents_the_weak_classes() -> None:
    """AC-02: `safety_shoe` y `Gloves` tienen su propio análisis."""
    # Arrange
    card = _read(MODEL_CARD)

    # Assert
    assert "safety_shoe" in card
    assert "Gloves" in card
    assert "sesgo" in card.lower()


def test_card_states_the_intended_use_is_limited() -> None:
    """AC-02: el sistema reporta EPP; no certifica cumplimiento."""
    # Arrange
    card = _read(MODEL_CARD)

    # Assert
    assert "Limitaciones" in card
    assert "no" in card.lower()
    assert "cumplimiento" in card.lower()


# --------------------------------------------------------------- HU-027 · AC-03


def test_card_links_the_model_manifest() -> None:
    """AC-03: el artefacto se identifica por `models.lock` y su SHA256."""
    # Arrange
    card = _read(MODEL_CARD)

    # Assert
    assert "models.lock" in card
    assert "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9" in card


def test_card_links_mlflow_and_the_evaluation_report() -> None:
    """AC-03: la evidencia vive en MLflow y en el informe de evaluación."""
    # Arrange
    card = _read(MODEL_CARD)

    # Assert
    assert "MLflow" in card
    assert "evaluation/YOLO26.md" in card
