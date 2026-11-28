"""Prueba de carga ligera e informe de capacidad (HU-063).

El CLI ejecuta un lote configurable de peticiones HTTP con concurrencia acotada y
escribe un informe con p50, p95, errores y uso de CPU/RAM. La medición versionada es
una validación local del instrumento: no sustituye la medición real en el Droplet.

Uso:
    uv run python -m ppe_detection.tools.load_test \
        --url http://127.0.0.1:8000 --requests 60 --concurrency 4

Las dependencias de red y muestreo se importan de forma diferida: las pruebas inyectan
un cliente, un reloj y un muestreador, por lo que no abren conexiones ni cargan pesos.
"""

from __future__ import annotations

import argparse
import importlib
import math
import os
import sys
import threading
import time
from collections import Counter
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

DEFAULT_URL = "http://127.0.0.1:8000"
DEFAULT_PATH = "/health"
DEFAULT_REQUESTS = 60
DEFAULT_CONCURRENCY = 4
DEFAULT_TIMEOUT = 10.0
DEFAULT_SAMPLE_INTERVAL = 0.25
DEFAULT_AUTH_ENV = "PPE_LOAD_AUTH"
DEFAULT_LABEL = "validación local del instrumento"
DEFAULT_REPORT = Path("docs/operacion/capacidad.md")

_PERFORMANCE_START = time.perf_counter()


@dataclass(frozen=True)
class LoadConfig:
    """Parámetros validados de un ensayo de carga."""

    url: str = DEFAULT_URL
    path: str = DEFAULT_PATH
    requests: int = DEFAULT_REQUESTS
    concurrency: int = DEFAULT_CONCURRENCY
    timeout: float = DEFAULT_TIMEOUT
    image: Path | None = None
    sample_interval: float = DEFAULT_SAMPLE_INTERVAL
    auth_env: str = DEFAULT_AUTH_ENV
    auth: tuple[str, str] | None = None
    label: str = DEFAULT_LABEL
    report: Path = DEFAULT_REPORT


@dataclass(frozen=True)
class RequestResult:
    """Latencia, código y error normalizado de una petición."""

    status: int
    latency_ms: float
    error: str | None = None

    @property
    def ok(self) -> bool:
        """True cuando la respuesta es 2xx."""
        return self.error is None and 200 <= self.status < 300


@dataclass(frozen=True)
class ResourceSample:
    """Una observación de CPU, memoria residente y RAM del sistema."""

    cpu_percent: float
    rss_mb: float
    ram_percent: float


@dataclass(frozen=True)
class ResourceUsage:
    """Máximos observados durante el ensayo."""

    cpu_percent_max: float
    rss_mb_max: float
    ram_percent_max: float
    sample_count: int


@dataclass(frozen=True)
class LoadSummary:
    """Agregación de resultados, percentiles y recursos."""

    config: LoadConfig
    results: tuple[RequestResult, ...]
    elapsed_s: float
    resources: ResourceUsage

    @property
    def total(self) -> int:
        """Número de peticiones ejecutadas."""
        return len(self.results)

    @property
    def ok_count(self) -> int:
        """Número de respuestas correctas."""
        return sum(1 for item in self.results if item.ok)

    @property
    def error_count(self) -> int:
        """Número de peticiones con error."""
        return self.total - self.ok_count

    @property
    def errors(self) -> dict[str, int]:
        """Errores agrupados por motivo, en orden determinista."""
        counts = Counter(item.error for item in self.results if item.error is not None)
        return dict(sorted(counts.items()))

    @property
    def error_rate(self) -> float:
        """Proporción de errores sobre el total."""
        return self.error_count / self.total if self.total else 0.0

    @property
    def p50_ms(self) -> float:
        """Latencia mediana con percentil nearest-rank."""
        return percentile([item.latency_ms for item in self.results], 0.50)

    @property
    def p95_ms(self) -> float:
        """Latencia p95 con percentil nearest-rank."""
        return percentile([item.latency_ms for item in self.results], 0.95)

    @property
    def throughput_rps(self) -> float:
        """Peticiones por segundo sobre la duración observada."""
        return self.total / self.elapsed_s if self.elapsed_s > 0 else 0.0


@dataclass(frozen=True)
class Recommendation:
    """Tamaño de Droplet, workers y motivo de la recomendación."""

    droplet: str
    workers: int
    reason: str


def percentile(values: Sequence[float], quantile: float) -> float:
    """Devuelve el percentil nearest-rank: `ceil(q·n)` sobre la lista ordenada."""
    if not values:
        return 0.0
    ordered = sorted(values)
    rank = max(1, math.ceil(quantile * len(ordered)))
    return float(ordered[min(rank, len(ordered)) - 1])


