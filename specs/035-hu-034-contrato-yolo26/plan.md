# Implementation Plan: HU-034 — Pruebas de contrato del detector con YOLO26

**Branch**: `feature/035-hu-034-contrato-yolo26` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #90 y `specs/035-hu-034-contrato-yolo26/spec.md`.

## Summary

Agregar una suite de contrato dedicada al adaptador `YoloDetector`. El modelo real no
se carga: un `FakeModel` imita la salida de Ultralytics (`Results.boxes`) y permite
probar catálogo, confianza, cajas y el modo NMS-free de YOLO26. No se modifica código
de producción.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `ppe_detection.contracts` y
`ppe_detection.detection.yolo`; numpy y pytest

**Storage**: ninguna; datos sintéticos en memoria

**Testing**: pytest AAA; sin Ultralytics, GPU, dataset ni red

**Target Platform**: CPU / CI

**Project Type**: pruebas de contrato de una biblioteca de detección

**Constraints**: no tocar producción; no cargar pesos; no cambiar el contrato

**Scale/Scope**: 8 pruebas, 6 clases, una imagen sintética de 8×6

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red.
- [x] Test-first: la suite fija el contrato antes de cualquier cambio.
- [x] No se cambia `ImageData → list[Detection]`.
- [x] No se versionan pesos ni datos.

## Project Structure

```text
tests/
└── test_detector_contract.py   # AC-01, AC-02 y AC-03
specs/035-hu-034-contrato-yolo26/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Modelo falso

`FakeTensor` imita `item()` y `tolist()`. `FakeBox` imita `cls`, `conf` y `xyxy`;
`FakeResult` imita `boxes`; `FakeModel` imita `names` y `predict()`. Así la suite no
depende de Ultralytics y sigue el mismo camino que el detector real.

### Casos

1. **Catálogo:** `CLASSES` y `detector.classes` conservan las seis clases en orden.
2. **Confianza:** se conservan 0,0 y 1,0; se descartan negativas, mayores que 1,
   `NaN` e infinito.
3. **Cajas:** una caja fuera de límites se recorta; una caja parcial también.
4. **YOLO26:** se convierten las seis clases y se comprueba `nms=False`.
5. **Errores:** `class_id` fuera de rango y catálogo ajeno fallan explícitamente.

### Decisiones

- No se reutilizan clases de `tests/test_yolo_detector.py` para no acoplar suites.
- Los valores de confianza límite se escriben explícitamente.
- No se prueba la inferencia real; eso corresponde a HU-002/HU-022.

## Phases

1. **Tests:** escribir los 8 casos y verificar que pasan contra el código actual.
2. **Documentación:** registrar la spec, el plan y las tareas.
3. **Cierre:** `make check`, PR con `Closes #90` y revisión.

## Risks

| Riesgo | Mitigación |
|---|---|
| Duplicar pruebas existentes | La suite se enfoca en el contrato, no en detalles internos |
| Acoplarse a Ultralytics | Todo el modelo es falso |
| Cambiar producción sin necesidad | Solo se agrega `tests/test_detector_contract.py` |
| Dependencia de dataset | La imagen y las cajas son sintéticas |

## Verification

```bash
uv run pytest tests/test_detector_contract.py -q
make specs-check
make check
```

No se actualiza `PRUEBAS.md` en esta rama porque es un archivo bloqueado de Jesús; el
conteo se solicita al cerrar.
