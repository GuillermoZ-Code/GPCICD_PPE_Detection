#!/bin/sh
# HU-046 — HEALTHCHECK del contenedor.
#
# REST (o ambos): consulta /health/ready, que ya distingue liveness de readiness (HU-045).
# gRPC: comprueba que el puerto 9000 acepta conexiones; no hay endpoint HTTP que consultar.
set -eu

services="${PPE_SERVICES:-both}"

if [ "$services" = "grpc" ]; then
    python - <<'PY'
import socket

with socket.create_connection(("127.0.0.1", 9000), timeout=3):
    pass
PY
    exit 0
fi

python - <<'PY'
import urllib.request

with urllib.request.urlopen("http://127.0.0.1:8000/health/ready", timeout=3) as response:
    if response.status != 200:
        raise SystemExit(1)
PY
