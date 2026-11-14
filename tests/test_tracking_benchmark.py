"""Pruebas de la medición de inferencia y el registro del modelo (rúbrica M3)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ppe_detection.tracking import (
    DEFAULT_BENCHMARK_EXPERIMENT,
    DEFAULT_MODEL_ALIAS,
    DEFAULT_MODEL_NAME,
    TrackingError,
    build_benchmark_payload,
    build_model_bundle,
    latency_stats,
    parse_args,
)

SHA256 = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"


def test_latency_stats_summarizes_mean_p95_and_throughput() -> None:
    """AC-009.1: la sesión mide latencia media, p95 y throughput."""
    # Arrange
    samples = [100.0, 200.0, 300.0, 400.0, 500.0]

    # Act
    stats = latency_stats(samples)

    # Assert
    assert stats.mean_ms == pytest.approx(300.0)
    assert stats.p95_ms == pytest.approx(500.0)
    assert stats.max_ms == pytest.approx(500.0)
    assert stats.throughput_fps == pytest.approx(1000.0 / 300.0)


def test_latency_stats_uses_nearest_rank_for_p95() -> None:
    """AC-009.1: el p95 es conservador y no interpola con muestras pequeñas."""
    # Arrange
    samples = [float(value) for value in range(1, 21)]

    # Act
    stats = latency_stats(samples)

    # Assert
    assert stats.p95_ms == pytest.approx(19.0)


def test_latency_stats_accepts_a_single_sample() -> None:
    """AC-009.1: una sola muestra es un caso válido de la medición."""
    # Arrange / Act
    stats = latency_stats([150.0])

    # Assert
    assert stats.mean_ms == pytest.approx(150.0)
    assert stats.p95_ms == pytest.approx(150.0)
    assert stats.throughput_fps == pytest.approx(1000.0 / 150.0)


@pytest.mark.parametrize("samples", [[], [0.0], [-1.0], [float("nan")]])
def test_latency_stats_rejects_invalid_samples(samples: list[float]) -> None:
    """AC-009.1: el resumen rechaza muestras vacías, no positivas o no finitas."""
    # Arrange / Act / Assert
    with pytest.raises(TrackingError):
        latency_stats(samples)


def test_build_benchmark_payload_registers_reproducible_parameters() -> None:
    """AC-009.1: el run conserva configuración, métricas y referencia del modelo."""
    # Arrange
    samples = [120.0, 150.0, 180.0]

    # Act
    payload = build_benchmark_payload(
        model_path="artifacts/best.pt",
        model_sha256=SHA256,
        samples_ms=samples,
        imgsz=640,
        conf=0.25,
        iou=0.7,
        device="cpu",
        images=2,
        iterations=3,
        detections_total=4,
    )

    # Assert
    assert payload.params["imgsz"] == "640"
    assert payload.params["conf"] == "0.25"
    assert payload.params["device"] == "cpu"
    assert payload.params["seed"] == "42"
    assert payload.metrics["latency_mean_ms"] == pytest.approx(150.0)
    assert payload.metrics["throughput_fps"] == pytest.approx(1000.0 / 150.0, abs=1e-3)
    assert payload.metrics["detections_per_image"] == pytest.approx(2.0)
    assert payload.tags["model_reference"] == f"sha256:{SHA256}"
    assert payload.tags["experiment_kind"] == "inference"


def test_build_benchmark_payload_rejects_invalid_sha256() -> None:
    """AC-009.1: sin SHA256 válido no se registra el run."""
    # Arrange / Act / Assert
    with pytest.raises(TrackingError):
        build_benchmark_payload(
            model_path="artifacts/best.pt",
            model_sha256="no-es-un-sha",
            samples_ms=[100.0],
            imgsz=640,
            conf=0.25,
            iou=0.7,
            device="cpu",
            images=1,
            iterations=1,
        )


@pytest.mark.parametrize("images,iterations", [(0, 1), (1, 0)])
def test_build_benchmark_payload_rejects_empty_workload(images: int, iterations: int) -> None:
    """AC-009.1: no se registra una medición sin imágenes o sin iteraciones."""
    # Arrange / Act / Assert
    with pytest.raises(TrackingError):
        build_benchmark_payload(
            model_path="artifacts/best.pt",
            model_sha256=SHA256,
            samples_ms=[100.0],
            imgsz=640,
            conf=0.25,
            iou=0.7,
            device="cpu",
            images=images,
            iterations=iterations,
        )


def test_parser_exposes_benchmark_with_comparable_defaults() -> None:
    """AC-009.2: la CLI permite repetir la medición con la misma configuración."""
    # Arrange / Act
    args = parse_args(["benchmark", "--model", "best.pt", "--images", "samples"])

    # Assert
    assert args.command == "benchmark"
    assert args.iterations == 30
    assert args.imgsz == 640
    assert args.conf == 0.25
    assert args.experiment == DEFAULT_BENCHMARK_EXPERIMENT


def test_parser_exposes_register_with_registry_defaults() -> None:
    """AC-009.3: la CLI registra la versión con alias de producción."""
    # Arrange / Act
    args = parse_args(["register", "--run-id", "abc", "--model", "best.pt"])

    # Assert
    assert args.command == "register"
    assert args.name == DEFAULT_MODEL_NAME
    assert args.alias == DEFAULT_MODEL_ALIAS
    assert args.model_card == Path("docs/model-card.md")
    assert args.no_weights is False


def test_build_model_bundle_writes_identity_and_weights(tmp_path: Path) -> None:
    """AC-009.3: el paquete registrado incluye identidad, Model Card y pesos."""
    # Arrange
    model = tmp_path / "best.pt"
    model.write_bytes(b"pesos")
    card = tmp_path / "model-card.md"
    card.write_text("# Model Card\n", encoding="utf-8")

    # Act
    bundle = build_model_bundle(
        tmp_path / "bundle",
        identity={"reference": f"sha256:{SHA256}", "version": "yolo11s-clean"},
        model_path=model,
        model_card=card,
    )

    # Assert
    identity = json.loads((bundle / "model_identity.json").read_text(encoding="utf-8"))
    assert identity["reference"] == f"sha256:{SHA256}"
    assert (bundle / "best.pt").read_bytes() == b"pesos"
    assert (bundle / "MODEL_CARD.md").is_file()
    assert (bundle / "README.md").is_file()


def test_build_model_bundle_can_omit_weights(tmp_path: Path) -> None:
    """AC-009.3: sin pesos el paquete sigue siendo una referencia verificable."""
    # Arrange
    model = tmp_path / "best.pt"
    model.write_bytes(b"pesos")

    # Act
    bundle = build_model_bundle(
        tmp_path / "bundle",
        identity={"reference": f"sha256:{SHA256}"},
        model_path=model,
        include_weights=False,
    )

    # Assert
    assert (bundle / "model_identity.json").is_file()
    assert not (bundle / "best.pt").exists()
