"""Sesgo de tamaño: AP por clase y rango de área (HU-037).

Clasifica cajas por área relativa a la imagen y calcula AP para objetos pequeños,
medianos y grandes. Es un módulo puro: no carga YOLO ni el dataset.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from ppe_detection.contracts import CLASSES
from ppe_detection.evaluation.errors import ImageAnnotations
from ppe_detection.evaluation.metrics import average_precision, iou

SMALL_MAX: Final = 0.01
MEDIUM_MAX: Final = 0.04
BUCKETS: Final = ("small", "medium", "large")


class SizeBiasError(ValueError):
    """Caja o umbral inválido para el análisis por tamaño."""


@dataclass(frozen=True, slots=True)
class SizeMetrics:
    """AP y conteos de una clase en un rango de tamaño."""

    class_name: str
    bucket: str
    gt_count: int
    predictions: int
    average_precision: float
    precision: float
    recall: float


def _area(box: Sequence[float]) -> float:
    x1, y1, x2, y2 = (float(value) for value in box)
    return max(0.0, x2 - x1) * max(0.0, y2 - y1)


def size_bucket(
    box: Sequence[float],
    width: int,
    height: int,
    *,
    small_max: float = SMALL_MAX,
    medium_max: float = MEDIUM_MAX,
) -> str:
    """Clasifica una caja xyxy por su área relativa a la imagen."""
    if width <= 0 or height <= 0:
        raise SizeBiasError("width y height deben ser positivos")
    if not 0.0 <= small_max < medium_max <= 1.0:
        raise SizeBiasError("small_max y medium_max deben cumplir 0 <= small < medium <= 1")
    ratio = _area(box) / (width * height)
    if ratio < small_max:
        return "small"
    if ratio < medium_max:
        return "medium"
    return "large"


def _bucket_or_error(bucket: str) -> str:
    if bucket not in BUCKETS:
        raise SizeBiasError(f"bucket inválido: {bucket!r}; usa {BUCKETS}")
    return bucket


def average_precision_by_size(
    records: Sequence[ImageAnnotations],
    class_name: str,
    bucket: str,
    *,
    iou_threshold: float = 0.5,
    small_max: float = SMALL_MAX,
    medium_max: float = MEDIUM_MAX,
) -> SizeMetrics:
    """Calcula AP de una clase usando GT y predicciones del mismo rango de tamaño."""
    _bucket_or_error(bucket)
    if class_name not in CLASSES:
        raise SizeBiasError(f"Clase desconocida: {class_name!r}")
    if not 0.0 <= iou_threshold <= 1.0:
        raise SizeBiasError("iou_threshold debe estar en [0, 1]")

    gt_total = 0
    predictions = 0
    scored: list[tuple[float, bool]] = []
    for record in records:
        gt_items = [
            (index, item.bbox)
            for index, item in enumerate(record.ground_truth)
            if item.class_name == class_name
            and size_bucket(
                item.bbox,
                record.width,
                record.height,
                small_max=small_max,
                medium_max=medium_max,
            )
            == bucket
        ]
        pred_items = [
            (index, item)
            for index, item in enumerate(record.predictions)
            if item.class_name == class_name
            and item.confidence >= 0.0
            and size_bucket(
                item.bbox,
                record.width,
                record.height,
                small_max=small_max,
                medium_max=medium_max,
            )
            == bucket
        ]
        gt_total += len(gt_items)
        predictions += len(pred_items)
        unmatched = {index for index, _ in gt_items}
        gt_lookup = dict(gt_items)
        for _, prediction in sorted(pred_items, key=lambda item: item[1].confidence, reverse=True):
            best_index = None
            best_iou = 0.0
            for gt_index in unmatched:
                overlap = iou(prediction.bbox, gt_lookup[gt_index])
                if overlap > best_iou:
                    best_iou = overlap
                    best_index = gt_index
            is_tp = best_index is not None and best_iou >= iou_threshold
            if is_tp:
                unmatched.remove(best_index)
            scored.append((prediction.confidence, is_tp))

    if gt_total == 0:
        return SizeMetrics(class_name, bucket, 0, predictions, 0.0, 0.0, 0.0)

    scored.sort(key=lambda item: item[0], reverse=True)
    tp = fp = 0
    recalls: list[float] = []
    precisions: list[float] = []
    for _, is_tp in scored:
        tp += int(is_tp)
        fp += int(not is_tp)
        precisions.append(tp / (tp + fp))
        recalls.append(tp / gt_total)
    if not recalls:
        return SizeMetrics(class_name, bucket, gt_total, predictions, 0.0, 0.0, 0.0)
    ap = average_precision(recalls, precisions)
    final_precision = sum(1 for _, is_tp in scored if is_tp) / len(scored)
    final_recall = sum(1 for _, is_tp in scored if is_tp) / gt_total
    return SizeMetrics(class_name, bucket, gt_total, predictions, ap, final_precision, final_recall)


def evaluate_size_bias(
    records: Sequence[ImageAnnotations],
    *,
    iou_threshold: float = 0.5,
    small_max: float = SMALL_MAX,
    medium_max: float = MEDIUM_MAX,
) -> dict[str, dict[str, SizeMetrics]]:
    """Devuelve AP por clase y bucket para las seis clases canónicas."""
    return {
        class_name: {
            bucket: average_precision_by_size(
                records,
                class_name,
                bucket,
                iou_threshold=iou_threshold,
                small_max=small_max,
                medium_max=medium_max,
            )
            for bucket in BUCKETS
        }
        for class_name in CLASSES
    }


__all__ = [
    "BUCKETS",
    "MEDIUM_MAX",
    "SMALL_MAX",
    "SizeBiasError",
    "SizeMetrics",
    "average_precision_by_size",
    "evaluate_size_bias",
    "size_bucket",
]
