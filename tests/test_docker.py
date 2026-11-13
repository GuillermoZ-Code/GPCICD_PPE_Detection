"""Pruebas de HU-011 — contenedor Docker CPU.

Las pruebas estáticas (AC-011.1, AC-011.3, AC-011.4) corren en cualquier
entorno y protegen la receta del contenedor. La prueba de inferencia
(AC-011.2) arranca el contenedor real y se omite sin Docker, sin la imagen
construida o sin artefacto local; se activa con:

    PPE_DOCKER_SMOKE=1 PPE_DOCKER_MODEL=ruta/best.pt uv run pytest -m docker
"""

from __future__ import annotations

import json
import os
import re
import shutil
import socket
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any

import cv2
import numpy as np
import pytest

from ppe_detection.grpc.client import detect as grpc_detect
from ppe_detection.results import NO_DETECTIONS_MESSAGE

DOCKER_IMAGE = "gpcicd-ppe-detection:local"
DOCKERFILE = Path("Dockerfile")
DOCKERIGNORE = Path(".dockerignore")
COMPOSE_FILE = Path("compose.yml")
ENTRYPOINT = Path("docker/entrypoint.sh")
RUNBOOK = Path("docs/operacion/docker.md")

#: Catálogo canónico del `data.yaml` (CONSTITUTION §6).
CANONICAL_CLASSES = ("Gloves", "Vest", "goggles", "helmet", "mask", "safety_shoe")

#: Extensiones de artefactos prohibidas dentro de la imagen.
WEIGHT_PATTERN = re.compile(r"\.(pt|pth|onnx|h5|safetensors)\b")

#: Candidatos de artefacto para la prueba de humo (siempre fuera de Git).
MODEL_CANDIDATES = (
    Path("artifacts/models/best.pt"),
    Path("artifacts/best.pt"),
    Path("artifacts/drive/yolo11s_clean/weights/best.pt"),
)


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def _docker(*args: str) -> subprocess.CompletedProcess[str]:
    """Ejecuta un comando de Docker CLI devolviendo el proceso sin lanzar error."""
    return subprocess.run(
        ["docker", *args], capture_output=True, text=True, timeout=180, check=False
    )


# ---------------------------------------------------------------------------
# AC-011.1 — Construcción reproducible (estáticas, sin Docker)
# ---------------------------------------------------------------------------


def test_dockerfile_sincroniza_con_uv_lock() -> None:
    """AC-011.1: dependencias desde `uv.lock` con uv; `pip` prohibido."""
    dockerfile = _read(DOCKERFILE)
    assert "uv sync --frozen" in dockerfile
    assert "uv.lock" in dockerfile
    assert "pip install" not in dockerfile


def test_dockerfile_instala_librerias_del_sistema() -> None:
    """AC-011.1: librerías nativas de OpenCV y torch CPU (Debian trixie)."""
    dockerfile = _read(DOCKERFILE)
    for library in ("libgl1", "libglib2.0-0t64", "libgomp1", "libquadmath0", "libxcb1"):
        assert library in dockerfile


def test_entrypoint_con_finales_de_linea_unix() -> None:
    """AC-011.1: CRLF en el entrypoint rompe la imagen con un error críptico."""
    raw = ENTRYPOINT.read_bytes()
    assert raw.startswith(b"#!"), "el entrypoint debe tener shebang"
    assert b"\r\n" not in raw, "el entrypoint debe usar finales de línea Unix"


# ---------------------------------------------------------------------------
# AC-011.3 — Separación de artefactos (estáticas, sin Docker)
# ---------------------------------------------------------------------------


def test_dockerfile_no_incorpora_pesos() -> None:
    """AC-011.3: ninguna instrucción COPY referencia pesos ni datos."""
    dockerfile = _read(DOCKERFILE)
    copy_lines = [
        line for line in dockerfile.splitlines() if line.lstrip().upper().startswith("COPY")
    ]
    assert copy_lines, "el Dockerfile debe copiar el código del proyecto"
    for line in copy_lines:
        assert not WEIGHT_PATTERN.search(line), f"COPY con artefacto pesado: {line!r}"
        for forbidden in ("artifacts", "weights", "datasets", "data/"):
            assert forbidden not in line, f"COPY referencia {forbidden}: {line!r}"


