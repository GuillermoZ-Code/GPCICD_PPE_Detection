"""CLI de inferencia y exportación de detecciones (HU-002)."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from ppe_detection.contracts import Detection
from ppe_detection.detection.yolo import (
    DEFAULT_CONF,
    DEFAULT_DEVICE,
    DEFAULT_IMGSZ,
    DEFAULT_IOU,
    YoloDetector,
)
from ppe_detection.io import load_image

DEFAULT_OUTPUT = Path("artifacts/predictions/demo")
CSV_FIELDS = ("image", "class_name", "confidence", "x1", "y1", "x2", "y2")
IMAGE_SUFFIXES = frozenset({".jpg", ".jpeg", ".png"})


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parsea la CLI de inferencia."""
    parser = argparse.ArgumentParser(
        prog="ppe-predict",
        description="Detecta EPP en imágenes con un modelo YOLO entrenado.",
    )
    parser.add_argument("--model", type=Path, required=True, help="best.pt o best.onnx")
    parser.add_argument("--source", type=Path, required=True, help="imagen o carpeta")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--conf", type=float, default=DEFAULT_CONF)
    parser.add_argument("--iou", type=float, default=DEFAULT_IOU)
    parser.add_argument("--imgsz", type=int, default=DEFAULT_IMGSZ)
    parser.add_argument("--device", default=DEFAULT_DEVICE, help="cpu o 0 para GPU")
    return parser.parse_args(argv)


def iter_images(source: Path) -> list[Path]:
    """Devuelve las imágenes de un archivo o carpeta, en orden estable."""
    if source.is_file():
        return [source]
    if source.is_dir():
        return sorted(
            path
            for path in source.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
        )
    raise FileNotFoundError(f"No existe la fuente: {source}")


def detection_rows(image_path: Path, detections: Sequence[Detection]) -> list[dict[str, Any]]:
    """Convierte detecciones en filas serializables para CSV."""
    return [
        {
            "image": str(image_path),
            "class_name": detection.class_name,
            "confidence": round(detection.confidence, 6),
            "x1": round(detection.bbox[0], 2),
            "y1": round(detection.bbox[1], 2),
            "x2": round(detection.bbox[2], 2),
            "y2": round(detection.bbox[3], 2),
        }
        for detection in detections
    ]


def write_detections_csv(rows: Sequence[dict[str, Any]], path: Path) -> None:
    """Guarda las detecciones en CSV, creando el directorio si hace falta."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def format_summary(rows: Sequence[dict[str, Any]]) -> str:
    """Resumen legible por clase."""
    counts = Counter(str(row["class_name"]) for row in rows)
    images = len({str(row["image"]) for row in rows})
    lines = [
        f"Imágenes con detecciones: {images}",
        f"Total de detecciones: {len(rows)}",
    ]
    for name, count in sorted(counts.items()):
        lines.append(f"  {name}: {count}")
    return "\n".join(lines)


def run(args: argparse.Namespace) -> None:
    """Ejecuta la inferencia y escribe el CSV de detecciones."""
    if not args.model.is_file():
        raise FileNotFoundError(f"No existe el modelo: {args.model}")
    images = iter_images(args.source)
    if not images:
        raise FileNotFoundError(f"No hay imágenes JPEG/PNG en: {args.source}")

    detector = YoloDetector(
        args.model,
        conf=args.conf,
        iou=args.iou,
        imgsz=args.imgsz,
        device=args.device,
    )
    rows: list[dict[str, Any]] = []
    for image_path in images:
        image = load_image(image_path)
        detections = detector.detect(image)
        rows.extend(detection_rows(image_path, detections))
        print(f"{image_path}: {len(detections)} detecciones")

    csv_path = args.output / "detections.csv"
    write_detections_csv(rows, csv_path)
    print(format_summary(rows))
    print(f"CSV: {csv_path}")


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada de la CLI."""
    run(parse_args(argv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
