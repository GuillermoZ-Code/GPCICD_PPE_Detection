"""Pruebas de métricas de detección (HU-008)."""

from __future__ import annotations

import numpy as np
import pytest

from ppe_detection.evaluation.metrics import (
    average_precision,
    box_area,
    iou,
    match_by_class,
    match_detections,
    mean_average_precision,
    precision_recall_f1,
)


@pytest.mark.parametrize(
    ("box_a", "box_b", "expected"),
    [
        ((0, 0, 10, 10), (0, 0, 10, 10), 1.0),
        ((0, 0, 10, 10), (20, 20, 30, 30), 0.0),
        ((0, 0, 10, 10), (5, 0, 15, 10), 1 / 3),
        ((0, 0, 10, 10), (2, 2, 8, 8), 0.36),
        ((0, 0, 10, 10), (10, 0, 20, 10), 0.0),
        ((0, 0, 4, 4), (2, 2, 6, 6), 1 / 7),
    ],
)
def test_iou_known_cases(box_a, box_b, expected) -> None:
    """AC-008.1: IoU para cajas idénticas, disjuntas, anidadas y parciales."""
    assert iou(box_a, box_b) == pytest.approx(expected)


def test_iou_degenerate_is_zero() -> None:
    """AC-008.1: una caja sin área no produce división por cero."""
    assert iou((0, 0, 0, 10), (0, 0, 0, 10)) == 0.0


def test_iou_accepts_float32() -> None:
    """AC-008.1: los arreglos float32 se convierten a flotantes."""
    box = np.array([0, 0, 10, 10], dtype=np.float32).tolist()
    assert iou(box, box) == 1.0


def test_iou_out_of_range_boxes_are_supported() -> None:
    """AC-008.1: las cajas fuera de la imagen no rompen el cálculo."""
    assert iou((-5, -5, 5, 5), (0, 0, 10, 10)) == pytest.approx(1 / 7)


def test_iou_rejects_wrong_length() -> None:
    """El contrato exige cuatro valores xyxy."""
    with pytest.raises(ValueError, match="cuatro"):
        iou((0, 0, 1), (0, 0, 1, 1))


def test_iou_rejects_non_finite() -> None:
    """El contrato rechaza NaN e infinito."""
    with pytest.raises(ValueError, match="finitos"):
        iou((0, 0, float("nan"), 1), (0, 0, 1, 1))


@pytest.mark.parametrize(
    ("box", "expected"),
    [
        ((0, 0, 10, 10), 100.0),
        ((0, 0, 0, 10), 0.0),
        ((10, 10, 0, 0), 0.0),
    ],
)
def test_box_area(box, expected) -> None:
    """AC-008.1: área normal, nula e invertida."""
    assert box_area(box) == expected


def test_match_detections_perfect() -> None:
    """AC-008.2: una caja perfecta se empareja con IoU 1."""
    assert match_detections([(0, 0, 10, 10)], [(0, 0, 10, 10)]) == [(0, 0, 1.0)]


def test_match_detections_threshold() -> None:
    """AC-008.2: el umbral descarta coincidencias débiles."""
    assert match_detections([(0, 0, 10, 10)], [(5, 0, 15, 10)], iou_threshold=0.5) == []
    assert match_detections([(0, 0, 10, 10)], [(5, 0, 15, 10)], iou_threshold=0.3) != []


def test_match_detections_greedy_and_unique() -> None:
    """AC-008.2: una predicción no se reutiliza para dos objetos."""
    matches = match_detections(
        [(0, 0, 10, 10), (20, 20, 30, 30)],
        [(0, 0, 10, 10), (1, 1, 9, 9), (20, 20, 30, 30)],
    )
    assert matches == [(0, 0, 1.0), (1, 2, 1.0)]


def test_match_detections_empty() -> None:
    """AC-008.1: listas vacías devuelven una lista vacía."""
    assert match_detections([], []) == []


