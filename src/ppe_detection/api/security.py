"""Clave de API opcional para `/predict` (HU-051).

El módulo es puro: resuelve claves desde el entorno y las compara sin registrarlas.
La traducción a respuesta HTTP vive en la capa de la API.
"""

from __future__ import annotations

import hashlib
import hmac
import os
from collections.abc import Mapping, Sequence

API_KEY_HEADER = "X-API-Key"
ENV_API_KEYS = "PPE_API_KEYS"
ENV_API_KEY = "PPE_API_KEY"


def configured_keys(env: Mapping[str, str] | None = None) -> tuple[str, ...]:
    """Devuelve las claves no vacías; una lista vacía desactiva la autenticación."""
    environ = dict(os.environ if env is None else env)
    raw = environ.get(ENV_API_KEYS) or environ.get(ENV_API_KEY) or ""
    return tuple(key.strip() for key in raw.split(",") if key.strip())


def is_authorized(supplied: str | None, keys: Sequence[str]) -> bool:
    """Compara en tiempo constante la clave recibida contra todas las configuradas.

    Se comparan digests SHA-256 de longitud fija con `hmac.compare_digest` y se
    acumula el resultado con `|=`: no hay `any()` ni `break` que cortocircuite y
    revele qué clave coincidió. Sin claves configuradas la guarda es transparente.
    """
    if not keys:
        return True
    if not supplied:
        return False
    candidate = hashlib.sha256(supplied.encode("utf-8")).digest()
    authorised = False
    for key in keys:
        expected = hashlib.sha256(key.encode("utf-8")).digest()
        authorised |= hmac.compare_digest(candidate, expected)
    return authorised
