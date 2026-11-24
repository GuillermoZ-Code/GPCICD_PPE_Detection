"""Pruebas de los runs comparables en MLflow (HU-097, issue #153)."""

from __future__ import annotations

import pytest

from ppe_detection.tracking import TrackingError, build_comparison_payloads

SHA_A = "AA" * 32
SHA_B = "BB" * 32
SHA_C = "CC" * 32


def _summary(sha: str, *, seed: int = 42, imgsz: int = 640) -> dict[str, object]:
    return {
        "model": {"path": f"artifacts/{sha[:8].lower()}.pt", "sha256": sha},
        "dataset": {"path": "data.yaml", "split": "test"},
        "config": {
            "imgsz": imgsz,
            "conf": 0.001,
            "iou": 0.7,
            "seed": seed,
            "device": "cpu",
        },
        "metrics": {
            "metrics/precision(B)": 0.8,
            "metrics/recall(B)": 0.7,
            "metrics/mAP50(B)": 0.75,
            "metrics/mAP50-95(B)": 0.45,
        },
        "per_class": {"Gloves": {"p": 0.7, "r": 0.6, "ap50": 0.65, "ap": 0.4}},
        "images": 100,
        "instances": 200,
    }


def test_builds_one_payload_per_summary() -> None:
    """AC-01: tres resumenes producen tres runs."""
    # Arrange
    summaries = [_summary(SHA_A), _summary(SHA_B), _summary(SHA_C)]

    # Act
    runs = build_comparison_payloads(summaries)

    # Assert
    assert len(runs) == 3


def test_run_names_are_distinct() -> None:
    """AC-01: cada run se distingue por el SHA del modelo."""
    # Arrange
    summaries = [_summary(SHA_A), _summary(SHA_B), _summary(SHA_C)]

    # Act
    names = [name for name, _ in build_comparison_payloads(summaries)]

    # Assert
    assert len(set(names)) == 3


def test_shared_params_are_identical() -> None:
    """AC-01: los runs comparten imgsz, conf, iou, seed y particion."""
    # Arrange
    summaries = [_summary(SHA_A), _summary(SHA_B), _summary(SHA_C)]

    # Act
    payloads = [payload for _, payload in build_comparison_payloads(summaries)]

    # Assert
    for key in ("imgsz", "conf", "iou", "seed", "dataset_split"):
        assert len({payload.params[key] for payload in payloads}) == 1


def test_per_class_metrics_are_logged() -> None:
    """AC-01: cada run registra metricas por clase."""
    # Arrange
    summaries = [_summary(SHA_A), _summary(SHA_B)]

    # Act
    payloads = [payload for _, payload in build_comparison_payloads(summaries)]

    # Assert
    for payload in payloads:
        assert "Gloves_map50" in payload.metrics
        assert payload.metrics["Gloves_precision"] == pytest.approx(0.7)


def test_artifact_reference_uses_sha256() -> None:
    """AC-02: el run referencia el artefacto por SHA256."""
    # Arrange
    summaries = [_summary(SHA_A), _summary(SHA_B)]

    # Act
    payloads = [payload for _, payload in build_comparison_payloads(summaries)]

    # Assert
    assert payloads[0].tags["model_reference"] == f"sha256:{SHA_A}"
    assert payloads[1].tags["model_reference"] == f"sha256:{SHA_B}"


def test_rejects_different_seed() -> None:
    """AC-01: un run con otra semilla no es comparable."""
    # Arrange
    summaries = [_summary(SHA_A), _summary(SHA_B, seed=7)]

    # Act / Assert
    with pytest.raises(TrackingError, match="comparten"):
        build_comparison_payloads(summaries)


def test_rejects_different_imgsz() -> None:
    """AC-01: un run con otro imgsz no es comparable."""
    # Arrange
    summaries = [_summary(SHA_A), _summary(SHA_B, imgsz=320)]

    # Act / Assert
    with pytest.raises(TrackingError, match="comparten"):
        build_comparison_payloads(summaries)


def test_requires_at_least_two_summaries() -> None:
    """AC-01: comparar exige al menos dos resumenes."""
    # Arrange
    summaries = [_summary(SHA_A)]

    # Act / Assert
    with pytest.raises(TrackingError, match="dos"):
        build_comparison_payloads(summaries)
