# Implementation Plan: HU-098 — Model Registry con alias champion/challenger

**Branch**: `feature/099-hu-098-registry` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #154 y `specs/099-hu-098-registry/spec.md`.

## Summary

Crear `tracking/registry.py` con la lógica pura del registro: `ModelAlias`,
`build_aliases` (champion = `yolo26n-clean` del ADR 0009, challenger = candidato),
`validate_aliases` y `plan_promotion` (nuevo champion y rollback).

## Technical Context

**Python 3.13, biblioteca estándar; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin pesos en Git.
- [x] Cada AC tiene prueba.
- [x] `tracking/` y `tests/test_tracking*.py` son del autor.

## Project Structure

```text
src/ppe_detection/tracking/registry.py   # nuevo
tests/test_tracking_registry.py          # nuevo: 9 pruebas
specs/099-hu-098-registry/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

- Constantes: `CHAMPION_VERSION`, `CHAMPION_SHA256`, `ROLLBACK_VERSION`.
- `validate_aliases` comprueba nombre, duplicados, versión y SHA256.
- `plan_promotion(champion, challenger)` devuelve
  `{alias: champion, from, to, rollback}`.

## Phases

1. Tests first (9 pruebas).
2. Módulo.
3. `make check`, ownership y PR.

## Risks

- **Sin MLflow real**: la prueba cubre la lógica; el registro real se hará en el Droplet.
- **SHA fijo**: si cambia el modelo productivo, se actualizan las constantes con el ADR.
