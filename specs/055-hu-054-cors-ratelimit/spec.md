# HU-054 — CORS de producción y rate limit en el proxy

## Contexto

Como operador, quiero limitar orígenes y peticiones por IP, para reducir el abuso
del servicio público.

## Criterios de aceptación

- **AC-01:** CORS solo permite el dominio público.
- **AC-02:** Rate limit configurado y documentado.
- **AC-03:** Prueba de configuración.

## Entregables

- `docker/Caddyfile`
- `compose.prod.yml`
- `docker/Dockerfile.caddy` (build de Caddy con módulo `rate_limit`)
- `tests/test_caddyfile_cors_ratelimit.py`

## Notas

- El rate limit usa `github.com/mholt/caddy-ratelimit` compilado con `xcaddy`
  porque la imagen estándar de Caddy no incluye el módulo.
- Variables: `PPE_CORS_ORIGIN`, `PPE_RATE_LIMIT_EVENTS`, `PPE_RATE_LIMIT_WINDOW`.
- `events` y `window` usan `{$VAR:default}` (sustitución al adaptar el Caddyfile):
  `caddy-ratelimit` parsea esos valores como entero/duración y no acepta los
  placeholders dinámicos `{env.VAR}`.
- La HU no se declara completa hasta publicar `PPE_CADDY_IMAGE`, ajustar
  deploy/CI y verificar el despliegue remoto.
