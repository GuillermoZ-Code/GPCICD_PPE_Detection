"""Levanta la API y el frontend con un solo comando (ejecución local).

Uso:
    uv run python -m ppe_detection.tools.launcher
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.request
from collections.abc import Sequence
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
FRONTEND_DIR = REPO_ROOT / "frontend"
VITE_BIN = FRONTEND_DIR / "node_modules" / "vite" / "bin" / "vite.js"

MODEL_CANDIDATES = (
    Path("artifacts/drive/yolo11s_clean/weights/best.pt"),
    Path("artifacts/models/yolo11s_clean/weights/best.pt"),
    Path("artifacts/models/yolov8n_clean/weights/best.pt"),
)
DOWNLOAD_HINT = (
    "uv run --with gdown gdown --folder "
    '"https://drive.google.com/drive/folders/1sUvUScA2vjGgrBwcYbfrpa9z5_5mBXap" '
    "-O artifacts/drive"
)
IS_WINDOWS = os.name == "nt"


def resolve_model(explicit: str | None = None, env: dict[str, str] | None = None) -> Path:
    """Devuelve la ruta del modelo: argumento, variable de entorno o candidatos."""
    environ = os.environ if env is None else env
    candidate = explicit or environ.get("PPE_MODEL_PATH")
    if candidate:
        path = Path(candidate)
        return path if path.is_absolute() else REPO_ROOT / path
    for relative in MODEL_CANDIDATES:
        path = REPO_ROOT / relative
        if path.is_file():
            return path
    return REPO_ROOT / MODEL_CANDIDATES[0]


def model_version(path: Path) -> str:
    """Deriva la versión del modelo a partir de ``.../<version>/weights/best.pt``."""
    parent = path.parent
    return parent.parent.name if parent.name == "weights" else parent.name or "unknown"


def api_env(model: Path, host: str, api_port: int, web_port: int) -> dict[str, str]:
    """Entorno de la API con modelo, puertos y CORS para la SPA."""
    env = os.environ.copy()
    env.update(
        {
            "PPE_MODEL_PATH": str(model),
            "PPE_MODEL_VERSION": model_version(model),
            "PPE_API_HOST": host,
            "PPE_API_PORT": str(api_port),
            "PPE_CORS_ORIGINS": (f"http://localhost:{web_port},http://127.0.0.1:{web_port}"),
        }
    )
    return env


def web_env(api_url: str) -> dict[str, str]:
    """Entorno del frontend apuntando a la API."""
    env = os.environ.copy()
    env["VITE_API_URL"] = api_url
    return env


def npm_command(*args: str) -> list[str]:
    """Construye un comando npm válido en Windows y en Unix."""
    if IS_WINDOWS:
        return ["cmd", "/c", "npm", *args]
    return ["npm", *args]


def spawn(command: Sequence[str], env: dict[str, str], cwd: Path) -> subprocess.Popen[str]:
    """Arranca un proceso con su salida redirigida al terminal."""
    flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) if IS_WINDOWS else 0
    return subprocess.Popen(
        list(command),
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        creationflags=flags,
    )


def pump(process: subprocess.Popen[str], name: str) -> None:
    """Imprime la salida del proceso con un prefijo."""
    stream = process.stdout
    if stream is None:
        return
    for line in stream:
        print(f"[{name}] {line.rstrip()}", flush=True)


def wait_for(url: str, timeout: float, process: subprocess.Popen[str]) -> bool:
    """Espera a que una URL responda; falla si el proceso muere."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            return False
        try:
            with urllib.request.urlopen(url, timeout=2):
                return True
        except (urllib.error.URLError, OSError):
            time.sleep(0.5)
    return False


def stop(process: subprocess.Popen[str]) -> None:
    """Detiene un proceso y su árbol de hijos."""
    if process.poll() is not None:
        return
    if IS_WINDOWS:
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            capture_output=True,
            check=False,
        )
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


def ensure_frontend() -> bool:
    """Instala las dependencias del frontend si faltan."""
    if VITE_BIN.is_file():
        return True
    print("Faltan las dependencias del frontend; ejecutando `npm ci`…", flush=True)
    if shutil.which("npm") is None and not IS_WINDOWS:
        print("No se encontró `npm` en el PATH.", flush=True)
        return False
    result = subprocess.run(
        npm_command("ci"),
        cwd=FRONTEND_DIR,
        check=False,
    )
    return result.returncode == 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parsea los argumentos del comando."""
    parser = argparse.ArgumentParser(
        prog="app",
        description="Levanta la API y el frontend para la ejecución local.",
    )
    parser.add_argument("--model", help="ruta del best.pt (por defecto, la del Drive)")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--api-port", type=int, default=8000)
    parser.add_argument("--web-port", type=int, default=5173)
    parser.add_argument("--timeout", type=float, default=60.0, help="segundos de espera")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Arranca la API y el frontend y espera hasta Ctrl+C."""
    args = parse_args(argv)
    model = resolve_model(args.model)
    if not model.is_file():
        print(f"No se encontró el modelo: {model}", flush=True)
        print("Descárgalo con:", flush=True)
        print(f"  {DOWNLOAD_HINT}", flush=True)
        return 1
    if not ensure_frontend():
        print("No se pudieron instalar las dependencias del frontend.", flush=True)
        return 1
    node = shutil.which("node")
    if node is None:
        print("No se encontró `node` en el PATH.", flush=True)
        return 1

    api_url = f"http://{args.host}:{args.api_port}"
    web_url = f"http://localhost:{args.web_port}"
    api_process = spawn(
        ["uv", "run", "--extra", "inference", "python", "-m", "ppe_detection.api"],
        api_env(model, args.host, args.api_port, args.web_port),
        REPO_ROOT,
    )
    web_process = spawn(
        [node, str(VITE_BIN), "--port", str(args.web_port), "--strictPort"],
        web_env(api_url),
        FRONTEND_DIR,
    )
    for process, name in ((api_process, "api"), (web_process, "web")):
        threading.Thread(target=pump, args=(process, name), daemon=True).start()

    api_ready = wait_for(f"{api_url}/openapi.json", args.timeout, api_process)
    web_ready = wait_for(f"{web_url}/", args.timeout, web_process)
    if not api_ready or not web_ready:
        print("No se pudo arrancar el sistema completo.", flush=True)
        stop(web_process)
        stop(api_process)
        return 1

    print("", flush=True)
    print(f"Modelo:  {model} ({model_version(model)})", flush=True)
    print(f"API:     {api_url}/docs", flush=True)
    print(f"Web:     {web_url}", flush=True)
    print("Ctrl+C para detener ambos.", flush=True)

    try:
        while True:
            time.sleep(1)
            if api_process.poll() is not None:
                print("La API terminó inesperadamente.", flush=True)
                break
            if web_process.poll() is not None:
                print("El frontend terminó inesperadamente.", flush=True)
                break
    except KeyboardInterrupt:
        print("\nDeteniendo…", flush=True)
    finally:
        stop(web_process)
        stop(api_process)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
