"""Pruebas estáticas de MLflow en el Droplet (HU-110, issue #166)."""

from __future__ import annotations

from pathlib import Path

COMPOSE = Path("compose.prod.yml")
CADDY = Path("docker/Caddyfile")
ENV_EXAMPLE = Path(".env.example")
RUNBOOK = Path("docs/operacion/mlflow.md")


def _read(path: Path) -> str:
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def _service(name: str) -> str:
    lines = _read(COMPOSE).splitlines()
    start = next(index for index, line in enumerate(lines) if line == f"  {name}:")
    block: list[str] = []
    for line in lines[start + 1 :]:
        if line.startswith("  ") and not line.startswith("    ") and line.strip():
            break
        block.append(line)
    return "\n".join(block)


def _caddy_mlflow() -> str:
    text = _read(CADDY)
    start = text.index("handle /mlflow/*")
    end = text.index("\n\t}", start)
    return text[start:end]


def test_compose_has_mlflow_service() -> None:
    # Act / Assert
    assert "  mlflow:" in _read(COMPOSE)


def test_mlflow_is_behind_a_profile() -> None:
    # Act
    block = _service("mlflow")

    # Assert
    assert 'profiles: ["mlflow"]' in block


def test_mlflow_uses_pinned_image_variable() -> None:
    # Act
    block = _service("mlflow")

    # Assert
    assert "${PPE_MLFLOW_IMAGE:-ghcr.io/mlflow/mlflow:v3.18.0}" in block


def test_mlflow_has_no_published_ports() -> None:
    # Act
    block = _service("mlflow")

    # Assert
    assert "5000:5000" not in block
    assert "expose:" in block
    assert '"5000"' in block


def test_mlflow_keeps_backend_store_on_host() -> None:
    # Act
    block = _service("mlflow")

    # Assert
    assert "--backend-store-uri=sqlite:////mlflow/mlflow.db" in block
    assert "${PPE_MLFLOW_DATA:-/opt/ppe/mlflow}:/mlflow" in block


def test_mlflow_serves_artifacts_from_volume() -> None:
    # Act
    block = _service("mlflow")

    # Assert
    assert "--default-artifact-root=/mlflow/artifacts" in block


def test_mlflow_uses_static_prefix() -> None:
    # Act
    block = _service("mlflow")

    # Assert
    assert "--static-prefix=/mlflow" in block


def test_mlflow_restarts() -> None:
    # Act / Assert
    assert "restart: unless-stopped" in _service("mlflow")


def test_mlflow_has_healthcheck() -> None:
    # Act
    block = _service("mlflow")

    # Assert
    assert "healthcheck:" in block
    assert "/health" in block


def test_caddy_routes_mlflow_with_auth() -> None:
    # Act
    block = _caddy_mlflow()

    # Assert
    assert "import protegido" in block


def test_caddy_mlflow_proxies_to_service() -> None:
    # Act
    block = _caddy_mlflow()

    # Assert
    assert "reverse_proxy mlflow:5000" in block


def test_caddy_does_not_strip_prefix() -> None:
    # Act
    text = _read(CADDY)

    # Assert
    assert "handle_path /mlflow" not in text


def test_caddyfile_has_no_hardcoded_credentials() -> None:
    # Act
    text = _read(CADDY)

    # Assert
    for marker in ("$2a$", "$2b$", "$2y$"):
        assert marker not in text


def test_env_example_documents_mlflow_variables() -> None:
    # Act
    text = _read(ENV_EXAMPLE)

    # Assert
    assert "PPE_MLFLOW_IMAGE=" in text
    assert "PPE_MLFLOW_DATA=" in text


def test_runbook_has_droplet_section() -> None:
    # Act
    text = _read(RUNBOOK)

    # Assert
    assert "## 9. MLflow en el Droplet" in text
    assert "--profile mlflow" in text


def test_runbook_documents_backup() -> None:
    # Act
    text = _read(RUNBOOK)

    # Assert
    assert "tar -czf" in text
    assert "PPE_MLFLOW_DATA" in text


def test_runbook_documents_auth() -> None:
    # Act
    text = _read(RUNBOOK)

    # Assert
    assert "PPE_AUTH_HASH" in text
    assert "basic auth" in text.lower()