def test_dockerignore_bloquea_pesos_datos_y_secretos() -> None:
    """AC-011.3: el contexto de construcción no puede incluir artefactos."""
    patterns = {
        line.strip()
        for line in _read(DOCKERIGNORE).splitlines()
        if line.strip() and not line.startswith("#")
    }
    for pattern in (
        "*.pt",
        "*.pth",
        "*.onnx",
        "*.zip",
        "artifacts/",
        "weights/",
        "datasets/",
        "data/",
        ".env",
        ".git",
    ):
        assert pattern in patterns, f"falta {pattern!r} en {DOCKERIGNORE}"


def test_gitignore_cubre_pesos_y_entorno() -> None:
    """AC-011.3: regresión — `.gitignore` sigue bloqueando pesos y secretos."""
    patterns = {
        line.strip() for line in Path(".gitignore").read_text(encoding="utf-8").splitlines()
    }
    for pattern in (
        "*.pt",
        "*.pth",
        "*.onnx",
        "artifacts/",
        "weights/",
        "datasets/",
        "data/",
        ".env",
    ):
        assert pattern in patterns, f"falta {pattern!r} en .gitignore"


def test_compose_monta_el_modelo_solo_lectura() -> None:
    """AC-011.3: compose provee el artefacto por montaje read-only externo a Git."""
    compose = _read(COMPOSE_FILE)
    assert ":/models:ro" in compose, "los servicios deben montar /models read-only"
    assert "PPE_MODEL_PATH: /models/best.pt" in compose


# ---------------------------------------------------------------------------
# AC-011.4 — Documentación (estática, sin Docker)
# ---------------------------------------------------------------------------


def test_runbook_documenta_construccion_configuracion_inferencia() -> None:
    """AC-011.4: el runbook explica build, configuración, arranque e inferencia."""
    doc = _read(RUNBOOK).lower()
    for needle in (
        "docker build",
        "docker run",
        "docker compose",
        "ppe_model_path",
        "/predict",
        "grpc.client",
        ":ro",
    ):
        assert needle in doc, f"falta {needle!r} en {RUNBOOK}"


# ---------------------------------------------------------------------------
# AC-011.2 — Inferencia en CPU con el servicio dentro del contenedor
# ---------------------------------------------------------------------------


def _imagen_existe(image: str) -> bool:
    """Comprueba si la imagen ya está construida en el daemon local."""
    return _docker("image", "inspect", image).returncode == 0


def _artefacto_local() -> Path | None:
    """Artefacto de la prueba: PPE_DOCKER_MODEL o candidatos bajo artifacts/."""
    explicit = os.getenv("PPE_DOCKER_MODEL")
    if explicit:
        path = Path(explicit)
        return path if path.is_file() else None
    return next((candidate for candidate in MODEL_CANDIDATES if candidate.is_file()), None)


def _puerto_libre() -> int:
    """Reserva un puerto efímero en 127.0.0.1 y lo devuelve al cerrar el socket."""
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def _imagen_de_prueba() -> bytes:
    """JPEG sintético determinista (640x480); no requiere dataset ni red."""
    generator = np.random.default_rng(11)
    array = generator.integers(0, 256, (480, 640, 3), dtype=np.uint8)
    ok, buffer = cv2.imencode(".jpg", array)
    assert ok
    return buffer.tobytes()


