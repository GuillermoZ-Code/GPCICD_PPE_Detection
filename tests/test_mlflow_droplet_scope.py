"""HU-110 — MLflow en el Droplet: decisión de alcance.

MLflow se usa en local (HU-009); no se publica como servicio ni como ruta en el
Droplet. La prueba protege la decisión y la documentación asociada.
"""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
COMPOSE = REPO / "compose.prod.yml"
CADDY = REPO / "docker" / "Caddyfile"
RUNBOOK = REPO / "docs" / "operacion" / "mlflow.md"
SPEC = REPO / "specs" / "111-hu-110-mlflow-droplet" / "spec.md"


def _read(path: Path) -> str:
    """Lee un archivo esperado; su ausencia falla con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def test_ac01_mlflow_is_not_a_production_service() -> None:
    """AC-01: MLflow no se publica en compose ni en Caddy."""
    # Arrange
    compose = _read(COMPOSE)
    caddy = _read(CADDY)

    # Assert
    assert "mlflow:" not in compose
    assert "/mlflow" not in caddy


def test_ac02_no_new_deployment_secrets() -> None:
    """AC-02: la decisión no añade credenciales ni variables de MLflow."""
    # Arrange
    compose = _read(COMPOSE)

    # Assert
    assert "MLFLOW_TRACKING_PASSWORD" not in compose
    assert "MLFLOW_TRACKING_USERNAME" not in compose


def test_ac03_scope_is_documented() -> None:
    """AC-03: la spec y el runbook documentan el uso local de MLflow."""
    # Arrange
    spec = _read(SPEC)
    runbook = _read(RUNBOOK)

    # Assert
    assert "HU-110" in spec
    assert "Cerrada por alcance" in spec
    assert "MLflow local" in runbook