def validate_config(config: LoadConfig) -> None:
    """Rechaza configuraciones inválidas antes de construir clientes o abrir red."""
    if config.requests < 1:
        raise ValueError("requests debe ser mayor que cero")
    if config.concurrency < 1:
        raise ValueError("concurrency debe ser mayor que cero")
    if config.timeout <= 0:
        raise ValueError("timeout debe ser mayor que cero")
    if config.sample_interval <= 0:
        raise ValueError("sample-interval debe ser mayor que cero")
    parsed = urlparse(config.url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("url debe ser http o https y tener host")
    if not config.path.startswith("/"):
        raise ValueError("path debe empezar por /")
    if config.image is not None and not config.image.is_file():
        raise ValueError(f"la imagen no existe: {config.image}")


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser del CLI de carga."""
    parser = argparse.ArgumentParser(description="Prueba de carga ligera sobre una API HTTP.")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL base del objetivo")
    parser.add_argument("--path", default=DEFAULT_PATH, help="Ruta absoluta a ejercitar")
    parser.add_argument("--requests", type=int, default=DEFAULT_REQUESTS)
    parser.add_argument("--concurrency", type=int, default=DEFAULT_CONCURRENCY)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--image", type=Path, default=None, help="Imagen para POST multipart")
    parser.add_argument("--sample-interval", type=float, default=DEFAULT_SAMPLE_INTERVAL)
    parser.add_argument("--auth-env", default=DEFAULT_AUTH_ENV, help="Variable con usuario:clave")
    parser.add_argument("--label", default=DEFAULT_LABEL, help="Etiqueta del ensayo")
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT, help="Informe Markdown")
    return parser


def parse_args(argv: Sequence[str] | None = None) -> LoadConfig:
    """Parsea y valida los argumentos; convierte errores en `SystemExit`."""
    parser = build_parser()
    args = parser.parse_args(argv)
    config = LoadConfig(
        url=args.url,
        path=args.path,
        requests=args.requests,
        concurrency=args.concurrency,
        timeout=args.timeout,
        image=args.image,
        sample_interval=args.sample_interval,
        auth_env=args.auth_env,
        label=args.label,
        report=args.output,
    )
    try:
        validate_config(config)
    except ValueError as exc:
        parser.error(str(exc))
    return config


def _httpx_module() -> Any:
    """Importa `httpx`; usa `httpx2` en entornos que no instalan los extras."""
    try:
        return importlib.import_module("httpx")
    except ModuleNotFoundError:
        return importlib.import_module("httpx2")


def build_client(config: LoadConfig) -> Any:
    """Construye el cliente real con la configuración validada."""
    module = _httpx_module()
    return module.Client(base_url=config.url, timeout=config.timeout)


def _sysconf(name: str) -> int | None:
    """Lee `os.sysconf` cuando la plataforma lo expone."""
    sysconf = getattr(os, "sysconf", None)
    if sysconf is None:
        return None
    try:
        return int(sysconf(name))
    except (OSError, TypeError, ValueError):
        return None


def _process_rss_mb() -> float:
    """Memoria residente aproximada sin dependencias externas."""
    statm = Path("/proc/self/statm")
    if statm.is_file():
        try:
            pages = int(statm.read_text(encoding="utf-8").split()[1])
            page_size = _sysconf("SC_PAGE_SIZE")
            if page_size:
                return pages * page_size / (1024**2)
        except (IndexError, OSError, ValueError):
            return 0.0
    try:
        resource = importlib.import_module("resource")
        getrusage = getattr(resource, "getrusage", None)
        rusage_self = getattr(resource, "RUSAGE_SELF", None)
        if getrusage is None or rusage_self is None:
            return 0.0
        rss = int(getrusage(rusage_self).ru_maxrss)
        divisor = 1024.0 if sys.platform == "linux" else 1024.0**2
        return rss / divisor
    except (ImportError, OSError, TypeError, ValueError):
        return 0.0


def _system_ram_percent() -> float:
    """Porcentaje de RAM usada, con librería estándar cuando no hay psutil."""
    total = _sysconf("SC_PHYS_PAGES")
    available = _sysconf("SC_AVPHYS_PAGES")
    if total is not None and available is not None and total > 0:
        return (1.0 - available / total) * 100.0
    if sys.platform == "win32":
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                """Estructura de `GlobalMemoryStatusEx`."""

                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
            return float(status.dwMemoryLoad)
        except (AttributeError, OSError, ValueError):
            return 0.0
    return 0.0


def sample_resources() -> ResourceSample:
    """Muestra CPU/RAM con psutil si está disponible; si no, usa una aproximación."""
    try:
        psutil = importlib.import_module("psutil")
    except ModuleNotFoundError:
        cpu = time.process_time() / max(time.perf_counter() - _PERFORMANCE_START, 1e-9)
        return ResourceSample(cpu * 100.0, _process_rss_mb(), _system_ram_percent())
    process = psutil.Process()
    return ResourceSample(
        cpu_percent=float(psutil.cpu_percent(interval=None)),
        rss_mb=float(process.memory_info().rss) / (1024**2),
        ram_percent=float(psutil.virtual_memory().percent),
    )


def _monitor(
    stop: threading.Event,
    samples: list[ResourceSample],
    sample: Callable[[], ResourceSample],
    interval: float,
) -> None:
    """Toma muestras hasta que el lote termina."""
    samples.append(sample())
    while not stop.wait(interval):
        samples.append(sample())


def _request_once(
    client: Any,
    config: LoadConfig,
    clock: Callable[[], float],
) -> RequestResult:
    """Ejecuta una petición y normaliza su resultado."""
    url = f"{config.url.rstrip('/')}{config.path}"
    kwargs: dict[str, Any] = {"timeout": config.timeout}
    if config.auth is not None:
        kwargs["auth"] = config.auth
    if config.image is not None:
        kwargs["files"] = {"file": (config.image.name, config.image.read_bytes(), "image/png")}
    started = clock()
    try:
        method = "POST" if config.image is not None else "GET"
        response = client.request(method, url, **kwargs)
        status = int(response.status_code)
        error = None if 200 <= status < 300 else f"HTTP {status}"
    except Exception as exc:
        status = 0
        error = f"{type(exc).__name__}: {exc}"
    return RequestResult(status, (clock() - started) * 1000.0, error)


def run_load(
    config: LoadConfig,
    client: Any,
    *,
    clock: Callable[[], float] = time.perf_counter,
    sample: Callable[[], ResourceSample] = sample_resources,
    monitor_interval: float | None = None,
    executor_factory: Callable[[int], Any] | None = None,
) -> LoadSummary:
    """Ejecuta `requests` peticiones con concurrencia acotada y devuelve el resumen."""
    validate_config(config)
    start = clock()
    stop = threading.Event()
    samples: list[ResourceSample] = []
    interval = config.sample_interval if monitor_interval is None else monitor_interval
    monitor = threading.Thread(target=_monitor, args=(stop, samples, sample, interval), daemon=True)
    monitor.start()

    factory = executor_factory or (lambda workers: ThreadPoolExecutor(max_workers=workers))
    try:
        with factory(config.concurrency) as pool:
            futures = [
                pool.submit(_request_once, client, config, clock) for _ in range(config.requests)
            ]
            results = tuple(future.result() for future in futures)
    finally:
        stop.set()
        monitor.join(timeout=1.0)

    if not samples:
        samples.append(sample())
    elapsed_s = max(clock() - start, 1e-9)
    resources = ResourceUsage(
        cpu_percent_max=max(item.cpu_percent for item in samples),
        rss_mb_max=max(item.rss_mb for item in samples),
        ram_percent_max=max(item.ram_percent for item in samples),
        sample_count=len(samples),
    )
    return LoadSummary(config, results, elapsed_s, resources)


def recommend(summary: LoadSummary) -> Recommendation:
    """Deriva tamaño de Droplet y workers de p95, throughput, CPU y errores."""
    if summary.error_rate > 0.05:
        return Recommendation("s-2vcpu-4gb", 2, "corregir errores antes de ampliar la instancia")
    if (
        summary.p95_ms <= 200.0
        and summary.throughput_rps >= 15.0
        and summary.resources.cpu_percent_max < 70.0
    ):
        return Recommendation(
            "s-1vcpu-2gb", 2, "hipótesis local: 2 workers; confirmar en el Droplet"
        )
    if summary.p95_ms <= 500.0 and summary.resources.cpu_percent_max < 85.0:
        return Recommendation(
            "s-2vcpu-4gb", 4, "hipótesis local: 4 workers; confirmar en el Droplet"
        )
    return Recommendation("s-4vcpu-8gb", 6, "saturación local: repetir la medición en el Droplet")


def _error_table(errors: dict[str, int]) -> list[str]:
    """Renderiza la tabla de errores del informe."""
    if not errors:
        return ["Sin errores."]
    lines = ["| Motivo | Veces |", "|---|---:|"]
    lines.extend(f"| {reason} | {count} |" for reason, count in errors.items())
    return lines


def render_report(
    summary: LoadSummary,
    recommendation: Recommendation,
    *,
    label: str,
    date: str,
) -> str:
    """Renderiza el informe Markdown de la validación local."""
    config = summary.config
    body = f"{config.image.name}" if config.image is not None else "sin cuerpo (GET)"
    lines = [
        "# Capacidad del servicio — validación local del instrumento",
        "",
        f"**Fecha:** {date} · **Etiqueta:** {label}",
        "",
        "> ⚠️ Esta medición se ejecutó contra un servidor local o ficticio para validar "
        "el instrumento; **no es una medición real del Droplet**. La medición real "
        "contra el servicio desplegado queda pendiente y es responsabilidad de "
        "Guillermo Zabala (@GuillermoZ-Code).",
        "",
        "## 1. Configuración",
        "",
        "| Parámetro | Valor |",
        "|---|---|",
        f"| Objetivo | `{config.url}{config.path}` |",
        f"| Peticiones | {config.requests} |",
        f"| Concurrencia | {config.concurrency} |",
        f"| Timeout | {config.timeout:.1f} s |",
        f"| Cuerpo | {body} |",
        f"| Muestreo de recursos | cada {config.sample_interval:.2f} s |",
        "",
        "## 2. Resultados",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| p50 | {summary.p50_ms:.1f} ms |",
        f"| p95 | {summary.p95_ms:.1f} ms |",
        f"| Throughput | {summary.throughput_rps:.2f} req/s |",
        f"| Éxitos | {summary.ok_count}/{summary.total} |",
        f"| Errores | {summary.error_count} |",
        f"| Duración | {summary.elapsed_s:.2f} s |",
        "",
        "### Errores",
        "",
        *_error_table(summary.errors),
        "",
        "## 3. CPU y RAM",
        "",
        "| Métrica | Valor |",
        "|---|---:|",
        f"| CPU máxima del proceso | {summary.resources.cpu_percent_max:.1f} % |",
        f"| RSS máxima | {summary.resources.rss_mb_max:.1f} MB |",
        f"| RAM del sistema | {summary.resources.ram_percent_max:.1f} % |",
        f"| Muestras | {summary.resources.sample_count} |",
        "",
        "## 4. Recomendación provisional (validación local)",
        "",
        "| Parámetro | Valor |",
        "|---|---|",
        f"| Droplet | `{recommendation.droplet}` |",
        f"| Workers API | {recommendation.workers} |",
        f"| Motivo | {recommendation.reason} |",
        "",
        "> La recomendación se deriva de una medición local: no autoriza cambiar el "
        "despliegue hasta repetir el ensayo en el Droplet.",
        "",
        "## 5. Reproducción",
        "",
        "```bash",
        "uv run python -m ppe_detection.tools.load_test \\",
        f"  --url {config.url} --path {config.path} \\",
        f"  --requests {config.requests} --concurrency {config.concurrency} \\",
        f"  --output {config.report.as_posix()}",
        "```",
        "",
        "## 6. Pendiente real",
        "",
        "- [ ] Guillermo: ejecutar el mismo script contra la URL pública con basic auth.",
        "- [ ] Guillermo: adjuntar salida real, repetir con `--image` sobre `/predict`.",
        "- [ ] Guillermo: decidir tamaño y workers definitivos con esa medición.",
        "",
    ]
    return "\n".join(lines)


def _auth_from_env(value: str | None, env_name: str) -> tuple[str, str] | None:
    """Lee `usuario:clave` del entorno sin versionar credenciales."""
    if not value:
        return None
    user, separator, password = value.partition(":")
    if not separator or not user or not password:
        raise ValueError(f"{env_name} debe tener forma usuario:clave")
    return user, password


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada: ejecuta la carga, escribe el informe y devuelve 0."""
    config = parse_args(argv)
    auth = _auth_from_env(os.environ.get(config.auth_env), config.auth_env)
    config = replace(config, auth=auth)
    client = build_client(config)
    try:
        summary = run_load(config, client)
    finally:
        close = getattr(client, "close", None)
        if close is not None:
            close()
    recommendation = recommend(summary)
    report = render_report(
        summary,
        recommendation,
        label=config.label,
        date=time.strftime("%Y-%m-%d", time.gmtime()),
    )
    config.report.parent.mkdir(parents=True, exist_ok=True)
    config.report.write_text(report, encoding="utf-8")
    print(
        f"Carga local: p50 {summary.p50_ms:.1f} ms · p95 {summary.p95_ms:.1f} ms · "
        f"{summary.error_count} errores · informe en {config.report}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
