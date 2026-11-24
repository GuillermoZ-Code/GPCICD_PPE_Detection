"""Pruebas de la latencia como metrica del run (HU-100, issue #156)."""

from __future__ import annotations

import pytest

from ppe_detection.tracking import (
    ResolutionLatency,
    TrackingError,
    build_latency_payload,
    latency_stats,
)

SHA = "AB" * 32
SAMPLES = (100.0, 120.0, 140.0, 160.0, 200.0)


def _measurement(imgsz: int = 640) -> ResolutionLatency:
    return ResolutionLatency(imgsz=imgsz, samples_ms=SAMPLES)


def test_payload_has_p50_and_p95_per_resolution() -> None:
    """AC-01: p50 y p95 se registran por resolucion."""
    # Act
    payload = build_latency_payload(
        [_measurement(640)], hardware="i5-1235U", model_version="yolo26n", model_sha256=SHA
    )

    # Assert
    assert "p50_ms_640" in payload.metrics
    assert "p95_ms_640" in payload.metrics
    assert payload.metrics["p50_ms_640"] == pytest.approx(140.0)


def test_multiple_resolutions_are_separate_metrics() -> None:
    """AC-01: cada resolucion tiene sus propias metricas."""
    # Act
    payload = build_latency_payload(
        [_measurement(320), _measurement(640)],
        hardware="i5-1235U",
        model_version="yolo26n",
        model_sha256=SHA,
    )

    # Assert
    assert "p95_ms_320" in payload.metrics
    assert "p95_ms_640" in payload.metrics
    assert payload.params["resolutions"] == "320,640"


def test_payload_records_hardware_params() -> None:
    """AC-02: el hardware y la version son parametros del run."""
    # Act
    payload = build_latency_payload(
        [_measurement()], hardware="i5-1235U", model_version="yolo26n", model_sha256=SHA
    )

    # Assert
    assert payload.params["hardware"] == "i5-1235U"
    assert payload.params["model_version"] == "yolo26n"


def test_payload_references_model_by_sha() -> None:
    """AC-02: el run referencia el modelo por SHA256."""
    # Act
    payload = build_latency_payload(
        [_measurement()], hardware="cpu", model_version="yolo26n", model_sha256=SHA
    )

    # Assert
    assert payload.tags["model_reference"] == f"sha256:{SHA}"


def test_rejects_empty_measurements() -> None:
    """AC-01: sin mediciones no hay run."""
    # Act / Assert
    with pytest.raises(TrackingError, match="medicion"):
        build_latency_payload([], hardware="cpu", model_version="yolo26n", model_sha256=SHA)


def test_rejects_invalid_sha() -> None:
    """AC-02: el SHA debe ser hexadecimal de 64 caracteres."""
    # Act / Assert
    with pytest.raises(TrackingError, match="SHA256"):
        build_latency_payload(
            [_measurement()], hardware="cpu", model_version="yolo26n", model_sha256="abc"
        )


def test_p50_uses_nearest_rank() -> None:
    """AC-01: el p50 sigue el rango mas cercano."""
    # Act
    stats = latency_stats(SAMPLES)

    # Assert
    assert stats.p50_ms == 140.0
    assert stats.p95_ms == 200.0


def test_rejects_non_positive_samples() -> None:
    """AC-01: una muestra no positiva no es valida."""
    # Act / Assert
    with pytest.raises(TrackingError, match="positivas"):
        latency_stats([100.0, 0.0])