def _post_predict(url: str, image: bytes, total_timeout: float = 300.0) -> dict[str, Any]:
    """`POST /predict` reintentando mientras el contenedor arranca y torch carga."""
    boundary = "----ppe-hu011"
    body = (
        (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="file"; filename="prueba.jpg"\r\n'
            "Content-Type: image/jpeg\r\n\r\n"
        ).encode()
        + image
        + f"\r\n--{boundary}--\r\n".encode()
    )
    request_headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    deadline = time.monotonic() + total_timeout
    last_error = ""
    while time.monotonic() < deadline:
        request = urllib.request.Request(url, data=body, headers=request_headers)
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            raise AssertionError(f"/predict respondió HTTP {exc.code}: {detail}") from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = str(exc)
        time.sleep(2)
    raise AssertionError(f"/predict no respondió a tiempo: {last_error}")


def _validar_deteccion(detection: dict[str, Any]) -> None:
    """Comprueba los campos del contrato de detección (ADR 0005 + HU-006)."""
    assert set(detection) == {
        "class_id",
        "class_name",
        "confidence",
        "bbox",
        "image_width",
        "image_height",
    }
    assert detection["class_name"] in CANONICAL_CLASSES
    assert 0.0 <= detection["confidence"] <= 1.0
    bbox = detection["bbox"]
    assert len(bbox) == 4
    assert bbox[0] <= bbox[2] and bbox[1] <= bbox[3]


@pytest.mark.docker
@pytest.mark.skipif(shutil.which("docker") is None, reason="Docker no disponible")
@pytest.mark.skipif(
    os.getenv("PPE_DOCKER_SMOKE") != "1",
    reason="prueba de humo: activar con PPE_DOCKER_SMOKE=1",
)
def test_contenedor_sirve_inferencia_rest_y_grpc() -> None:
    """AC-011.2: inferencia CPU con REST y gRPC ejecutándose en el contenedor."""
    artefacto = _artefacto_local()
    if artefacto is None:
        pytest.skip("sin artefacto local (PPE_DOCKER_MODEL)")
    if not _imagen_existe(DOCKER_IMAGE):
        pytest.skip("construye la imagen primero: make docker-build")

    name = f"ppe-hu011-{uuid.uuid4().hex[:8]}"
    api_port, grpc_port = _puerto_libre(), _puerto_libre()
    started = _docker(
        "run",
        "-d",
        "--name",
        name,
        "--rm",
        "-p",
        f"{api_port}:8000",
        "-p",
        f"{grpc_port}:9000",
        "-v",
        f"{artefacto.resolve().parent}:/models:ro",
        "-e",
        "PPE_MODEL_PATH=/models/best.pt",
        "-e",
        "PPE_SERVICES=rest,grpc",
        DOCKER_IMAGE,
    )
    if started.returncode != 0:
        pytest.fail(f"docker run falló: {started.stderr.strip()}")
    try:
        # REST (HU-006): la primera petición carga torch dentro del contenedor.
        payload = _post_predict(f"http://127.0.0.1:{api_port}/predict", _imagen_de_prueba())
        assert set(payload) == {
            "detections",
            "image_width",
            "image_height",
            "model_version",
            "elapsed_ms",
        }
        assert payload["model_version"] == "best", "debe derivarse del artefacto montado"
        assert payload["image_width"] > 0 and payload["image_height"] > 0
        assert payload["elapsed_ms"] >= 0
        for detection in payload["detections"]:
            _validar_deteccion(detection)

        # gRPC (HU-010): el mismo contrato desde el cliente del paquete.
        response = grpc_detect(f"127.0.0.1:{grpc_port}", _imagen_de_prueba(), source="prueba.jpg")
        assert response.model_version == "best"
        assert response.image_width > 0 and response.image_height > 0
        assert response.elapsed_ms >= 0
        for detection in response.detections:
            assert detection.class_name in CANONICAL_CLASSES
            assert 0.0 <= detection.confidence <= 1.0
            assert detection.bbox.x1 <= detection.bbox.x2
            assert detection.bbox.y1 <= detection.bbox.y2
        if not response.detections:
            assert response.message == NO_DETECTIONS_MESSAGE
        else:
            assert response.message.startswith("Se detect")
    finally:
        subprocess.run(["docker", "rm", "-f", name], capture_output=True, timeout=60)
