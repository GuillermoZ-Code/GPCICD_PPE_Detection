# Implementation Plan: HU-087 — Actualizar CONSTITUTION, AGENTS y README para el M4

**Branch**: `feature/088-hu-087-docs-m4` | **Date**: 2026-11-28 | **Spec**:
[spec.md](./spec.md)

**Input**: `specs/088-hu-087-docs-m4/spec.md`

## Summary

Sincronizar la documentación de gobierno con el estado real del M4: modelo YOLO26n +
ONNX, CI/CD de GitHub + GitLab, despliegue en Droplet con Caddy y basic auth, release
v1.0.0 y mínimo de 1.200 pruebas. Se actualizan `CONSTITUTION.md`, la constitución
derivada de `.specify/memory/`, `AGENTS.md` (comandos de despliegue) y `README.md`
(modelo, stack, enlaces y métricas). Cuatro pruebas estáticas protegen los AC.

## Technical Context

**Language/Version**: Markdown + Python 3.13 para las pruebas

**Primary Dependencies**: pytest; sin dependencias nuevas

**Storage**: documentos versionados en el repositorio

**Testing**: pytest estático sobre texto y enlaces Markdown

**Target Platform**: documentación del repositorio

**Project Type**: documentación de gobierno

**Performance Goals**: N/A

**Constraints**: no editar el bloque generado de `AGENTS.md` §0; no tocar
`docs/curso/PRUEBAS.md` ni `docs/curso/backlog.md` (bloqueados a Jesús); no incluir
secretos

**Scale/Scope**: 4 documentos, 1 archivo de pruebas, 4 pruebas

## Constitution Check

- **Spec Kit antes de implementar**: spec/plan/tasks creados antes del commit. ✅
- **Test-first**: las 4 pruebas se escribieron antes de actualizar los documentos y
  fallaron primero. ✅
- **Sin secretos**: solo nombres de variables (`PPE_AUTH_HASH`, `DOCKERHUB_TOKEN`). ✅
- **Sin cambios de código de producción**: solo documentación y pruebas. ✅
- **Trazabilidad**: cada AC tiene su prueba en `tests/test_docs_m4.py`. ✅

## Project Structure

### Documentation

```text
CONSTITUTION.md                         # módulo activo, stack, ADR 0013, release
.specify/memory/constitution.md         # derivado v1.2 con foco M4
AGENTS.md                               # comandos de despliegue
README.md                               # modelo, stack, enlaces, métricas
specs/088-hu-087-docs-m4/               # spec, plan y tasks
tests/test_docs_m4.py                   # 4 pruebas AC-01/AC-02/AC-03
```

## Phase Plan

### Phase 0 — Investigación

- Leer la issue #143, `CONSTITUTION.md`, el derivado de `.specify/memory/`, `AGENTS.md`
  y `README.md`; detectar referencias al M3 (YOLO11s, 451 pruebas, URL plantilla).

### Phase 1 — Diseño

- Definir los 3 AC y su mapa a 4 pruebas.
- Fijar el alcance: no tocar archivos bloqueados ni el bloque generado de `AGENTS.md`.

### Phase 2 — Test-first

- Escribir `tests/test_docs_m4.py` y confirmar la fase roja.

### Phase 3 — Implementación documental

- Actualizar `CONSTITUTION.md`: módulo activo M4, CI/CD con GitLab/Caddy, ADR 0013 y
  release v1.0.0.
- Actualizar `.specify/memory/constitution.md` a la versión 1.2 con stack, roadmap,
  riesgos y decisiones del M4; corregir el mínimo de pruebas a 1.200.
- Actualizar `README.md`: YOLO26n + ONNX, Caddy, URL pública, registry, métricas y
  roadmap; retirar `yolo11s-clean`.
- Actualizar `AGENTS.md`: comandos `make deploy` y `make verify` (sin tocar §0).

### Phase 4 — Verificación

- `uv run pytest -q tests/test_docs_m4.py`
- `make check`
- `python -m ppe_detection.tools.check_specs --check`
- `make ownership-check`

## Risks

- **Documentación que promete más que el estado real**: el M4 sigue en cierre; el README
  marca el release como «en preparación», no como publicado.
- **Deriva del derivado**: la versión 1.2 se sincroniza en el mismo commit que
  `CONSTITUTION.md`; si cambia la fuente, se actualiza aquí.
- **Enlaces internos**: la prueba los valida; si se mueve un documento, falla y obliga a
  corregir la referencia.
