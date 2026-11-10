"""Servidor gRPC de inferencia de EPP (HU-010)."""

from __future__ import annotations

from concurrent import futures

import grpc

from ppe_detection.contracts import Detector
from ppe_detection.grpc.protos import ppe_pb2_grpc
from ppe_detection.grpc.servicer import PpeDetectionServicer
from ppe_detection.io import MAX_IMAGE_BYTES

#: Hilos por omisión: suficiente para llamadas unary en CPU.
DEFAULT_MAX_WORKERS = 4

#: gRPC trunca por omisión los mensajes en 4 MiB (RESOURCE_EXHAUSTED de
#: transporte). Aceptamos hasta el límite de HU-005 más margen para que la
#: validación del adaptador decida y responda INVALID_ARGUMENT con el mismo
#: detalle que la API REST (AC-010.2).
MAX_RECEIVE_BYTES = MAX_IMAGE_BYTES + 4096


def default_options() -> list[tuple[str, int]]:
    """Opciones de canal compartidas entre servidor y cliente de prueba."""
    return [("grpc.max_receive_message_length", MAX_RECEIVE_BYTES)]


def create_server(
    detector: Detector | None = None,
    model_version: str | None = None,
    max_workers: int = DEFAULT_MAX_WORKERS,
) -> grpc.Server:
    """Crea el servidor enlazable; permite inyectar el detector para pruebas."""
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=max_workers),
        options=default_options(),
    )
    servicer = PpeDetectionServicer(detector=detector, model_version=model_version)
    ppe_pb2_grpc.add_PpeDetectionServicer_to_server(servicer, grpc_server)
    return grpc_server


def serve(host: str = "0.0.0.0", port: int = 9000) -> int:
    """Ejecuta el servidor en primer plano: bloquea hasta la terminación."""
    grpc_server = create_server()
    bound = grpc_server.add_insecure_port(f"{host}:{port}")
    if bound == 0:
        raise SystemExit(f"No se pudo abrir el puerto {host}:{port}.")
    grpc_server.start()
    print(f"Servidor gRPC de EPP escuchando en {host}:{bound}")
    grpc_server.wait_for_termination()
    return bound
