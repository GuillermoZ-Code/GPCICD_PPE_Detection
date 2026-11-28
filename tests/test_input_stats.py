"""HU-038 — Pruebas de estadísticas de entrada para deriva."""

from __future__ import annotations

from typing import Any, cast

import numpy as np
import pytest

from ppe_detection.contracts import ImageData
from ppe_detection.io.stats import (
    ImageStats,
    InputStatsError,
    image_statistics,
    summarize_statistics,
)


def _image(array: np.ndarray) -> ImageData:
    height, width = array.shape[:2]
    return ImageData(array=array, width=width, height=height, format="png")


def test_image_statistics_calculates_size_aspect_and_brightness() -> None:
    """AC-01: tamaño, relación de aspecto y brillo se calculan por imagen."""

    # Arrange
    array = np.full((10, 20, 3), (10, 20, 30), dtype=np.uint8)

    # Act
    stats = image_statistics(_image(array))

    # Assert
    assert stats.width == 20
    assert stats.height == 10
    assert stats.aspect_ratio == pytest.approx(2.0)
    assert stats.brightness_mean == pytest.approx(18.15)
    assert stats.brightness_std == pytest.approx(0.0)


def test_image_statistics_does_not_keep_the_image() -> None:
    """AC-02: el resultado solo contiene números, no píxeles ni metadatos personales."""

    # Arrange
    array = np.zeros((4, 4, 3), dtype=np.uint8)

    # Act
    stats = image_statistics(_image(array))

    # Assert
    assert isinstance(stats, ImageStats)
    assert not hasattr(stats, "array")
    assert set(ImageStats.__dataclass_fields__) == {
        "width",
        "height",
        "aspect_ratio",
        "brightness_mean",
        "brightness_std",
    }


def test_summary_aggregates_a_batch_without_images() -> None:
    """AC-01/AC-03: el resumen agrega un lote de estadísticas puras."""

    # Arrange
    first = image_statistics(_image(np.full((10, 20, 3), 10, dtype=np.uint8)))
    second = image_statistics(_image(np.full((20, 20, 3), 30, dtype=np.uint8)))

    # Act
    summary = summarize_statistics([first, second])

    # Assert
    assert summary.count == 2
    assert summary.mean_width == pytest.approx(20.0)
    assert summary.mean_height == pytest.approx(15.0)
    assert summary.mean_aspect_ratio == pytest.approx(1.5)
    assert summary.mean_brightness == pytest.approx(20.0)
    assert summary.min_brightness == pytest.approx(10.0)
    assert summary.max_brightness == pytest.approx(30.0)


def test_invalid_inputs_are_rejected() -> None:
    """AC-03: una entrada que no es ImageData o un lote vacío fallan."""

    # Assert
    with pytest.raises(InputStatsError, match="ImageData"):
        image_statistics(cast(Any, object()))
    with pytest.raises(InputStatsError, match="al menos una"):
        summarize_statistics([])
