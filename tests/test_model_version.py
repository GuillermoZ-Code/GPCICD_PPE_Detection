"""Pruebas de la identidad y versión del modelo (HU-013)."""

from __future__ import annotations

import hashlib
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import cv2
import grpc
import numpy as np
import pytest
from fastapi.testclient import TestClient

from ppe_detection.api import create_app
from ppe_detection.contracts import Detection, FakeDetector
from ppe_detection.detector_config import (
    ModelIdentity,
    default_model_identity,
    default_model_version,
    sha256_file,
)
from ppe_detection.grpc import server
from ppe_detection.grpc.protos import ppe_pb2, ppe_pb2_grpc
from ppe_detection.tracking import build_run_payload

MODEL_VERSION = "yolo11s-clean"
MODEL_SHA = "A" * 64
OTHER_SHA = "B" * 64
YAML_SHA = "C" * 64


def _detection() -> Detection:
    return Detection(
        class_id=3,
        class_name="helmet",
        confidence=0.9,
        bbox=(1.0, 2.0, 5.0, 6.0),
        image_width=8,
        image_height=6,
    )


def _png_bytes() -> bytes:
    rgb = np.zeros((6, 8, 3), dtype=np.uint8)
    rgb[0, 0] = (255, 0, 0)
    bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode(".png", bgr)
    assert ok
    return buffer.tobytes()


def _identity(
    *,
    version: str = MODEL_VERSION,
    sha256: str | None = MODEL_SHA,
    artifact: str | None = "C:/models/yolo11s-clean/best.pt",
) -> ModelIdentity:
    return ModelIdentity(version=version, sha256=sha256, artifact=artifact)


def _client(identity: ModelIdentity) -> TestClient:
    return TestClient(
        create_app(
            detector=FakeDetector([_detection()]),
            model_identity=identity,
        )
    )


def _post(client: TestClient) -> dict[str, Any]:
    response = client.post(
        "/predict",
        files={"file": ("image.png", _png_bytes(), "image/png")},
    )
    assert response.status_code == 200
    return response.json()


@contextmanager
def _grpc_stub(identity: ModelIdentity) -> Generator[ppe_pb2_grpc.PpeDetectionStub]:
    grpc_server = server.create_server(
        detector=FakeDetector([_detection()]),
        model_identity=identity,
    )
    port = grpc_server.add_insecure_port("127.0.0.1:0")
    assert port > 0
    grpc_server.start()
    channel = grpc.insecure_channel(f"127.0.0.1:{port}", options=server.default_options())
    stub = ppe_pb2_grpc.PpeDetectionStub(channel)
    try:
        yield stub
    finally:
        channel.close()
        grpc_server.stop(0)


def _call(stub: ppe_pb2_grpc.PpeDetectionStub) -> Any:
    return stub.Detect(ppe_pb2.PredictRequest(image=_png_bytes(), source="pruebas"), timeout=30)


def test_model_identity_reference_uses_sha256() -> None:
    # Arrange
    identity = _identity(sha256=MODEL_SHA)

    # Act
    reference = identity.reference

    # Assert
    assert reference == f"sha256:{MODEL_SHA}"


def test_model_identity_reference_falls_back_to_artifact() -> None:
    # Arrange
    identity = _identity(sha256=None, artifact="C:/models/best.pt")

    # Act
    reference = identity.reference

    # Assert
    assert reference == "artifact:C:/models/best.pt"


def test_model_identity_reference_falls_back_to_version() -> None:
    # Arrange
    identity = _identity(sha256=None, artifact=None)

    # Act
    reference = identity.reference

    # Assert
    assert reference == f"version:{MODEL_VERSION}"


def test_sha256_file_returns_uppercase_digest(tmp_path: Path) -> None:
    # Arrange
    artifact = tmp_path / "best.pt"
    artifact.write_bytes(b"pesos")
    expected = hashlib.sha256(b"pesos").hexdigest().upper()

    # Act
    digest = sha256_file(artifact)

    # Assert
    assert digest == expected
    assert digest == digest.upper()
    assert len(digest) == 64


