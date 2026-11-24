"""Pruebas del catalogo de etiquetas del repositorio (HU-105, issue #161).

AC-01 epicas y prioridades del M4, AC-02 fuente versionada y AC-03 formato valido.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, cast

import yaml

LABELS_PATH = Path(__file__).resolve().parents[1] / ".github" / "labels.yml"

EPICS = [f"ep-{number:02d}" for number in range(1, 16)]
PRIORITIES = ["must-have", "should-have", "could-have"]
HEX_COLOR = re.compile(r"^[0-9a-fA-F]{6}$")


def _labels() -> list[dict[str, Any]]:
    raw: Any = yaml.safe_load(LABELS_PATH.read_text(encoding="utf-8"))
    assert isinstance(raw, list), "labels.yml debe ser una lista"
    return [cast(dict[str, Any], item) for item in raw]


def _names(labels: list[dict[str, Any]]) -> list[str]:
    return [cast(str, label.get("name")) for label in labels]


def test_labels_is_a_list_of_mappings() -> None:
    """AC-02: el archivo es una lista de mappings versionada."""
    # Arrange
    assert LABELS_PATH.is_file(), f"falta {LABELS_PATH}"

    # Act
    labels = _labels()

    # Assert
    assert labels, "labels.yml no declara etiquetas"
    for label in labels:
        assert isinstance(label, dict), f"etiqueta invalida: {label!r}"


def test_labels_have_unique_name_color_and_description() -> None:
    """AC-03: nombre unico, color de seis hexadecimales y descripcion no vacia."""
    # Arrange
    labels = _labels()

    # Act
    names = _names(labels)

    # Assert
    assert len(names) == len(set(names)), f"etiquetas duplicadas: {names}"
    for label in labels:
        name = label.get("name")
        color = label.get("color")
        description = label.get("description")
        assert isinstance(name, str) and name, f"etiqueta sin nombre: {label!r}"
        assert isinstance(color, str) and HEX_COLOR.match(color), f"color invalido en {name!r}"
        assert isinstance(description, str) and description.strip(), f"{name!r} sin descripcion"


def test_labels_cover_all_epics() -> None:
    """AC-01: el catalogo declara las quince epicas del proyecto."""
    # Arrange
    labels = _labels()

    # Act
    names = set(_names(labels))

    # Assert
    missing = [epic for epic in EPICS if epic not in names]
    assert not missing, f"faltan epicas en labels.yml: {missing}"


def test_labels_cover_priorities() -> None:
    """AC-01: el catalogo declara las tres prioridades, incluida could-have."""
    # Arrange
    labels = _labels()

    # Act
    names = set(_names(labels))

    # Assert
    missing = [priority for priority in PRIORITIES if priority not in names]
    assert not missing, f"faltan prioridades en labels.yml: {missing}"
