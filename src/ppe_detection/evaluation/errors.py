"""Análisis reutilizable de falsos positivos y negativos (HU-030).

Recibe cajas ya convertidas a píxeles y devuelve errores categorizados. No carga
YOLO, no lee imágenes y no publica archivos personales: el informe solo usa
conteos, clases y causas geométricas.
"""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from ppe_detection.contracts import CLASSES
from ppe_detection.evaluation.metrics import iou, match_detections, precision_recall_f1

Box = tuple[float, float, float, float]
FP_CATEGORIES = ("class_confusion", "duplicate", "localization", "small_object", "background")
FN_CATEGORIES = ("class_confusion", "localization", "small_object", "occlusion_or_missed")


@dataclass(frozen=True, slots=True)
class GroundTruthBox:
    """Objeto anotado de una imagen."""

    class_name: str
    bbox: Box

    def __post_init__(self) -> None:
        _validate_class(self.class_name)
        _validate_box(self.bbox)


@dataclass(frozen=True, slots=True)
class PredictionBox:
    """Detección candidata de una imagen."""

    class_name: str
    confidence: float
    bbox: Box

    def __post_init__(self) -> None:
        _validate_class(self.class_name)
        if (
            not isinstance(self.confidence, (int, float))
            or isinstance(self.confidence, bool)
            or not math.isfinite(float(self.confidence))
            or not 0.0 <= float(self.confidence) <= 1.0
        ):
            raise ValueError("confidence debe ser finita y estar en [0, 1]")
        _validate_box(self.bbox)


@dataclass(frozen=True, slots=True)
class ImageAnnotations:
    """Etiquetas, predicciones y dimensiones de una imagen."""

    image: str
    width: int
    height: int
    ground_truth: tuple[GroundTruthBox, ...]
    predictions: tuple[PredictionBox, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.image, str) or not self.image:
            raise ValueError("image no puede estar vacío")
        if not isinstance(self.width, int) or not isinstance(self.height, int):
            raise ValueError("width y height deben ser enteros")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("width y height deben ser positivos")


@dataclass(frozen=True, slots=True)
class ErrorCase:
    """Un FP o FN con su causa geométrica y su clase."""

    kind: str
    image: str
    class_name: str
    category: str
    confidence: float
    overlap: float
    area_ratio: float


@dataclass(frozen=True, slots=True)
class ErrorSummary:
    """Resultado agregado del análisis de errores."""

    images: int
    ground_truth: int
    predictions: int
    tp: int
    fp: int
    fn: int
    false_positives: tuple[ErrorCase, ...]
    false_negatives: tuple[ErrorCase, ...]
    category_counts: Mapping[str, int]
    per_class: Mapping[str, Mapping[str, int]]

    @property
    def precision(self) -> float:
        return precision_recall_f1(self.tp, self.fp, self.fn)[0]

    @property
    def recall(self) -> float:
        return precision_recall_f1(self.tp, self.fp, self.fn)[1]

    @property
    def f1(self) -> float:
        return precision_recall_f1(self.tp, self.fp, self.fn)[2]


def _validate_class(class_name: str) -> None:
    if class_name not in CLASSES:
        raise ValueError(f"Clase desconocida: {class_name!r}")


def _validate_box(box: Sequence[float]) -> None:
    if len(box) != 4 or not all(isinstance(value, (int, float)) for value in box):
        raise ValueError("bbox debe contener cuatro números xyxy")
    if not all(math.isfinite(float(value)) for value in box):
        raise ValueError("bbox debe contener números finitos")


def _area(box: Box) -> float:
    return max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1])


def _best_overlap(box: Box, candidates: Sequence[tuple[int, Box]]) -> tuple[float, int]:
    best = (0.0, -1)
    for index, candidate in candidates:
        overlap = iou(box, candidate)
        if overlap > best[0]:
            best = (overlap, index)
    return best


def _class_id(class_name: str) -> int:
    return CLASSES.index(class_name)


def _match_image(
    record: ImageAnnotations, confidence: float, iou_threshold: float
) -> tuple[set[int], set[int], list[tuple[int, int]]]:
    """Devuelve índices de GT y predicciones no emparejados, y pares TP."""
    matched_gt: set[int] = set()
    matched_pred: set[int] = set()
    matched_pairs: list[tuple[int, int]] = []
    for class_name in CLASSES:
        gt_items = [
            (index, item.bbox)
            for index, item in enumerate(record.ground_truth)
            if item.class_name == class_name
        ]
        pred_items = [
            (index, item.bbox)
            for index, item in enumerate(record.predictions)
            if item.class_name == class_name and item.confidence >= confidence
        ]
        matches = match_detections(
            [box for _, box in gt_items],
            [box for _, box in pred_items],
            iou_threshold=iou_threshold,
        )
        for local_gt, local_pred, _ in matches:
            gt_index = gt_items[local_gt][0]
            pred_index = pred_items[local_pred][0]
            matched_gt.add(gt_index)
            matched_pred.add(pred_index)
            matched_pairs.append((gt_index, pred_index))
    all_gt = set(range(len(record.ground_truth)))
    all_pred = {
        index for index, item in enumerate(record.predictions) if item.confidence >= confidence
    }
    return all_gt - matched_gt, all_pred - matched_pred, matched_pairs


