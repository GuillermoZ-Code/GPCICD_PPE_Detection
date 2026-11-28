# Implementation Plan: HU-071 — `compose.prod.yml` con healthchecks y perfiles

**Branch**: `feature/072-hu-071-compose-prod` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/072-hu-071-compose-prod/spec.md`

## Summary

El compose local construye la imagen; en producción se baja la imagen publicada y se reinicia sola. Sin esa separación el servidor no puede desplegar lo que construyó el pipeline.

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
compose.prod.yml        # nuevo: api, grpc, web y caddy
tests/test_compose_prod.py
specs/072-hu-071-compose-prod/
```

## Design decisions

1. **Sin `build:`.** Producción baja la imagen publicada; construir en el servidor duplicaría el trabajo del pipeline.
2. **Sin puertos publicados para api/grpc.** Caddy y nginx están en la misma red; publicar 8000/9000 abriría superficie sin necesidad.
3. **Variables obligatorias con `:?`.** Un compose que arranca con la imagen equivocada es peor que uno que falla al inicio.

## Risks

| Riesgo | Mitigación |
|---|---|
| Falta `.env` en el servidor | `env_file` obligatorio y plantilla en `.env.example` |
| El modelo no está montado | La API responde 503 y el healthcheck lo detecta |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_compose_prod.py` (servicios e imágenes por variable) |
| AC-02 | `tests/test_compose_prod.py` (`restart` y healthchecks) |
| AC-03 | `tests/test_compose_prod.py` (montaje `:ro` y `env_file`) |
