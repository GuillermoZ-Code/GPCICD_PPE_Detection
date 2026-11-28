"""HU-066, HU-067 y HU-068 — pipeline de GitLab (stages, build y publicación).

Pruebas estáticas: leen `.gitlab-ci.yml`, `Dockerfile` y `compose.yml` sin llamar a
GitLab, a un registry ni a la red. El comportamiento real se comprueba ejecutando el
pipeline; `glab ci lint` valida la sintaxis en la revisión.
"""

from __future__ import annotations

import re
from pathlib import Path

PIPELINE = Path(".gitlab-ci.yml")
DOCKERFILE = Path("Dockerfile")
COMPOSE = Path("compose.yml")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


# --------------------------------------------------------------- HU-066 · AC-01


def test_pipeline_declares_stages_in_order() -> None:
    """AC-01: los stages existen y van en el orden quality → test → package."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Act
    quality = pipeline.index("- quality")
    test = pipeline.index("- test")
    package = pipeline.index("- package")

    # Assert
    assert quality < test < package


def test_uv_cache_keys_on_lockfiles_per_job() -> None:
    """AC-01: el cache de uv se invalida con los manifiestos y no se comparte."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "- pyproject.toml" in pipeline
    assert "- uv.lock" in pipeline
    assert "prefix: $CI_JOB_NAME" in pipeline


def test_npm_cache_keys_on_package_lock() -> None:
    """AC-01: el frontend cachea node_modules con su propio archivo de bloqueo."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "frontend/package-lock.json" in pipeline
    assert "frontend/node_modules/" in pipeline


# --------------------------------------------------------------- HU-066 · AC-02


def test_quality_jobs_run_on_branches_and_merge_requests() -> None:
    """AC-02: ramas y MR ejecutan las compuertas de calidad."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert '$CI_PIPELINE_SOURCE == "merge_request_event"' in pipeline
    assert "- if: $CI_COMMIT_BRANCH" in pipeline


def test_build_runs_on_default_branch_or_manually() -> None:
    """AC-02: solo la rama por defecto empaqueta; otra rama lo hace a mano."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "- if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH" in pipeline
    assert "when: manual" in pipeline


def test_pipeline_cancels_outdated_runs_and_has_timeout() -> None:
    """AC-02: dos pushes seguidos no gastan minutos en el commit viejo."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "auto_cancel:" in pipeline
    assert "on_new_commit: interruptible" in pipeline
    assert "timeout: 20 minutes" in pipeline
    assert "interruptible: true" in pipeline


# --------------------------------------------------------------- HU-066 · AC-03


def test_pipeline_avoids_deprecated_only_except() -> None:
    """AC-03: el archivo usa `rules` y no las claves obsoletas `only`/`except`."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "only:" not in pipeline
    assert "except:" not in pipeline
    assert "rules:" in pipeline


def test_dependencies_are_frozen_and_tests_publish_junit() -> None:
    """AC-03: uv respeta uv.lock y pytest deja un reporte legible por GitLab."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert 'UV_FROZEN: "1"' in pipeline
    assert "junit: report.xml" in pipeline
    assert "when: always" in pipeline


# --------------------------------------------------------------- HU-067 · AC-01


def test_build_uses_docker_in_docker() -> None:
    """AC-01: el job construye con DinD, no en el runner anfitrión."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "docker:29.10.0-cli" in pipeline
    assert "docker:29.10.0-dind" in pipeline


def test_build_produces_runtime_and_web_targets() -> None:
    """AC-01: se construyen las dos imágenes del sistema."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "--target runtime" in pipeline
    assert "--target web" in pipeline


def test_build_reuses_layer_cache() -> None:
    """AC-01: el cache de capas evita reconstruir dependencias en cada push."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "--cache-from" in pipeline
    assert "BUILDKIT_INLINE_CACHE=1" in pipeline


# --------------------------------------------------------------- HU-067 · AC-02


def test_images_are_tagged_with_sha_and_latest() -> None:
    """AC-02: cada imagen lleva el SHA corto y el alias `latest`."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "$API_IMAGE:$CI_COMMIT_SHORT_SHA" in pipeline
    assert "$API_IMAGE:latest" in pipeline
    assert "$WEB_IMAGE:$CI_COMMIT_SHORT_SHA" in pipeline
    assert "$WEB_IMAGE:latest" in pipeline


# --------------------------------------------------------------- HU-067 · AC-03


def test_model_is_not_baked_into_the_image() -> None:
    """AC-03: el Dockerfile no copia pesos; el modelo se monta en el servidor."""
    # Arrange
    dockerfile = _read(DOCKERFILE)
    compose = _read(COMPOSE)

    # Act
    copies_weights = re.search(r"^\s*COPY\b.*\.(pt|onnx)\b", dockerfile, re.MULTILINE)

    # Assert
    assert "NUNCA va dentro de la imagen" in dockerfile
    assert copies_weights is None, "el Dockerfile no debe copiar pesos"
    assert "/models:ro" in compose


def test_image_is_smoked_before_publishing() -> None:
    """AC-03: un import roto no llega al registry."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Act
    smoke = pipeline.index("smoke ok")
    push = pipeline.index("docker push $API_IMAGE:$CI_COMMIT_SHORT_SHA")

    # Assert
    assert smoke < push


# --------------------------------------------------------------- HU-068 · AC-01


def test_registry_login_uses_job_token() -> None:
    """AC-01: el registry del proyecto se autentica con el token efímero del job."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert 'echo "$CI_JOB_TOKEN" | docker login -u "$CI_REGISTRY_USER"' in pipeline
    assert '--password-stdin "$CI_REGISTRY"' in pipeline


def test_images_are_pushed_to_project_registry() -> None:
    """AC-01: las imágenes van al registry del proyecto, con prefijo por servicio."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "API_IMAGE: $CI_REGISTRY_IMAGE/api" in pipeline
    assert "WEB_IMAGE: $CI_REGISTRY_IMAGE/web" in pipeline


# --------------------------------------------------------------- HU-068 · AC-02


def test_docker_hub_push_is_optional_and_uses_masked_variables() -> None:
    """AC-02: sin credenciales no se publica; con ellas, van enmascaradas."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "${DOCKERHUB_USER:-}" in pipeline
    assert "${DOCKERHUB_TOKEN:-}" in pipeline
    assert "se omite la publicación espejo" in pipeline


def test_pipeline_has_no_literal_credentials() -> None:
    """AC-02: ninguna contraseña viaja en el archivo."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "docker login -p " not in pipeline
    assert "--password " not in pipeline
    assert "glpat-" not in pipeline


# --------------------------------------------------------------- HU-068 · AC-03


def test_digests_are_published_as_artifacts() -> None:
    """AC-03: el digest de cada imagen queda para auditar qué se desplegó."""
    # Arrange
    pipeline = _read(PIPELINE)

    # Assert
    assert "api-digest.txt" in pipeline
    assert "web-digest.txt" in pipeline
    assert "RepoDigests" in pipeline
    assert "artifacts:" in pipeline
