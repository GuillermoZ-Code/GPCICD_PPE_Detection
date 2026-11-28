"""Pruebas de la plantilla de issue de HU (HU-091, issue #147).

Cada prueba referencia su criterio de aceptación en el docstring: AC-01 campos,
AC-02 DoR/DoD y AC-03 YAML válido con el contrato de los issue forms.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import yaml

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / ".github" / "ISSUE_TEMPLATE" / "hu.yml"

ALLOWED_TYPES = {"markdown", "textarea", "input", "dropdown", "checkboxes"}
REQUIRED_FIELDS = {"historia", "criterios", "sp", "dependencias", "spec", "pruebas"}
FIBONACCI = ["1", "2", "3", "5", "8", "13"]

Field = dict[str, Any]


def _load_template() -> Field:
    """Carga el archivo una sola vez por prueba."""
    raw: Any = yaml.safe_load(TEMPLATE_PATH.read_text(encoding="utf-8"))
    assert isinstance(raw, dict), "la plantilla debe ser un mapping YAML"
    return cast(Field, raw)


def _body(template: Field) -> list[Field]:
    body = template.get("body")
    assert isinstance(body, list), "el formulario debe declarar body como lista"
    return [cast(Field, item) for item in body]


def _field(template: Field, field_id: str) -> Field:
    matches = [item for item in _body(template) if item.get("id") == field_id]
    assert len(matches) == 1, f"se esperaba un unico campo con id {field_id!r}"
    return matches[0]


def _attributes(field: Field) -> Field:
    attributes = field.get("attributes")
    assert isinstance(attributes, dict), f"el campo {field.get('id')!r} no tiene attributes"
    return cast(Field, attributes)


def test_hu_template_is_valid_yaml() -> None:
    """AC-03: el archivo existe y es YAML válido."""
    # Arrange
    assert TEMPLATE_PATH.is_file(), f"falta {TEMPLATE_PATH}"

    # Act
    template = _load_template()

    # Assert
    assert isinstance(template, dict)


def test_hu_template_form_contract() -> None:
    """AC-03: cumple el contrato de los issue forms de GitHub."""
    # Arrange
    template = _load_template()

    # Act
    body = _body(template)

    # Assert
    assert template.get("name"), "falta name"
    assert template.get("description"), "falta description"
    assert body, "el formulario no tiene campos"
    for field in body:
        assert field.get("type") in ALLOWED_TYPES, f"tipo no soportado: {field.get('type')!r}"
        if field["type"] == "markdown":
            assert _attributes(field).get("value"), "markdown sin value"
        else:
            assert field.get("id"), f"campo sin id: {field}"


def test_hu_template_has_unique_field_ids() -> None:
    """AC-03: los ids de los campos no se repiten."""
    # Arrange
    template = _load_template()

    # Act
    ids = [item["id"] for item in _body(template) if item["type"] != "markdown"]

    # Assert
    assert len(ids) == len(set(ids)), f"ids duplicados: {ids}"


def test_hu_template_requests_required_fields() -> None:
    """AC-01: pide historia, AC, SP, dependencias, spec y pruebas objetivo."""
    # Arrange
    template = _load_template()

    # Act
    fields = {item["id"]: item for item in _body(template) if item["type"] != "markdown"}

    # Assert
    assert set(fields) >= REQUIRED_FIELDS, f"faltan campos: {REQUIRED_FIELDS - set(fields)}"
    for field_id in REQUIRED_FIELDS:
        validations = fields[field_id].get("validations")
        assert isinstance(validations, dict), f"{field_id} no tiene validations"
        assert validations.get("required") is True, f"{field_id} no es obligatorio"
    assert fields["historia"]["type"] == "textarea"
    assert fields["criterios"]["type"] == "textarea"


def test_hu_template_uses_fibonacci_story_points() -> None:
    """AC-01: los SP salen de un desplegable con la serie Fibonacci."""
    # Arrange
    template = _load_template()

    # Act
    sp = _field(template, "sp")
    options = _attributes(sp).get("options")

    # Assert
    assert sp["type"] == "dropdown"
    assert options == FIBONACCI, f"opciones de SP fuera de Fibonacci: {options}"


def test_hu_template_has_dor_and_dod_checklists() -> None:
    """AC-02: incluye checklists de DoR y DoD con items obligatorios."""
    # Arrange
    template = _load_template()

    # Act
    dor = _field(template, "dor")
    dod = _field(template, "dod")

    # Assert
    for field_id, checklist in (("dor", dor), ("dod", dod)):
        assert checklist["type"] == "checkboxes", f"{field_id} debe ser checkboxes"
        options = _attributes(checklist).get("options")
        assert isinstance(options, list) and len(options) >= 3, f"{field_id} sin items"
        for option in options:
            assert option.get("label"), f"{field_id} tiene un item sin label"
            assert option.get("required") is True, f"{field_id} tiene un item opcional"
    dod_text = " ".join(option["label"] for option in _attributes(dod)["options"]).lower()
    assert "make check" in dod_text
    assert "pr" in dod_text
    assert "issue" in dod_text
