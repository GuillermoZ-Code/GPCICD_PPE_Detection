"""AC-01, AC-02 y AC-03 (HU-066) — pipeline base de GitLab CI.

Pruebas estáticas: leen `.gitlab-ci.yml` y su runbook sin ejecutar GitLab.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

PIPELINE = Path(".gitlab-ci.yml")
RUNBOOK = Path("docs/operacion/gitlab-ci.md")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def _pipeline() -> dict[str, Any]:
    """Carga el YAML del pipeline; un archivo inválido falla la prueba."""
    data = yaml.safe_load(_read(PIPELINE))
    assert isinstance(data, dict), "el pipeline no es un mapa YAML"
    return data


def _script(job: dict[str, Any]) -> str:
    """Une el script de un job para buscarlo como texto."""
    return "\n".join(job.get("script", []))


# ---------------------------------------------------------------- AC-01 · stages y caché


def test_stages_define_quality_frontend_build_and_deploy() -> None:
    """AC-01: el pipeline declara las cuatro etapas en orden."""
    # Arrange / Act
    pipeline = _pipeline()

    # Assert
    assert pipeline["stages"] == ["quality", "frontend", "build", "deploy"]


def test_uv_and_npm_caches_are_declared() -> None:
    """AC-01: hay caché de `uv` por `uv.lock` y de `npm` por `package-lock.json`."""
    # Arrange
    pipeline = _pipeline()

    # Act
    quality_cache = pipeline["quality"]["cache"]
    frontend_cache = pipeline["frontend"]["cache"]

    # Assert
    assert "uv.lock" in quality_cache["key"]["files"]
    assert ".uv-cache/" in quality_cache["paths"]
    assert "frontend/package-lock.json" in frontend_cache["key"]["files"]
    assert "frontend/node_modules/" in frontend_cache["paths"]


def test_quality_runs_ruff_ty_and_pytest_with_uv() -> None:
    """AC-01: la compuerta de calidad usa `uv` y no instala con pip."""
    # Arrange / Act
    pipeline = _pipeline()
    quality = pipeline["quality"]
    script = _script(quality)

    # Assert
    assert quality["image"].startswith("ghcr.io/astral-sh/uv:")
    assert "uv sync --frozen --all-groups" in script
    for gate in ("uv run ruff check", "uv run ty check", "uv run pytest"):
        assert gate in script, f"falta la compuerta {gate!r}"


# ---------------------------------------------------------------- AC-02 · reglas


def test_workflow_rules_cover_merge_requests_and_branches() -> None:
    """AC-02: MR, `develop`, `main` y ejecución manual disparan el pipeline."""
    # Arrange / Act
    rules = _pipeline()["workflow"]["rules"]

    # Assert
    sources = " ".join(str(rule) for rule in rules)
    assert "merge_request_event" in sources
    assert '"develop"' in sources or "develop" in sources
    assert "main" in sources
    assert "web" in sources


def test_quality_and_frontend_run_on_every_pipeline() -> None:
    """AC-02: lint y pruebas no se restringen a una rama."""
    # Arrange / Act
    pipeline = _pipeline()

    # Assert
    assert "rules" not in pipeline["quality"]
    assert "rules" not in pipeline["frontend"]


def test_build_and_deploy_are_restricted_to_main() -> None:
    """AC-02: build y deploy solo corren en `main` o de forma manual."""
    # Arrange / Act
    pipeline = _pipeline()

    # Act
    build_rules = pipeline["build"]["rules"]
    deploy_rules = pipeline["deploy"]["rules"]

    # Assert
    assert all("main" in str(rule) or "web" in str(rule) for rule in build_rules)
    assert all("main" in str(rule) for rule in deploy_rules)


def test_deploy_is_manual_until_hu_070() -> None:
    """AC-02: el despliegue es manual y se declara pendiente de HU-070."""
    # Arrange / Act
    deploy = _pipeline()["deploy"]

    # Assert
    assert deploy["rules"][0]["when"] == "manual"
    assert "HU-070" in _script(deploy)
    assert deploy.get("allow_failure") is True


# ---------------------------------------------------------------- AC-03 · validación


def test_pipeline_avoids_pip_and_hardcoded_secrets() -> None:
    """AC-03: el archivo es válido y no usa pip ni secretos embebidos."""
    # Arrange / Act
    text = _read(PIPELINE)

    # Assert
    assert "pip install -r" not in text
    assert "requirements.txt" not in text
    assert "glpat-" not in text


def test_runbook_documents_glab_ci_lint() -> None:
    """AC-03: el runbook explica cómo validar el archivo con `glab ci lint`."""
    # Arrange / Act
    runbook = _read(RUNBOOK)

    # Assert
    assert "glab ci lint" in runbook
    assert "etapa" in runbook.lower()