def _categorize_fp(
    record: ImageAnnotations,
    prediction: PredictionBox,
    *,
    iou_threshold: float,
    small_area_ratio: float,
) -> tuple[str, float]:
    gt_other = [
        (index, item.bbox)
        for index, item in enumerate(record.ground_truth)
        if item.class_name != prediction.class_name
    ]
    gt_same = [
        (index, item.bbox)
        for index, item in enumerate(record.ground_truth)
        if item.class_name == prediction.class_name
    ]
    best_other, _ = _best_overlap(prediction.bbox, gt_other)
    best_same, _ = _best_overlap(prediction.bbox, gt_same)
    if best_other >= iou_threshold:
        return "class_confusion", best_other
    if best_same >= iou_threshold:
        return "duplicate", best_same
    best_any = max(best_other, best_same)
    if best_any >= 0.1:
        return "localization", best_any
    area_ratio = _area(prediction.bbox) / (record.width * record.height)
    if area_ratio < small_area_ratio:
        return "small_object", best_any
    return "background", best_any


def _categorize_fn(
    record: ImageAnnotations,
    ground_truth: GroundTruthBox,
    *,
    confidence: float,
    iou_threshold: float,
    small_area_ratio: float,
) -> tuple[str, float]:
    preds_other = [
        (index, item.bbox)
        for index, item in enumerate(record.predictions)
        if item.class_name != ground_truth.class_name and item.confidence >= confidence
    ]
    preds_same = [
        (index, item.bbox)
        for index, item in enumerate(record.predictions)
        if item.class_name == ground_truth.class_name and item.confidence >= confidence
    ]
    best_other, _ = _best_overlap(ground_truth.bbox, preds_other)
    best_same, _ = _best_overlap(ground_truth.bbox, preds_same)
    if best_other >= iou_threshold:
        return "class_confusion", best_other
    if best_same >= 0.1:
        return "localization", best_same
    area_ratio = _area(ground_truth.bbox) / (record.width * record.height)
    if area_ratio < small_area_ratio:
        return "small_object", best_same
    return "occlusion_or_missed", best_same


def analyze_errors(
    records: Sequence[ImageAnnotations],
    *,
    confidence: float = 0.25,
    iou_threshold: float = 0.5,
    small_area_ratio: float = 0.01,
) -> ErrorSummary:
    """Analiza FP/FN por imagen y clase con categorías geométricas estables."""
    if not 0.0 <= confidence <= 1.0:
        raise ValueError("confidence debe estar en [0, 1]")
    if not 0.0 <= iou_threshold <= 1.0:
        raise ValueError("iou_threshold debe estar en [0, 1]")
    if not 0.0 <= small_area_ratio <= 1.0:
        raise ValueError("small_area_ratio debe estar en [0, 1]")

    false_positives: list[ErrorCase] = []
    false_negatives: list[ErrorCase] = []
    per_class_counts = {class_name: {"tp": 0, "fp": 0, "fn": 0} for class_name in CLASSES}
    tp_total = 0
    pred_total = 0
    gt_total = 0

    for record in records:
        unmatched_gt, unmatched_pred, matches = _match_image(record, confidence, iou_threshold)
        gt_total += len(record.ground_truth)
        pred_total += sum(item.confidence >= confidence for item in record.predictions)
        tp_total += len(matches)
        for gt_index in unmatched_gt:
            item = record.ground_truth[gt_index]
            category, overlap = _categorize_fn(
                record,
                item,
                confidence=confidence,
                iou_threshold=iou_threshold,
                small_area_ratio=small_area_ratio,
            )
            false_negatives.append(
                ErrorCase(
                    kind="fn",
                    image=record.image,
                    class_name=item.class_name,
                    category=category,
                    confidence=0.0,
                    overlap=overlap,
                    area_ratio=_area(item.bbox) / (record.width * record.height),
                )
            )
            per_class_counts[item.class_name]["fn"] += 1
        for pred_index in unmatched_pred:
            item = record.predictions[pred_index]
            category, overlap = _categorize_fp(
                record,
                item,
                iou_threshold=iou_threshold,
                small_area_ratio=small_area_ratio,
            )
            false_positives.append(
                ErrorCase(
                    kind="fp",
                    image=record.image,
                    class_name=item.class_name,
                    category=category,
                    confidence=item.confidence,
                    overlap=overlap,
                    area_ratio=_area(item.bbox) / (record.width * record.height),
                )
            )
            per_class_counts[item.class_name]["fp"] += 1
        for gt_index, _pred_index in matches:
            class_name = record.ground_truth[gt_index].class_name
            per_class_counts[class_name]["tp"] += 1

    category_counts = Counter(
        [item.category for item in false_positives] + [item.category for item in false_negatives]
    )
    return ErrorSummary(
        images=len(records),
        ground_truth=gt_total,
        predictions=pred_total,
        tp=tp_total,
        fp=len(false_positives),
        fn=len(false_negatives),
        false_positives=tuple(false_positives),
        false_negatives=tuple(false_negatives),
        category_counts=dict(sorted(category_counts.items())),
        per_class=per_class_counts,
    )


