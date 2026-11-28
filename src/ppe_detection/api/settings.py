"""Configuración por entorno validada al arrancar la API (HU-044)."""

from __future__ import annotations

import os
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from urllib.parse import urlparse

SHA256_PATTERN = re.compile(r"^[0-9A-Fa-f]{64}$")
TARGET_PATTERN = re.compile(r"^[^:\s]+:(\d{1,5})$")
SECRET_VARS = frozenset({"PPE_API_KEY"})
DEFAULT_SOURCE_URL = "https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection"
KNOWN_VARS = frozenset(
    {
        "PPE_API_HOST",
        "PPE_API_PORT",
        "PPE_API_KEY",
        "PPE_CONF",
        "PPE_CORS_ORIGINS",
        "PPE_DEVICE",
        "PPE_GRPC_HOST",
        "PPE_GRPC_PORT",
        "PPE_GRPC_TARGET",
        "PPE_IMGSZ",
        "PPE_IOU",
        "PPE_MODEL_FORMAT",
        "PPE_MODEL_MANIFEST",
        "PPE_MODEL_PATH",
        "PPE_MODEL_SHA256",
        "PPE_MODEL_VERSION",
        "PPE_SOURCE_URL",
        "PPE_DEPLOY_COMMIT",
    }
)

__all__ = [
    "DEFAULT_SOURCE_URL",
    "Settings",
    "SettingsError",
    "load_settings",
    "validate_environment",
]


@dataclass(frozen=True, slots=True)
class Settings:
    """Valores tipados y validados que usa el servicio."""

    model_path: str | None
    model_manifest: str | None
    model_version: str | None
    model_sha256: str | None
    model_format: str
    conf: float
    iou: float
    imgsz: int
    device: str
    cors_origins: tuple[str, ...]
    api_host: str
    api_port: int
    grpc_host: str
    grpc_port: int
    grpc_target: str
    api_key: str | None


class SettingsError(ValueError):
    """Configuración inválida; el mensaje ya nombra las variables afectadas."""


def _describe(name: str, raw: str) -> str:
    """Muestra el valor salvo que sea secreto."""
    return "<redactado>" if name in SECRET_VARS else repr(raw)


def _non_empty(
    env: Mapping[str, str], name: str, default: str | None, errors: list[str]
) -> str | None:
    raw = env.get(name)
    if raw is None:
        return default
    value = raw.strip()
    if not value:
        errors.append(f"{name} no puede estar vacía.")
        return default
    return value


def _number(
    env: Mapping[str, str],
    name: str,
    default: float,
    minimum: float,
    maximum: float,
    errors: list[str],
) -> float:
    raw = env.get(name)
    if raw is None:
        return default
    try:
        value = float(raw)
    except ValueError:
        errors.append(
            f"{name} debe ser un número entre {minimum} y {maximum}; "
            f"recibió {_describe(name, raw)}."
        )
        return default
    if not minimum <= value <= maximum:
        errors.append(
            f"{name} debe estar entre {minimum} y {maximum}; recibió {_describe(name, raw)}."
        )
    return value


def _integer(
    env: Mapping[str, str], name: str, default: int, minimum: int, maximum: int, errors: list[str]
) -> int:
    raw = env.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        errors.append(
            f"{name} debe ser un entero entre {minimum} y {maximum}; "
            f"recibió {_describe(name, raw)}."
        )
        return default
    if not minimum <= value <= maximum:
        errors.append(
            f"{name} debe estar entre {minimum} y {maximum}; recibió {_describe(name, raw)}."
        )
    return value


def _sha256(env: Mapping[str, str], errors: list[str]) -> str | None:
    raw = env.get("PPE_MODEL_SHA256")
    if raw is None:
        return None
    value = raw.strip()
    if not SHA256_PATTERN.fullmatch(value):
        errors.append(
            "PPE_MODEL_SHA256 debe tener 64 caracteres hexadecimales; "
            f"recibió {_describe('PPE_MODEL_SHA256', raw)}."
        )
    return value or None