def test_default_model_identity_reads_explicit_sha(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setenv("PPE_MODEL_VERSION", MODEL_VERSION)
    monkeypatch.setenv("PPE_MODEL_PATH", "C:/models/yolo11s-clean/best.pt")
    monkeypatch.setenv("PPE_MODEL_SHA256", MODEL_SHA)

    # Act
    identity = default_model_identity()

    # Assert
    assert identity.version == MODEL_VERSION
    assert identity.sha256 == MODEL_SHA
    assert identity.artifact == "C:/models/yolo11s-clean/best.pt"
    assert identity.reference == f"sha256:{MODEL_SHA}"


def test_default_model_identity_computes_sha_from_path(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange
    artifact = tmp_path / "best.pt"
    artifact.write_bytes(b"pesos")
    monkeypatch.setenv("PPE_MODEL_PATH", str(artifact))
    monkeypatch.delenv("PPE_MODEL_SHA256", raising=False)
    monkeypatch.delenv("PPE_MODEL_VERSION", raising=False)
    expected = hashlib.sha256(b"pesos").hexdigest().upper()

    # Act
    identity = default_model_identity()

    # Assert
    assert identity.version == "best"
    assert identity.sha256 == expected
    assert identity.artifact == str(artifact)


def test_default_model_identity_rejects_invalid_sha_env(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setenv("PPE_MODEL_SHA256", "no-es-un-sha")

    # Act / Assert
    with pytest.raises(ValueError, match="SHA256"):
        default_model_identity()


def test_default_model_identity_without_path_has_no_sha(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.delenv("PPE_MODEL_PATH", raising=False)
    monkeypatch.delenv("PPE_MODEL_VERSION", raising=False)
    monkeypatch.delenv("PPE_MODEL_SHA256", raising=False)

    # Act
    identity = default_model_identity()

    # Assert
    assert identity.version == "unknown"
    assert identity.sha256 is None
    assert identity.artifact is None
    assert identity.reference == "version:unknown"


def test_default_model_identity_reads_version_and_artifact(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setenv("PPE_MODEL_VERSION", MODEL_VERSION)
    monkeypatch.setenv("PPE_MODEL_PATH", "C:/models/yolo11s-clean/best.pt")
    monkeypatch.delenv("PPE_MODEL_SHA256", raising=False)

    # Act
    identity = default_model_identity()

    # Assert
    assert identity.version == MODEL_VERSION
    assert identity.artifact == "C:/models/yolo11s-clean/best.pt"
    assert identity.sha256 is None


def test_default_model_version_uses_explicit_env(monkeypatch: pytest.MonkeyPatch) -> None:
    # Arrange
    monkeypatch.setenv("PPE_MODEL_VERSION", MODEL_VERSION)

    # Act
    version = default_model_version()

    # Assert
    assert version == MODEL_VERSION


def test_model_identity_exposes_artifact_path(tmp_path: Path) -> None:
    # Arrange
    artifact = tmp_path / "best.pt"
    identity = _identity(sha256=MODEL_SHA, artifact=str(artifact))

    # Act
    reference = identity.reference

    # Assert
    assert identity.artifact == str(artifact)
    assert reference == f"sha256:{MODEL_SHA}"


def test_model_identity_reference_matches_mlflow_tag() -> None:
    # Arrange
    identity = _identity(sha256=MODEL_SHA)
    summary = {
        "model": {"path": "C:/models/best.pt", "sha256": MODEL_SHA},
        "dataset": {"path": "C:/data/data.yaml", "split": "test", "yaml_sha256": YAML_SHA},
        "config": {"imgsz": 640, "conf": 0.001, "iou": 0.7, "seed": 42, "device": "cpu"},
        "images": 1,
        "instances": 1,
        "metrics": {
            "metrics/precision(B)": 0.5,
            "metrics/recall(B)": 0.5,
            "metrics/mAP50(B)": 0.5,
            "metrics/mAP50-95(B)": 0.5,
        },
        "per_class": {"helmet": {"p": 0.5, "r": 0.5, "ap50": 0.5, "ap": 0.5}},
    }

    # Act
    payload = build_run_payload(summary)

    # Assert
    assert payload.tags["model_reference"] == identity.reference


def test_api_response_includes_model_identity() -> None:
    # Arrange
    identity = _identity()
    client = _client(identity)

    # Act
    body = _post(client)

    # Assert
    assert body["model_version"] == MODEL_VERSION
    assert body["model_sha256"] == MODEL_SHA
    assert body["model_artifact"] == "C:/models/yolo11s-clean/best.pt"
    assert body["model_reference"] == f"sha256:{MODEL_SHA}"


def test_api_two_versions_are_distinguishable() -> None:
    # Arrange
    first = _client(_identity(version="v1", sha256=MODEL_SHA))
    second = _client(_identity(version="v2", sha256=OTHER_SHA))

    # Act
    first_body = _post(first)
    second_body = _post(second)

    # Assert
    assert first_body["model_version"] != second_body["model_version"]
    assert first_body["model_sha256"] != second_body["model_sha256"]
    assert first_body["model_reference"] != second_body["model_reference"]


def test_api_falls_back_to_version_reference() -> None:
    # Arrange
    identity = _identity(sha256=None, artifact=None)
    client = _client(identity)

    # Act
    body = _post(client)

    # Assert
    assert body["model_sha256"] is None
    assert body["model_artifact"] is None
    assert body["model_reference"] == f"version:{MODEL_VERSION}"


def test_api_openapi_documents_model_identity() -> None:
    # Arrange
    client = _client(_identity())

    # Act
    schema = client.get("/openapi.json").json()

    # Assert
    properties = schema["components"]["schemas"]["PredictResponse"]["properties"]
    assert "model_version" in properties
    assert "model_sha256" in properties
    assert "model_artifact" in properties
    assert "model_reference" in properties


def test_grpc_response_includes_model_identity() -> None:
    # Arrange
    identity = _identity()

    # Act
    with _grpc_stub(identity) as stub:
        response = _call(stub)

    # Assert
    assert response.model_version == MODEL_VERSION
    assert response.model_sha256 == MODEL_SHA
    assert response.model_artifact == "C:/models/yolo11s-clean/best.pt"
    assert response.model_reference == f"sha256:{MODEL_SHA}"


def test_grpc_two_versions_are_distinguishable() -> None:
    # Arrange
    first = _identity(version="v1", sha256=MODEL_SHA)
    second = _identity(version="v2", sha256=OTHER_SHA)

    # Act
    with _grpc_stub(first) as stub:
        first_response = _call(stub)
    with _grpc_stub(second) as stub:
        second_response = _call(stub)

    # Assert
    assert first_response.model_version != second_response.model_version
    assert first_response.model_sha256 != second_response.model_sha256
    assert first_response.model_reference != second_response.model_reference


def test_grpc_falls_back_to_version_reference() -> None:
    # Arrange
    identity = _identity(sha256=None, artifact=None)

    # Act
    with _grpc_stub(identity) as stub:
        response = _call(stub)

    # Assert
    assert response.model_sha256 == ""
    assert response.model_artifact == ""
    assert response.model_reference == f"version:{MODEL_VERSION}"


def test_grpc_proto_defines_model_identity_fields() -> None:
    # Arrange
    fields = ppe_pb2.PredictResponse.DESCRIPTOR.fields_by_name

    # Act / Assert
    assert "model_version" in fields
    assert "model_sha256" in fields
    assert "model_artifact" in fields
    assert "model_reference" in fields
