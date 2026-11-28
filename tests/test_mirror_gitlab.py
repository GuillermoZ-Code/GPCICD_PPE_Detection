"""AC-01, AC-02 y AC-03 (HU-065) — espejo GitHub → GitLab.

Pruebas estáticas: leen el workflow y el runbook sin llamar a GitHub, a GitLab ni a la
red. El comportamiento real se comprueba en el propio workflow con la API de GitLab.
"""

from __future__ import annotations

from pathlib import Path

WORKFLOW = Path(".github/workflows/mirror-gitlab.yml")
RUNBOOK = Path("docs/operacion/gitlab-espejo.md")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- AC-01 · disparo


def test_workflow_triggers_on_develop_and_main() -> None:
    """AC-01: el espejo corre en cada push a `develop` y `main`, y se puede repetir."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "branches: [develop, main]" in workflow
    assert "workflow_dispatch:" in workflow


def test_checkout_fetches_full_history() -> None:
    """AC-01: el checkout es completo para no empujar una rama superficial."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "actions/checkout@v7" in workflow
    assert "fetch-depth: 0" in workflow


def test_push_targets_gitlab_project_and_same_branch() -> None:
    """AC-01: el push va al proyecto de GitLab y a la misma rama del evento."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "educacional-group/GPCICD_PPE_Detection" in workflow
    assert "gitlab.com/${GITLAB_REPO}.git" in workflow
    assert "HEAD:refs/heads/${GITHUB_REF_NAME}" in workflow


def test_push_does_not_force_protected_branches() -> None:
    """AC-01: `main` está protegida; el espejo no la reescribe con `--force`."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "--force" not in workflow


def test_token_is_used_through_credential_helper() -> None:
    """AC-03: el token no viaja en la URL del remoto ni en un mensaje de error."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "credential.helper" in workflow
    assert "https://oauth2:" not in workflow


# ---------------------------------------------------------------- AC-02 · SHA


def test_workflow_verifies_commit_sha_against_gitlab() -> None:
    """AC-02: el workflow compara el último commit de GitLab con `GITHUB_SHA`."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "repository/commits?ref_name=" in workflow
    assert "${GITHUB_SHA}" in workflow
    assert "::error::" in workflow


# ---------------------------------------------------------------- AC-03 · token


def test_token_comes_from_github_secret() -> None:
    """AC-03: el token se lee del secret `GITLAB_TOKEN`, nunca del repositorio."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "secrets.GITLAB_TOKEN" in workflow


def test_token_is_masked_before_use() -> None:
    """AC-03: el token se enmascara para que no quede en los logs."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "::add-mask::${GITLAB_TOKEN}" in workflow


def test_workflow_has_no_literal_tokens() -> None:
    """AC-03: no hay tokens escritos en el workflow."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "glpat-" not in workflow
    assert "PRIVATE-TOKEN: glpat" not in workflow


def test_workflow_is_read_only_and_keeps_pushes() -> None:
    """AC-03: permisos mínimos y concurrencia que no descarta pushes."""
    # Arrange / Act
    workflow = _read(WORKFLOW)

    # Assert
    assert "contents: read" in workflow
    assert "cancel-in-progress: false" in workflow


# ---------------------------------------------------------------- Runbook


def test_runbook_documents_secret_scope_and_verification() -> None:
    """AC-03: el runbook explica el token, el secret y la verificación del SHA."""
    # Arrange / Act
    runbook = _read(RUNBOOK)

    # Assert
    assert "GITLAB_TOKEN" in runbook
    assert "write_repository" in runbook
    assert "GITHUB_SHA" in runbook


def test_runbook_declares_source_of_truth_and_pull_mirror() -> None:
    """AC-01: GitHub es la fuente de verdad y el espejo *pull* queda deshabilitado."""
    # Arrange / Act
    runbook = _read(RUNBOOK)

    # Assert
    assert "fuente de verdad" in runbook
    assert "pull" in runbook.lower()
    assert "89281003" in runbook


def test_verification_falls_back_to_git_when_the_api_rejects() -> None:
    """AC-02: si la API responde 403, el espejo verifica con `git ls-remote`."""
    # Arrange
    workflow = _read(WORKFLOW)

    # Assert
    assert "git ls-remote" in workflow
    assert "La API de GitLab rechazó la consulta" in workflow
