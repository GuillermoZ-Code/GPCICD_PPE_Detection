"""HU-041 — Caddy con HTTPS automático (AC-01, AC-02 y AC-03).

Pruebas estáticas: leen el `Caddyfile` sin levantar Caddy ni pedir certificados.
"""

from __future__ import annotations

from pathlib import Path

CADDYFILE = Path("docker/Caddyfile")


def _read(path: Path) -> str:
    """Lee un archivo esperado; la ausencia hace fallar la prueba con contexto."""
    assert path.is_file(), f"no existe {path}"
    return path.read_text(encoding="utf-8")


def test_api_requests_are_routed_to_fastapi_without_the_prefix() -> None:
    """AC-01: `/api/predict` llega a FastAPI como `/predict`."""
    # Arrange
    caddyfile = _read(CADDYFILE)

    # Assert
    assert "handle_path /api/*" in caddyfile
    assert "reverse_proxy api:8000" in caddyfile


def test_everything_else_goes_to_the_spa() -> None:
    """AC-01: la raíz y las rutas del cliente caen en nginx."""
    # Arrange
    caddyfile = _read(CADDYFILE)

    # Assert
    assert "reverse_proxy web:80" in caddyfile
    assert "handle {" in caddyfile


def test_health_is_reachable_through_the_proxy() -> None:
    """AC-01: el smoke del despliegue consulta `/health` por el dominio."""
    # Arrange
    caddyfile = _read(CADDYFILE)

    # Assert
    assert "handle /health*" in caddyfile


def test_https_redirect_is_automatic() -> None:
    """AC-02: el sitio se declara por dominio, así Caddy redirige 80 → 443."""
    # Arrange
    caddyfile = _read(CADDYFILE)

    # Assert
    assert "{$PPE_DOMAIN:localhost}" in caddyfile
    assert "http://" not in caddyfile


def test_security_headers_are_present() -> None:
    """AC-02: HSTS, tipo de contenido y política de referencia."""
    # Arrange
    caddyfile = _read(CADDYFILE)

    # Assert
    assert "Strict-Transport-Security" in caddyfile
    assert "X-Content-Type-Options" in caddyfile
    assert "X-Frame-Options" in caddyfile
    assert "Referrer-Policy" in caddyfile


def test_domain_is_not_hardcoded() -> None:
    """AC-03: el mismo archivo sirve para el Droplet y para local."""
    # Arrange
    caddyfile = _read(CADDYFILE)

    # Assert
    assert "PPE_DOMAIN" in caddyfile
    assert "gpcicd" not in caddyfile.lower()


def test_compression_is_enabled() -> None:
    """AC-01: la SPA y el JSON viajan comprimidos."""
    # Arrange
    caddyfile = _read(CADDYFILE)

    # Assert
    assert "encode zstd gzip" in caddyfile


def test_caddyfile_is_versioned_next_to_the_compose() -> None:
    """AC-03: el archivo vive en `docker/` y lo monta el compose de producción."""
    # Arrange
    compose = Path("compose.prod.yml").read_text(encoding="utf-8")

    # Assert
    assert CADDYFILE.is_file()
    assert "./Caddyfile:/etc/caddy/Caddyfile:ro" in compose
