"""Pruebas de las funciones puras del lanzador."""

from __future__ import annotations

from pathlib import Path

from ppe_detection.tools.launcher import api_env, model_version, resolve_model


def _weights(tmp_path: Path) -> Path:
    path = tmp_path / "yolo11s_clean" / "weights" / "best.pt"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"pesos simulados")
    return path


def test_resolve_model_prefers_explicit_path(tmp_path: Path) -> None:
    # Arrange
    weights = _weights(tmp_path)

    # Act
    result = resolve_model(str(weights), {})

    # Assert
    assert result == weights


def test_resolve_model_uses_env_var(tmp_path: Path) -> None:
    # Arrange
    weights = _weights(tmp_path)

    # Act
    result = resolve_model(None, {"PPE_MODEL_PATH": str(weights)})

    # Assert
    assert result == weights


def test_resolve_model_returns_default_candidate_without_files() -> None:
    # Arrange / Act
    result = resolve_model(None, {})

    # Assert
    assert result.name == "best.pt"
    assert "yolo11s_clean" in str(result)


def test_model_version_reads_weights_parent(tmp_path: Path) -> None:
    # Arrange
    weights = _weights(tmp_path)

    # Act
    version = model_version(weights)

    # Assert
    assert version == "yolo11s_clean"


def test_api_env_sets_model_ports_and_cors(tmp_path: Path) -> None:
    # Arrange
    weights = _weights(tmp_path)

    # Act
    env = api_env(weights, "127.0.0.1", 8000, 5173)

    # Assert
    assert env["PPE_MODEL_PATH"] == str(weights)
    assert env["PPE_MODEL_VERSION"] == "yolo11s_clean"
    assert env["PPE_API_HOST"] == "127.0.0.1"
    assert env["PPE_API_PORT"] == "8000"
    assert "http://localhost:5173" in env["PPE_CORS_ORIGINS"]
