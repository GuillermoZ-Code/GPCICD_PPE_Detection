# Implementation Plan: HU-067 — Job `build_image` con Docker-in-Docker

**Branch**: `feature/067-hu-066-gitlab-ci` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/068-hu-067-build-image/spec.md`

## Summary

Construir en GitLab las dos imágenes del sistema (`runtime` y `web`) con DinD, cache de
capas contra `:latest` y un smoke de importación antes de publicar. El modelo no viaja
en la imagen: se monta `:ro` en el servidor (ADR 0008).

## Technical Context

**Language/Version**: Docker 29 (cliente y daemon), Dockerfile multi-stage existente

**Primary Dependencies**: `docker:29.10.0-cli`, `docker:29.10.0-dind`,
`ghcr.io/astral-sh/uv` (dentro del Dockerfile)

**Testing**: pytest estático sobre `.gitlab-ci.yml` y el `Dockerfile`

**Target Platform**: gitlab.com con DinD

**Project Type**: infraestructura CI/CD

**Constraints**: sin pesos en la imagen; sin `:latest` desde ramas de trabajo

**Scale/Scope**: 2 imágenes, 2 tags por build

## Constitution Check

- **Sin pesos en Git ni en la imagen**: el Dockerfile solo copia `src/` y `.venv`. ✅
- **`uv` con `--frozen`**: la imagen resuelve desde `uv.lock`. ✅
- **Test-first**: pruebas estáticas antes del job. ✅
- **Una HU por PR**: el pipeline y su build; el deploy va aparte. ✅

## Project Structure

```text
.gitlab-ci.yml                        # job `build_image`
tests/test_gitlab_ci.py               # pruebas de AC-01 a AC-03
specs/068-hu-067-build-image/
├── spec.md
├── plan.md
└── tasks.md
```

## Design decisions

1. **Dos targets, dos imágenes.** `runtime` sirve API y gRPC y `web` sirve la SPA; el
   compose de producción las referencia por tag.
2. **Cache contra `:latest`.** En el primer build no existe y el `pull` se ignora; a
   partir del segundo, las capas de dependencias se reutilizan.
3. **Smoke antes de publicar.** Un import roto no debe llegar al Droplet: si
   `create_app()` falla, no se empuja.
4. **El modelo, fuera.** El peso se monta en el servidor desde `models.lock`; la imagen
   queda genérica y se puede reutilizar.
5. **`:latest` solo desde `main`.** Una rama de trabajo no debe pisar la imagen que se
   despliega.

## Risks

| Riesgo | Mitigación |
|---|---|
| DinD deshabilitado en el runner | El job declara el servicio; si falta, falla con mensaje claro |
| Build de torch lento | Cache de capas + `timeout` de 45 minutos |
| Imagen enorme | Multi-stage: `runtime` no lleva uv ni node |
| Tag mutable | Además de `latest`, se publica el SHA corto |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_gitlab_ci.py` (DinD, targets `runtime` y `web`, `--cache-from`) |
| AC-02 | `tests/test_gitlab_ci.py` (`$CI_COMMIT_SHORT_SHA` y `latest`) |
| AC-03 | `tests/test_gitlab_ci.py` (el Dockerfile no copia pesos; el deploy los monta) |
