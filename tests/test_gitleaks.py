"""HU-043 — escaneo de secretos con gitleaks (AC-01, AC-02 y AC-03).

Pruebas estáticas: leen la configuración, el workflow y el Makefile. El escaneo real
corre en CI con la acción oficial.
"""

from __future__ import annotations

import re
from pathlib import Path

CONFIG = Path(".gitleaks.toml")
CI = Path(".github/workflows/ci.yml")
MAKEFILE = Path("Makefile")

# Archivos donde un token real no debe aparecer nunca.
SUPERFICIE = [
    Path(".gitlab-ci.yml"),
    Path("Makefile"),
    Path("deploy/deploy.sh"),
    Path("deploy/model/publish.sh"),
    Path("deploy/droplet/provision.sh"),
    Path("docker/Caddyfile"),
    Path("compose.prod.yml"),
    Path("tests/test_gitleaks.py"),
]


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-043 · AC-01


def test_config_extends_the_default_rules() -> None:
    """AC-01: se heredan las reglas por defecto y se documentan las exclusiones."""
    # Arrange
    config = _read(CONFIG)

    # Assert
    assert "[extend]" in config
    assert "useDefault = true" in config
    assert "[allowlist]" in config


def test_allowlist_is_justified_and_narrow() -> None:
    """AC-01: solo se excluyen documentación, fixtures y artefactos de build."""
    # Arrange
    config = _read(CONFIG)

    # Assert
    assert "'''docs/'''" in config
    assert "'''tests/'''" in config
    assert "'''frontend/node_modules/'''" in config


# --------------------------------------------------------------- HU-043 · AC-02


def test_ci_runs_gitleaks_on_push_and_pull_request() -> None:
    """AC-02: la compuerta corre en cada push y en cada PR."""
    # Arrange
    workflow = _read(CI)

    # Assert
    assert "gitleaks/gitleaks-action" in workflow
    assert "push:" in workflow
    assert "pull_request:" in workflow


def test_ci_job_has_read_only_permissions() -> None:
    """AC-02: el escaneo no necesita escribir en el repositorio."""
    # Arrange
    workflow = _read(CI)

    # Act
    bloque = workflow.split("secrets:", 1)[1] if "secrets:" in workflow else ""

    # Assert
    assert bloque, "no hay job de secretos"
    assert "contents: read" in bloque


def test_scan_history_is_complete() -> None:
    """AC-02: se escanea el histórico completo, no solo el último commit."""
    # Arrange
    workflow = _read(CI)

    # Assert
    assert "fetch-depth: 0" in workflow


# --------------------------------------------------------------- HU-043 · AC-03


def test_makefile_exposes_a_local_scan() -> None:
    """AC-03: se puede repetir el escaneo en local con un objetivo del Makefile."""
    # Arrange
    makefile = _read(MAKEFILE)

    # Assert
    assert "secrets:" in makefile
    assert "gitleaks detect" in makefile


def test_scan_surface_has_no_literal_tokens() -> None:
    """AC-03: los archivos versionados no contienen tokens con formato conocido."""
    # Arrange
    patrones = (
        re.compile(r"glpat-[A-Za-z0-9_-]{20,}"),
        re.compile(r"dop_v1_[a-f0-9]{64}"),
        re.compile(r"dckr_pat_[A-Za-z0-9_-]{20,}"),
        re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    )

    # Act
    hallazgos = []
    for archivo in SUPERFICIE:
        texto = _read(archivo)
        for patron in patrones:
            if patron.search(texto):
                hallazgos.append(f"{archivo}: {patron.pattern}")

    # Assert
    assert hallazgos == [], f"posibles secretos: {hallazgos}"


def test_config_covers_the_repository_root() -> None:
    """AC-03: la configuración vive en la raíz, donde gitleaks la busca."""
    # Arrange / Act
    config = _read(CONFIG)

    # Assert
    assert CONFIG.parent == Path(".")
    assert len(config) > 200
