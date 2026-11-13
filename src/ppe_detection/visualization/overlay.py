"""Dibujo de detecciones sobre la imagen (HU-003)."""

from __future__ import annotations

from collections.abc import Sequence

import cv2
import numpy as np

from ppe_detection.contracts import Detection, ImageData

#: Etiquetas legibles para la interfaz. El contrato conserva los nombres canónicos.
DISPLAY_NAMES: dict[str, str] = {
    "Gloves": "Guantes",
    "Vest": "Chaleco",
    "goggles": "Gafas",
    "helmet": "Casco",
    "mask": "Mascarilla",
    "safety_shoe": "Calzado",
}

#: Color RGB por clase, para que cada categoría se distinga de un vistazo.
COLORS: dict[str, tuple[int, int, int]] = {
    "Gloves": (214, 39, 40),
    "Vest": (31, 119, 180),
    "goggles": (44, 160, 44),
    "helmet": (255, 127, 14),
    "mask": (148, 103, 189),
    "safety_shoe": (23, 190, 207),
}
FALLBACK_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)
FONT = cv2.FONT_HERSHEY_SIMPLEX


def _bgr(color: tuple[int, int, int]) -> tuple[int, int, int]:
    """Convierte un color RGB a BGR, que es lo que espera OpenCV."""
    red, green, blue = color
    return blue, green, red


def format_label(detection: Detection) -> str:
    """Devuelve la etiqueta legible: categoría en español y confianza."""
    name = DISPLAY_NAMES.get(detection.class_name, detection.class_name)
    return f"{name} {detection.confidence:.2f}"


def _draw_box(
    canvas: np.ndarray,
    image: ImageData,
    detection: Detection,
    thickness: int,
    font_scale: float,
) -> None:
    scale_x = image.width / detection.image_width
    scale_y = image.height / detection.image_height
    x1 = min(max(round(detection.bbox[0] * scale_x), 0), image.width - 1)
    y1 = min(max(round(detection.bbox[1] * scale_y), 0), image.height - 1)
    x2 = min(max(round(detection.bbox[2] * scale_x), x1 + 1), image.width - 1)
    y2 = min(max(round(detection.bbox[3] * scale_y), y1 + 1), image.height - 1)
    color = _bgr(COLORS.get(detection.class_name, FALLBACK_COLOR))

    cv2.rectangle(canvas, (x1, y1), (x2, y2), color, thickness)

    text = format_label(detection)
    (text_width, text_height), baseline = cv2.getTextSize(text, FONT, font_scale, 1)
    top = y1 - text_height - baseline - 2
    if top < 0:
        top = y1 + 2
    bottom = top + text_height + baseline + 2
    cv2.rectangle(canvas, (x1, top), (x1 + text_width + 4, bottom), color, -1)
    cv2.putText(
        canvas,
        text,
        (x1 + 2, top + text_height + 1),
        FONT,
        font_scale,
        TEXT_COLOR,
        1,
        cv2.LINE_AA,
    )


def draw_detections(
    image: ImageData,
    detections: Sequence[Detection],
    *,
    thickness: int | None = None,
    font_scale: float | None = None,
) -> ImageData:
    """Devuelve una copia de la imagen con una caja y una etiqueta por detección.

    No modifica la imagen de entrada. Si el lienzo tiene un tamaño distinto al de la
    detección, las coordenadas se escalan proporcionalmente.
    """
    canvas = cv2.cvtColor(image.array, cv2.COLOR_RGB2BGR)
    if detections:
        base = max(image.width, image.height)
        box_thickness = thickness if thickness is not None else max(1, round(base / 400))
        text_scale = font_scale if font_scale is not None else max(0.4, base / 1600)
        for detection in detections:
            _draw_box(canvas, image, detection, box_thickness, text_scale)
    rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
    return ImageData(
        array=rgb,
        width=image.width,
        height=image.height,
        format=image.format,
        source=image.source,
    )
