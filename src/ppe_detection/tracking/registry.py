"""Alias champion/challenger del Model Registry (HU-098).

Mantiene la lógica pura de los alias del modelo productivo: `champion` apunta al modelo
del ADR 0009 (`yolo26n-clean`) y `challenger` al candidato alternativo. La promoción
intercambia los alias y deja el campeón anterior como rollback.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass

CHAMPION = "champion"
CHALLENGER = "challenger"
CHAMPION_VERSION = "yolo26n-clean"
CHAMPION_SHA256 = "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9"
ROLLBACK_VERSION = "yolo11s-clean"
ROLLBACK_SHA256 = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"

SHA256 = re.compile(r"^[0-9A-Fa-f]{64}$")


class RegistryError(ValueError):
    """Alias o promoción inválida."""


@dataclass(frozen=True, slots=True)
class ModelAlias:
    """Alias del registro con su versión y artefacto."""

    alias: str
    version: str
    sha256: str


def build_aliases(
    *,
    champion_version: str = CHAMPION_VERSION,
    champion_sha256: str = CHAMPION_SHA256,
    challenger_version: str,
    challenger_sha256: str,
) -> tuple[ModelAlias, ModelAlias]:
    """Construye los alias champion y challenger y valida sus campos."""
    aliases = (
        ModelAlias(CHAMPION, champion_version, champion_sha256),
        ModelAlias(CHALLENGER, challenger_version, challenger_sha256),
    )
    errors = validate_aliases(aliases)
    if errors:
        raise RegistryError("; ".join(errors))
    return aliases


def validate_aliases(aliases: Sequence[ModelAlias]) -> list[str]:
    """Errores de los alias: nombres, versiones, duplicados y SHA256."""
    errors: list[str] = []
    seen: set[str] = set()
    for alias in aliases:
        if alias.alias not in {CHAMPION, CHALLENGER}:
            errors.append(f"alias desconocido: {alias.alias}")
        if alias.alias in seen:
            errors.append(f"alias duplicado: {alias.alias}")
        seen.add(alias.alias)
        if not alias.version.strip():
            errors.append(f"{alias.alias} sin version")
        if not SHA256.fullmatch(alias.sha256):
            errors.append(f"{alias.alias} con SHA256 invalido")
    return errors


def plan_promotion(champion: ModelAlias, challenger: ModelAlias) -> dict[str, str]:
    """Promociona el challenger y deja el campeón anterior como rollback."""
    return {
        "alias": CHAMPION,
        "from": champion.version,
        "to": challenger.version,
        "rollback": champion.version,
    }
