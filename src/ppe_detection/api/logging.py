"""Logs estructurados JSON con identificador de petición (HU-047)."""

from __future__ import annotations

import json
import logging as std_logging
from time import perf_counter
from uuid import uuid4

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

logger = std_logging.getLogger("ppe_detection.api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Registra metadatos de cada petición sin tocar cabeceras ni cuerpo."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Emite una línea JSON y propaga `X-Request-ID` en la respuesta."""
        request_id = (request.headers.get("X-Request-ID") or "").strip() or str(uuid4())
        started = perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            self._log(request, 500, started, request_id)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
                headers={"X-Request-ID": request_id},
            )
        self._log(request, response.status_code, started, request_id)
        response.headers["X-Request-ID"] = request_id
        return response

    @staticmethod
    def _log(request: Request, status: int, started: float, request_id: str) -> None:
        """Serializa solo metadatos seguros de la petición."""
        payload = {
            "event": "http_request",
            "method": request.method,
            "path": request.url.path,
            "status": status,
            "duration_ms": round((perf_counter() - started) * 1000, 2),
            "request_id": request_id,
        }
        logger.info(json.dumps(payload, ensure_ascii=False, sort_keys=True))
