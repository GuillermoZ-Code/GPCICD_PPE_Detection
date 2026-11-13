"""Cliente de prueba del servicio gRPC (HU-010).

Uso:  uv run python -m ppe_detection.grpc.client --target 127.0.0.1:9000 \
          --image ruta/imagen.png
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from pathlib import Path

import grpc

from ppe_detection.grpc.protos import ppe_pb2, ppe_pb2_grpc
from ppe_detection.grpc.server import default_options

#: Objetivo por omisión, coherente con `PPE_GRPC_PORT` del servidor.
DEFAULT_TARGET = "127.0.0.1:9000"


def call_status(error: BaseException) -> tuple[str, str]:
    """Estado definido de un error gRPC: (nombre del código, detalle).

    Los stubs de grpc no exponen `code`/`details` de `RpcError` al análisis
    estático; la interfaz `grpc.Call` los garantiza en runtime y se reduce
    con `getattr`.
    """
    code = getattr(error, "code", None)
    if callable(code):
        status = code()
        name = str(getattr(status, "name", status))
    else:
        name = "UNKNOWN"
    details = getattr(error, "details", None)
    return name, str(details()) if callable(details) else str(error)


def detect(
    target: str,
    image: bytes,
    timeout: float = 60.0,
    source: str = "",
) -> ppe_pb2.PredictResponse:
    """Envía la imagen al servicio y devuelve la respuesta tipada.

    Raises:
        grpc.RpcError: si el servidor responde con un estado de error definido.
    """
    request = ppe_pb2.PredictRequest(image=image, source=source)
    with grpc.insecure_channel(target, options=default_options()) as channel:
        stub = ppe_pb2_grpc.PpeDetectionStub(channel)
        return stub.Detect(request, timeout=timeout)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI del cliente de prueba; devuelve 0 en éxito y 1 ante error gRPC."""
    parser = argparse.ArgumentParser(description="Cliente gRPC de detección de EPP.")
    parser.add_argument(
        "--target",
        default=os.getenv("PPE_GRPC_TARGET", DEFAULT_TARGET),
        help="host:puerto del servidor (por omisión %(default)s).",
    )
    parser.add_argument("--image", required=True, type=Path, help="JPEG o PNG de entrada.")
    parser.add_argument("--timeout", type=float, default=60.0, help="Segundos de espera.")
    args = parser.parse_args(argv)

    image = args.image.read_bytes()
    try:
        response = detect(args.target, image, timeout=args.timeout, source=args.image.name)
    except grpc.RpcError as exc:
        state, detail = call_status(exc)
        print(f"Error gRPC {state}: {detail}", file=sys.stderr)
        return 1

    print(response.message)
    for detection in response.detections:
        bbox = detection.bbox
        print(
            f"- {detection.class_name} (id {detection.class_id}) "
            f"conf={detection.confidence:.2f} "
            f"bbox=({bbox.x1:.1f}, {bbox.y1:.1f}, {bbox.x2:.1f}, {bbox.y2:.1f})"
        )
    print(
        f"Imagen {response.image_width}x{response.image_height} · "
        f"modelo {response.model_version} · {response.elapsed_ms:.1f} ms"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
