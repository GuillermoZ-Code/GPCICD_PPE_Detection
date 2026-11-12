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
# URL de la API que la SPA hornea en el bundle (por omisión, el puerto de la API).
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# --- runtime: backend CPU con dependencias de uv.lock ------------------------
FROM python:3.13-slim AS runtime
ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Bibliotecas del sistema en Debian trixie:
#   OpenCV headless → libgl1, libglib2.0-0t64, libxcb1
#   torch CPU       → libgomp1 (OpenMP), libquadmath0
#   TLS del cliente → ca-certificates
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates libgl1 libglib2.0-0t64 libgomp1 libquadmath0 libxcb1 \
    && rm -rf /var/lib/apt/lists/*

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

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod 0755 /entrypoint.sh

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000 9000
ENTRYPOINT ["/entrypoint.sh"]

# --- web: SPA estática servida por nginx --------------------------------------
FROM nginx:1.29-alpine AS web
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend-builder /app/dist /usr/share/nginx/html
EXPOSE 80
