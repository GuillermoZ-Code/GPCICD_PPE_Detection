"""Perturbaciones deterministas para evaluar robustez (HU-032).

Aplica brillo, ruido gaussiano y escala a imÃ¡genes RGB `uint8`. Las funciones son
puras y reciben la semilla cuando la perturbaciÃ³n es aleatoria.
"""

from __future__ import annotations

from typing import Final

import cv2
import numpy as np
from numpy.typing import NDArray

ImageArray = NDArray[np.uint8]
PERTURBATIONS: Final = ("clean", "brightness", "noise", "scale")
DEFAULT_SEED: Final = 42


class RobustnessError(ValueError):
    """Imagen o parÃ¡metro invÃ¡lido para una perturbaciÃ³n."""


def _validate_image(image: np.ndarray) -> None:
    if not isinstance(image, np.ndarray):
        raise RobustnessError("la imagen debe ser un arreglo NumPy")
    if image.dtype != np.uint8:
        raise RobustnessError("la imagen debe ser uint8")
    if image.ndim != 3 or image.shape[2] != 3:
        raise RobustnessError("la imagen debe tener forma (H, W, 3)")
    if image.shape[0] == 0 or image.shape[1] == 0:
        raise RobustnessError("la imagen no puede estar vacÃ­a")


def adjust_brightness(image: np.ndarray, factor: float) -> ImageArray:
    """Multiplica los canales por `factor` y recorta a [0, 255]."""
    _validate_image(image)
    if not np.isfinite(factor) or factor < 0:
        raise RobustnessError("factor de brillo debe ser finito y >= 0")
    scaled = image.astype(np.float32) * float(factor)
    return np.clip(scaled, 0, 255).astype(np.uint8)


def add_gaussian_noise(
    image: np.ndarray,
    sigma: float,
    *,
    seed: int = DEFAULT_SEED,
) -> ImageArray:
    """Suma ruido gaussiano con media 0 y desviaciÃ³n `sigma` (determinista)."""
    _validate_image(image)
    if not np.isfinite(sigma) or sigma < 0:
        raise RobustnessError("sigma debe ser finito y >= 0")
    if not isinstance(seed, int) or seed < 0:
        raise RobustnessError("seed debe ser un entero >= 0")
    rng = np.random.default_rng(seed)
    noise = rng.normal(0.0, float(sigma), size=image.shape)
    noisy = image.astype(np.float32) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)


def resize_scale(
    image: np.ndarray,
    factor: float,
    *,
    interpolation: int = cv2.INTER_LINEAR,
) -> ImageArray:
    """Escala la imagen por `factor` conservando los tres canales."""
    _validate_image(image)
    if not np.isfinite(factor) or factor <= 0:
        raise RobustnessError("factor de escala debe ser finito y > 0")
    height = max(1, round(image.shape[0] * float(factor)))
    width = max(1, round(image.shape[1] * float(factor)))
    resized = cv2.resize(image, (width, height), interpolation=interpolation)
    return np.asarray(resized, dtype=np.uint8)


def apply_perturbation(
    image: np.ndarray,
    name: str,
    *,
    factor: float = 1.0,
    sigma: float = 0.0,
    seed: int = DEFAULT_SEED,
) -> ImageArray:
    """Aplica una perturbaciÃ³n por nombre canÃ³nico."""
    if name == "clean":
        _validate_image(image)
        return image.copy()
    if name == "brightness":
        return adjust_brightness(image, factor)
    if name == "noise":
        return add_gaussian_noise(image, sigma, seed=seed)
    if name == "scale":
        return resize_scale(image, factor)
    raise RobustnessError(f"perturbaciÃ³n desconocida: {name!r}; usa {PERTURBATIONS}")


__all__ = [
    "DEFAULT_SEED",
    "PERTURBATIONS",
    "ImageArray",
    "RobustnessError",
    "add_gaussian_noise",
    "adjust_brightness",
    "apply_perturbation",
    "resize_scale",
]
