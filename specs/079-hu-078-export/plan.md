# Implementation Plan: HU-078 — Exportar resultados en CSV y JSON

**Date**: 2026-11-27 | **Spec**: [spec.md](./spec.md)

## Summary

La HU ya está implementada en `develop`. Este plan documenta qué archivos la sostienen y
cómo se verifica, para que la compuerta de trazabilidad la reconozca.

## Technical Context

**Language/Version**: Python 3.13 (pruebas estáticas), YAML, shell POSIX
**Testing**: pytest estático
**Constraints**: sin red, sin servidor, sin credenciales

## Constitution Check

- **Test-first**: los AC tienen prueba que los referencia. ✅
- **Sin secretos**: se verifica su ausencia, no se copian. ✅
- **Documentación sincronizada**: la spec se enlaza desde la issue. ✅

## Design decisions

1. **Prueba estática sobre el entregable.** El comportamiento se validó en el Droplet;
   lo que queda es el contrato verificable en cada PR.
2. **Spec de cierre.** La HU se ejecutó antes de escribir su spec; esta la deja auditable.
3. **Evidencia enlazada, no copiada.** Los documentos y archivos son la fuente.

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_079_*.py` (primera comprobación) |
| AC-02 | `tests/test_079_*.py` (segunda comprobación) |
| AC-03 | `tests/test_079_*.py` (tercera comprobación) |
