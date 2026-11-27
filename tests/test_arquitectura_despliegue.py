"""Pruebas estáticas del diagrama de despliegue (HU-086)."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ARCH = REPO / "docs" / "architecture"
SOURCE = ARCH / "arquitectura.json"
HTML = ARCH / "arquitectura.html"
README = ARCH / "README.md"


def _source() -> dict:
    """Devuelve la fuente versionada del diagrama."""
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def test_ac_01_cadena_de_despliegue() -> None:
    """AC-01: GitHub → GitLab → Registry → Droplet → usuario, con proxy."""
    data = _source()
    ids = {component["id"] for component in data["components"]}
    required = {"github", "gitlab", "registry", "droplet", "user", "caddy", "web", "grpc"}
    assert required <= ids

    edges = {(link["from"], link["to"]) for link in data["connections"]}
    required_edges = {
        ("github", "gitlab"),
        ("gitlab", "registry"),
        ("registry", "droplet"),
        ("droplet", "caddy"),
        ("caddy", "web"),
        ("caddy", "api"),
    }
    assert required_edges <= edges


def test_ac_02_secretos_puertos_y_healthchecks() -> None:
    """AC-02: secretos por nombre, puertos y healthchecks documentados."""
    text = json.dumps(_source(), ensure_ascii=False)

    for secret in ("SSH_KEY", "DOCKERHUB_TOKEN", "PPE_AUTH_HASH"):
        assert secret in text
    for port in ("443", "8000", "9000"):
        assert port in text
    for health in ("/health", "/health/ready"):
        assert health in text
    # Se documentan nombres de variables, nunca valores.
    assert "PRIVATE KEY" not in text


def test_ac_03_fuente_json_versionada() -> None:
    """AC-03: la fuente JSON es válida y apunta al HTML generado."""
    data = _source()
    assert data["schema_version"] >= 1
    assert data["meta"]["output"] == "docs/architecture/arquitectura.html"

    readme = README.read_text(encoding="utf-8")
    assert "arquitectura.json" in readme
    assert "no se edita a mano" in readme


def test_html_regenerado_contiene_cadena() -> None:
    """AC-01/AC-03: el HTML generado refleja la cadena de despliegue."""
    html = HTML.read_text(encoding="utf-8")
    for label in ("GitHub", "GitLab CI", "Registry", "Droplet", "Caddy"):
        assert label in html
