# Implementation Plan: HU-033 — Pruebas de regresión de métricas

**Branch**: `feature/034-hu-033-regresion-metricas` | **Date**: 2026-11-21

**Spec**: [spec.md](spec.md)

**Input**: Issue #89 y `specs/034-hu-033-regresion-metricas/spec.md`.

## Summary

Añadir una suite de casos dorados para las métricas de HU-008. No se modifica
`metrics.py`: las pruebas fijan el comportamiento actual con valores calculados a
mano, una tolerancia explícita y casos sintéticos que no requieren GPU, dataset ni
red.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: pytest; solo `ppe_detection.evaluation.metrics`

**Storage**: ninguna; datos sintéticos en memoria

**Testing**: pytest AAA, `pytest.approx` con `abs=1e-12`

**Target Platform**: CPU / CI

**Project Type**: biblioteca de evaluación

**Constraints**: no modificar producción; no cargar Ultralytics; no usar dataset

**Scale/Scope**: una suite de 8 pruebas; ejecución en milisegundos

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red.
- [x] Test-first: la suite es el entregable y define el contrato esperado.
- [x] No se cambia el contrato de detecciones.

## Project Structure

```text
tests/
└── test_metrics_golden.py          # 8 casos dorados de AC-01/02/03
specs/034-hu-033-regresion-metricas/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Casos

1. IoU: idénticas, disjuntas, parciales, anidadas y degeneradas.
2. Emparejamiento: perfecto, umbral, greedy sin reutilizar predicciones y clases.
3. Precision/recall/F1: perfecto, parcial y vacío.
4. AP: secuencia conocida con interpolación de todos los puntos.
5. mAP: media de AP por clase.
6. Escenario compuesto: 3 GT y 3 predicciones con TP, FP y FN por clase.
7. Tolerancia explícita: `TOL = 1e-12` en todas las comparaciones.
8. Independencia: la suite no importa `ultralytics`, `torch`, `cv2` ni `yaml`.

### Reglas

- Los valores esperados se escriben como fracciones o decimales exactos.
- No se parametriza en exceso: cada caso debe leerse como un documento.
- Si una fórmula cambia, el test debe fallar; no se actualizan los valores sin
  justificar la regresión.

## Phases

1. **Tests**: escribir los 8 casos y ejecutarlos contra el código actual.
2. **Verificación**: confirmar que la suite pasa sin extras de inferencia.
3. **Cierre**: `make check`, PR con `Closes #89` y revisión.

## Risks

- **Falsa sensación de cobertura**: los casos son pequeños; cubren primitivas, no el
  modelo real. HU-008 conserva la evaluación con dataset.
- **Tolerancia demasiado laxa**: se usa `1e-12`; si una operación necesita más margen,
  se documenta en el caso.
- **Specs/ es de Jesús**: la spec genera aviso de propiedad; el PR necesita su
  revisión.
