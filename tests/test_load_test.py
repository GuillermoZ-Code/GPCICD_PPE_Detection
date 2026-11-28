"""HU-063 — Pruebas del instrumento de carga y del informe de capacidad.

AC-01: CLI reproducible con httpx; AC-02: métricas; AC-03: recomendación.
Las pruebas inyectan cliente, reloj y muestreo: no abren red ni cargan pesos.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from ppe_detection.tools import load_test


class FakeResponse:
    """Respuesta HTTP mínima para el cliente inyectable."""

    def __init__(self, status_code: int) -> None:
        self.status_code = status_code


class FakeClient:
    """Cliente con la interfaz `request` que usa `run_load`."""

    def __init__(self, handler: Any) -> None:
        self.handler = handler
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def request(self, method: str, url: str, **kwargs: Any) -> FakeResponse:
        """Registra la llamada y devuelve la respuesta simulada."""
        self.calls.append((method, url, kwargs))
        return self.handler(method, url, kwargs)


def _clock(values: list[float]) -> Any:
    """Reloj determinista que consume los valores en orden."""
    iterator = iter(values)

    def clock() -> float:
        return next(iterator)

    return clock


def _sample() -> load_test.ResourceSample:
    """Muestreo fijo para las pruebas."""
    return load_test.ResourceSample(cpu_percent=42.0, rss_mb=180.0, ram_percent=55.0)


def _results(latency_ms: float, count: int, *, errors: int = 0) -> tuple[Any, ...]:
    """Construye resultados con latencia uniforme y errores HTTP 500."""
    results = []
    for index in range(count):
        failed = index < errors
        results.append(
            load_test.RequestResult(
                status=500 if failed else 200,
                latency_ms=latency_ms,
                error="HTTP 500" if failed else None,
            )
        )
    return tuple(results)


def _summary(
    *,
    latency_ms: float = 100.0,
    count: int = 20,
    errors: int = 0,
    elapsed_s: float = 1.0,
    cpu_percent: float = 40.0,
    rss_mb: float = 200.0,
    ram_percent: float = 50.0,
) -> Any:
    """Construye un resumen directo para probar agregación y recomendación."""
    return load_test.LoadSummary(
        config=load_test.LoadConfig(url="http://127.0.0.1:8000", requests=count),
        results=_results(latency_ms, count, errors=errors),
        elapsed_s=elapsed_s,
        resources=load_test.ResourceUsage(
            cpu_percent_max=cpu_percent,
            rss_mb_max=rss_mb,
            ram_percent_max=ram_percent,
            sample_count=4,
        ),
    )


def test_ac01_parse_args_defaults_and_validation() -> None:
    """AC-01: el CLI expone los parámetros y valores por defecto acordados."""
    # Act
    config = load_test.parse_args(["--url", "https://ejemplo.test/api"])

    # Assert
    assert config.url == "https://ejemplo.test/api"
    assert config.path == "/health"
    assert config.requests == 60
    assert config.concurrency == 4
    assert config.timeout == 10.0
    assert config.sample_interval == 0.25
    assert config.auth_env == "PPE_LOAD_AUTH"
    assert config.label == "validación local del instrumento"
    assert config.report == Path("docs/operacion/capacidad.md")


def test_ac01_rejects_invalid_configuration() -> None:
    """AC-01: la configuración inválida falla antes de abrir conexiones."""
    # Act / Assert
    with pytest.raises(SystemExit):
        load_test.parse_args(["--requests", "0"])
    with pytest.raises(SystemExit):
        load_test.parse_args(["--concurrency", "-1"])
    with pytest.raises(SystemExit):
        load_test.parse_args(["--url", "ftp://ejemplo.test"])
    with pytest.raises(SystemExit):
        load_test.parse_args(["--path", "health"])
    with pytest.raises(SystemExit):
        load_test.parse_args(["--image", "no-existe.png"])


def test_ac01_sends_get_requests_through_client() -> None:
    """AC-01: sin imagen se envían GET al path configurado y se mide su latencia."""
    # Arrange
    config = load_test.LoadConfig(url="http://127.0.0.1:8000", requests=2, concurrency=1)
    client = FakeClient(lambda *_: FakeResponse(200))
    clock = _clock([0.0, 0.0, 0.01, 0.1, 0.115, 0.2])

    # Act
    summary = load_test.run_load(config, client, clock=clock, sample=_sample)

    # Assert
    assert len(client.calls) == 2
    assert all(call[0] == "GET" for call in client.calls)
    assert client.calls[0][1] == "http://127.0.0.1:8000/health"
    assert client.calls[0][2]["timeout"] == 10.0
    assert summary.p50_ms == 10.0
    assert summary.p95_ms == 15.0


def test_ac01_sends_multipart_post_when_image_is_given(tmp_path: Path) -> None:
    """AC-01: con imagen se envía POST multipart y se lee el archivo una vez."""
    # Arrange
    image = tmp_path / "muestra.png"
    image.write_bytes(b"contenido-png")
    config = load_test.LoadConfig(
        url="http://127.0.0.1:8000", path="/predict", requests=1, image=image
    )
    client = FakeClient(lambda *_: FakeResponse(200))
    clock = _clock([0.0, 0.0, 0.02, 0.1])

    # Act
    load_test.run_load(config, client, clock=clock, sample=_sample)

    # Assert
    method, url, kwargs = client.calls[0]
    assert method == "POST"
    assert url == "http://127.0.0.1:8000/predict"
    assert kwargs["files"]["file"][0] == "muestra.png"
    assert kwargs["files"]["file"][1] == b"contenido-png"


def test_ac01_concurrency_configures_executor(monkeypatch: pytest.MonkeyPatch) -> None:
    """AC-01: la concurrencia configurable se pasa al executor como max_workers."""
    # Arrange
    real_executor = load_test.ThreadPoolExecutor
    observed: list[int] = []

    def factory(max_workers: int) -> Any:
        observed.append(max_workers)
        return real_executor(max_workers=max_workers)

    monkeypatch.setattr(load_test, "ThreadPoolExecutor", factory)
    config = load_test.LoadConfig(url="http://127.0.0.1:8000", requests=6, concurrency=3)
    client = FakeClient(lambda *_: FakeResponse(200))

    # Act
    summary = load_test.run_load(config, client, sample=_sample)

    # Assert
    assert observed == [3]
    assert summary.total == 6
    assert len(client.calls) == 6


def test_ac01_forwards_timeout_and_auth() -> None:
    """AC-01: timeout y credenciales llegan a cada petición."""
    # Arrange
    config = load_test.LoadConfig(
        url="http://127.0.0.1:8000",
        requests=1,
        timeout=1.5,
        auth=("demo", "clave"),
    )
    client = FakeClient(lambda *_: FakeResponse(200))
    clock = _clock([0.0, 0.0, 0.01, 0.1])

    # Act
    load_test.run_load(config, client, clock=clock, sample=_sample)

    # Assert
    assert client.calls[0][2]["timeout"] == 1.5
    assert client.calls[0][2]["auth"] == ("demo", "clave")


def test_ac02_percentile_uses_nearest_rank() -> None:
    """AC-02: p50 y p95 usan nearest-rank, incluso con una sola muestra."""
    # Act / Assert
    assert load_test.percentile([10.0, 20.0, 30.0, 40.0], 0.50) == 20.0
    assert load_test.percentile([10.0, 20.0, 30.0, 40.0], 0.95) == 40.0
    assert load_test.percentile([5.0], 0.95) == 5.0
    assert load_test.percentile([], 0.50) == 0.0


def test_ac02_counts_successes_and_normalizes_errors() -> None:
    """AC-02: respuestas 5xx y excepciones se agrupan como errores."""
    # Arrange
    config = load_test.LoadConfig(url="http://127.0.0.1:8000", requests=3, concurrency=1)
    outcomes = [FakeResponse(200), FakeResponse(500), TimeoutError("sin respuesta")]
    index = 0

    def handler(*_: Any) -> Any:
        nonlocal index
        outcome = outcomes[index]
        index += 1
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    client = FakeClient(handler)
    clock = _clock([0.0, 0.0, 0.01, 0.1, 0.11, 0.2, 0.21, 0.3])

    # Act
    summary = load_test.run_load(config, client, clock=clock, sample=_sample)

    # Assert
    assert summary.total == 3
    assert summary.ok_count == 1
    assert summary.error_count == 2
    assert summary.errors == {"HTTP 500": 1, "TimeoutError: sin respuesta": 1}


def test_ac02_computes_throughput_from_elapsed_time() -> None:
    """AC-02: el throughput sale del total de peticiones entre la duración."""
    # Arrange
    config = load_test.LoadConfig(url="http://127.0.0.1:8000", requests=2, concurrency=1)
    client = FakeClient(lambda *_: FakeResponse(200))
    clock = _clock([0.0, 0.0, 0.0, 0.5, 0.5, 2.0])

    # Act
    summary = load_test.run_load(config, client, clock=clock, sample=_sample)

    # Assert
    assert summary.elapsed_s == 2.0
    assert summary.throughput_rps == 1.0


def test_ac02_captures_cpu_ram_and_rss_samples() -> None:
    """AC-02: se registran CPU, RSS y RAM del muestreo durante la carga."""
    # Arrange
    config = load_test.LoadConfig(url="http://127.0.0.1:8000", requests=1, concurrency=1)
    client = FakeClient(lambda *_: FakeResponse(200))

    # Act
    summary = load_test.run_load(config, client, sample=_sample, monitor_interval=0.001)

    # Assert
    assert summary.resources.sample_count >= 1
    assert summary.resources.cpu_percent_max == 42.0
    assert summary.resources.rss_mb_max == 180.0
    assert summary.resources.ram_percent_max == 55.0


def test_ac02_report_contains_metrics() -> None:
    """AC-02: el informe muestra p50, p95, errores, CPU, RAM y RSS."""
    # Arrange
    summary = _summary(latency_ms=350.0, count=20, errors=1, elapsed_s=2.0, cpu_percent=70.0)
    recommendation = load_test.recommend(summary)

    # Act
    report = load_test.render_report(
        summary, recommendation, label="validación local", date="2026-11-27"
    )

    # Assert
    assert "| p50 | 350.0 ms |" in report
    assert "| p95 | 350.0 ms |" in report
    assert "| Throughput | 10.00 req/s |" in report
    assert "| Éxitos | 19/20 |" in report
    assert "| Errores | 1 |" in report
    assert "| CPU máxima del proceso | 70.0 % |" in report
    assert "| RAM del sistema | 50.0 % |" in report
    assert "| RSS máxima | 200.0 MB |" in report


def test_ac02_report_labels_local_validation_not_real_droplet() -> None:
    """AC-02: el informe no puede presentarse como medición real del Droplet."""
    # Arrange
    summary = _summary()
    recommendation = load_test.recommend(summary)

    # Act
    report = load_test.render_report(summary, recommendation, label="local", date="2026-11-27")

    # Assert
    assert "validación local del instrumento" in report
    assert "no es una medición real del Droplet" in report
    assert "Guillermo Zabala" in report
    assert "sslip.io" not in report


def test_ac03_recommends_small_droplet_when_headroom() -> None:
    """AC-03: con p95 bajo y CPU holgada se recomienda el Droplet pequeño."""
    # Arrange
    summary = _summary(latency_ms=120.0, count=20, elapsed_s=1.0, cpu_percent=40.0)

    # Act
    recommendation = load_test.recommend(summary)

    # Assert
    assert recommendation.droplet == "s-1vcpu-2gb"
    assert recommendation.workers == 2


def test_ac03_recommends_medium_droplet_when_p95_grows() -> None:
    """AC-03: al crecer p95 se recomienda el Droplet mediano y 4 workers."""
    # Arrange
    summary = _summary(latency_ms=350.0, count=20, elapsed_s=2.0, cpu_percent=70.0)

    # Act
    recommendation = load_test.recommend(summary)

    # Assert
    assert recommendation.droplet == "s-2vcpu-4gb"
    assert recommendation.workers == 4


def test_ac03_recommends_large_droplet_or_error_fix() -> None:
    """AC-03: saturación y errores altos tienen recomendaciones distintas."""
    # Arrange
    saturated = _summary(latency_ms=800.0, count=20, elapsed_s=2.0, cpu_percent=95.0)
    with_errors = _summary(latency_ms=100.0, count=20, errors=2, elapsed_s=1.0)

    # Act
    large = load_test.recommend(saturated)
    fix = load_test.recommend(with_errors)

    # Assert
    assert large.droplet == "s-4vcpu-8gb"
    assert large.workers == 6
    assert fix.droplet == "s-2vcpu-4gb"
    assert fix.workers == 2
    assert "errores" in fix.reason.lower()


def test_ac03_report_shows_recommendation_and_reproduction() -> None:
    """AC-03: el informe explica la recomendación y cómo reproducir la medición."""
    # Arrange
    summary = _summary(latency_ms=350.0, count=20, elapsed_s=2.0)
    recommendation = load_test.recommend(summary)

    # Act
    report = load_test.render_report(
        summary, recommendation, label="validación local", date="2026-11-27"
    )

    # Assert
    assert f"`{recommendation.droplet}`" in report
    assert f"| Workers API | {recommendation.workers} |" in report
    assert recommendation.reason in report
    assert "uv run python -m ppe_detection.tools.load_test" in report
