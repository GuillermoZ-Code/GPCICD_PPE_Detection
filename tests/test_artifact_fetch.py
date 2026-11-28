"""Pruebas de descarga y verificación del modelo (HU-026).

Cubren AC-01, AC-02 y AC-03 con archivos locales y un `urlopen` simulado; no usan
red externa, GPU ni dataset.
"""

from __future__ import annotations

import hashlib
import io
from pathlib import Path
from typing import Any

import pytest

from ppe_detection.detection import artifact
from ppe_detection.detector_config import ModelManifest

PAYLOAD = b"pesos-de-prueba"
SHA = hashlib.sha256(PAYLOAD).hexdigest().upper()
WRONG_SHA = "0" * 64


class _Response(io.BytesIO):
    """Respuesta mínima compatible con el context manager de urlopen."""


def _manifest(url: str, sha: str = SHA) -> ModelManifest:
    return ModelManifest(
        name="ppe-detection",
        version="test-model",
        sha256=sha,
        url=url,
    )


def _write_manifest(path: Path, *, url: str, sha: str = SHA) -> Path:
    path.write_text(
        f'name = "ppe-detection"\nversion = "test-model"\nsha256 = "{sha}"\nurl = "{url}"\n',
        encoding="utf-8",
    )
    return path


def test_fetch_from_manifest_file_url(tmp_path: Path) -> None:
    """AC-01: copia un archivo file:// y devuelve el SHA verificado."""

    # Arrange
    source = tmp_path / "source.pt"
    source.write_bytes(PAYLOAD)
    destination = tmp_path / "models" / "best.pt"

    # Act
    result = artifact.fetch_artifact(_manifest(source.as_uri()), destination)

    # Assert
    assert destination.read_bytes() == PAYLOAD
    assert result.path == destination
    assert result.sha256 == SHA
    assert result.bytes_written == len(PAYLOAD)


def test_cli_fetch_success(tmp_path: Path) -> None:
    """AC-01: la CLI lee models.lock y descarga en --output."""

    # Arrange
    source = tmp_path / "source.pt"
    source.write_bytes(PAYLOAD)
    manifest = _write_manifest(tmp_path / "models.lock", url=source.as_uri())
    destination = tmp_path / "best.pt"

    # Act
    code = artifact.main(
        [
            "fetch",
            "--manifest",
            str(manifest),
            "--output",
            str(destination),
        ]
    )

    # Assert
    assert code == 0
    assert destination.read_bytes() == PAYLOAD


def test_fetch_rejects_sha_mismatch(tmp_path: Path) -> None:
    """AC-02: un SHA distinto aborta y no deja destino."""

    # Arrange
    source = tmp_path / "source.pt"
    source.write_bytes(PAYLOAD)
    destination = tmp_path / "best.pt"

    # Act / Assert
    with pytest.raises(artifact.ArtifactError, match="SHA256"):
        artifact.fetch_artifact(_manifest(source.as_uri(), WRONG_SHA), destination)
    assert not destination.exists()
    assert not destination.with_suffix(destination.suffix + ".part").exists()


def test_cli_fetch_sha_mismatch(tmp_path: Path) -> None:
    """AC-02: la CLI devuelve código no cero si el SHA no coincide."""

    # Arrange
    source = tmp_path / "source.pt"
    source.write_bytes(PAYLOAD)
    manifest = _write_manifest(
        tmp_path / "models.lock",
        url=source.as_uri(),
        sha=WRONG_SHA,
    )
    destination = tmp_path / "best.pt"

    # Act
    code = artifact.main(
        [
            "fetch",
            "--manifest",
            str(manifest),
            "--output",
            str(destination),
        ]
    )

    # Assert
    assert code == 1
    assert not destination.exists()


def test_fetch_http_uses_injected_urlopen(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-03: la descarga HTTP usa el urlopen inyectado, sin red real."""

    # Arrange
    calls: list[tuple[str, float]] = []

    def fake_urlopen(url: str, timeout: float) -> _Response:
        calls.append((url, timeout))
        return _Response(PAYLOAD)

    monkeypatch.setattr(artifact, "urlopen", fake_urlopen)
    destination = tmp_path / "best.pt"
    manifest = _manifest("https://example.test/model.pt")

    # Act
    result = artifact.fetch_artifact(manifest, destination, timeout=5.0)

    # Assert
    assert destination.read_bytes() == PAYLOAD
    assert result.sha256 == SHA
    assert calls == [("https://example.test/model.pt", 5.0)]


def test_fetch_cleans_temp_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-03/FR-006: un error de descarga no deja un `.part`."""

    # Arrange
    def failing_urlopen(url: str, timeout: float) -> Any:
        raise OSError("fallo simulado")

    monkeypatch.setattr(artifact, "urlopen", failing_urlopen)
    destination = tmp_path / "best.pt"

    # Act / Assert
    with pytest.raises(artifact.ArtifactError, match="descargar"):
        artifact.fetch_artifact(_manifest("https://example.test/model.pt"), destination)
    assert not destination.with_suffix(destination.suffix + ".part").exists()


def test_fetch_rejects_unsupported_scheme(tmp_path: Path) -> None:
    """FR-003: un esquema que no sea file/http/https falla con claridad."""

    # Act / Assert
    with pytest.raises(artifact.ArtifactError, match="Esquema"):
        artifact.fetch_artifact(
            _manifest("ftp://example.test/model.pt"),
            tmp_path / "best.pt",
        )


def test_fetch_does_not_replace_existing_on_failure(tmp_path: Path) -> None:
    """FR-004/FR-006: el destino existente no se toca si la verificación falla."""

    # Arrange
    source = tmp_path / "source.pt"
    source.write_bytes(PAYLOAD)
    destination = tmp_path / "best.pt"
    destination.write_bytes(b"modelo-anterior")

    # Act / Assert
    with pytest.raises(artifact.ArtifactError, match="SHA256"):
        artifact.fetch_artifact(_manifest(source.as_uri(), WRONG_SHA), destination)
    assert destination.read_bytes() == b"modelo-anterior"
