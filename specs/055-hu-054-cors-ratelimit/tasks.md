# Tasks — HU-054

- [x] Spec/plan/tasks creados.
- [x] `Dockerfile.caddy` con módulo `rate_limit`.
- [x] `Caddyfile` con CORS y `rate_limit`.
- [x] `compose.prod.yml` con variables `PPE_CORS_ORIGIN` / `PPE_RATE_LIMIT_*`.
- [x] Prueba estructural de configuración.
- [x] Validación local real de Caddy: construcción, `caddy validate` y
      comportamiento HTTP.
- [ ] Publicar la imagen `PPE_CADDY_IMAGE` construida con
      `docker/Dockerfile.caddy`.
- [ ] Configurar `deploy/deploy.sh`, `deploy/remote.sh` y CI para consumir esa
      imagen publicada (responsabilidad de Guillermo; requiere coordinación).
- [ ] Validar CI remoto y despliegue real.

## Evidencia local (2026-11-27)

- Docker Desktop `29.8.2`, Docker Compose `v5.6.0`.
- `docker build -q -f docker/Dockerfile.caddy -t ppe-caddy:hu054-local .`
  → `sha256:3cf1739bcb25...`, 161 MB.
- `caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile`
  → `Valid configuration`.
  - Corrección aplicada: `events`/`window` usan `{$PPE_RATE_LIMIT_EVENTS:60}` y
    `{$PPE_RATE_LIMIT_WINDOW:1m}`; con `{env.VAR}` el adaptador fallaba con
    `invalid max events integer`.
- Contenedor local con `PPE_DOMAIN=localhost` y
  `PPE_CORS_ORIGIN=https://localhost`:
  - `OPTIONS /api/predict` con `Origin: https://localhost` → `204` con
    `Access-Control-Allow-Origin: https://localhost`, métodos, headers,
    credenciales y `Vary: Origin`.
  - `OPTIONS /api/predict` con `Origin: https://evil.example` → `204` sin
    cabecera `Access-Control-Allow-Origin`.
- Con `PPE_RATE_LIMIT_EVENTS=2` y `PPE_RATE_LIMIT_WINDOW=1m`, tres preflights
  consecutivos → `204,204,429`; el log registra
  `http.handlers.rate_limit zone=api_limit`.
- `uv run pytest -q tests/test_caddy.py tests/test_compose_prod.py tests/test_caddyfile_cors_ratelimit.py`
  → 21 passed.
- `uv run ruff check tests/test_caddyfile_cors_ratelimit.py` y
  `uv run ruff format --check tests/test_caddyfile_cors_ratelimit.py` → limpio.
- `uv run python -m ppe_detection.tools.ownership --base origin/develop` → ok.
- Verificación completa equivalente a `make check` (Ruff, `ruff format --check`,
  `ty check`, `pytest -q`) → exit `0` (2 tests omitidos, sin fallos).
- `uv build` → sdist y wheel construidos correctamente.

## Estado

- La evidencia es **solo local**. No hay evidencia de CI remoto ni de
  despliegue real.
- No se modificaron `deploy/*` ni workflows: pertenecen a Guillermo y cualquier
  cambio requiere coordinación previa.
- La HU permanece abierta; tras abrir la PR en borrador se mueve a
  *In review*, nunca a *Done*.
