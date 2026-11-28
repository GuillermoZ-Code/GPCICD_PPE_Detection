# syntax=docker/dockerfile:1
# =============================================================================
# HU-011 — Imagen Docker CPU del sistema de detección de EPP
# =============================================================================
# Targets:
#   runtime — backend completo (API REST + gRPC) con dependencias de uv.lock
#   web     — SPA React (HU-007) construida con Node 24 y servida por nginx
#
# El artefacto del modelo NUNCA va dentro de la imagen: se monta read-only al
# arrancar (-v <dir>/modelos:/models:ro + PPE_MODEL_PATH=/models/best.pt).
# =============================================================================

# --- frontend-builder: SPA React + Vite + TypeScript (HU-007) -----------------
FROM node:24-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
# HU-072 — sin VITE_API_URL el bundle usa la ruta relativa `/api` y nginx la
# reenvía al servicio `api` del mismo compose (sin CORS ni localhost horneado).
RUN npm run build

# --- runtime-deps: entorno resuelto, no se publica ---------------------------
FROM python:3.13-slim AS runtime-deps
ENV UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# uv como único gestor de dependencias; sin pip ni requirements.txt.
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /usr/local/bin/uv

WORKDIR /app
# Primero los manifiestos: la capa de dependencias queda cacheada y no se
# repite cuando cambia el código. uv resuelve con --frozen el uv.lock.
COPY pyproject.toml uv.lock README.md LICENSE ./
RUN uv sync --frozen --no-dev --no-install-project --extra inference --extra grpc
# Después el código: el proyecto se instala sobre el entorno ya resuelto.
# Extras de runtime: `inference` (ultralytics/torch CPU por pytorch-cpu) y
# `grpc` (servidor gRPC de HU-010). Sin grupo dev.
COPY src ./src
RUN uv sync --frozen --no-dev --extra inference --extra grpc

# --- runtime: backend CPU publicado, sin uv y con usuario no root -------------
FROM python:3.13-slim AS runtime
ENV UV_PYTHON_DOWNLOADS=never \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Bibliotecas del sistema en Debian trixie:
#   OpenCV headless → libgl1, libglib2.0-0t64, libxcb1
#   torch CPU       → libgomp1 (OpenMP), libquadmath0
#   TLS del cliente → ca-certificates
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates libgl1 libglib2.0-0t64 libgomp1 libquadmath0 libxcb1 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid appuser --create-home --shell /bin/sh appuser \
    && install -d -o appuser -g appuser /app

WORKDIR /app
COPY --chown=appuser:appuser --from=runtime-deps /app/.venv /app/.venv
COPY --chown=appuser:appuser --from=runtime-deps /app/src /app/src
COPY --chmod=0755 --chown=appuser:appuser docker/entrypoint.sh /entrypoint.sh
# HU-046 — el contenedor informa si puede atender: REST por HTTP, gRPC por TCP.
COPY --chmod=0755 --chown=appuser:appuser docker/healthcheck.sh /healthcheck.sh

USER appuser
EXPOSE 8000 9000
# `start-period` amplio: importar torch tarda decenas de segundos y sin margen
# el contenedor se marcaría enfermo antes de poder responder.
HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD ["/healthcheck.sh"]
ENTRYPOINT ["/entrypoint.sh"]

# --- web: SPA estática servida por nginx --------------------------------------
FROM nginx:1.29-alpine AS web
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
# HU-046 — nginx tiene que responder antes de que Caddy lo publique.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget -q --spider http://127.0.0.1/ || exit 1
EXPOSE 80
