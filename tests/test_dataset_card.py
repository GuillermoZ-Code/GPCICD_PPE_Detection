"""Pruebas de la Dataset Card y la atribución CC-BY-4.0 (HU-028)."""

from __future__ import annotations

from pathlib import Path

CARD = Path(__file__).resolve().parents[1] / "docs" / "dataset" / "README.md"


def _text() -> str:
    return CARD.read_text(encoding="utf-8")


def test_dataset_card_has_source_license_and_counts() -> None:
    """AC-01: la ficha declara origen, licencia, particiones y limpieza."""

    # Act
    text = _text()

    # Assert
    assert "51ddhesh/PPE_Detection" in text
    assert "CC-BY-4.0" in text
    assert "10.941" in text
    assert "7.658" in text
    assert "2.188" in text
    assert "1.095" in text
    assert "1.137" in text
    assert "2.647" in text


def test_dataset_card_declares_missing_origin_and_consent() -> None:
    """AC-02: la ficha declara los riesgos de fuente y consentimiento."""

    # Act
    text = _text()

    # Assert
    assert "Fuente original no declarada" in text
    assert "Consentimiento de rostros no documentado" in text
    assert "no se declara consentimiento" in text
    assert "person" in text and "no-EPP" in text


def test_dataset_card_has_reusable_attribution() -> None:
    """AC-03: la atribución se puede copiar y contiene licencia y enlace."""

    # Act
    text = _text()

    # Assert
    assert "Atribución reutilizable" in text
    assert "creativecommons.org/licenses/by/4.0" in text
    assert "Modificaciones del proyecto" in text
    assert "README, la SPA o una publicación" in text


def test_dataset_card_links_to_evidence() -> None:
    """AC-01: la ficha enlaza EDA, ADR y Model Card."""

    # Act
    text = _text()

    # Assert
    assert "[EDA](EDA.md)" in text
    assert "../adr/0002-dataset.md" in text
    assert "../model-card.md" in text
