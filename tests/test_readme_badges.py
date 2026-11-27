"""Pruebas del README con badges y enlaces públicos del M4 (HU-061, #117)."""

from __future__ import annotations

import re
from pathlib import Path

README = Path(__file__).resolve().parents[1] / "README.md"

LINK = re.compile(r"\]\(([^)]+)\)")
BADGE = re.compile(r"\[!\[([^\]]+)\]\(([^)]+)\)\]\(([^)]+)\)")

CI_BADGE = (
    "https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/actions/workflows/ci.yml/badge.svg"
)
GITLAB_BADGE = (
    "https://gitlab.com/educacional-group/GPCICD_PPE_Detection/badges/develop/pipeline.svg"
)
DOCKER_HUB_REPO = "https://hub.docker.com/r/guillermozabala/gpcicd-ppe-api"
HTTPS_REMOTE = "https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection"
REGISTRY = "https://gitlab.com/educacional-group/GPCICD_PPE_Detection/-/container_registry"


def _text() -> str:
    return README.read_text(encoding="utf-8")


def _badges() -> list[tuple[str, str, str]]:
    return BADGE.findall(_text())


def test_badges_de_ci_pipeline_licencia_y_docker_hub_ac_01() -> None:
    """AC-01: el README muestra badges de CI, pipeline, licencia y Docker Hub."""
    # Arrange
    badges = _badges()

    # Act
    destinos = {destino for _, _, destino in badges}
    imagenes = {imagen for _, imagen, _ in badges}

    # Assert
    assert CI_BADGE in imagenes, "falta el badge de GitHub CI"
    assert GITLAB_BADGE in imagenes, "falta el badge del pipeline de GitLab"
    assert any("AGPL" in alt and destino == "./LICENSE" for alt, _, destino in badges), (
        "falta el badge de licencia AGPL hacia ./LICENSE"
    )
    assert any("Docker Hub" in alt for alt, _, _ in badges), "falta el badge de Docker Hub"
    assert DOCKER_HUB_REPO in destinos, "el badge de Docker Hub no enlaza el repositorio publicado"


def test_badge_docker_hub_apunta_al_repositorio_publicado_ac_01() -> None:
    """AC-01: el badge enlaza la imagen pública publicada por HU-068."""
    # Arrange
    text = _text()

    # Act
    docker_badge = [b for b in _badges() if "Docker Hub" in b[0]]

    # Assert
    assert docker_badge, "no hay badge de Docker Hub que validar"
    assert DOCKER_HUB_REPO in {destino for _, _, destino in docker_badge}
    assert "gpcicd-ppe-api" in text


def test_enlaces_https_registry_y_constitucion_ac_02() -> None:
    """AC-02: el README enlaza el remoto HTTPS, el Registry y CONSTITUTION."""
    # Arrange
    text = _text()

    # Act
    enlaces = set(LINK.findall(text))

    # Assert
    assert HTTPS_REMOTE in enlaces, "falta la URL HTTPS del repositorio"
    assert REGISTRY in enlaces, "falta el enlace al Registry de GitLab"
    assert "./CONSTITUTION.md" in enlaces, "falta el enlace a CONSTITUTION.md"
    assert "<URL_PUBLICA>" in text, "falta la plantilla de URL pública de HU-053"


def test_enlaces_internos_resuelven_y_toc_existe_ac_03() -> None:
    """AC-03: los enlaces internos resuelven y el índice incluye la sección M4."""
    # Arrange
    links = LINK.findall(_text())

    # Act
    broken = [
        link
        for link in links
        if not link.startswith(("http://", "https://", "#", "mailto:", "<"))
        and not (README.parent / link.split("#")[0]).resolve().exists()
    ]

    # Assert
    assert links, "el README no tiene enlaces"
    assert not broken, f"enlaces rotos: {broken}"
    assert "[Enlaces públicos del M4](#enlaces-públicos-del-m4)" in _text()
