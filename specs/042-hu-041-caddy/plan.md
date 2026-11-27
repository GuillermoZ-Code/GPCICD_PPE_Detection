# Implementation Plan: HU-041 — Proxy inverso Caddy con HTTPS automático

**Branch**: `feature/042-hu-041-caddy` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/042-hu-041-caddy/spec.md`

## Summary

La rúbrica pide el sistema desplegado; sin TLS y sin dominio no hay URL pública que mostrar, y AGPL exige que el servicio publicado enlace su fuente.

## Technical Context

**Language/Version**: Docker Compose, shell POSIX, YAML de GitLab CI/CD

**Primary Dependencies**: imágenes del registry del proyecto, Caddy 2, OpenSSH

**Testing**: pytest estático sobre los archivos de despliegue (sin servidor)

**Target Platform**: Droplet con Docker CPU

**Project Type**: infraestructura de despliegue

**Constraints**: sin secretos en el repositorio; sin puertos innecesarios abiertos

**Scale/Scope**: 4 servicios, 1 servidor

## Constitution Check

- **Sin secretos versionados**: llaves y tokens solo en variables de CI/CD. ✅
- **Pesos fuera de Git y fuera de la imagen**: montaje `:ro`. ✅
- **Test-first**: pruebas estáticas antes de los archivos. ✅
- **AGPL**: la interfaz publicada enlaza el código fuente. ✅
- **Una HU por PR**: el bloque de despliegue se revisa junto y se cierra por issue. ✅

## Project Structure

```text
docker/Caddyfile        # nuevo: TLS automático y rutas
tests/test_caddy.py
specs/042-hu-041-caddy/
```

## Design decisions

1. **Caddy en vez de nginx con certbot.** Un binario, certificado y renovación automáticos; menos piezas que operar en una semana.
2. **`/api` con `strip_prefix`.** La SPA llama a `/api/predict` y la API expone `/predict`; el prefijo se quita en el borde.
3. **`PPE_DOMAIN` como variable.** El mismo archivo sirve para el Droplet y para una prueba local con `localhost`.

## Risks

| Riesgo | Mitigación |
|---|---|
| El dominio no apunta al Droplet | Caddy no emite certificado; se documenta el registro DNS |
| Puerto 80/443 cerrado | UFW los abre en el aprovisionamiento (HU-069) |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_caddy.py` (rutas `/` y `/api/*` a sus servicios) |
| AC-02 | `tests/test_caddy.py` (redirección y cabeceras de seguridad) |
| AC-03 | `tests/test_caddy.py` (archivo versionado y dominio por variable) |
