"""API REST de inferencia y healthcheck (HU-006 y rúbrica del M3)."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import replace
from time import perf_counter
from typing import Annotated, Literal, cast

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from ppe_detection.api.logging import RequestLoggingMiddleware
from ppe_detection.api.settings import load_settings
from ppe_detection.contracts import Detection, Detector
from ppe_detection.detector_config import (
    DetectorNotConfiguredError,
    ModelIdentity,
    build_detector,
    default_model_identity,
)
from ppe_detection.io import InvalidImageError, validate_image_bytes

DEFAULT_SOURCE_URL = "https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection"


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


class HealthResponse(BaseModel):
    """Estado del servicio y contrato publicado en `GET /health`."""

    status: Literal["ok", "degraded"]
    api_version: str
    model_loaded: bool
    model_version: str
    model_reference: str
    model_sha256: str | None
    model_artifact: str | None
    source_url: str
    commit: str | None


ALLOWED_IMAGE_TYPES = ("image/png", "image/jpeg")


def _configured_upload_bytes() -> tuple[int, float] | None:
    """Devuelve bytes y MB si `PPE_MAX_UPLOAD_MB` fue configurado explícitamente."""
    raw = os.getenv("PPE_MAX_UPLOAD_MB")
    if raw is None:
        return None
    try:
        megabytes = float(raw)
    except ValueError:
        return None
    if not 0 < megabytes <= 1024:
        return None
    return int(megabytes * 1024 * 1024), megabytes


def _is_allowed_type(content_type: str | None) -> bool:
    """True si el MIME anunciado es PNG o JPEG."""
    normalized = (content_type or "").split(";", 1)[0].strip().lower()
    return normalized in ALLOWED_IMAGE_TYPES


class LiveResponse(BaseModel):
    """Contrato mínimo de `GET /health/live`, independiente del modelo."""

    status: Literal["ok"]


class ReadyResponse(BaseModel):
    """Contrato de `GET /health/ready`, con identidad verificable del modelo."""

    status: Literal["ready", "not_ready"]
    api_version: str
    model_loaded: bool
    model_version: str
    model_reference: str
    model_sha256: str | None
    model_artifact: str | None


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
    settings = load_settings()

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
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(RequestLoggingMiddleware)
    application.state.detector = detector
    application.state.source_url = (os.getenv("PPE_SOURCE_URL") or "").strip() or DEFAULT_SOURCE_URL
    application.state.deploy_commit = (os.getenv("PPE_DEPLOY_COMMIT") or "").strip() or None
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

    @application.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        """Informa el estado del componente y la identidad del modelo cargado.

        No construye el detector: si aún no está cargado responde `degraded`, de
        modo que el chequeo nunca bloquea ni provoca una carga accidental.
        """
        identity = cast(ModelIdentity, application.state.model_identity)
        loaded = application.state.detector is not None
        return HealthResponse(
            status="ok" if loaded else "degraded",
            api_version=str(application.version),
            model_loaded=loaded,
            model_version=identity.version,
            model_reference=identity.reference,
            model_sha256=identity.sha256,
            model_artifact=identity.artifact,
            source_url=cast(str, application.state.source_url),
            commit=cast(str | None, application.state.deploy_commit),
        )

    @application.get("/health/live", response_model=LiveResponse)
    async def live() -> LiveResponse:
        """Confirma que el proceso responde sin mirar ni cargar el modelo."""
        return LiveResponse(status="ok")

    @application.get(
        "/health/ready",
        response_model=ReadyResponse,
        responses={
            503: {
                "model": ReadyResponse,
                "description": "El modelo todavía no está cargado.",
            }
        },
    )
    async def ready() -> ReadyResponse | JSONResponse:
        """Informa si el modelo está listo sin provocar su carga."""
        identity = cast(ModelIdentity, application.state.model_identity)
        loaded = application.state.detector is not None
        response = ReadyResponse(
            status="ready" if loaded else "not_ready",
            api_version=str(application.version),
            model_loaded=loaded,
            model_version=identity.version,
            model_reference=identity.reference,
            model_sha256=identity.sha256,
            model_artifact=identity.artifact,
        )
        if not loaded:
            return JSONResponse(status_code=503, content=response.model_dump(mode="json"))
        return response

    @application.post("/predict", response_model=PredictResponse)
    async def predict(
        file: Annotated[UploadFile, File(description="Imagen JPEG o PNG")],
        conf: Annotated[float | None, Form(ge=0.01, le=0.99)] = None,
    ) -> PredictResponse:
        """Valida la imagen y devuelve las detecciones del modelo configurado."""
        configured_limit = _configured_upload_bytes()
        data = await file.read()
        if configured_limit is not None and len(data) > configured_limit[0]:
            raise HTTPException(
                status_code=413,
                detail=f"Archivo demasiado grande: el límite es {configured_limit[1]:g} MB.",
            )
        if data and not _is_allowed_type(file.content_type):
            raise HTTPException(
                status_code=415,
                detail="Tipo de archivo no permitido: se aceptan image/png e image/jpeg.",
            )
        try:
            image = validate_image_bytes(data, source=file.filename or "upload")
        except InvalidImageError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        started = perf_counter()
        try:
            detections: list[Detection] = get_detector().detect(image, conf=conf)
        except DetectorNotConfiguredError as exc:
            # Un detector inyectado también puede quedar sin modelo en tiempo de
            # inferencia: REST debe traducirlo igual que gRPC (503 ↔ UNAVAILABLE).
            raise HTTPException(status_code=503, detail=str(exc)) from exc
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
