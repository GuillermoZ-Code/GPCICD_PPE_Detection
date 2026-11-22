"""Pruebas del manifiesto canónico del modelo (HU-025).

Cubren AC-01, AC-02 y AC-03: el manifiesto versionado, su validación y el uso de la
misma referencia en /health y en el payload de MLflow.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import FakeDetector
from ppe_detection.detector_config import (
    DEFAULT_MANIFEST_PATH,
    ModelManifest,
    ModelManifestError,
    default_model_identity,
    load_model_manifest,
)
from ppe_detection.tracking import build_run_payload

SHA = "A" * 64
OTHER_SHA = "B" * 64


def _manifest_text(
    *,
    name: str = "ppe-detection",
    version: str = "yolo11s-clean",
    sha256: str = SHA,
    url: str = "file:///models/best.pt",
) -> str:
    return f'name = "{name}"\nversion = "{version}"\nsha256 = "{sha256}"\nurl = "{url}"\n'


def _write_manifest(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "models.lock"
    path.write_text(text, encoding="utf-8")
    return path


def _summary(model_sha: str = SHA) -> dict[str, Any]:
    return {
        "generated_at": "2026-11-21T00:00:00+00:00",
        "model": {"path": "artifacts/models/best.pt", "sha256": model_sha},
        "dataset": {
            "path": "artifacts/datasets/data.yaml",
            "split": "test",
            "yaml_sha256": OTHER_SHA,
        },
        "config": {"imgsz": 640, "conf": 0.001, "iou": 0.7, "seed": 42, "device": "cpu"},
        "images": 10,
        "instances": 20,
        "metrics": {
            "metrics/precision(B)": 0.5,
            "metrics/recall(B)": 0.6,
            "metrics/mAP50(B)": 0.7,
            "metrics/mAP50-95(B)": 0.4,
        },
        "per_class": {
            "helmet": {"p": 0.5, "r": 0.6, "ap50": 0.7, "ap": 0.4},
        },
    }


def test_models_lock_has_required_fields() -> None:
    """AC-01: el manifiesto versionado contiene los cuatro campos obligatorios."""

    # Arrange / Act
    manifest = load_model_manifest(DEFAULT_MANIFEST_PATH)

    # Assert
    assert isinstance(manifest, ModelManifest)
    assert manifest.name == "ppe-detection"
    assert manifest.version == "yolo11s-clean"
    assert manifest.sha256 == manifest.sha256.upper()
    assert len(manifest.sha256) == 64
    assert manifest.url


def test_load_model_manifest_reads_toml(tmp_path: Path) -> None:
    """FR-002: el cargador lee TOML y normaliza el SHA a mayúsculas."""

    # Arrange
    path = _write_manifest(tmp_path, _manifest_text(sha256=SHA.lower()))

    # Act
    manifest = load_model_manifest(path)

    # Assert
    assert manifest == ModelManifest(
        name="ppe-detection",
        version="yolo11s-clean",
        sha256=SHA,
        url="file:///models/best.pt",
    )


def test_models_lock_rejects_missing_field(tmp_path: Path) -> None:
    """AC-02: falta `url` y el cargador lo reporta."""

    # Arrange
    path = _write_manifest(
        tmp_path,
        'name = "ppe-detection"\nversion = "v1"\nsha256 = "' + SHA + '"\n',
    )

    # Act / Assert
    with pytest.raises(ModelManifestError, match="url"):
        load_model_manifest(path)


def test_models_lock_rejects_invalid_sha(tmp_path: Path) -> None:
    """AC-02: un SHA que no tiene 64 hexadecimales es inválido."""

    # Arrange
    path = _write_manifest(tmp_path, _manifest_text(sha256="abc"))

    # Act / Assert
    with pytest.raises(ModelManifestError, match="SHA256"):
        load_model_manifest(path)


def test_load_model_manifest_rejects_invalid_toml(tmp_path: Path) -> None:
    """Edge case: un TOML mal formado no se ignora en silencio."""

    # Arrange
    path = _write_manifest(tmp_path, "name = [")

    # Act / Assert
    with pytest.raises(ModelManifestError, match="TOML"):
        load_model_manifest(path)


def test_explicit_manifest_path_is_required_to_exist(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """FR-004: si el usuario define `PPE_MODEL_MANIFEST`, la ruta debe existir."""

    # Arrange
    monkeypatch.setenv("PPE_MODEL_MANIFEST", str(tmp_path / "missing.lock"))

    # Act / Assert
    with pytest.raises(ModelManifestError, match="manifiesto"):
        load_model_manifest()


def test_default_model_identity_uses_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """FR-003: sin overrides, la identidad viene del manifiesto."""

    # Arrange
    path = _write_manifest(tmp_path, _manifest_text())
    monkeypatch.setenv("PPE_MODEL_MANIFEST", str(path))
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    monkeypatch.delenv("PPE_MODEL_VERSION", raising=False)
    monkeypatch.delenv("PPE_MODEL_SHA256", raising=False)

    # Act
    identity = default_model_identity()

    # Assert
    assert identity.version == "yolo11s-clean"
    assert identity.sha256 == SHA
    assert identity.artifact == "file:///models/best.pt"
    assert identity.reference == f"sha256:{SHA}"


def test_explicit_environment_wins_over_manifest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """FR-003: los overrides explícitos conservan la precedencia."""

    # Arrange
    path = _write_manifest(tmp_path, _manifest_text())
    monkeypatch.setenv("PPE_MODEL_MANIFEST", str(path))
    monkeypatch.setenv("PPE_MODEL_VERSION", "explicit")
    monkeypatch.setenv("PPE_MODEL_SHA256", OTHER_SHA)

    # Act
    identity = default_model_identity()

    # Assert
    assert identity.version == "explicit"
    assert identity.sha256 == OTHER_SHA
    assert identity.reference == f"sha256:{OTHER_SHA}"


def test_health_uses_manifest_identity(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-03: /health reporta la versión y el SHA del manifiesto."""

    # Arrange
    path = _write_manifest(tmp_path, _manifest_text())
    monkeypatch.setenv("PPE_MODEL_MANIFEST", str(path))
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    monkeypatch.delenv("PPE_MODEL_VERSION", raising=False)
    monkeypatch.delenv("PPE_MODEL_SHA256", raising=False)
    client = TestClient(create_app(detector=FakeDetector([])))

    # Act
    response = client.get("/health")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert body["model_version"] == "yolo11s-clean"
    assert body["model_sha256"] == SHA
    assert body["model_artifact"] == "file:///models/best.pt"
    assert body["model_reference"] == f"sha256:{SHA}"


def test_mlflow_payload_uses_manifest_reference(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """AC-03: MLflow y /health comparten la misma referencia de modelo."""

    # Arrange
    path = _write_manifest(tmp_path, _manifest_text())
    monkeypatch.setenv("PPE_MODEL_MANIFEST", str(path))
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    monkeypatch.delenv("PPE_MODEL_VERSION", raising=False)
    monkeypatch.delenv("PPE_MODEL_SHA256", raising=False)

    # Act
    identity = default_model_identity()
    payload = build_run_payload(_summary(model_sha=identity.sha256 or ""))

    # Assert
    assert payload.tags["model_reference"] == identity.reference
    assert payload.params["model_sha256"] == identity.sha256
