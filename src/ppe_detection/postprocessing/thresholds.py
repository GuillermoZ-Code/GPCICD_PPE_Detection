"""Postprocesamiento de detecciones con umbrales por clase (HU-036).

Lee ``configs/thresholds.yaml`` (HU-029) y filtra las detecciones que no alcanzan
el umbral de su clase. No modifica el contrato ``Detection`` ni la lista original.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from ppe_detection.contracts import CLASSES, Detection
from ppe_detection.evaluation.thresholds import DEFAULT_THRESHOLD, load_thresholds

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[3] / "configs" / "thresholds.yaml"


class ThresholdConfigError(ValueError):
    """La configuración de umbrales no existe, está incompleta o es inválida."""


@dataclass(frozen=True, slots=True)
class ThresholdConfig:
    """Mapa inmutable clase -> umbral con validación de las seis clases."""

    thresholds: Mapping[str, float]
    source: Path | None = None

    def __post_init__(self) -> None:
        missing = [class_name for class_name in CLASSES if class_name not in self.thresholds]
        extra = [class_name for class_name in self.thresholds if class_name not in CLASSES]
        if missing or extra:
            raise ThresholdConfigError(
                f"El mapa de umbrales debe cubrir exactamente {list(CLASSES)}; "
                f"faltan={missing}, sobran={extra}."
            )
        for class_name, value in self.thresholds.items():
            if (
                not isinstance(value, (int, float))
                or isinstance(value, bool)
                or not 0.0 <= float(value) <= 1.0
            ):
                raise ThresholdConfigError(
                    f"Umbral inválido para {class_name}: {value!r}; debe estar en [0, 1]."
                )

    @classmethod
    def default(cls) -> ThresholdConfig:
        """Configuración segura cuando no hay archivo: 0,25 para todas las clases."""
        return cls(dict.fromkeys(CLASSES, DEFAULT_THRESHOLD))


def load_threshold_config(path: Path | None = None) -> ThresholdConfig:
    """Carga el YAML de umbrales; si falta el archivo por defecto, usa 0,25.

    Una ruta explícita inexistente o un YAML inválido fallan con un mensaje claro,
    apto para detener el arranque del servicio.
    """
    candidate = Path(path) if path is not None else DEFAULT_CONFIG_PATH
    if not candidate.is_file():
        if path is None:
            return ThresholdConfig.default()
        raise ThresholdConfigError(f"No existe el archivo de umbrales: {candidate}")
    try:
        values = load_thresholds(candidate)
    except (OSError, UnicodeError, ValueError) as exc:
        raise ThresholdConfigError(
            f"Configuración de umbrales inválida en {candidate}: {exc}"
        ) from exc
    return ThresholdConfig(values, source=candidate)


def apply_thresholds(
    detections: Sequence[Detection],
    config: ThresholdConfig | None = None,
) -> list[Detection]:
    """Devuelve las detecciones que alcanzan el umbral de su clase, en orden."""
    active = config or load_threshold_config()
    return [
        detection
        for detection in detections
        if detection.confidence >= active.thresholds[detection.class_name]
    ]


__all__ = [
    "DEFAULT_CONFIG_PATH",
    "ThresholdConfig",
    "ThresholdConfigError",
    "apply_thresholds",
    "load_threshold_config",
]
