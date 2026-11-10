"""CLI de inferencia y exportación de detecciones (HU-002)."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from collections.abc import Sequence
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import Any

from ppe_detection.contracts import Detection, ImageData
from ppe_detection.detection.yolo import (
    DEFAULT_CONF,
    DEFAULT_DEVICE,
    DEFAULT_IMGSZ,
    DEFAULT_IOU,
    YoloDetector,
)
from ppe_detection.io import load_image

DEFAULT_OUTPUT = Path("artifacts/predictions/demo")
DEFAULT_SEED = 42
CSV_FIELDS = ("image", "class_name", "confidence", "x1", "y1", "x2", "y2")
IMAGE_SUFFIXES = frozenset({".jpg", ".jpeg", ".png"})
MANIFEST_NAME = "run.json"
PACKAGE_NAME = "gpcicd-ppe-detection"


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
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help="semilla declarada en el manifiesto de la ejecución",
    )
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


def sha256_file(path: Path) -> str:
    """Calcula el SHA256 de un archivo por bloques, sin cargarlo en memoria."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def git_commit() -> str | None:
    """Devuelve el commit corto del repositorio, si está disponible."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    commit = result.stdout.strip()
    return commit or None


def package_version() -> str:
    """Devuelve la versión instalada del paquete."""
    try:
        return metadata.version(PACKAGE_NAME)
    except metadata.PackageNotFoundError:
        return "unknown"


def image_record(image_path: Path, image: ImageData, detections: int) -> dict[str, Any]:
    """Resume una imagen procesada para el manifiesto."""
    return {
        "path": str(image_path),
        "width": image.width,
        "height": image.height,
        "format": image.format,
        "detections": detections,
    }


def build_manifest(
    args: argparse.Namespace,
    images: Sequence[dict[str, Any]],
    detection_count: int,
) -> dict[str, Any]:
    """Construye el manifiesto de procedencia de la inferencia."""
    return {
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "code": {
            "package": PACKAGE_NAME,
            "version": package_version(),
            "git_commit": git_commit(),
        },
        "model": {
            "path": str(args.model),
            "sha256": sha256_file(args.model),
            "size_bytes": args.model.stat().st_size,
        },
        "parameters": {
            "conf": args.conf,
            "iou": args.iou,
            "imgsz": args.imgsz,
            "device": args.device,
            "seed": getattr(args, "seed", DEFAULT_SEED),
        },
        "images": list(images),
        "totals": {
            "images": len(images),
            "images_with_detections": sum(1 for item in images if item["detections"]),
            "detections": detection_count,
        },
    }


def write_manifest(manifest: dict[str, Any], path: Path) -> None:
    """Guarda el manifiesto en JSON, creando el directorio si hace falta."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(manifest, ensure_ascii=False, indent=2)
    path.write_text(f"{text}\n", encoding="utf-8")


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
    """Ejecuta la inferencia y escribe el CSV y el manifiesto de la ejecución."""
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
    records: list[dict[str, Any]] = []
    for image_path in images:
        image = load_image(image_path)
        detections = detector.detect(image)
        rows.extend(detection_rows(image_path, detections))
        records.append(image_record(image_path, image, len(detections)))
        print(f"{image_path}: {len(detections)} detecciones")

    csv_path = args.output / "detections.csv"
    write_detections_csv(rows, csv_path)
    manifest_path = args.output / MANIFEST_NAME
    write_manifest(build_manifest(args, records, len(rows)), manifest_path)
    print(format_summary(rows))
    print(f"CSV: {csv_path}")
    print(f"Manifiesto: {manifest_path}")


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada de la CLI."""
    run(parse_args(argv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
