"""Pruebas del registro champion/challenger (HU-098, issue #154)."""

from __future__ import annotations

import pytest

from ppe_detection.tracking.registry import (
    CHAMPION,
    CHAMPION_SHA256,
    CHAMPION_VERSION,
    ModelAlias,
    RegistryError,
    build_aliases,
    plan_promotion,
    validate_aliases,
)

CHALLENGER_SHA = "AB" * 32


def _aliases() -> tuple[ModelAlias, ModelAlias]:
    return build_aliases(challenger_version="yolo26s-clean", challenger_sha256=CHALLENGER_SHA)


def test_champion_points_to_adr_model() -> None:
    """AC-01: champion apunta al modelo del ADR 0009."""
    # Act
    champion, _ = _aliases()

    # Assert
    assert champion.alias == CHAMPION
    assert champion.version == CHAMPION_VERSION


def test_champion_sha_matches_adr() -> None:
    """AC-01: el SHA del champion es el del ADR 0009."""
    # Act
    champion, _ = _aliases()

    # Assert
    assert champion.sha256 == CHAMPION_SHA256


def test_challenger_points_to_candidate() -> None:
    """AC-02: challenger apunta al candidato alternativo."""
    # Act
    _, challenger = _aliases()

    # Assert
    assert challenger.version == "yolo26s-clean"
    assert challenger.sha256 == CHALLENGER_SHA


def test_build_aliases_returns_two() -> None:
    """AC-02: el registro tiene exactamente dos alias."""
    # Act
    aliases = _aliases()

    # Assert
    assert [alias.alias for alias in aliases] == ["champion", "challenger"]


def test_validate_rejects_unknown_alias() -> None:
    """AC-02: un alias desconocido no es válido."""
    # Arrange
    alias = ModelAlias("produccion", "v1", "AB" * 32)

    # Act
    errors = validate_aliases([alias])

    # Assert
    assert any("desconocido" in error for error in errors)


def test_validate_rejects_invalid_sha() -> None:
    """AC-02: un SHA256 inválido no es válido."""
    # Arrange
    alias = ModelAlias("challenger", "v1", "abc")

    # Act
    errors = validate_aliases([alias])

    # Assert
    assert any("SHA256" in error for error in errors)


def test_plan_promotion_moves_challenger() -> None:
    """AC-03: la promoción convierte al challenger en champion."""
    # Arrange
    champion, challenger = _aliases()

    # Act
    plan = plan_promotion(champion, challenger)

    # Assert
    assert plan["to"] == challenger.version
    assert plan["from"] == champion.version


def test_plan_promotion_keeps_rollback() -> None:
    """AC-03: el campeón anterior queda como rollback."""
    # Arrange
    champion, challenger = _aliases()

    # Act
    plan = plan_promotion(champion, challenger)

    # Assert
    assert plan["rollback"] == champion.version


def test_build_aliases_rejects_invalid_candidate() -> None:
    """AC-02: un candidato sin SHA válido falla al construir."""
    # Act / Assert
    with pytest.raises(RegistryError, match="SHA256"):
        build_aliases(challenger_version="v1", challenger_sha256="abc")
