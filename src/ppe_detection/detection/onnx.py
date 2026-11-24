"""Exportación ONNX y selección de backend (HU-022)."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import importlib.util
import json
import os
import shutil
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ppe_detection.contracts import Detection
from ppe_detection.detector_config import sha256_file

DEFAULT_IMGSZ = 640
DEFAULT_OPSET = 17


class OnnxError(RuntimeError):
    """El backend ONNX no está disponible o la exportación falló."""


@dataclass(frozen=True, slots=True)
class OnnxExportResult:
    """Resultado reproducible de una exportación ONNX."""

    weights: Path
    onnx: Path
    imgsz: int
    opset: int
    weights_sha256: str
    onnx_sha256: str
    manifest: Path


def _export_dependencies_available() -> bool:
    """True si onnx y onnxslim están instalados."""
    return all(importlib.util.find_spec(name) is not None for name in ("onnx", "onnxslim"))


def _load_yolo() -> Any:
    try:
        return importlib.import_module("ultralytics").YOLO
    except ImportError as exc:
        raise OnnxError(
            "Falta ultralytics. Instala el extra con `uv sync --extra inference`."
        ) from exc


def resolve_backend_path(model_path: str | Path, fmt: str | None = None) -> Path:
    """Resuelve el artefacto `.pt` o `.onnx` según `PPE_MODEL_FORMAT`."""
    selected = (fmt if fmt is not None else os.getenv("PPE_MODEL_FORMAT", "pt")).strip().lower()
    if selected not in {"pt", "onnx"}:
        raise OnnxError(f"Formato de modelo no soportado: {selected!r}. Usa 'pt' u 'onnx'.")

    path = Path(model_path)
    if selected == "onnx" and path.suffix.lower() != ".onnx":
        path = path.with_suffix(".onnx")
    if not path.is_file():
        raise OnnxError(f"No existe el artefacto {selected.upper()}: {path}")
    return path


def export_onnx(
    weights: str | Path,
    *,
    imgsz: int = DEFAULT_IMGSZ,
    opset: int = DEFAULT_OPSET,
    output: str | Path | None = None,
) -> OnnxExportResult:
    """Exporta un checkpoint Ultralytics a ONNX y escribe su manifiesto."""
    source = Path(weights)
    if not source.is_file():
        raise OnnxError(f"No existe el checkpoint: {source}")
    if not _export_dependencies_available():
        raise OnnxError("Faltan dependencias para exportar ONNX: instala 'onnx' y 'onnxslim'.")

    yolo = _load_yolo()
    model = yolo(str(source))
    try:
        exported = Path(
            model.export(
                format="onnx",
                imgsz=imgsz,
                opset=opset,
                simplify=True,
                dynamic=False,
            )
        )
    except Exception as exc:
        raise OnnxError(f"Falló la exportación ONNX de {source}: {exc}") from exc

    target = Path(output) if output is not None else exported
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.resolve() != exported.resolve():
        shutil.copy2(exported, target)
    if not target.is_file():
        raise OnnxError(f"La exportación no produjo un archivo ONNX: {target}")

    weights_sha = sha256_file(source)
    onnx_sha = sha256_file(target)
    manifest = target.with_name(target.name + ".json")
    manifest.write_text(
        json.dumps(
            {
                "weights": str(source),
                "weights_sha256": weights_sha,
                "onnx": str(target),
                "onnx_sha256": onnx_sha,
                "imgsz": imgsz,
                "opset": opset,
                "ultralytics": importlib.metadata.version("ultralytics"),
                "torch": importlib.metadata.version("torch"),
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return OnnxExportResult(
        weights=source,
        onnx=target,
        imgsz=imgsz,
        opset=opset,
        weights_sha256=weights_sha,
        onnx_sha256=onnx_sha,
        manifest=manifest,
    )


def compare_detections(
    reference: Sequence[Detection],
    candidate: Sequence[Detection],
    *,
    confidence_tolerance: float = 1e-4,
    bbox_tolerance: float = 1e-3,
) -> list[str]:
    """Compara dos listas de detecciones con tolerancias explícitas."""
    if len(reference) != len(candidate):
        return [f"Cantidad de detecciones: {len(reference)} vs {len(candidate)}"]

    differences: list[str] = []
    for index, (expected, actual) in enumerate(zip(reference, candidate, strict=True)):
        reasons: list[str] = []
        if expected.class_name != actual.class_name:
            reasons.append(f"clase {expected.class_name} vs {actual.class_name}")
        if abs(expected.confidence - actual.confidence) > confidence_tolerance:
            reasons.append(f"confianza {expected.confidence:.6f} vs {actual.confidence:.6f}")
        if any(
            abs(left - right) > bbox_tolerance
            for left, right in zip(expected.bbox, actual.bbox, strict=True)
        ):
            reasons.append(f"bbox {expected.bbox} vs {actual.bbox}")
        if reasons:
            differences.append(f"detección {index}: " + "; ".join(reasons))
    return differences


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ppe-onnx", description="Exporta un YOLO a ONNX.")
    commands = parser.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export")
    export.add_argument("--weights", type=Path, required=True)
    export.add_argument("--imgsz", type=int, default=DEFAULT_IMGSZ)
    export.add_argument("--opset", type=int, default=DEFAULT_OPSET)
    export.add_argument("--output", type=Path, default=None)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI de exportación."""
    args = _build_parser().parse_args(argv)
    try:
        result = export_onnx(
            args.weights,
            imgsz=args.imgsz,
            opset=args.opset,
            output=args.output,
        )
    except OnnxError as exc:
        print(f"onnx: {exc}")
        return 1
    print(f"onnx: {result.onnx}")
    print(f"manifest: {result.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
