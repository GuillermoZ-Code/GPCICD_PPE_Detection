"""Adaptador de inferencia YOLO (HU-002)."""

from __future__ import annotations

import importlib
import math
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Protocol

import cv2

from ppe_detection.contracts import CLASSES, Detection, ImageData

DEFAULT_CONF = 0.25
DEFAULT_IOU = 0.7
DEFAULT_IMGSZ = 640
DEFAULT_DEVICE = "cpu"


class ModelProtocol(Protocol):
    """Forma mínima que se espera de un modelo Ultralytics o de un fake."""

    @property
    def names(self) -> Any:
        """Catálogo de clases del modelo."""
        ...

    def predict(self, source: Any, **kwargs: Any) -> Iterable[Any]: ...


def _load_model(model_path: Path) -> ModelProtocol:
    try:
        ultralytics = importlib.import_module("ultralytics")
    except ImportError as exc:
        raise RuntimeError(
            "Falta ultralytics. Instala el extra con `uv sync --extra inference` "
            "o ejecuta con `uv run --with ultralytics ...`."
        ) from exc
    return ultralytics.YOLO(str(model_path))


def _normalize_names(names: Any) -> dict[int, str]:
    if isinstance(names, dict):
        return {int(key): str(value) for key, value in names.items()}
    if isinstance(names, (list, tuple)):
        return {index: str(value) for index, value in enumerate(names)}
    raise ValueError("El modelo no expone un catálogo de clases válido.")


def _clip(value: float, lower: float, upper: float) -> float:
    return max(lower, min(value, upper))


class YoloDetector:
    """Adapta un artefacto Ultralytics al protocolo ``Detector``."""

    def __init__(
        self,
        model_path: str | Path | None = None,
        *,
        conf: float = DEFAULT_CONF,
        iou: float = DEFAULT_IOU,
        imgsz: int = DEFAULT_IMGSZ,
        device: str = DEFAULT_DEVICE,
        model: ModelProtocol | None = None,
    ) -> None:
        if model is None and model_path is None:
            raise ValueError("Se requiere model_path o un modelo inyectado.")
        self.model_path = Path(model_path) if model_path is not None else None
        self.conf = conf
        self.iou = iou
        self.imgsz = imgsz
        self.device = device
        if model is not None:
            self._model = model
        elif model_path is not None:
            self._model = _load_model(Path(model_path))
        else:  # pragma: no cover - cubierto por la validación inicial
            raise ValueError("Se requiere model_path o un modelo inyectado.")
        self._names = _normalize_names(self._model.names)
        self._validate_catalog()
        self.classes: tuple[str, ...] = tuple(self._names[index] for index in range(len(CLASSES)))

    def _validate_catalog(self) -> None:
        expected = dict(enumerate(CLASSES))
        if self._names != expected:
            raise ValueError(
                "El modelo no usa el catálogo de EPP esperado. "
                f"Esperado: {expected}. Recibido: {self._names}."
            )

    def detect(self, image: ImageData) -> list[Detection]:
        """Ejecuta inferencia y devuelve detecciones validadas."""
        bgr = cv2.cvtColor(image.array, cv2.COLOR_RGB2BGR)
        results = list(
            self._model.predict(
                source=bgr,
                conf=self.conf,
                iou=self.iou,
                imgsz=self.imgsz,
                device=self.device,
                verbose=False,
            )
        )
        if not results:
            return []
        boxes = getattr(results[0], "boxes", None)
        if boxes is None:
            return []
        detections: list[Detection] = []
        for box in boxes:
            class_id = int(box.cls.item())
            if not 0 <= class_id < len(CLASSES):
                raise ValueError(f"El modelo devolvió class_id fuera de rango: {class_id}")
            confidence = float(box.conf.item())
            if not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0:
                continue
            x1, y1, x2, y2 = (float(value) for value in box.xyxy[0].tolist())
            x1 = _clip(x1, 0.0, float(image.width))
            y1 = _clip(y1, 0.0, float(image.height))
            x2 = _clip(x2, 0.0, float(image.width))
            y2 = _clip(y2, 0.0, float(image.height))
            if x2 <= x1 or y2 <= y1:
                continue
            detections.append(
                Detection(
                    class_id=class_id,
                    class_name=CLASSES[class_id],
                    confidence=float(box.conf.item()),
                    bbox=(x1, y1, x2, y2),
                    image_width=image.width,
                    image_height=image.height,
                )
            )
        return detections
