"""Punto de entrada para `python -m ppe_detection.grpc` (servidor gRPC)."""

from __future__ import annotations

import os

from ppe_detection.grpc.server import serve


def main() -> None:
    """Levanta el servidor gRPC según `PPE_GRPC_HOST` y `PPE_GRPC_PORT`."""
    host = os.getenv("PPE_GRPC_HOST", "0.0.0.0")
    port = int(os.getenv("PPE_GRPC_PORT", "9000"))
    serve(host=host, port=port)


if __name__ == "__main__":
    main()
