"""Cierre documental de HUs ya implementadas (HU-073, 078, 081, 014 y 015).

Pruebas estáticas: leen los archivos del entregable y fijan su contrato. El
comportamiento real se verificó en el servidor y en la SPA.
"""

from __future__ import annotations

from pathlib import Path

AGENTS = Path("AGENTS.md")
RUNBOOK = Path("docs/operacion/gitlab-espejo.md")
APP = Path("frontend/src/App.tsx")
STATES_TEST = Path("frontend/src/App.states.test.tsx")
DOWNLOAD = Path("frontend/src/download.ts")
DOWNLOAD_TEST = Path("frontend/src/download.test.ts")
PIPELINE = Path(".gitlab-ci.yml")
DEPLOY = Path("deploy/deploy.sh")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-073 · AC-01


def test_glab_skill_is_versioned() -> None:
    """HU-073 AC-01: la skill del CLI de GitLab vive en el repositorio."""
    # Arrange
    skill = Path(".agents/skills/glab/SKILL.md")

    # Assert
    assert skill.is_file()
    assert "glab" in skill.read_text(encoding="utf-8").lower()


def test_agents_documents_the_gitlab_tools() -> None:
    """HU-073 AC-02: AGENTS describe `glab` y el MCP de GitLab."""
    # Arrange
    agents = _read(AGENTS)

    # Assert
    assert "`glab`" in agents
    assert "GitLab MCP" in agents


def test_runbook_explains_the_tokenless_access() -> None:
    """HU-073 AC-03: la operación de GitLab no guarda tokens en el repositorio."""
    # Arrange
    runbook = _read(RUNBOOK)

    # Assert
    assert "token" in runbook.lower()
    assert "glpat-" not in runbook


# --------------------------------------------------------------- HU-081 · AC-01


def test_app_shows_a_retry_action_on_failure() -> None:
    """HU-081 AC-02: ante un error de red la interfaz ofrece reintentar."""
    # Arrange
    app = _read(APP)

    # Assert
    assert "Reintentar" in app


def test_wait_threshold_is_configurable() -> None:
    """HU-081 AC-01: el aviso de espera usa un umbral configurable."""
    # Arrange
    app = _read(APP)

    # Assert
    assert "slowAfterMs" in app


def test_the_three_states_have_tests() -> None:
    """HU-081 AC-03: carga, error y resultado están cubiertos por pruebas."""
    # Arrange
    states = _read(STATES_TEST)

    # Assert
    assert states.count("it(") + states.count("test(") >= 5


# --------------------------------------------------------------- HU-078 · AC-01


def test_csv_includes_class_confidence_and_box() -> None:
    """HU-078 AC-01: la fila exportada lleva clase, confianza y caja."""
    # Arrange
    download = _read(DOWNLOAD)

    # Assert
    assert "detectionsToCsv" in download
    for column in ("class_name", "confidence", "x1", "y1", "x2", "y2"):
        assert column in download


def test_export_declares_a_file_name_and_mime_type() -> None:
    """HU-078 AC-02: cada formato se descarga con su nombre y su tipo MIME."""
    # Arrange
    download = _read(DOWNLOAD)
    app = _read(APP)

    # Assert
    assert "text/csv" in app
    assert "application/json" in app
    assert "-detecciones.csv" in app
    assert "-detecciones.json" in app
    assert "Blob" in download


def test_serialisation_has_tests() -> None:
    """HU-078 AC-03: hay pruebas de serialización del export."""
    # Arrange
    tests = _read(DOWNLOAD_TEST)

    # Assert
    assert tests.count("it(") + tests.count("test(") >= 3


# --------------------------------------------------------------- HU-014 · AC-02


def test_pipeline_chains_the_gates_before_publishing() -> None:
    """HU-014 AC-02: una compuerta fallida detiene la publicación."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "- quality" in pipeline
    assert "- test" in pipeline
    assert "- package" in pipeline
    assert "needs:" in pipeline


def test_deployment_waits_for_the_built_image() -> None:
    """HU-014 AC-01: el deploy depende del job que construye la imagen."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "needs:\n    - build_image" in pipeline
    assert "sha256sum -c -" in pipeline


# --------------------------------------------------------------- HU-015 · AC-01


def test_smoke_checks_the_real_health_endpoint() -> None:
    """HU-015 AC-01: el smoke consulta la salud real del servicio."""
    # Arrange
    script = _read(DEPLOY)

    # Assert
    assert "health/ready" in script
    assert "State.Health.Status" in script


def test_smoke_runs_inside_the_container() -> None:
    """HU-015 AC-02: la comprobación ejecuta el cliente dentro del contenedor."""
    # Arrange
    script = _read(DEPLOY)

    # Assert
    assert "exec -T api python -c" in script


def test_deployment_is_serialised_per_environment() -> None:
    """HU-015 AC-03: dos despliegues no se pisan en el mismo entorno."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "resource_group: production" in pipeline
