# Inventario de pruebas — GPCICD PPE Detection

> **Actualizado:** 2026-11-12.
> **Requisito del curso:** **400 pruebas unitarias o más** (≥ 400) para la entrega
> (indicación del docente; no constaba en el repositorio hasta este documento).

## 1. Resumen

| Suite | Herramienta | Archivos | Pruebas | Comando |
|-------|-------------|---------:|--------:|---------|
| Backend Python | pytest | 20 | **234** | `make test` |
| Frontend | Vitest | 8 | **39** | `make frontend-test` |
| **Total** | | **28** | **273** | `make check` + `make frontend-check` |

Dos pruebas se omiten sin hardware o artefactos: `test_real_weights_smoke` (sin
pesos locales) y la de contenedor de HU-011 (sin Docker/imagen/artefacto,
`@pytest.mark.docker`); la corrida muestra **232 passed + 2 skipped**.

> Incluye todas las HU del M3 fusionadas hasta el 12/11/2026: HU-005 (#39),
> HU-006 (#42), HU-007 (SPA), HU-009 (+11 en `test_tracking.py`), HU-010 (#46),
> HU-011 (#52, +9 en `test_docker.py`), HU-012 (+5 en `test_calidad.py`), HU-013
> (+20 en `test_model_version.py`) y el plan de Jesús (+25 en
> `test_tracking_mlflow.py` y +10 en `test_estado_tools.py`).

## 2. Desglose del backend

| Archivo | Pruebas |
|---------|--------:|
| `tests/test_api.py` | 12 |
| `tests/test_calidad.py` | 5 |
| `tests/test_contracts.py` | 28 |
| `tests/test_docker.py` | 9 |
| `tests/test_estado.py` | 10 |
| `tests/test_evaluation.py` | 9 |
| `tests/test_grpc.py` | 9 |
| `tests/test_image_loader.py` | 17 |
| `tests/test_image_validation.py` | 7 |
| `tests/test_launcher.py` | 5 |
| `tests/test_model_version.py` | 20 |
| `tests/test_tracking_mlflow.py` | 25 |
| `tests/test_estado_tools.py` | 10 |
| `tests/test_overlay.py` | 7 |
| `tests/test_predict.py` | 16 |
| `tests/test_results.py` | 10 |
| `tests/test_smoke.py` | 1 |
| `tests/test_tracking.py` | 11 |
| `tests/test_training.py` | 7 |
| `tests/test_yolo_detector.py` | 16 |
| **Total** | **234** |

## 3. Desglose del frontend

| Archivo | Pruebas |
|---------|--------:|
| `src/App.test.tsx` | 8 |
| `src/api/client.test.ts` | 7 |
| `src/config.test.ts` | 5 |
| `src/download.test.ts` | 3 |
| `src/filter.test.ts` | 3 |
| `src/validate.test.ts` | 9 |
| `src/components/AnnotatedCanvas.test.tsx` | 2 |
| `src/components/DetectionTable.test.tsx` | 2 |
| **Total** | **39** |

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
| Requisito | **≥ 400** |
| Actual | **273** (234 pytest + 39 Vitest) |
| Brecha mínima | **127** |
| Objetivo operativo | **430** (157 nuevas) |

> El requisito es un **mínimo**: superar 400 no es un problema. El objetivo operativo
> del plan es **430** para tener margen de descarte en revisión.

## 6. Plan para llegar a 400 o más

El reparto por integrante, los archivos propuestos y los casos concretos viven en
[`PLAN-PRUEBAS.md`](PLAN-PRUEBAS.md). Resumen:

| Integrante | Frente | Nuevas |
|------------|--------|-------:|
| Hernán Estrada | Evaluación, métricas, contratos y geometría | 75 |
| Jesús Riveros | MLflow, versión del modelo y trazabilidad | 0 (completado) |
| Eliana Cardona | API REST, gRPC y Docker | 40 |
| Guillermo Zabala | Frontend, visualización y herramientas | 42 |
| **Total** | | **157** → **430** |

> Jesús completó sus 55 pruebas: 20 de HU-013 y 35 de tracking/estado. El plan
> restante es 157; el mínimo de 400 exige al menos 127.

> Los frentes de HU-005 (#39), HU-006 (#42), HU-010 (#46), HU-011 (PR #52) y
> HU-012 (PR #49) ya están aplicados y contados en el total actual.

## 7. Reglas

- Toda prueba nueva referencia su AC o FR en el nombre o en el docstring (test-first).
- Sin GPU, dataset completo ni red en las pruebas unitarias.
- **Sin umbral de cobertura:** el requisito de la entrega es un número de pruebas, no
  un porcentaje; la decisión se registró al cerrar HU-012.
- El conteo se actualiza al cerrar cada HU, en el mismo PR (regla de sincronía).
- No se aceptan pruebas triviales ni duplicadas; ver la definición de terminado en
  [`PLAN-PRUEBAS.md`](PLAN-PRUEBAS.md) §6.
