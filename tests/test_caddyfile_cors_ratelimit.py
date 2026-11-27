"""Pruebas estructurales de CORS y rate limit del proxy (HU-054)."""

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CADDYFILE = REPO / "docker" / "Caddyfile"
COMPOSE = REPO / "compose.prod.yml"
DOCKERFILE_CADDY = REPO / "docker" / "Dockerfile.caddy"


def test_ac_01_cors_solo_permite_dominio_publico() -> None:
    """AC-01: CORS solo permite el dominio público."""
    caddy = CADDYFILE.read_text(encoding="utf-8")
    compose = COMPOSE.read_text(encoding="utf-8")

    assert "PPE_CORS_ORIGIN" in caddy
    assert "Access-Control-Allow-Origin {env.PPE_CORS_ORIGIN}" in caddy
    assert "PPE_CORS_ORIGIN" in compose
    # No debe permitir origen comodín.
    assert 'Access-Control-Allow-Origin "*"' not in caddy


def test_ac_02_rate_limit_configurado_y_documentado() -> None:
    """AC-02: Rate limit configurado y documentado."""
    caddy = CADDYFILE.read_text(encoding="utf-8")
    compose = COMPOSE.read_text(encoding="utf-8")
    dockerfile = DOCKERFILE_CADDY.read_text(encoding="utf-8")

    assert "rate_limit" in caddy
    # `caddy-ratelimit` parsea estos valores al adaptar el Caddyfile: deben usar
    # sustitución de entorno de Caddy ({$VAR:default}), no placeholders {env.VAR}.
    assert "events {$PPE_RATE_LIMIT_EVENTS:60}" in caddy
    assert "window {$PPE_RATE_LIMIT_WINDOW:1m}" in caddy
    assert "PPE_RATE_LIMIT_EVENTS" in compose
    assert "PPE_RATE_LIMIT_WINDOW" in compose
    assert "caddy-ratelimit" in dockerfile
    # Documentado en config/comentarios.
    assert "HU-054" in caddy


def test_ac_03_prueba_de_configuracion_archivos_entregables() -> None:
    """AC-03: Prueba de configuración."""
    assert CADDYFILE.exists()
    assert COMPOSE.exists()
    assert DOCKERFILE_CADDY.exists()

    compose = COMPOSE.read_text(encoding="utf-8")
    assert "docker/Dockerfile.caddy" in compose
    assert "${PPE_CADDY_IMAGE:?" in compose
    assert "./Caddyfile:/etc/caddy/Caddyfile:ro" in compose
