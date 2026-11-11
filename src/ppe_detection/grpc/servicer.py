"""Adaptador gRPC hacia el pipeline compartido de inferencia (HU-010).

No conoce YOLO ni entrenamiento: reutiliza `validate_image_bytes` (HU-005), el
protocolo `Detector` (ADR 0005) y `build_inference_result` (HU-004), el mismo
componente central que la API REST (AC-010.2).
"""

from __future__ import annotations

from time import perf_counter

import grpc

from ppe_detection.contracts import Detection, Detector
from ppe_detection.detector_config import (
    DetectorNotConfiguredError,
    build_detector,
    default_model_version,
)
from ppe_detection.grpc.protos import ppe_pb2, ppe_pb2_grpc
from ppe_detection.io import InvalidImageError, validate_image_bytes
from ppe_detection.results import build_inference_result


class PpeDetectionServicer(ppe_pb2_grpc.PpeDetectionServicer):
    """Implementa `ppe.v1.PpeDetection` sobre el detector compartido."""

    def __init__(
        self,
        detector: Detector | None = None,
        model_version: str | None = None,
    ) -> None:
        """Acepta un detector inyectado (pruebas) y una versión explícita."""
        self._detector = detector
        self._model_version = model_version or default_model_version()

    def _resolve_detector(self) -> Detector:
        """Devuelve el detector inyectado o lo construye perezosamente."""
        if self._detector is None:
            self._detector = build_detector()
        return self._detector

    def Detect(
        self,
        request: ppe_pb2.PredictRequest,
        context: grpc.ServicerContext,
    ) -> ppe_pb2.PredictResponse:
        """Valida la imagen, ejecuta el detector compartido y mapea los errores."""
        try:
            image = validate_image_bytes(bytes(request.image), source=request.source)
        except InvalidImageError as exc:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(exc))
            raise  # inalcanzable: satisface el análisis de flujo (abort lanza)

        started = perf_counter()
        try:
            detector = self._resolve_detector()
            detections: list[Detection] = detector.detect(image)
        except DetectorNotConfiguredError as exc:
            context.abort(grpc.StatusCode.UNAVAILABLE, str(exc))
            raise
        except Exception as exc:
            context.abort(grpc.StatusCode.INTERNAL, f"Error de inferencia: {type(exc).__name__}")
            raise

        elapsed_ms = (perf_counter() - started) * 1000
        result = build_inference_result(detections)
        return ppe_pb2.PredictResponse(
            detections=[_to_proto(detection) for detection in result.detections],
            image_width=image.width,
            image_height=image.height,
            model_version=self._model_version,
            elapsed_ms=round(elapsed_ms, 2),
            message=result.message,
        )


def _to_proto(detection: Detection) -> ppe_pb2.Detection:
    """Serializa una `Detection` del contrato al mensaje protobuf espejo."""
    x1, y1, x2, y2 = detection.bbox
    return ppe_pb2.Detection(
        class_id=detection.class_id,
        class_name=detection.class_name,
        confidence=detection.confidence,
        bbox=ppe_pb2.BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
        image_width=detection.image_width,
        image_height=detection.image_height,
    )
