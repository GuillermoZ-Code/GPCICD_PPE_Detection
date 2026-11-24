# Implementation Plan: HU-108 — Retrospectiva y lecciones aprendidas

**Branch**: `feature/109-hu-108-retrospectiva` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #164 y `specs/109-hu-108-retrospectiva/spec.md`.

## Summary

Crear `docs/curso/M4/RETRO.md` con start/stop/continue por integrante y una tabla de
acciones con dueño y fecha, más una prueba estructural que valide el formato.

## Technical Context

**Markdown + Python 3.13 para las pruebas; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin datos ni secretos.
- [x] Cada AC tiene prueba.
- [x] `docs/curso/` es del autor.

## Project Structure

```text
docs/curso/M4/RETRO.md        # nuevo
tests/test_retro_m4.py        # nuevo
specs/109-hu-108-retrospectiva/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

Secciones `## Guillermo Zabala`, `## Eliana Cardona`, `## Hernán Estrada`,
`## Jesús Riveros`, cada una con `### Start`, `### Stop` y `### Continue` y al menos un
ítem. Tabla `| Acción | Dueño | Fecha |` con acciones del M5.

La prueba busca los encabezados y cuenta los ítems con `- `.

## Phases

1. Tests first (4 pruebas).
2. Documento.
3. `make check`, ownership y PR.

## Risks

- **Retrospectiva genérica**: las acciones deben ser concretas y con fecha.
- **Sesgo**: se evalúan prácticas, no personas.
