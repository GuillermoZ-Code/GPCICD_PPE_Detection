#!/bin/sh
# HU-011 — arranque del contenedor: REST, gRPC o ambos según PPE_SERVICES.
#
# Variables:
#   PPE_SERVICES      rest | grpc | rest,grpc (por omisión: rest,grpc)
#   PPE_MODEL_PATH    ruta del artefacto montado read-only (/models/best.pt)
#   PPE_API_HOST/PORT y PPE_GRPC_HOST/PORT — ver README y docs/operacion/docker.md
set -eu

model="${PPE_MODEL_PATH:-}"
if [ -n "$model" ] && [ ! -f "$model" ]; then
    echo "ADVERTENCIA: no se encuentra el artefacto '$model' (PPE_MODEL_PATH)." >&2
    echo "  La API responderá 503 y gRPC UNAVAILABLE hasta montar el modelo :ro." >&2
fi

services="${PPE_SERVICES:-rest,grpc}"

case "$services" in
    rest) exec python -m ppe_detection.api ;;
    grpc) exec python -m ppe_detection.grpc ;;
    rest,grpc | both)
        python -m ppe_detection.api &
        api_pid=$!
        python -m ppe_detection.grpc &
        grpc_pid=$!
        trap 'kill "$api_pid" "$grpc_pid" 2>/dev/null || true' TERM INT
        wait "$api_pid" "$grpc_pid"
        ;;
    *)
        echo "ERROR: PPE_SERVICES='$services' no válido (rest | grpc | rest,grpc)." >&2
        exit 64
        ;;
esac
