"""API REST de inferencia (HU-006)."""

from __future__ import annotations

import os
from pathlib import Path
from time import perf_counter
from typing import Annotated, cast

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ppe_detection.contracts import Detection, Detector
from ppe_detection.detection.yolo import (
    DEFAULT_CONF,
    DEFAULT_DEVICE,
    DEFAULT_IMGSZ,
    DEFAULT_IOU,
    YoloDetector,
)
from ppe_detection.io import InvalidImageError, validate_image_bytes


class DetectionOut(BaseModel):
    """Detección serializada para la API."""

    class_id: int
    class_name: str
    confidence: float
    bbox: tuple[float, float, float, float]
    image_width: int
    image_height: int


class PredictResponse(BaseModel):
    """Respuesta de `POST /predict`, espejo de `frontend/src/types.ts`."""

    detections: list[DetectionOut]
    image_width: int
    image_height: int
    model_version: str
    elapsed_ms: float


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _default_model_version() -> str:
    explicit = os.getenv("PPE_MODEL_VERSION")
    if explicit:
        return explicit
    model_path = os.getenv("PPE_MODEL_PATH")
    return Path(model_path).stem if model_path else "unknown"


def _build_detector() -> Detector:
    model_path = os.getenv("PPE_MODEL_PATH")
    if not model_path:
        raise HTTPException(
            status_code=503,
            detail="No hay modelo configurado: define PPE_MODEL_PATH.",
        )
    return YoloDetector(
        model_path,
        conf=_env_float("PPE_CONF", DEFAULT_CONF),
        iou=_env_float("PPE_IOU", DEFAULT_IOU),
        imgsz=_env_int("PPE_IMGSZ", DEFAULT_IMGSZ),
        device=os.getenv("PPE_DEVICE", DEFAULT_DEVICE),
    )


def create_app(detector: Detector | None = None, model_version: str | None = None) -> FastAPI:
    """Crea la aplicación; permite inyectar un detector para pruebas."""
    application = FastAPI(
        title="GPCICD PPE Detection API",
        version="0.1.0",
        description="Detección de EPP sobre imágenes JPEG/PNG.",
    )
    origins = [
        origin.strip()
        for origin in os.getenv("PPE_CORS_ORIGINS", "http://localhost:5173").split(",")
        if origin.strip()
    ]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.state.detector = detector
    application.state.model_version = model_version or _default_model_version()

    def get_detector() -> Detector:
        if application.state.detector is None:
            application.state.detector = _build_detector()
        return cast(Detector, application.state.detector)

    @application.post("/predict", response_model=PredictResponse)
    async def predict(
        file: Annotated[UploadFile, File(description="Imagen JPEG o PNG")],
    ) -> PredictResponse:
        """Valida la imagen y devuelve las detecciones del modelo configurado."""
        data = await file.read()
        try:
            image = validate_image_bytes(data, source=file.filename or "upload")
        except InvalidImageError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        started = perf_counter()
        detections: list[Detection] = get_detector().detect(image)
        elapsed_ms = (perf_counter() - started) * 1000
        return PredictResponse(
            detections=[
                DetectionOut(
                    class_id=detection.class_id,
                    class_name=detection.class_name,
                    confidence=detection.confidence,
                    bbox=detection.bbox,
                    image_width=detection.image_width,
                    image_height=detection.image_height,
                )
                for detection in detections
            ],
            image_width=image.width,
            image_height=image.height,
            model_version=str(application.state.model_version),
            elapsed_ms=round(elapsed_ms, 2),
        )

    return application


app = create_app()
