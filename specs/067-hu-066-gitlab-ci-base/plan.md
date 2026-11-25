# Implementation Plan: HU-066 — `.gitlab-ci.yml` base

**Branch**: `feature/067-hu-066-gitlab-ci-base` | **Date**: 2026-11-25 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/067-hu-066-gitlab-ci-base/spec.md`

## Summary

Versionar un `.gitlab-ci.yml` con cuatro etapas (calidad, frontend, build, deploy) que
replica las compuertas de GitHub, con caché de `uv` y `npm` y reglas que evitan pipelines
duplicados. El despliegue queda como marcador manual hasta HU-070.

## Technical Context

**Language/Version**: GitLab CI YAML

**Primary Dependencies**: `ghcr.io/astral-sh/uv:python3.13-bookworm-slim`,
`node:24-alpine`, `alpine:3.20`

**Storage**: cachés de GitLab (`.uv-cache/`, `frontend/node_modules/`)

**Testing**: pytest estático con PyYAML (transitiva del entorno)

**Target Platform**: GitLab.com, runner compartido

**Project Type**: infraestructura CI/CD

**Performance Goals**: pipeline de MR por debajo de 5 minutos con caché caliente

**Constraints**: sin `pip`, sin secretos, sin duplicar pipelines

**Scale/Scope**: un archivo y su runbook

## Constitution Check

- **uv como único gestor**: `uv sync --frozen`; sin `pip`. ✅
- **Test-first**: cada AC tiene prueba estática. ✅
- **Sin secretos**: no hay tokens en el archivo. ✅
- **Propiedad**: `.gitlab-ci.yml` es de Guillermo; `docs/operacion/` es de Eliana (aviso). ✅
- **Una HU por PR**. ✅

## Project Structure

```text
.gitlab-ci.yml                    # nuevo
docs/operacion/gitlab-ci.md       # nuevo: etapas, reglas y validación
tests/test_gitlab_ci.py           # 9 pruebas estáticas
specs/067-hu-066-gitlab-ci-base/
```

## Design decisions

1. **Imagen oficial de `uv`.** Evita instalar el gestor con `pip` y garantiza Python 3.13.
2. **`workflow.rules` en vez de reglas por job.** Un solo punto decide cuándo hay pipeline;
   evita el clásico duplicado MR + rama.
3. **Caché por lockfile.** Si el lock cambia, la clave cambia y no se reutiliza una caché
   obsoleta.
4. **`build` en `main` (o manual).** El paquete de entrega sale de la rama de release; en
   `develop` no hace falta.
5. **`deploy` marcador manual.** Reserva la etapa sin fingir un despliegue que HU-070
   implementa; `allow_failure` evita bloquear la entrega.

## Risks

| Riesgo | Mitigación |
|---|---|
| Imagen `uv` no disponible en el runner | Es pública en GHCR; si falla, se cambia a `python:3.13-slim` + script de `uv` |
| Caché corrupta | Clave por lockfile y `uv sync --frozen` |
| `deploy` manual olvidado | `allow_failure` y aviso en el runbook |
| Duplicación de pipelines | `workflow.rules` y prueba que lo verifica |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_gitlab_ci.py` (etapas, cachés, `uv sync` y compuertas) |
| AC-02 | `tests/test_gitlab_ci.py` (workflow, jobs sin regla, build/deploy en `main`) |
| AC-03 | `tests/test_gitlab_ci.py` (sin `pip` ni secretos) + `glab ci lint` como evidencia |
