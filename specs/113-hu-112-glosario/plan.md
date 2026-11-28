# Implementation Plan: HU-112 — Glosario y mapa de documentación

**Branch**: `feature/113-hu-112-glosario` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #168 y `specs/113-hu-112-glosario/spec.md`.

## Summary

Crear `docs/README.md` con un mapa por tema, un glosario de términos y una prueba que
valide que los enlaces relativos resuelven y que los términos obligatorios están.

## Technical Context

**Markdown + Python 3.13 para las pruebas; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin datos ni secretos.
- [x] Cada AC tiene prueba.
- [x] `docs/README.md` es libre (sin dueño en el manifiesto).

## Project Structure

```text
docs/README.md                 # nuevo: mapa y glosario
tests/test_docs_readme.py      # nuevo
specs/113-hu-112-glosario/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

- Secciones: Gobierno, Curso, Operación, Datos y modelo, Arquitectura, Specs, Entrega.
- Enlaces relativos a `docs/` (`../CONSTITUTION.md`, `curso/backlog.md`, ...).
- Glosario en tabla `| Término | Definición |`.
- La prueba extrae `](destino)` y verifica `(docs / destino).exists()`.

## Phases

1. Tests first (4 pruebas).
2. Documento.
3. `make check`, ownership y PR.

## Risks

- **Enlaces rotos al mover documentos**: la prueba lo detecta.
- **Términos del curso**: se mantienen los del glosario de `CONTEXTO_CURSO.md`.
