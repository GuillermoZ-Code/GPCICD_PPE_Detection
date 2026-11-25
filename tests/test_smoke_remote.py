"""Pruebas del cliente de verificación remota REST y gRPC (HU-050, issue #106)."""

from __future__ import annotations

from typing import Any

import pytest

from ppe_detection.tools.smoke_remote import (
    GrpcRejected,
    RestResponse,
    check_grpc,
    check_ready,
    check_rest_prediction,
    format_summary,
    run_checks,
)

PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0"
    b"\xf0\x1f\x00\x05\x05\x02\x00\x8f\xa4\xd4\x0e\x00\x00\x00\x00IEND\xaeB`\x82"
)


class FakeRest:
    """Transporte REST simulado; nunca abre conexiones."""

    def __init__(self, responses: list[tuple[int, dict[str, Any]]]) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[str, str, bytes | None]] = []

    def __call__(
        self,
        method: str,
        url: str,
        data: bytes | None = None,
        content_type: str | None = None,
        timeout: float = 5.0,
    ) -> RestResponse:
        self.calls.append((method, url, data))
        status, body = self.responses.pop(0)
        return RestResponse(status=status, body=body)


class FakeGrpc:
    """Transporte gRPC simulado; nunca abre canales."""

    def __init__(self, responses: list[Any]) -> None:
        self.responses = list(responses)
        self.calls: list[bytes] = []

    def __call__(self, target: str, image: bytes, timeout: float = 5.0) -> Any:
        self.calls.append(image)
        response = self.responses.pop(0)
        if isinstance(response, BaseException):
            raise response
        return response


class FakeResponse:
    """Respuesta gRPC mínima con los campos del contrato."""

    model_version = "yolo26n-onnx-640"
    elapsed_ms = 12.5
    detections: list[Any] = []


def _ready(status: str = "ready", version: str = "yolo26n-onnx-640") -> dict[str, Any]:
    return {"status": status, "model_loaded": status == "ready", "model_version": version}


def _prediction(version: str = "yolo26n-onnx-640") -> dict[str, Any]:
    return {"model_version": version, "elapsed_ms": 12.5, "detections": []}


def test_ready_reports_model_version_ac_01() -> None:
    """AC-01: `/health/ready` aporta la versión del modelo cuando está listo."""
    rest = FakeRest([(200, _ready())])

    result = check_ready(rest, "http://ejemplo.test", 5.0)

    assert result.ok is True
    assert result.detail == "yolo26n-onnx-640"
    assert rest.calls == [("GET", "http://ejemplo.test/health/ready", None)]


def test_valid_rest_prediction_reports_latency_ac_01() -> None:
    """AC-01: una predicción REST válida informa versión y latencia."""
    rest = FakeRest([(200, _prediction())])

    result = check_rest_prediction(rest, "http://ejemplo.test", PNG, "yolo26n-onnx-640", 5.0)

    assert result.ok is True
    assert "12.5 ms" in result.detail
    assert rest.calls[0][0] == "POST"
    assert rest.calls[0][2] is not None


def test_grpc_prediction_reports_version_and_latency_ac_01() -> None:
    """AC-01: una predicción gRPC válida informa versión y latencia."""
    grpc_call = FakeGrpc([FakeResponse()])

    result = check_grpc(grpc_call, "127.0.0.1:9000", PNG, "yolo26n-onnx-640", 5.0)

    assert result.ok is True
    assert "12.5 ms" in result.detail
    assert grpc_call.calls == [PNG]


def test_invalid_rest_image_returns_400_ac_02() -> None:
    """AC-02: una imagen inválida se rechaza con 400 antes de inferir."""
    rest = FakeRest([(400, {"detail": "imagen no válida"})])

    result = check_rest_prediction(rest, "http://ejemplo.test", b"no-imagen", "", 5.0)

    assert result.ok is True
    assert "400" in result.detail


def test_invalid_grpc_image_is_rejected_ac_02() -> None:
    """AC-02: gRPC rechaza la entrada inválida con INVALID_ARGUMENT."""
    error = GrpcRejected(code="INVALID_ARGUMENT", detail="imagen no válida")
    grpc_call = FakeGrpc([error])

    result = check_grpc(grpc_call, "127.0.0.1:9000", b"no-imagen", "", 5.0)

    assert result.ok is True
    assert "INVALID_ARGUMENT" in result.detail


def test_failed_check_returns_nonzero_ac_02() -> None:
    """AC-02: un `ready` caído produce código de salida distinto de cero."""
    rest = FakeRest(
        [
            (503, _ready(status="not_ready")),
            (200, _prediction()),
            (400, {"detail": "inválida"}),
            (503, _ready(status="not_ready")),
        ]
    )
    grpc_call = FakeGrpc([FakeResponse(), GrpcRejected("INVALID_ARGUMENT", "inválida")])

    report = run_checks(rest, grpc_call, "http://ejemplo.test", "127.0.0.1:9000", PNG, 5.0)

    assert report.ok is False
    assert any(item.name == "rest_ready" and not item.ok for item in report.checks)
    assert "FALLO" in format_summary(report)


def test_service_stays_ready_after_rejection_ac_02() -> None:
    """AC-02: tras un rechazo, el servicio sigue respondiendo `ready`."""
    rest = FakeRest(
        [
            (200, _ready()),
            (200, _prediction()),
            (400, {"detail": "inválida"}),
            (200, _ready()),
        ]
    )
    grpc_call = FakeGrpc([FakeResponse(), GrpcRejected("INVALID_ARGUMENT", "inválida")])

    report = run_checks(rest, grpc_call, "http://ejemplo.test", "127.0.0.1:9000", PNG, 5.0)

    assert report.ok is True
    assert len([item for item in report.checks if item.name == "rest_ready"]) == 2


def test_simulated_transports_need_no_network_ac_03(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-03: las pruebas usan transportes simulados, sin red ni pesos."""

    def sin_red(*_: object, **__: object) -> None:
        raise AssertionError("Se intentó usar la red")

    monkeypatch.setattr("urllib.request.urlopen", sin_red)
    monkeypatch.setattr("grpc.insecure_channel", sin_red)
    rest = FakeRest([(200, _ready())])

    result = check_ready(rest, "http://ejemplo.test", 5.0)

    assert result.ok is True
