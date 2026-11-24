# Implementation Plan: HU-092 — Sincronizar `backlog.md` con las 113 HU

**Branch**: `feature/093-hu-092-backlog-espejo` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #148 y `specs/093-hu-092-backlog-espejo/spec.md`.

## Summary

Regenerar `docs/curso/backlog.md` como espejo de las 113 HU: 13 del M3 y 100 del M4, con
issue, SP, dueño, ola, spec y estado. El reparto y las olas salen de
`M4/ASIGNACION.md`; el número y el estado de cada issue, de GitHub. Añadir cuatro
pruebas que validan el conteo, los totales y la coherencia con `specs/`.

## Technical Context

**Language/Version**: Markdown + Python 3.13 para las pruebas

**Primary Dependencies**: biblioteca estándar; sin dependencias nuevas

**Storage**: `docs/curso/backlog.md` (espejo versionado)

**Testing**: pytest con lectura de archivos; sin red

**Target Platform**: repositorio

**Project Type**: gobierno del repositorio

**Constraints**: no cambiar títulos, AC ni SP; no crear issues

**Scale/Scope**: 113 filas, tres tablas de resumen y cuatro pruebas

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Cada AC tiene una prueba que lo referencia.
- [x] Sin cambios en el contrato `ImageData → list[Detection]`.
- [x] `docs/curso/backlog.md` es `[[locked]]` de `jesusriverosUAO`.
- [x] Documentación en español.

## Project Structure

```text
docs/curso/backlog.md              # reescrito: 113 HU
tests/test_backlog_mirror.py       # nuevo: conteo, totales y specs
specs/093-hu-092-backlog-espejo/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Estructura del espejo

```text
# Backlog — espejo de las issues
## Resumen                     (7/11, 6/8, 100/200, 113/219)
## Reparto del M4 por integrante (24/26/25/25 HU; 50 SP y 192 pruebas cada uno)
## M3 — HUs 001 a 013         (tablas por sprint: HU, issue, título, SP, spec, estado)
## M4 — HUs 014 a 113         (una tabla por integrante con épica, SP, prio, ola, spec)
## Dependencias entre integrantes
## Decisiones de planificación
```

### Generación

El espejo es una instantánea construida a partir de:

1. Las tablas de `M4/ASIGNACION.md` (HU, spec, título, épica, SP, prioridad, pruebas,
   dependencia y ola).
2. Los títulos de las issues (`HU-NNN`) para el número y el estado.
3. Los 13 registros del M3 que ya estaban en `backlog.md`.

No se versiona el generador: el espejo es un documento, no una herramienta. La prueba
verifica la coherencia interna y con `specs/`, no vuelve a consultar GitHub.

### Pruebas

`tests/test_backlog_mirror.py`:

1. `test_backlog_lists_all_113_hus` → AC-01: 113 HU únicas.
2. `test_backlog_m4_rows_have_epic_sp_wave_and_spec` → AC-01: 100 filas del M4 con SP
   Fibonacci, ola 1–3 y 24/26/25/25 por integrante.
3. `test_backlog_totals_match_rows` → AC-02: totales por sprint e integrante.
4. `test_backlog_specs_match_repository` → AC-03: enlaces existentes y todas las
   carpetas de `specs/` referenciadas.

### Alternativas descartadas

- **Copiar los AC completos de las 100 issues**: el archivo tendría miles de líneas y
  duplicaría la issue; el espejo resume y enlaza.
- **Generar el espejo en cada push**: añade una dependencia de red a la CI sin que el AC
  lo pida.
- **Unir M3 y M4 en una sola tabla**: se pierden las olas y el reparto por persona.

## Phases

1. **Tests first**: las cuatro pruebas y confirmar rojo.
2. **Implementación**: regenerar el espejo.
3. **Cierre**: `make ownership-check`, `make check`, PR y `Closes #148`.

## Risks

- **Instantánea**: el estado de las issues cambia; se regenera al cerrar cada ola.
- **Specs pendientes**: se muestran como número, no como enlace; la prueba exige que las
  carpetas existentes estén referenciadas.
- **Totales**: 219 SP se explica por HU-014/HU-015 contadas en el M4.
