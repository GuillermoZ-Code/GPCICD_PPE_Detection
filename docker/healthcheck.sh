#!/bin/sh
# HU-046 — healthcheck del contenedor.
#
# El mismo script sirve para los dos modos del entrypoint:
#   PPE_SERVICES=rest  → comprueba GET /health/ready en el puerto 8000
#   PPE_SERVICES=grpc  → comprueba que el puerto 9000 acepta conexiones
#
# No usa curl: la imagen runtime no lo trae y `python` ya está en el PATH.

set -eu

services="${PPE_SERVICES:-rest,grpc}"

case "$services" in
*rest*)
    exec python -c "import sys, urllib.request; \
sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health/ready', timeout=4).status == 200 else 1)"
    ;;
*)
    exec python -c "import socket, sys; \
s = socket.socket(); s.settimeout(4); \
sys.exit(0 if s.connect_ex(('127.0.0.1', 9000)) == 0 else 1)"
    ;;
esac