def _format(env: Mapping[str, str], errors: list[str]) -> str:
    raw = env.get("PPE_MODEL_FORMAT", "pt").strip().lower()
    if raw not in {"pt", "onnx"}:
        errors.append(
            "PPE_MODEL_FORMAT debe ser 'pt' u 'onnx'; "
            f"recibió {_describe('PPE_MODEL_FORMAT', raw)}."
        )
        return "pt"
    return raw


def _origins(env: Mapping[str, str], errors: list[str]) -> tuple[str, ...]:
    raw = env.get("PPE_CORS_ORIGINS", "http://localhost:5173")
    origins = tuple(origin.strip() for origin in raw.split(","))
    if not origins or any(not origin for origin in origins):
        errors.append("PPE_CORS_ORIGINS no puede contener orígenes vacíos.")
    for origin in origins:
        parsed = urlparse(origin)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(
                "PPE_CORS_ORIGINS debe usar orígenes http/https con host; "
                f"recibió {_describe('PPE_CORS_ORIGINS', raw)}."
            )
            break
    return origins or ("http://localhost:5173",)


def _target(env: Mapping[str, str], errors: list[str]) -> str:
    raw = env.get("PPE_GRPC_TARGET", "127.0.0.1:9000")
    match = TARGET_PATTERN.fullmatch(raw.strip())
    if match is None or not 1 <= int(match.group(1)) <= 65535:
        errors.append(
            "PPE_GRPC_TARGET debe tener forma host:puerto con puerto entre 1 y 65535; "
            f"recibió {_describe('PPE_GRPC_TARGET', raw)}."
        )
        return "127.0.0.1:9000"
    return raw.strip()


def _parse(env: Mapping[str, str]) -> tuple[Settings, list[str]]:
    errors: list[str] = []
    settings = Settings(
        model_path=_non_empty(env, "PPE_MODEL_PATH", None, errors),
        model_manifest=_non_empty(env, "PPE_MODEL_MANIFEST", None, errors),
        model_version=_non_empty(env, "PPE_MODEL_VERSION", None, errors),
        model_sha256=_sha256(env, errors),
        model_format=_format(env, errors),
        conf=_number(env, "PPE_CONF", 0.25, 0.0, 1.0, errors),
        iou=_number(env, "PPE_IOU", 0.7, 0.0, 1.0, errors),
        imgsz=_integer(env, "PPE_IMGSZ", 640, 1, 4096, errors),
        device=_non_empty(env, "PPE_DEVICE", "cpu", errors) or "cpu",
        cors_origins=_origins(env, errors),
        api_host=_non_empty(env, "PPE_API_HOST", "0.0.0.0", errors) or "0.0.0.0",
        api_port=_integer(env, "PPE_API_PORT", 8000, 1, 65535, errors),
        grpc_host=_non_empty(env, "PPE_GRPC_HOST", "0.0.0.0", errors) or "0.0.0.0",
        grpc_port=_integer(env, "PPE_GRPC_PORT", 9000, 1, 65535, errors),
        grpc_target=_target(env, errors),
        api_key=_non_empty(env, "PPE_API_KEY", None, errors),
    )
    return settings, errors


def validate_environment(env: Mapping[str, str] | None = None) -> list[str]:
    """Devuelve mensajes accionables para cada variable inválida."""
    return _parse(dict(os.environ if env is None else env))[1]


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    """Devuelve la configuración validada o lanza `SettingsError`."""
    settings, errors = _parse(dict(os.environ if env is None else env))
    if errors:
        raise SettingsError("; ".join(errors))
    return settings


def main(argv: Sequence[str] | None = None) -> int:
    """Valida el entorno actual; 0 si es correcto, 1 si no."""
    if argv:
        print("Uso: python -m ppe_detection.api.settings", file=sys.stderr)
        return 2
    try:
        load_settings()
    except SettingsError as exc:
        print(f"Configuración inválida: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
