"""Verificación remota de la API REST y el servicio gRPC (HU-050).

Uso:
    uv run python -m ppe_detection.tools.smoke_remote --image ruta/imagen.png

Los transportes son inyectables para que las pruebas no abran conexiones ni
carguen pesos. El CLI construye transportes reales con `urllib` y el cliente
gRPC existente.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
import uuid
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

from ppe_detection.grpc import client as grpc_client

DEFAULT_API_URL = "http://127.0.0.1:8000"
DEFAULT_GRPC_TARGET = "127.0.0.1:9000"
DEFAULT_TIMEOUT = 5.0


@dataclass(frozen=True)
class RestResponse:
    """Respuesta REST normalizada: código HTTP y cuerpo decodificado."""

    status: int
    body: dict[str, Any]


@dataclass(frozen=True)
class CheckResult:
    """Resultado de una comprobación independiente."""

    name: str
    ok: bool
    detail: str


class GrpcRejected(Exception):
    """Rechazo gRPC esperado, con el código del estado y su detalle."""

    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class SmokeReport:
    """Informe agregado de la verificación remota."""

    checks: tuple[CheckResult, ...]
    model_version: str
    latency_ms: float

    @property
    def ok(self) -> bool:
        """True solo si todas las comprobaciones pasaron."""
        return all(item.ok for item in self.checks)


@runtime_checkable
class RestTransport(Protocol):
    """Transporte REST inyectable."""

    def __call__(
        self,
        method: str,
        url: str,
        data: bytes | None = None,
        content_type: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> RestResponse: ...


@runtime_checkable
class GrpcTransport(Protocol):
    """Transporte gRPC inyectable."""

    def __call__(self, target: str, image: bytes, timeout: float = DEFAULT_TIMEOUT) -> Any: ...


def multipart(image: bytes, filename: str = "smoke.png") -> tuple[bytes, str]:
    """Construye el cuerpo `multipart/form-data` para `/predict`."""
    boundary = f"----ppe-smoke-{uuid.uuid4().hex}"
    body = (
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            "Content-Type: image/png\r\n\r\n"
        ).encode("ascii")
        + image
        + f"\r\n--{boundary}--\r\n".encode("ascii")
    )
    return body, f"multipart/form-data; boundary={boundary}"


def _url(api_url: str, path: str) -> str:
    """Compone una URL sin duplicar la barra final."""
    return f"{api_url.rstrip('/')}{path}"


def _version_of(body: dict[str, Any]) -> str:
    """Extrae la versión del modelo de un cuerpo JSON."""
    return str(body.get("model_version") or "")


def _latency_of(body: dict[str, Any]) -> float:
    """Extrae la latencia declarada; devuelve -1 si no es válida."""
    try:
        return float(body.get("elapsed_ms", -1))
    except (TypeError, ValueError):
        return -1.0


def check_ready(rest: RestTransport, api_url: str, timeout: float) -> CheckResult:
    """Comprueba `/health/ready`; el detalle es la versión del modelo."""
    try:
        response = rest("GET", _url(api_url, "/health/ready"), timeout=timeout)
    except Exception as exc:
        return CheckResult("rest_ready", False, f"sin respuesta: {exc}")
    if response.status != 200 or response.body.get("status") != "ready":
        return CheckResult("rest_ready", False, f"HTTP {response.status}: no está listo")
    version = _version_of(response.body)
    if not version:
        return CheckResult("rest_ready", False, "sin versión de modelo")
    return CheckResult("rest_ready", True, version)


def check_rest_prediction(
    rest: RestTransport,
    api_url: str,
    image: bytes,
    expected_version: str,
    timeout: float,
) -> CheckResult:
    """Comprueba una predicción REST; sin versión esperada exige un 400."""
    data, content_type = multipart(image)
    name = "rest_predict_invalid" if not expected_version else "rest_predict_valid"
    try:
        response = rest("POST", _url(api_url, "/predict"), data, content_type, timeout)
    except Exception as exc:
        return CheckResult(name, False, f"sin respuesta: {exc}")
    if not expected_version:
        if response.status == 400:
            return CheckResult(name, True, "HTTP 400: entrada rechazada")
        return CheckResult(name, False, f"se esperaba HTTP 400, se obtuvo {response.status}")
    if response.status != 200:
        return CheckResult(name, False, f"HTTP {response.status}")
    version = _version_of(response.body)
    latency = _latency_of(response.body)
    if version != expected_version or latency < 0:
        return CheckResult(name, False, "respuesta sin versión o latencia coherente")
    return CheckResult(name, True, f"{version} · {latency:.1f} ms")


def check_grpc(
    grpc_call: GrpcTransport,
    target: str,
    image: bytes,
    expected_version: str,
    timeout: float,
) -> CheckResult:
    """Comprueba `Detect`; sin versión esperada exige `INVALID_ARGUMENT`."""
    name = "grpc_predict_invalid" if not expected_version else "grpc_predict_valid"
    try:
        response = grpc_call(target, image, timeout)
    except GrpcRejected as exc:
        if not expected_version and exc.code == "INVALID_ARGUMENT":
            return CheckResult(name, True, f"{exc.code}: {exc.detail}")
        return CheckResult(name, False, f"{exc.code}: {exc.detail}")
    except Exception as exc:
        return CheckResult(name, False, f"sin respuesta: {exc}")
    if not expected_version:
        return CheckResult(name, False, "la entrada inválida fue aceptada")
    version = str(getattr(response, "model_version", "") or "")
    try:
        latency = float(getattr(response, "elapsed_ms", -1))
    except (TypeError, ValueError):
        latency = -1.0
    if version != expected_version or latency < 0:
        return CheckResult(name, False, "respuesta sin versión o latencia coherente")
    return CheckResult(name, True, f"{version} · {latency:.1f} ms")


def run_checks(
    rest: RestTransport,
    grpc_call: GrpcTransport,
    api_url: str,
    target: str,
    image: bytes,
    timeout: float,
) -> SmokeReport:
    """Ejecuta todas las comprobaciones remotas y devuelve el informe."""
    ready = check_ready(rest, api_url, timeout)
    version = ready.detail if ready.ok else ""
    checks = [
        ready,
        check_rest_prediction(rest, api_url, image, version, timeout),
        check_rest_prediction(rest, api_url, b"no-imagen", "", timeout),
        check_grpc(grpc_call, target, image, version, timeout),
        check_grpc(grpc_call, target, b"no-imagen", "", timeout),
        check_ready(rest, api_url, timeout),
    ]
    valid_rest = checks[1]
    latency = _latency_of({"elapsed_ms": valid_rest.detail.split("·")[-1].strip().split(" ")[0]})
    return SmokeReport(tuple(checks), version, latency)


def format_summary(report: SmokeReport) -> str:
    """Formatea el informe para la terminal."""
    state = "OK" if report.ok else "FALLO"
    lines = [f"Verificación remota: {state}"]
    lines.extend(
        f"  [{'ok' if item.ok else 'FALLO'}] {item.name}: {item.detail}" for item in report.checks
    )
    modelo = report.model_version or "desconocido"
    lines.append(f"Modelo: {modelo} · latencia REST {report.latency_ms:.1f} ms")
    return "\n".join(lines)


def _real_rest(
    method: str,
    url: str,
    data: bytes | None = None,
    content_type: str | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> RestResponse:
    """Transporte REST real basado en `urllib`, sin dependencias nuevas."""
    request = urllib.request.Request(url, data=data, method=method)
    if content_type:
        request.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
            status = int(getattr(response, "status", response.getcode()))
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        status = int(exc.code)
    body = json.loads(raw.decode("utf-8")) if raw else {}
    return RestResponse(status=status, body=body)


def _real_grpc(target: str, image: bytes, timeout: float = DEFAULT_TIMEOUT) -> Any:
    """Transporte gRPC real que normaliza los errores del cliente."""
    try:
        return grpc_client.detect(target, image, timeout=timeout)
    except Exception as exc:
        code, detail = grpc_client.call_status(exc)
        raise GrpcRejected(code=code, detail=detail) from exc


def main(argv: Sequence[str] | None = None) -> int:
    """CLI de verificación; devuelve 0 solo si todo pasa."""
    parser = argparse.ArgumentParser(description="Verifica la API REST y gRPC desplegadas.")
    parser.add_argument(
        "--api-url",
        default=os.getenv("PPE_API_URL", DEFAULT_API_URL),
        help="URL base de la API (por omisión %(default)s).",
    )
    parser.add_argument(
        "--grpc-target",
        default=os.getenv("PPE_GRPC_TARGET", DEFAULT_GRPC_TARGET),
        help="host:puerto de gRPC (por omisión %(default)s).",
    )
    parser.add_argument("--image", required=True, type=Path, help="JPEG o PNG de entrada.")
    parser.add_argument(
        "--timeout", type=float, default=DEFAULT_TIMEOUT, help="Segundos por petición."
    )
    args = parser.parse_args(argv)

    report = run_checks(
        _real_rest,
        _real_grpc,
        args.api_url,
        args.grpc_target,
        args.image.read_bytes(),
        args.timeout,
    )
    print(format_summary(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