def test_match_detections_invalid_threshold() -> None:
    """El umbral IoU debe estar en [0, 1]."""
    with pytest.raises(ValueError, match="iou_threshold"):
        match_detections([], [], iou_threshold=1.5)


def test_match_by_class_separates_classes() -> None:
    """AC-008.2: clases distintas no se emparejan entre sí."""
    gt = [((0, 0, 10, 10), 0), ((20, 20, 30, 30), 1)]
    predictions = [((0, 0, 10, 10), 0), ((20, 20, 30, 30), 1)]
    assert match_by_class(gt, predictions) == [(0, 0, 1.0), (1, 1, 1.0)]


def test_match_by_class_empty() -> None:
    """AC-008.1: sin objetos no hay emparejamientos."""
    assert match_by_class([], []) == []


def test_precision_recall_f1_known() -> None:
    """AC-008.2: P, R y F1 se calculan por clase."""
    precision, recall, f1 = precision_recall_f1(tp=3, fp=1, fn=2)
    assert precision == pytest.approx(0.75)
    assert recall == pytest.approx(0.6)
    assert f1 == pytest.approx(2 * 0.75 * 0.6 / (0.75 + 0.6))


def test_precision_recall_f1_zero_denominators() -> None:
    """AC-008.2: sin objetos ni predicciones el resultado es cero."""
    assert precision_recall_f1(tp=0, fp=0, fn=0) == (0.0, 0.0, 0.0)


def test_precision_recall_f1_no_predictions() -> None:
    """AC-008.2: sin predicciones la precisión es cero y el recall también."""
    assert precision_recall_f1(tp=0, fp=0, fn=5) == (0.0, 0.0, 0.0)


def test_precision_recall_f1_negative_rejected() -> None:
    """Los conteos negativos son un error de contrato."""
    with pytest.raises(ValueError, match="negativos"):
        precision_recall_f1(tp=-1, fp=0, fn=0)


def test_average_precision_perfect() -> None:
    """AC-008.2: una curva perfecta tiene AP 1."""
    assert average_precision([0.0, 1.0], [1.0, 1.0]) == pytest.approx(1.0)


def test_average_precision_zero() -> None:
    """AC-008.2: una curva sin aciertos tiene AP 0."""
    assert average_precision([0.0, 1.0], [0.0, 0.0]) == 0.0


def test_average_precision_step() -> None:
    """AC-008.2: la interpolación por puntos calcula el área de la curva."""
    assert average_precision([0.0, 0.5, 1.0], [1.0, 0.5, 0.5]) == pytest.approx(0.5)


def test_average_precision_empty() -> None:
    """AC-008.1: una curva vacía vale 0."""
    assert average_precision([], []) == 0.0


def test_average_precision_mismatch() -> None:
    """Las listas de recall y precision deben tener la misma longitud."""
    with pytest.raises(ValueError, match="misma longitud"):
        average_precision([0.0], [1.0, 0.0])


def test_average_precision_unsorted() -> None:
    """AC-008.2: el orden de entrada no altera la interpolación."""
    assert average_precision([1.0, 0.0], [0.5, 1.0]) == pytest.approx(0.5)


def test_average_precision_clamps_values() -> None:
    """AC-008.2: los valores fuera de [0,1] se recortan."""
    assert average_precision([-0.5, 1.5], [0.5, 2.0]) == pytest.approx(1.0)


def test_mean_average_precision_sequence() -> None:
    """AC-008.2: mAP es la media de los AP por clase."""
    assert mean_average_precision([0.5, 1.0]) == pytest.approx(0.75)


def test_mean_average_precision_mapping() -> None:
    """AC-008.2: se acepta un mapping nombre -> AP."""
    assert mean_average_precision({"helmet": 0.5, "Vest": 1.0}) == pytest.approx(0.75)


def test_mean_average_precision_empty() -> None:
    """AC-008.1: sin clases el mAP es 0."""
    assert mean_average_precision([]) == 0.0
