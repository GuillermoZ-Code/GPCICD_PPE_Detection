"""Pruebas de geometría de cajas (HU-003/HU-008)."""

from __future__ import annotations

import pytest

from ppe_detection.contracts import CLASSES, Detection
from ppe_detection.geometry import (
    clip_xyxy,
    is_degenerate,
    letterbox_box,
    letterbox_params,
    scale_xyxy,
    xywh_to_xyxy,
    xyxy_to_xywh,
)


def test_xyxy_to_xywh() -> None:
    """Convierte esquinas a origen, ancho y alto."""
    assert xyxy_to_xywh((10, 20, 40, 60)) == (10, 20, 30, 40)


def test_xyxy_to_xywh_with_negative_origin() -> None:
    """El origen negativo se conserva en la conversión."""
    assert xyxy_to_xywh((-5, -10, 5, 10)) == (-5, -10, 10, 20)


def test_xywh_to_xyxy() -> None:
    """Convierte origen, ancho y alto a esquinas."""
    assert xywh_to_xyxy((10, 20, 30, 40)) == (10, 20, 40, 60)


def test_xywh_to_xyxy_with_zero_size() -> None:
    """Una caja de tamaño cero conserva sus esquinas."""
    assert xywh_to_xyxy((5, 6, 0, 0)) == (5, 6, 5, 6)


def test_xyxy_roundtrip() -> None:
    """La conversión de ida y vuelta conserva la caja."""
    box = (11.5, 22.5, 111.5, 222.5)
    assert xywh_to_xyxy(xyxy_to_xywh(box)) == box


def test_clip_inside() -> None:
    """Una caja dentro de la imagen no cambia."""
    assert clip_xyxy((10, 20, 30, 40), 100, 100) == (10, 20, 30, 40)


def test_clip_outside() -> None:
    """Una caja fuera de la imagen se recorta a sus límites."""
    assert clip_xyxy((-10, -20, 130, 140), 100, 100) == (0, 0, 100, 100)


def test_clip_negative_values() -> None:
    """Las coordenadas negativas se llevan a cero."""
    assert clip_xyxy((-5, 10, 50, 60), 100, 100) == (0, 10, 50, 60)


def test_clip_invalid_dimensions() -> None:
    """Las dimensiones de la imagen deben ser positivas."""
    with pytest.raises(ValueError, match="positivos"):
        clip_xyxy((0, 0, 10, 10), 0, 100)


def test_degenerate_zero_width() -> None:
    """Una caja sin ancho es degenerada."""
    assert is_degenerate((10, 10, 10, 20)) is True


def test_degenerate_zero_height() -> None:
    """Una caja sin alto es degenerada."""
    assert is_degenerate((10, 10, 20, 10)) is True


def test_degenerate_min_size() -> None:
    """El tamaño mínimo configurable también marca cajas pequeñas."""
    assert is_degenerate((0, 0, 1, 20), min_size=2) is True
    assert is_degenerate((0, 0, 3, 20), min_size=2) is False


def test_scale_xyxy() -> None:
    """La escala se aplica por eje."""
    assert scale_xyxy((10, 20, 30, 40), 2, 3) == (20, 60, 60, 120)


def test_scale_rejects_invalid_factor() -> None:
    """Los factores de escala deben ser positivos."""
    with pytest.raises(ValueError, match="escala"):
        scale_xyxy((0, 0, 10, 10), 0, 1)


def test_letterbox_landscape() -> None:
    """Una imagen horizontal recibe relleno vertical."""
    assert letterbox_params(640, 480, 640) == (1.0, 0.0, 80.0)


def test_letterbox_portrait() -> None:
    """Una imagen vertical recibe relleno horizontal."""
    assert letterbox_params(480, 640, 640) == (1.0, 80.0, 0.0)


def test_letterbox_square() -> None:
    """Una imagen cuadrada no requiere relleno."""
    assert letterbox_params(100, 100, 640) == (6.4, 0.0, 0.0)


def test_letterbox_box() -> None:
    """La caja se escala y se desplaza con el relleno."""
    assert letterbox_box((0, 0, 640, 480), 640, 480, 640) == (0.0, 80.0, 640.0, 560.0)


def test_letterbox_invalid_target() -> None:
    """El lienzo destino debe ser positivo."""
    with pytest.raises(ValueError, match="positivos"):
        letterbox_params(640, 480, 0)


def test_geometry_supports_the_six_classes() -> None:
    """Las seis clases del catálogo se pueden convertir sin pérdida."""
    for class_id, class_name in enumerate(CLASSES):
        box = (float(class_id), 1.0, float(class_id + 10), 11.0)
        detection = Detection(
            class_id=class_id,
            class_name=class_name,
            confidence=0.5,
            bbox=box,
            image_width=100,
            image_height=100,
        )
        assert xywh_to_xyxy(xyxy_to_xywh(detection.bbox)) == box
