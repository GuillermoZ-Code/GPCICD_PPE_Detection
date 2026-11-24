# Implementation Plan: HU-095 — Corregir el inventario y el plan hacia 1.200 pruebas

**Branch**: `feature/096-hu-095-corregir-pruebas-md` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #151 y `specs/096-hu-095-corregir-pruebas-md/spec.md`.

## Summary

Reescribir `docs/curso/PLAN-PRUEBAS.md` sobre el conteo real: baseline 533 (457 pytest +
76 Vitest), objetivo 1.200 y brecha 667, repartida por integrante. Conservar las cifras
anteriores en una tabla de historial y apuntar el conteo al comando de HU-094. No se
edita `PRUEBAS.md` a mano: lo regenera `make pruebas-write`.

## Technical Context

**Language/Version**: Markdown + Python 3.13 para las pruebas

**Primary Dependencies**: biblioteca estándar; sin dependencias nuevas

**Storage**: `docs/curso/PLAN-PRUEBAS.md` (versionado) y `docs/curso/PRUEBAS.md`
(generado)

**Testing**: pytest con lectura de archivos; sin red

**Target Platform**: repositorio

**Project Type**: gobierno del repositorio

**Constraints**: no editar issues; no tocar `uv.lock`; `PRUEBAS.md` es de HU-094

**Scale/Scope**: un documento de plan y cuatro pruebas estructurales

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Cada AC tiene una prueba que lo referencia.
- [x] Sin cambios en el contrato `ImageData → list[Detection]`.
- [x] `docs/curso/` pertenece a `jesusriverosUAO`.
- [x] Documentación en español.

## Project Structure

```text
docs/curso/PLAN-PRUEBAS.md      # reescrito: baseline, brecha y reparto
docs/curso/PRUEBAS.md           # regenerado por make pruebas-write
tests/test_plan_pruebas.py      # nuevo: valida baseline, reparto, comando e historial
specs/096-hu-095-corregir-pruebas-md/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Cifras

| Concepto | Valor |
|---|---:|
| Baseline (23/11/2026) | 533 |
| Objetivo | 1.200 |
| Brecha | 667 |

Reparto:

| Integrante | Plan | Cerradas | Restante | Ajuste | Aportar |
|---|---:|---:|---:|---:|---:|
| Guillermo | 192 | 0 | 192 | 0 | 192 |
| Hernán | 192 | 80 | 112 | 0 | 112 |
| Eliana | 192 | 0 | 192 | 0 | 192 |
| Jesús | 192 | 24 | 168 | +3 | 171 |
| **Total** | **768** | **104** | **664** | **+3** | **667** |

- Las 104 cerradas son las pruebas planificadas de HU-016, HU-017, HU-019, HU-020,
  HU-021, HU-023, HU-025, HU-026, HU-033, HU-091, HU-094, HU-095, HU-105 y HU-107.
- El ajuste de +3 va a HU-113 (informe de rúbrica) porque el entregable real supera al
  planificado en algunas HU y queda corto en otras; con el ajuste, 533 + 667 = 1.200.

### Pruebas

`tests/test_plan_pruebas.py`:

1. `test_plan_has_one_baseline_and_target` → AC-01: baseline, objetivo y brecha en la
   tabla, y la aritmética 533 + 667 = 1.200.
2. `test_plan_splits_remaining_tests_by_integrator` → AC-02: las cuatro filas y el total
   667.
3. `test_plan_documents_counting_command_and_date` → AC-03: `make pruebas-write` y la
   fecha de medición.
4. `test_plan_keeps_correction_history` → AC-01: 375 y 451 aparecen como historial, no
   como baseline.

### Alternativas descartadas

- **Mantener el 451 del AC literal**: se descartó porque el repositorio tiene 533 y el
  plan quedaría en contradicción con `make pruebas`.
- **Repartir la brecha en partes iguales**: se descartó porque ignora las HU abiertas de
  cada integrante y el reparto de `ASIGNACION.md`.
- **Generar también `PLAN-PRUEBAS.md`**: se descartó; el plan incluye decisiones y
  contexto que no salen de un conteo automático.

## Phases

1. **Tests first**: las cuatro pruebas del plan y confirmar rojo.
2. **Implementación**: reescribir `PLAN-PRUEBAS.md`.
3. **Regeneración**: `make pruebas-write` para dejar `PRUEBAS.md` en 533.
4. **Cierre**: `make ownership-check`, `make check`, PR y `Closes #151`.

## Risks

- **Cifras volátiles**: cada fusión cambia el conteo; el plan declara la fecha y el
  comando, y el historial se actualiza en el mismo PR que cambie el baseline.
- **Reparto por integrante**: depende de las HU cerradas; se revisa al cerrar cada ola.
- **PRUEBAS.md**: si alguien lo edita a mano, `make pruebas-write` lo sobrescribe.
