"""Calibración de umbrales de confianza por clase (HU-029).

El módulo es puro: recibe etiquetas y predicciones ya calculadas y elige, por
clase, el umbral de confianza que maximiza F1. No carga Ultralytics ni el
dataset, de modo que la calibración se puede probar con casos sintéticos.

El resultado se exporta a ``configs/thresholds.yaml`` con el formato que puede
consumir el postprocesamiento.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ppe_detection.contracts import CLASSES
from ppe_detection.evaluation.metrics import match_detections, precision_recall_f1

DEFAULT_THRESHOLD = 0.25
DEFAULT_IOU = 0.5
DEFAULT_GRID: tuple[float, ...] = tuple(round(index / 100, 2) for index in range(1, 100))
THRESHOLDS_VERSION = 1

Box = tuple[float, float, float, float]


@dataclass(frozen=True, slots=True)
class GroundTruth:
    """Objeto anotado de una imagen, en coordenadas xyxy."""

    class_name: str
    bbox: Box

    def __post_init__(self) -> None:
        _validate_class_name(self.class_name)
        _validate_box(self.bbox, "bbox")


@dataclass(frozen=True, slots=True)
class Prediction:
    """Detección candidata con su confianza, en coordenadas xyxy."""

    class_name: str
    confidence: float
    bbox: Box

    def __post_init__(self) -> None:
        _validate_class_name(self.class_name)
        if (
            not isinstance(self.confidence, (int, float))
            or isinstance(self.confidence, bool)
            or not math.isfinite(float(self.confidence))
            or not 0.0 <= float(self.confidence) <= 1.0
        ):
            raise ValueError("confidence debe ser finita y estar en [0, 1]")
        _validate_box(self.bbox, "bbox")


@dataclass(frozen=True, slots=True)
class ImageRecord:
    """Etiquetas y predicciones de una imagen."""

    ground_truth: tuple[GroundTruth, ...]
    predictions: tuple[Prediction, ...]


@dataclass(frozen=True, slots=True)
class ThresholdMetrics:
    """Métricas de una clase en un umbral concreto."""

    class_name: str
    threshold: float
    tp: int
    fp: int
    fn: int
    precision: float
    recall: float
    f1: float


def _validate_class_name(class_name: str) -> None:
    if class_name not in CLASSES:
        raise ValueError(f"Clase desconocida: {class_name!r}")


def _validate_box(box: Sequence[float], name: str) -> None:
    if len(box) != 4 or not all(isinstance(value, (int, float)) for value in box):
        raise ValueError(f"{name} debe contener cuatro números xyxy")
    if not all(math.isfinite(float(value)) for value in box):
        raise ValueError(f"{name} debe contener números finitos")


def _validate_threshold(threshold: float) -> None:
    if (
        not isinstance(threshold, (int, float))
        or isinstance(threshold, bool)
        or not math.isfinite(float(threshold))
        or not 0.0 <= float(threshold) <= 1.0
    ):
        raise ValueError("threshold debe estar en [0, 1]")


def _validate_grid(thresholds: Sequence[float]) -> tuple[float, ...]:
    if not thresholds:
        raise ValueError("La rejilla de umbrales no puede estar vacía")
    for threshold in thresholds:
        _validate_threshold(threshold)
    return tuple(sorted({float(threshold) for threshold in thresholds}))


def _counts(
    records: Sequence[ImageRecord],
    class_name: str,
    threshold: float,
    iou_threshold: float,
) -> tuple[int, int, int]:
    tp = fp = fn = 0
    for record in records:
        gt_boxes = [item.bbox for item in record.ground_truth if item.class_name == class_name]
        pred_boxes = [
            item.bbox
            for item in record.predictions
            if item.class_name == class_name and item.confidence >= threshold
        ]
        matches = match_detections(gt_boxes, pred_boxes, iou_threshold=iou_threshold)
        matched = len(matches)
        tp += matched
        fp += len(pred_boxes) - matched
        fn += len(gt_boxes) - matched
    return tp, fp, fn


def _metrics(
    class_name: str,
    threshold: float,
    records: Sequence[ImageRecord],
    iou_threshold: float,
) -> ThresholdMetrics:
    tp, fp, fn = _counts(records, class_name, threshold, iou_threshold)
    precision, recall, f1 = precision_recall_f1(tp, fp, fn)
    return ThresholdMetrics(
        class_name=class_name,
        threshold=threshold,
        tp=tp,
        fp=fp,
        fn=fn,
        precision=precision,
        recall=recall,
        f1=f1,
    )


def evaluate_thresholds(
    records: Sequence[ImageRecord],
    thresholds: Mapping[str, float],
    *,
    iou_threshold: float = DEFAULT_IOU,
) -> dict[str, ThresholdMetrics]:
    """Calcula P, R y F1 por clase para un mapa de umbrales ya decidido."""
    result: dict[str, ThresholdMetrics] = {}
    for class_name in CLASSES:
        threshold = thresholds.get(class_name, DEFAULT_THRESHOLD)
        _validate_threshold(threshold)
        result[class_name] = _metrics(class_name, threshold, records, iou_threshold)
    return result


def calibrate_thresholds(
    records: Sequence[ImageRecord],
    thresholds: Sequence[float] = DEFAULT_GRID,
    *,
    iou_threshold: float = DEFAULT_IOU,
) -> dict[str, ThresholdMetrics]:
    """Elige por clase el umbral que maximiza F1 en ``records``.

    Si una clase no aparece ni en etiquetas ni en predicciones, se conserva el
    umbral por defecto: no hay evidencia para calibrarla.
    """
    grid = _validate_grid(thresholds)
    calibrated: dict[str, ThresholdMetrics] = {}
    for class_name in CLASSES:
        gt_total = sum(
            1 for record in records for item in record.ground_truth if item.class_name == class_name
        )
        pred_total = sum(
            1 for record in records for item in record.predictions if item.class_name == class_name
        )
        if gt_total == 0 or pred_total == 0:
            calibrated[class_name] = _metrics(class_name, DEFAULT_THRESHOLD, records, iou_threshold)
            continue
        candidates = [_metrics(class_name, threshold, records, iou_threshold) for threshold in grid]
        best = max(candidates, key=lambda item: (item.f1, item.precision, item.threshold))
        calibrated[class_name] = best
    return calibrated


def threshold_map(results: Mapping[str, ThresholdMetrics]) -> dict[str, float]:
    """Convierte el resultado de calibración en un mapa clase -> umbral."""
    return {class_name: results[class_name].threshold for class_name in CLASSES}


def write_thresholds(
    path: Path,
    results: Mapping[str, ThresholdMetrics],
    *,
    iou_threshold: float = DEFAULT_IOU,
) -> None:
    """Escribe el YAML consumible por el postprocesamiento."""
    missing = [class_name for class_name in CLASSES if class_name not in results]
    if missing:
        raise ValueError(f"Faltan clases en la calibración: {missing}")
    lines = [
        "# Umbrales de confianza por clase (HU-029).",
        "# Generado por ppe_detection.evaluation.thresholds; no editar a mano.",
        f"version: {THRESHOLDS_VERSION}",
        f"iou: {float(iou_threshold):.2f}",
        "thresholds:",
    ]
    for class_name in CLASSES:
        lines.append(f"  {class_name}: {results[class_name].threshold:.2f}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_thresholds(path: Path) -> dict[str, float]:
    """Lee el YAML simple de umbrales sin depender de PyYAML."""
    values: dict[str, float] = {}
    in_thresholds = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.strip() == "thresholds:":
            in_thresholds = True
            continue
        if not in_thresholds:
            continue
        key, separator, raw_value = line.strip().partition(":")
        if not separator:
            raise ValueError(f"Línea de umbral inválida: {raw_line!r}")
        class_name = key.strip()
        _validate_class_name(class_name)
        try:
            value = float(raw_value.strip())
        except ValueError as exc:
            raise ValueError(f"Umbral inválido para {class_name}: {raw_value!r}") from exc
        _validate_threshold(value)
        values[class_name] = value
    missing = [class_name for class_name in CLASSES if class_name not in values]
    if missing:
        raise ValueError(f"Faltan clases en {path}: {missing}")
    return values


def calibration_payload(
    results: Mapping[str, ThresholdMetrics],
    *,
    iou_threshold: float = DEFAULT_IOU,
    split: str = "valid",
) -> dict[str, Any]:
    """Resumen serializable para informes y trazabilidad."""
    return {
        "version": THRESHOLDS_VERSION,
        "split": split,
        "iou": iou_threshold,
        "thresholds": threshold_map(results),
        "metrics": {
            class_name: {
                "threshold": results[class_name].threshold,
                "tp": results[class_name].tp,
                "fp": results[class_name].fp,
                "fn": results[class_name].fn,
                "precision": results[class_name].precision,
                "recall": results[class_name].recall,
                "f1": results[class_name].f1,
            }
            for class_name in CLASSES
        },
    }


__all__ = [
    "DEFAULT_GRID",
    "DEFAULT_IOU",
    "DEFAULT_THRESHOLD",
    "GroundTruth",
    "ImageRecord",
    "Prediction",
    "ThresholdMetrics",
    "calibrate_thresholds",
    "calibration_payload",
    "evaluate_thresholds",
    "load_thresholds",
    "threshold_map",
    "write_thresholds",
]
