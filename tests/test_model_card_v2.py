"""Pruebas estructurales de la Model Card v2 (HU-027)."""

from __future__ import annotations

from pathlib import Path

CARD = Path(__file__).resolve().parents[1] / "docs" / "model-card.md"


def _text() -> str:
    return CARD.read_text(encoding="utf-8")


def test_model_card_selects_yolo26n_and_adr() -> None:
    """AC-01: la ficha declara YOLO26n y enlaza el ADR 0009."""

    # Act
    text = _text()

    # Assert
    assert "YOLO26n" in text
    assert "yolo26n-clean" in text
    assert "adr/0009-modelo-productivo.md" in text


def test_model_card_includes_yolo11s_comparison() -> None:
    """AC-01: la comparación de calidad frente a YOLO11s está presente."""

    # Act
    text = _text()

    # Assert
    assert "YOLO11s" in text
    assert "0.614" in text
    assert "0.516" in text
    assert "mAP50-95" in text


def test_model_card_documents_safety_shoe_bias() -> None:
    """AC-02: se declara el sesgo de safety_shoe."""

    # Act
    text = _text()

    # Assert
    assert "safety_shoe" in text
    assert "0.852" in text
    assert "menos soporte" in text


def test_model_card_documents_gloves_bias() -> None:
    """AC-02: se declara la debilidad de Gloves."""

    # Act
    text = _text()

    # Assert
    assert "Gloves" in text
    assert "0.553" in text
    assert "débil" in text


def test_model_card_declares_non_compliance_use() -> None:
    """AC-02: la ficha no se presenta como certificación de cumplimiento."""

    # Act
    text = _text()

    # Assert
    assert "Uso no previsto" in text
    assert "no certifican cumplimiento" in text
    assert "presencia de EPP" in text


def test_model_card_links_manifest_and_evaluation() -> None:
    """AC-03: enlaza models.lock, evaluación y errores."""

    # Act
    text = _text()

    # Assert
    assert "models.lock" in text
    assert "evaluation/YOLO26.md" in text
    assert "evaluation/errores.md" in text


def test_model_card_links_mlflow() -> None:
    """AC-03: enlaza MLflow y la comparación de runs."""

    # Act
    text = _text()

    # Assert
    assert "operacion/mlflow.md" in text
    assert "evaluation/mlflow-comparacion.md" in text


def test_model_card_declares_license_and_six_classes() -> None:
    """AC-01/AC-02: licencia y catálogo de seis clases."""

    # Act
    text = _text()

    # Assert
    assert "AGPL-3.0-only" in text
    for class_name in ("Gloves", "Vest", "goggles", "helmet", "mask", "safety_shoe"):
        assert class_name in text
