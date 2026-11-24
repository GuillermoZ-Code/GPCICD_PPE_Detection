# Implementation Plan: HU-104 — Registro de riesgos del M4

**Branch**: `feature/105-hu-104-riesgos` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #160 y `specs/105-hu-104-riesgos/spec.md`.

## Summary

Crear `docs/curso/M4/RIESGOS.md` con una tabla de riesgos del cierre del M4 (categoría,
probabilidad, impacto, dueño, disparador, mitigación y estado) y una prueba estructural
que valide las cuatro categorías y los campos obligatorios.

## Technical Context

**Markdown + Python 3.13 para las pruebas; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin datos ni secretos.
- [x] Cada AC tiene una prueba.
- [x] `docs/curso/` es del autor.

## Project Structure

```text
docs/curso/M4/RIESGOS.md       # nuevo: registro
tests/test_riesgos_m4.py       # nuevo: prueba estructural
specs/105-hu-104-riesgos/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

Tabla con columnas `ID | Riesgo | Categoría | Prob. | Impacto | Dueño | Disparador |
Mitigación | Estado`. Categorías admitidas: `infraestructura`, `ci`, `modelo`, `equipo`.
La prueba parsea las filas y exige los campos, sin red.

## Phases

1. Tests first (4 pruebas).
2. Registro con diez riesgos.
3. `make check`, ownership y PR.

## Risks

- **Riesgos desactualizados**: el estado se revisa al cierre.
- **Categorías**: una nueva obliga a actualizar la prueba y el registro.
