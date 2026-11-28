# Implementation Plan: HU-038 — Estadísticas de entrada para deriva

**Branch**: `feature/039-hu-038-drift-entrada` | **Date**: 2026-11-27

**Spec**: [spec.md](./spec.md)

**Input**: Issue #94 y `specs/039-hu-038-drift-entrada/spec.md`.

## Summary

Agregar `io/stats.py` con funciones puras que resumen tamaño, aspecto y luminancia de
`ImageData`. El módulo no guarda píxeles ni conoce el modelo. La línea base se documenta
en `docs/evaluation/deriva.md` con 100 imágenes de test.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: NumPy; `ImageData` del contrato

**Testing**: pytest AAA con imágenes sintéticas; sin modelo ni dataset

**Target Platform**: CPU / CI

**Project Type**: biblioteca de entrada

**Constraints**: solo agregados numéricos; sin imágenes ni datos personales

**Scale/Scope**: 2 clases de datos, 4 pruebas, muestra de 100 imágenes

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` con patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset ni red en las pruebas.
- [x] Sin imágenes ni datos personales versionados.
- [x] No se cambia el contrato `ImageData`.
- [x] El módulo se limita a estadísticas; no decide cumplimiento.

## Project Structure

```text
src/ppe_detection/io/
├── stats.py        # nuevo
└── __init__.py     # exports
tests/
└── test_input_stats.py
docs/evaluation/
└── deriva.md
specs/039-hu-038-drift-entrada/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Cálculo

```text
luminancia = 0,299 R + 0,587 G + 0,114 B
brightness_mean = media(luminancia)
brightness_std  = desviación poblacional(luminancia)
aspect_ratio    = ancho / alto
```

### Resumen

`summarize_statistics()` recibe una secuencia de `ImageStats` y devuelve medias de
ancho, alto, aspecto y brillo, más mínimo y máximo de brillo. No recibe `ImageData` ni
guarda el arreglo.

### Evidencia

Se cargan las primeras 100 imágenes de test con `load_image()`, se calculan sus
estadísticas y se escribe `docs/evaluation/deriva.md`. El resumen local queda en
`dist/deriva/summary.json`, fuera de Git.

## Phases

1. **Tests:** cálculo, privacidad, resumen y errores.
2. **Implementación:** `stats.py` y exports de `io`.
3. **Evidencia:** muestra fija y línea base.
4. **Cierre:** `make specs-check`, `make check`, `uv build`, PR `Closes #94`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Guardar imágenes por accidente | `ImageStats` solo tiene números |
| Brillo no comparable | Fórmula BT.601 documentada |
| Muestra poco representativa | Se declara como línea base, no como detector de deriva |
| Confundir deriva con fallo del modelo | El informe separa estadísticas de métricas |
| Archivo de `io/` de otra persona | El cambio se revisa con la dueña del módulo |

## Verification

```bash
uv run pytest tests/test_input_stats.py -q
make specs-check
make check
uv build
```
