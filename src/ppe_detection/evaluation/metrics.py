"""Métricas de detección versionadas (HU-008).

Funciones puras para IoU, emparejamiento, precision/recall/F1, AP y mAP. No
dependen de Ultralytics, GPU ni dataset; sirven para verificar el cálculo con
casos pequeños y reproducibles.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from math import isfinite

type Box = tuple[float, float, float, float]


def _coerce_box(box: Sequence[float]) -> Box:
    """Valida una caja xyxy y la devuelve como flotantes."""
    if len(box) != 4:
        raise ValueError("La caja debe tener cuatro valores xyxy.")
    values = tuple(float(value) for value in box)
    if not all(isfinite(value) for value in values):
        raise ValueError("La caja debe contener números finitos.")
    return (values[0], values[1], values[2], values[3])


def box_area(box: Sequence[float]) -> float:
    """Área de una caja xyxy; las cajas invertidas o degeneradas valen 0."""
    x1, y1, x2, y2 = _coerce_box(box)
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def iou(box_a: Sequence[float], box_b: Sequence[float]) -> float:
    """Intersección sobre unión de dos cajas xyxy en ``[0, 1]``."""
    ax1, ay1, ax2, ay2 = _coerce_box(box_a)
    bx1, by1, bx2, by2 = _coerce_box(box_b)
    inter_width = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    inter_height = max(0.0, min(ay2, by2) - max(ay1, by1))
    intersection = inter_width * inter_height
    union = box_area(box_a) + box_area(box_b) - intersection
    return intersection / union if union > 0 else 0.0


def match_detections(
    gt_boxes: Sequence[Sequence[float]],
    pred_boxes: Sequence[Sequence[float]],
    *,
    iou_threshold: float = 0.5,
) -> list[tuple[int, int, float]]:
    """Empareja cajas por IoU con criterio greedy y sin reutilizar índices.

    Devuelve ``(gt_index, pred_index, iou)`` ordenados por índice de ground truth.
    """
    if not 0.0 <= iou_threshold <= 1.0:
        raise ValueError("iou_threshold debe estar en [0, 1].")
    candidates: list[tuple[float, int, int]] = []
    for gt_index, gt_box in enumerate(gt_boxes):
        for pred_index, pred_box in enumerate(pred_boxes):
            overlap = iou(gt_box, pred_box)
            if overlap >= iou_threshold:
                candidates.append((overlap, gt_index, pred_index))
    candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    used_gt: set[int] = set()
    used_pred: set[int] = set()
    matches: list[tuple[int, int, float]] = []
    for overlap, gt_index, pred_index in candidates:
        if gt_index in used_gt or pred_index in used_pred:
            continue
        used_gt.add(gt_index)
        used_pred.add(pred_index)
        matches.append((gt_index, pred_index, overlap))
    return sorted(matches, key=lambda item: (item[0], item[1]))


def match_by_class(
    gt: Sequence[tuple[Sequence[float], int]],
    predictions: Sequence[tuple[Sequence[float], int]],
    *,
    iou_threshold: float = 0.5,
) -> list[tuple[int, int, float]]:
    """Empareja detecciones por clase y luego por IoU."""
    matches: list[tuple[int, int, float]] = []
    for class_id in sorted({class_id for _, class_id in gt}):
        gt_indices = [index for index, (_, value) in enumerate(gt) if value == class_id]
        pred_indices = [index for index, (_, value) in enumerate(predictions) if value == class_id]
        local_gt = [gt[index][0] for index in gt_indices]
        local_pred = [predictions[index][0] for index in pred_indices]
        for local_gt_index, local_pred_index, overlap in match_detections(
            local_gt, local_pred, iou_threshold=iou_threshold
        ):
            matches.append((gt_indices[local_gt_index], pred_indices[local_pred_index], overlap))
    return sorted(matches, key=lambda item: (item[0], item[1]))


def precision_recall_f1(tp: int, fp: int, fn: int) -> tuple[float, float, float]:
    """Calcula precision, recall y F1 a partir de verdaderos/falsos positivos."""
    if min(tp, fp, fn) < 0:
        raise ValueError("tp, fp y fn no pueden ser negativos.")
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def average_precision(recalls: Sequence[float], precisions: Sequence[float]) -> float:
    """AP con interpolación de todos los puntos; listas vacías valen 0."""
    if len(recalls) != len(precisions):
        raise ValueError("recalls y precisions deben tener la misma longitud.")
    if not recalls:
        return 0.0
    points: list[tuple[float, float]] = []
    for recall, precision in zip(recalls, precisions, strict=True):
        if not isfinite(recall) or not isfinite(precision):
            raise ValueError("recalls y precisions deben ser finitos.")
        points.append((min(max(recall, 0.0), 1.0), min(max(precision, 0.0), 1.0)))
    points.sort(key=lambda item: item[0])
    mrec = [0.0, *(recall for recall, _ in points), 1.0]
    mpre = [0.0, *(precision for _, precision in points), 0.0]
    for index in range(len(mpre) - 2, -1, -1):
        mpre[index] = max(mpre[index], mpre[index + 1])
    return sum((mrec[index + 1] - mrec[index]) * mpre[index + 1] for index in range(len(mrec) - 1))


def mean_average_precision(values: Mapping[str, float] | Sequence[float]) -> float:
    """Media de AP por clase; un mapping o una secuencia vacía vale 0."""
    sequence = list(values.values()) if isinstance(values, Mapping) else list(values)
    if not sequence:
        return 0.0
    if not all(isfinite(float(value)) for value in sequence):
        raise ValueError("Los valores de AP deben ser finitos.")
    return sum(float(value) for value in sequence) / len(sequence)


__all__ = [
    "Box",
    "average_precision",
    "box_area",
    "iou",
    "match_by_class",
    "match_detections",
    "mean_average_precision",
    "precision_recall_f1",
]
