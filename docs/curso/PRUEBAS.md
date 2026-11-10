# Inventario de pruebas — GPCICD PPE Detection

> **Actualizado:** 2026-11-10.
> **Requisito del curso:** más de **400 pruebas unitarias** para la entrega
> (indicación del docente; no constaba en el repositorio hasta este documento).

## 1. Resumen

| Suite | Herramienta | Archivos | Pruebas | Comando |
|-------|-------------|---------:|--------:|---------|
| Backend Python | pytest | 9 | **111** | `make test` |
| Frontend | Vitest | 5 | **19** | `make frontend-test` |
| **Total** | | **14** | **130** | `make check` + `make frontend-check` |

Una prueba del backend se omite cuando no hay artefactos locales
(`test_real_weights_smoke`), por eso la corrida muestra **110 passed + 1 skipped**.

> Con la PR #39 (HU-005) se suman 7 pruebas de validación de imágenes: **137**.

## 2. Desglose del backend

| Archivo | Pruebas |
|---------|--------:|
| `tests/test_contracts.py` | 28 |
| `tests/test_image_loader.py` | 17 |
| `tests/test_predict.py` | 16 |
| `tests/test_yolo_detector.py` | 15 |
| `tests/test_estado.py` | 10 |
| `tests/test_results.py` | 10 |
| `tests/test_overlay.py` | 7 |
| `tests/test_training.py` | 7 |
| `tests/test_smoke.py` | 1 |
| **Total** | **111** |

## 3. Desglose del frontend

| Archivo | Pruebas |
|---------|--------:|
| `src/api/client.test.ts` | 6 |
| `src/validate.test.ts` | 5 |
| `src/App.test.tsx` | 4 |
| `src/components/AnnotatedCanvas.test.tsx` | 2 |
| `src/components/DetectionTable.test.tsx` | 2 |
| **Total** | **19** |

## 4. Cómo se cuentan

```bash
# Backend: suma de casos recogidos por pytest
uv run pytest --collect-only -q

# Frontend: Vitest informa el total al correr
cd frontend && npm run test
```

Cada caso parametrizado (`@pytest.mark.parametrize`) cuenta como una prueba.
Las pruebas que requieren GPU, dataset completo o red no entran: las unitarias deben
correr sin ellas.

## 5. Brecha frente al requisito

| Concepto | Valor |
|----------|------:|
| Requisito | **> 400** |
| Actual | **130** (137 con #39) |
| Brecha | **~263** |

## 6. Ruta propuesta para llegar a 400

| Frente | Pruebas objetivo | Enfoque |
|--------|-----------------:|---------|
| HU-005 (#39) | 7 | Validación de imágenes |
| HU-006 API REST | 60 | Endpoints, esquemas, errores, OpenAPI |
| HU-008 evaluación | 45 | IoU, mAP, matrices y métricas por clase |
| HU-009 MLflow | 25 | Runs, parámetros, métricas y artefactos |
| HU-010 gRPC | 30 | Contrato, errores y equivalencia con REST |
| HU-011 Docker CPU | 10 | Build, smoke y ejecución sin GPU |
| HU-012 calidad | 20 | Regresiones y contratos |
| HU-013 versión | 15 | Identificación y distinción de versiones |
| Frontend (ampliación) | 25 | Estados, accesibilidad y API real |
| Contratos y geometría parametrizados | 35 | Casos borde por clase y formato |
| **Total** | **~272** | **~402 acumuladas** |

> El requisito se cumple con pruebas que verifican un AC o un FR, no con duplicados.
> Si un frente produce menos casos, se compensa con parametrización de casos borde
> reales, no con pruebas artificiales.

## 7. Reglas

- Toda prueba nueva referencia su AC o FR en el nombre o en el docstring (test-first).
- Sin GPU, dataset completo ni red en las pruebas unitarias.
- Sin umbral de cobertura hasta HU-012.
- El conteo se actualiza al cerrar cada HU, en el mismo PR (regla de sincronía).
