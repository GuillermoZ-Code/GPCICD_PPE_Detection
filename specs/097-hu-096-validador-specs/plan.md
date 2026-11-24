# Implementation Plan: HU-096 — Validador de specs SDD

**Branch**: `feature/097-hu-096-validador-specs` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #152 y `specs/097-hu-096-validador-specs/spec.md`.

## Summary

Crear `src/ppe_detection/tools/check_specs.py`: recorre `specs/`, exige los tres
documentos, valida las secciones obligatorias y comprueba que cada AC declarado tenga
evidencia resoluble en la tabla de aceptación. Las specs anteriores a 092 se validan solo
por archivos (deuda histórica) y `--strict` aplica la regla completa a todas.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: biblioteca estándar (`re`, `pathlib`); sin dependencias nuevas

**Storage**: solo lectura sobre `specs/` y `tests/`

**Testing**: pytest con `tmp_path`; sin red

**Target Platform**: CPU, Windows/Linux

**Project Type**: herramienta de repositorio dentro del paquete

**Constraints**: no editar specs ajenas; no tocar `uv.lock`

**Scale/Scope**: 32 specs actuales, un comando y un workflow

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Cada AC tiene una prueba que lo referencia.
- [x] Sin cambios en el contrato `ImageData → list[Detection]`.
- [x] `src/ppe_detection/tools/` y `tests/test_tools*.py` son del autor;
      `.github/` y `Makefile` generan aviso de propiedad.
- [x] Documentación en español.

## Project Structure

```text
src/ppe_detection/tools/check_specs.py   # nuevo: validador
tests/test_tools_check_specs.py          # nuevo: specs de ejemplo en tmp_path
.github/workflows/specs.yml              # nuevo: job de CI
Makefile                                 # + specs-check
specs/097-hu-096-validador-specs/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Reglas

| Regla | Qué exige |
|---|---|
| Archivos | `spec.md`, `plan.md`, `tasks.md` |
| Secciones | `## User Scenarios & Testing`, `## Requirements`, `## Success Criteria` |
| Tabla | sección `## Acceptance →` con al menos una fila |
| AC declarado | cada `**AC-NN**` aparece como fila `| AC-NN ... |` |
| Evidencia | la fila cita una prueba existente o un documento |

### Funciones

- `spec_dirs(root)`, `spec_number(path)`: recorrido y número de la spec.
- `declared_acs(text)`: `**AC-NN**` de los escenarios.
- `acceptance_rows(text)`: `AC-NN` → celdas de la tabla.
- `resolves(root, ref)`: archivo/función de prueba o documento existente.
- `has_evidence(cell)`: referencia entre backticks o referencia seccional (`§`, `Tabla`).
- `validate(root, legacy_before=92)`: lista de problemas.
- `main()`: `--check` (código de salida), `--strict`, `--root`.

### Resolución de referencias

1. `tests/test_x.py::test_y` → archivo y función existen.
2. `tests/test_x.py` → archivo existe.
3. `src/...test.tsx` → archivo existe bajo `frontend/`.
4. `test_y` suelto → aparece en algún archivo de `tests/`.
5. `docs/...`, `.md`, `§`, `Tabla`, `ADR` → evidencia documental.

### Alternativas descartadas

- **Aplicar la regla completa a todas las specs**: 31 de 32 fallarían por formatos
  históricos; el CI quedaría rojo y la compuerta se desactivaría.
- **Validar solo archivos**: no aporta nada frente a `ls`.
- **Usar el parser de la matriz de trazabilidad**: mide otra cosa (HU → pruebas), no la
  calidad interna de la spec.

## Phases

1. **Tests first**: specs de ejemplo en `tmp_path` y los doce casos.
2. **Implementación**: módulo, objetivo del Makefile y workflow.
3. **Cierre**: `make specs-check`, `make check`, PR y `Closes #152`.

## Risks

- **Deuda histórica**: las specs antiguas no cumplen la tabla completa; se documenta y
  `--strict` la muestra.
- **Evidencia documental**: el criterio es heurístico; se acepta cualquier referencia
  entre backticks o seccional.
- **CI**: el job solo lee archivos; no necesita red ni `gh`.
