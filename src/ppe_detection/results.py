"""Contrato de resultado de inferencia: colección vacía sin detecciones (HU-004).

Una inferencia exitosa sin objetos es un resultado válido (AC-004.1) que no se
clasifica como error (AC-004.2) y cuya redacción evita afirmar incumplimiento o
ausencia real de EPP (AC-004.3). API (HU-006), interfaz (HU-007) y gRPC (HU-010)
consumen este contrato.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ppe_detection.contracts import CLASSES, Detection

#: Mensaje exacto para una inferencia exitosa sin detecciones. Redacción por
#: detección ("no se detectaron"), no por ausencia ("no hay") ni por norma.
NO_DETECTIONS_MESSAGE: str = "No se detectaron objetos EPP en la imagen."

#: Nota de uso responsable para API/UI (HU-006/007/010). No forma parte del
#: mensaje de resultado: declara el alcance del reporte sin conclusiones
#: normativas (AC-004.3).
RESPONSIBLE_USE_NOTE: str = (
    "Este resultado solo reporta detecciones: la ausencia de detección no indica "
    "ausencia real de EPP ni constituye un incumplimiento."
)


@dataclass(frozen=True, slots=True)
class InferenceResult:
    """Resultado clasificado de una inferencia de detección de EPP.

    - ``detections``: colección de ``Detection`` post-filtrado de HU-002.
    - ``is_empty``: inferencia exitosa sin objetos (`[]`); `False` si hay error.
    - ``is_error``: `True` solo ante fallos reales o violación del contrato.
    - ``message``: resumen en español listo para presentar al usuario.
    """

    detections: tuple[Detection, ...]
    is_empty: bool
    is_error: bool
    message: str


def _summarize(detections: tuple[Detection, ...]) -> str:
    """Resume las detecciones por clase en orden canónico del catálogo."""
    if not detections:
        return NO_DETECTIONS_MESSAGE

    counts: dict[str, int] = {}
    for detection in detections:
        counts[detection.class_name] = counts.get(detection.class_name, 0) + 1

    canonical_index = {name: index for index, name in enumerate(CLASSES)}
    ordered = sorted(counts.items(), key=lambda item: canonical_index[item[0]])
    listing = ", ".join(f"{name} (x{count})" for name, count in ordered)

    total = len(detections)
    verb = "Se detectó" if total == 1 else "Se detectaron"
    noun = "objeto" if total == 1 else "objetos"
    return f"{verb} {total} {noun} EPP: {listing}."


def build_inference_result(detections: Sequence[Detection] | None) -> InferenceResult:
    """Construye el resultado de una inferencia exitosa con su semántica.

    - `None` representa una respuesta sin colección: error de contrato (FR-004),
      no se normaliza a vacío.
    - Vacío (`[]`) es `is_empty=True`, `is_error=False` y `NO_DETECTIONS_MESSAGE`.

    Args:
        detections: detecciones post-filtrado del detector, o `None` si el
            modelo no devolvió una colección.

    Returns:
        Resultado clasificado determinista, sin excepciones para entradas válidas.
    """
    if detections is None:
        return InferenceResult(
            detections=(),
            is_empty=False,
            is_error=True,
            message="Error de inferencia: la ejecución no devolvió una colección de detecciones.",
        )
    collected = tuple(detections)
    return InferenceResult(
        detections=collected,
        is_empty=not collected,
        is_error=False,
        message=_summarize(collected),
    )


def build_error_result(error: BaseException) -> InferenceResult:
    """Construye el resultado de un fallo real de inferencia (AC-004.2.

    Args:
        error: excepción producida por la carga o la inferencia (imagen
            corrupta, artefacto ausente, dependencia faltante, etc.).

    Returns:
        Resultado clasificado como error, distinto del caso vacío.
    """
    return InferenceResult(
        detections=(),
        is_empty=False,
        is_error=True,
        message=f"Error de inferencia: {type(error).__name__}",
    )
