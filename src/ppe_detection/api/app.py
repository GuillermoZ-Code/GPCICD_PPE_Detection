"""API REST de inferencia (HU-006)."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import replace
from time import perf_counter
from typing import Annotated, cast

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ppe_detection.contracts import Detection, Detector
from ppe_detection.detector_config import (
    DetectorNotConfiguredError,
    ModelIdentity,
    build_detector,
    default_model_identity,
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
    model_sha256: str | None
    model_artifact: str | None
    model_reference: str
    elapsed_ms: float


def _build_detector() -> Detector:
    """Construye el detector compartido; el 503 es la traducción al mapa HTTP."""
    try:
        return build_detector()
    except DetectorNotConfiguredError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def create_app(
    detector: Detector | None = None,
    model_version: str | None = None,
    model_identity: ModelIdentity | None = None,
) -> FastAPI:
    """Crea la aplicación; permite inyectar un detector y la identidad del modelo."""

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        if application.state.detector is None and os.getenv("PPE_MODEL_PATH"):
            application.state.detector = _build_detector()
        yield

    application = FastAPI(
        title="GPCICD PPE Detection API",
        version="0.1.0",
        description="Detección de EPP sobre imágenes JPEG/PNG.",
        lifespan=lifespan,
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
    identity = model_identity or default_model_identity()
    if model_version is not None:
        identity = replace(identity, version=model_version)
    application.state.model_identity = identity

    def get_detector() -> Detector:
        if application.state.detector is None:
            try:
                application.state.detector = _build_detector()
            except RuntimeError as exc:
                raise HTTPException(status_code=503, detail=str(exc)) from exc
        return cast(Detector, application.state.detector)

    @application.post("/predict", response_model=PredictResponse)
    async def predict(
        file: Annotated[UploadFile, File(description="Imagen JPEG o PNG")],
        conf: Annotated[float | None, Form(ge=0.01, le=0.99)] = None,
    ) -> PredictResponse:
        """Valida la imagen y devuelve las detecciones del modelo configurado."""
        data = await file.read()
        try:
            image = validate_image_bytes(data, source=file.filename or "upload")
        except InvalidImageError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        started = perf_counter()
        detections: list[Detection] = get_detector().detect(image, conf=conf)
        elapsed_ms = (perf_counter() - started) * 1000
        identity = cast(ModelIdentity, application.state.model_identity)
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
            model_version=identity.version,
            model_sha256=identity.sha256,
            model_artifact=identity.artifact,
            model_reference=identity.reference,
            elapsed_ms=round(elapsed_ms, 2),
        )

    return application


app = create_app()
