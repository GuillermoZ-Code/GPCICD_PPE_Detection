"""Casos dorados de las métricas de detección (HU-033).

Protegen IoU, emparejamiento, precision/recall/F1, AP y mAP con datos sintéticos.
No usan GPU, dataset, red ni las dependencias opcionales de inferencia.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from ppe_detection.evaluation import metrics

TOL = 1e-12


def test_golden_iou_known_cases() -> None:
    """AC-01: IoU para cajas idénticas, disjuntas, parciales y anidadas."""

    # Arrange
    cases = [
        ((0, 0, 10, 10), (0, 0, 10, 10), 1.0),
        ((0, 0, 10, 10), (20, 20, 30, 30), 0.0),
        ((0, 0, 10, 10), (5, 0, 15, 10), 1 / 3),
        ((0, 0, 10, 10), (2, 2, 8, 8), 0.36),
    ]

    # Act / Assert
    for box_a, box_b, expected in cases:
        assert metrics.iou(box_a, box_b) == pytest.approx(expected, abs=TOL)


def test_golden_match_detections() -> None:
    """AC-01: el emparejamiento greedy no reutiliza una predicción."""

    # Arrange
    gt = [(0, 0, 10, 10), (20, 20, 30, 30)]
    predictions = [(0, 0, 10, 10), (1, 1, 9, 9), (20, 20, 30, 30)]

    # Act
    matches = metrics.match_detections(gt, predictions, iou_threshold=0.5)

    # Assert
    assert matches == [(0, 0, 1.0), (1, 2, 1.0)]


def test_golden_match_by_class() -> None:
    """AC-01: clases distintas no se emparejan aunque sus cajas se solapen."""

    # Arrange
    gt = [((0, 0, 10, 10), 0), ((20, 20, 30, 30), 1)]
    predictions = [((0, 0, 10, 10), 1), ((20, 20, 30, 30), 1)]

    # Act
    matches = metrics.match_by_class(gt, predictions)

    # Assert
    assert matches == [(1, 1, 1.0)]


def test_golden_precision_recall_f1() -> None:
    """AC-01: P, R y F1 con TP/FP/FN conocidos y sin división por cero."""

    # Arrange / Act
    perfect = metrics.precision_recall_f1(4, 0, 0)
    partial = metrics.precision_recall_f1(2, 1, 1)
    empty = metrics.precision_recall_f1(0, 0, 0)

    # Assert
    assert perfect == pytest.approx((1.0, 1.0, 1.0), abs=TOL)
    assert partial == pytest.approx((2 / 3, 2 / 3, 2 / 3), abs=TOL)
    assert empty == pytest.approx((0.0, 0.0, 0.0), abs=TOL)


def test_golden_average_precision() -> None:
    """AC-01: AP con interpolación de todos los puntos."""

    # Arrange
    recalls = [0.0, 0.5, 1.0]
    precisions = [1.0, 0.5, 0.25]

    # Act
    ap = metrics.average_precision(recalls, precisions)

    # Assert
    assert ap == pytest.approx(0.375, abs=TOL)


def test_golden_mean_average_precision() -> None:
    """AC-01: mAP es la media de AP por clase."""

    # Arrange
    per_class = {"helmet": 0.375, "vest": 0.625}

    # Act
    mean_ap = metrics.mean_average_precision(per_class)

    # Assert
    assert mean_ap == pytest.approx(0.5, abs=TOL)


def test_golden_composite_class_scenario() -> None:
    """AC-01: escenario compuesto con 2 TP, 1 FP y 1 FN."""

    # Arrange
    gt = [
        ((0, 0, 10, 10), 0),
        ((20, 20, 30, 30), 0),
        ((40, 40, 50, 50), 1),
    ]
    predictions = [
        ((0, 0, 10, 10), 0),
        ((20, 20, 30, 30), 0),
        ((60, 60, 70, 70), 1),
    ]

    # Act
    matches = metrics.match_by_class(gt, predictions)
    tp = len(matches)
    fp = len(predictions) - tp
    fn = len(gt) - tp
    precision, recall, f1 = metrics.precision_recall_f1(tp, fp, fn)

    # Assert
    assert tp == 2
    assert fp == 1
    assert fn == 1
    assert (precision, recall, f1) == pytest.approx((2 / 3, 2 / 3, 2 / 3), abs=TOL)


def test_golden_tolerance_is_explicit() -> None:
    """AC-02: la tolerancia es explícita y detecta una desviación apreciable."""

    # Arrange
    actual = metrics.average_precision([0.0, 0.5, 1.0], [1.0, 0.5, 0.25])
    expected = 0.375

    # Act / Assert
    assert abs(actual - expected) <= TOL
    assert abs(actual - (expected + 2 * TOL)) > TOL


def test_golden_suite_has_no_optional_imports() -> None:
    """AC-03: `metrics.py` no importa Ultralytics, torch, OpenCV ni YAML."""

    # Arrange
    source = Path(metrics.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])

    # Act / Assert
    assert imported.isdisjoint({"ultralytics", "torch", "cv2", "yaml"})