def _fmt(value: float) -> str:
    return f"{value:.3f}".replace(".", ",")


def render_error_report(
    summary: ErrorSummary,
    *,
    model_version: str,
    model_sha256: str,
    split: str = "test",
) -> str:
    """Genera un Markdown sin imágenes ni datos personales."""
    lines = [
        "# Análisis de falsos positivos y negativos — HU-030",
        "",
        "**Estado:** Completado.",
        "",
        "**Fecha:** 2026-11-24.",
        "",
        "**Responsable:** Hernán Estrada (`HestradaUAO`).",
        "",
        "**Issue:** #86.",
        "",
        "---",
        "",
        "## 1. Configuración",
        "",
        "| Parámetro | Valor |",
        "|---|---|",
        f"| Modelo | `{model_version}` |",
        f"| SHA256 | `{model_sha256}` |",
        f"| Partición | `{split}` |",
        f"| Imágenes | {summary.images} |",
        f"| Objetos GT | {summary.ground_truth} |",
        f"| Predicciones | {summary.predictions} |",
        "| Confianza | 0,25 |",
        "| IoU de emparejamiento | 0,50 |",
        "| Objeto pequeño | área < 1 % de la imagen |",
        "",
        "No se publican imágenes ni recortes. El informe solo usa conteos, clases,",
        "confianza y geometría de las cajas.",
        "",
        "## 2. Resumen",
        "",
        "| TP | FP | FN | Precision | Recall | F1 |",
        "|---:|---:|---:|---:|---:|---:|",
        f"| {summary.tp} | {summary.fp} | {summary.fn} | {_fmt(summary.precision)} | "
        f"{_fmt(summary.recall)} | {_fmt(summary.f1)} |",
        "",
        "## 3. Categorías",
        "",
        "| Categoría | Casos |",
        "|---|---:|",
    ]
    for category, count in summary.category_counts.items():
        lines.append(f"| {category} | {count} |")
    lines += [
        "",
        "## 4. Errores por clase",
        "",
        "| Clase | TP | FP | FN |",
        "|---|---:|---:|---:|",
    ]
    for class_name in CLASSES:
        counts = summary.per_class[class_name]
        lines.append(f"| {class_name} | {counts['tp']} | {counts['fp']} | {counts['fn']} |")
    lines += [
        "",
        "## 5. Ejemplos",
        "",
        "Los ejemplos se identifican por imagen y clase; no se adjuntan recortes.",
        "",
        "### Falsos positivos",
        "",
        "| Imagen | Clase | Categoría | Confianza | IoU con GT | Área relativa |",
        "|---|---|---|---:|---:|---:|",
    ]
    for item in summary.false_positives[:10]:
        lines.append(
            f"| {item.image} | {item.class_name} | {item.category} | "
            f"{_fmt(item.confidence)} | {_fmt(item.overlap)} | {_fmt(item.area_ratio)} |"
        )
    lines += [
        "",
        "### Falsos negativos",
        "",
        "| Imagen | Clase | Categoría | IoU con predicción | Área relativa |",
        "|---|---|---|---:|---:|",
    ]
    for item in summary.false_negatives[:10]:
        lines.append(
            f"| {item.image} | {item.class_name} | {item.category} | "
            f"{_fmt(item.overlap)} | {_fmt(item.area_ratio)} |"
        )
    lines += [
        "",
        "## 6. Lectura",
        "",
        "- `class_confusion` indica una caja que se solapa con un objeto de otra clase.",
        "- `localization` indica una caja cerca del objeto pero con IoU insuficiente.",
        "- `small_object` agrupa objetos con área menor al 1 % de la imagen.",
        "- `background` es un falso positivo sin solapamiento relevante.",
        "- `occlusion_or_missed` es un FN sin predicción cercana; requiere revisión visual.",
        "",
        "## 7. Limitaciones",
        "",
        "- La categoría es geométrica; la oclusión real necesita revisión de imágenes.",
        "- El análisis usa IoU 0,50 y confianza 0,25; otros umbrales cambian los conteos.",
        "- Las imágenes con personas no se publican ni se recortan.",
        "",
    ]
    return "\n".join(lines) + "\n"


def _validate_summary(summary: ErrorSummary) -> None:
    if summary.images < 0 or summary.ground_truth < 0 or summary.predictions < 0:
        raise ValueError("Los conteos no pueden ser negativos")


__all__ = [
    "FN_CATEGORIES",
    "FP_CATEGORIES",
    "ErrorCase",
    "ErrorSummary",
    "GroundTruthBox",
    "ImageAnnotations",
    "PredictionBox",
    "analyze_errors",
    "render_error_report",
]
