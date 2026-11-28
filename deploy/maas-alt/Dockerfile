# syntax=docker/dockerfile:1
# =============================================================================
# HU-053 — segunda URL pública del modelo (Hugging Face Spaces, Docker SDK).
# El contexto de construcción es la raíz del repositorio:
#   docker build -f deploy/maas-alt/Dockerfile -t gpcicd-ppe-alt:ci .
# Los pesos del modelo NO se copian: se inyectan en ejecución (HU-026).
# =============================================================================

FROM python:3.13-slim AS runtime

ENV UV_PYTHON_DOWNLOADS=never \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=7860

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates libgl1 libglib2.0-0t64 libgomp1 libquadmath0 libxcb1 \
    && rm -rf /var/lib/apt/lists/*

# uv es el único gestor de dependencias; la versión está fijada para repetir build.
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock README.md LICENSE ./
RUN uv sync --frozen --no-dev --no-install-project --extra inference
COPY src ./src
RUN uv sync --frozen --no-dev --extra inference

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 7860
CMD exec uvicorn ppe_detection.api:app --host 0.0.0.0 --port 7860
