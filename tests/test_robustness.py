"""HU-032 — Pruebas de perturbaciones de robustez."""

from __future__ import annotations

import numpy as np
import pytest

from ppe_detection.evaluation.robustness import (
    RobustnessError,
    add_gaussian_noise,
    adjust_brightness,
    apply_perturbation,
    resize_scale,
)


def _image(value: int = 100) -> np.ndarray:
    return np.full((4, 6, 3), value, dtype=np.uint8)


def test_brightness_is_deterministic_and_clipped() -> None:
    """AC-01/AC-03: el brillo escala y recorta sin salir de [0, 255]."""

    # Arrange
    image = _image(100)

    # Act
    darker = adjust_brightness(image, 0.5)
    brighter = adjust_brightness(image, 3.0)

    # Assert
    assert darker.dtype == np.uint8
    assert darker.shape == image.shape
    assert np.all(darker == 50)
    assert np.all(brighter == 255)


def test_gaussian_noise_is_reproducible_with_the_same_seed() -> None:
    """AC-01: la semilla fija hace reproducible el ruido."""

    # Arrange
    image = _image(120)

    # Act
    first = add_gaussian_noise(image, 10.0, seed=7)
    same = add_gaussian_noise(image, 10.0, seed=7)
    other = add_gaussian_noise(image, 10.0, seed=8)

    # Assert
    assert np.array_equal(first, same)
    assert not np.array_equal(first, other)
    assert first.dtype == np.uint8
    assert first.shape == image.shape


def test_resize_scale_changes_dimensions_and_preserves_channels() -> None:
    """AC-01/AC-03: la escala devuelve una imagen RGB con el tamaño esperado."""

    # Arrange
    image = _image(80)

    # Act
    resized = resize_scale(image, 0.5)

    # Assert
    assert resized.shape == (2, 3, 3)
    assert resized.dtype == np.uint8


def test_invalid_perturbation_parameters_are_rejected() -> None:
    """AC-03: imagen, factor, sigma y semilla inválidos fallan explícitamente."""

    # Assert
    with pytest.raises(RobustnessError, match="uint8"):
        adjust_brightness(np.zeros((4, 4, 3), dtype=np.float32), 1.0)
    with pytest.raises(RobustnessError, match="factor"):
        adjust_brightness(_image(), -1.0)
    with pytest.raises(RobustnessError, match="sigma"):
        add_gaussian_noise(_image(), -0.1)
    with pytest.raises(RobustnessError, match="factor de escala"):
        resize_scale(_image(), 0.0)
    with pytest.raises(RobustnessError, match="desconocida"):
        apply_perturbation(_image(), "blur")


def test_apply_perturbation_covers_the_canonical_names() -> None:
    """AC-01: las cuatro variantes se pueden aplicar desde un solo punto."""

    # Act
    clean = apply_perturbation(_image(), "clean")
    bright = apply_perturbation(_image(), "brightness", factor=1.5)
    noisy = apply_perturbation(_image(), "noise", sigma=5.0, seed=1)
    scaled = apply_perturbation(_image(), "scale", factor=2.0)

    # Assert
    assert clean.shape == (4, 6, 3)
    assert bright.shape == (4, 6, 3)
    assert noisy.shape == (4, 6, 3)
    assert scaled.shape == (8, 12, 3)
