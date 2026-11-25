# Implementation Plan: HU-102 — Protocolo de uso de Engram y ADR

**Branch**: `feature/103-hu-102-protocolo-engram` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #158 y `specs/103-hu-102-protocolo-engram/spec.md`.

## Summary

Escribir el ADR 0011 con el protocolo de memoria (qué se guarda, qué no, sincronización y
exportación), indexarlo en `docs/adr/README.md` y enlazarlo desde la tabla de herramientas
de `AGENTS.md`. Una prueba estructural valida el contenido.

## Technical Context

**Markdown + Python 3.13 para las pruebas; sin dependencias nuevas.**

## Constitution Check

- [x] Sin dependencias nuevas; sin datos ni secretos.
- [x] Cada AC tiene prueba.
- [x] `docs/adr/` y `AGENTS.md` (Guillermo) generan aviso, no bloqueo.

## Project Structure

```text
docs/adr/0011-memoria-agentes.md   # nuevo
docs/adr/README.md                 # índice
AGENTS.md                          # fila de Engram
tests/test_engram_protocol.py      # 7 pruebas
specs/103-hu-102-protocolo-engram/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

- Jerarquía: repositorio > memoria.
- Qué se guarda: decisiones, bugs, hallazgos, convenciones y resumen de sesión.
- Qué no: credenciales, datos personales, datasets/pesos y transcripciones.
- Sincronización local; exportación fuera de Git.

## Phases

1. Tests first (7 pruebas).
2. ADR, índice y `AGENTS.md`.
3. `make check`, ownership y PR.

## Risks

- **Número de ADR**: la issue pide 0011; 0010 queda libre.
- **Propiedad**: dos archivos de Guillermo; aviso esperado.
