# Implementation Plan: HU-113 — Informe de cumplimiento de la rúbrica M4

**Branch**: `feature/114-hu-113-rubrica` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #169 y `specs/114-hu-113-rubrica/spec.md`.

## Summary

Crear `src/ppe_detection/tools/rubrica.py` con los 14 ítems de la rúbrica del M4
(evidencia y responsable), un generador del informe `docs/entrega/RUBRICA-M4.md` con
estado ✔/✘ y un modo `--check` que valida la estructura de los ítems.

## Technical Context

**Python 3.13, biblioteca estándar; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin datos ni secretos.
- [x] Cada AC tiene prueba.
- [x] `docs/entrega/` (Eliana) genera aviso, no bloqueo.

## Project Structure

```text
src/ppe_detection/tools/rubrica.py   # nuevo
tests/test_tools_rubrica.py          # nuevo
Makefile                             # + rubrica, rubrica-write, rubrica-check
docs/entrega/RUBRICA-M4.md           # generado
specs/114-hu-113-rubrica/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

- `RubricItem(id, area, criterion, evidence, owner)`; `RUBRIC` con 14 ítems.
- `build_rows(root, items)` comprueba `(root / evidence).exists()`.
- `render(rows)` produce la tabla con ✔/✘ y el corte 27/11/2026.
- `--write` genera; `--check` valida los ítems.

## Phases

1. Tests first (8 pruebas).
2. Módulo y Makefile.
3. Generar el informe, `make check`, PR.

## Risks

- **Evidencia pendiente**: los documentos de PRs abiertas salen ✘ hasta el merge.
- **Rúbrica cambiante**: la lista vive en el módulo y se actualiza con la rúbrica.
