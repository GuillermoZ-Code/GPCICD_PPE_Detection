# Stub manual de `ppe_pb2_grpc` para el análisis de tipos (ty).
# Descripción de la superficie usada por HU-010; la regeneración no lo toca.

from collections.abc import Sequence
from typing import Any

import grpc

from ppe_detection.grpc.protos.ppe_pb2 import PredictRequest, PredictResponse


class PpeDetectionServicer:
    """Servidor base de `ppe.v1.PpeDetection`."""

    def Detect(
        self,
        request: PredictRequest,
        context: Any,
    ) -> PredictResponse: ...


class PpeDetectionStub:
    """Stub de cliente de `ppe.v1.PpeDetection`."""

    def __init__(self, channel: Any) -> None: ...

    def Detect(
        self,
        request: PredictRequest,
        timeout: float | None = None,
    ) -> PredictResponse: ...


def add_PpeDetectionServicer_to_server(
    servicer: PpeDetectionServicer,
    server: Any,
) -> None: ...
