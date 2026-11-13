# Inventario de pruebas — GPCICD PPE Detection

> **Actualizado:** 2026-11-12, tras el frente de pruebas de Eliana.
> **Requisito del curso:** **400 pruebas unitarias o más** (≥ 400) para la entrega
> (indicación del docente; no constaba en el repositorio hasta este documento).

## 1. Resumen

| Suite | Herramienta | Archivos | Pruebas | Comando |
|-------|-------------|---------:|--------:|---------|
| Backend Python | pytest | 24 | **279** | `make test` |
| Frontend | Vitest | 9 | **76** | `make frontend-test` |
| **Total** | | **33** | **355** | `make check` + `make frontend-check` |

Dos pruebas se omiten sin hardware o artefactos: `test_real_weights_smoke` (sin
pesos locales) y la de contenedor de HU-011 (sin Docker/imagen/artefacto,
`@pytest.mark.docker`); la corrida muestra **277 passed + 2 skipped**.

> Incluye todas las HU del M3 fusionadas hasta el 12/11/2026: HU-005 (#39),
> HU-006 (#42), HU-007 (SPA), HU-009 (+11 en `test_tracking.py`), HU-010 (#46),
> HU-011 (#52, +9 en `test_docker.py`), HU-012 (+5 en `test_calidad.py`), HU-013
> (+20 en `test_model_version.py`), el plan de Jesús (+25 en
> `test_tracking_mlflow.py` y +10 en `test_estado_tools.py`), el frente de
> Guillermo (+42: 37 de frontend y 5 en `test_overlay_launcher.py`) y el frente
> de Eliana (+40: 15 REST, 12 gRPC y 13 Docker estáticos).

## 2. Desglose del backend

| Archivo | Pruebas |
|---------|--------:|
| `tests/test_api.py` | 12 |
| `tests/test_api_contract.py` | 15 |
| `tests/test_calidad.py` | 5 |
| `tests/test_contracts.py` | 28 |
| `tests/test_docker.py` | 9 |
| `tests/test_docker_assets.py` | 13 |
| `tests/test_estado.py` | 10 |
| `tests/test_evaluation.py` | 9 |
| `tests/test_grpc.py` | 9 |
| `tests/test_grpc_contract.py` | 12 |
| `tests/test_image_loader.py` | 17 |
| `tests/test_image_validation.py` | 7 |
| `tests/test_launcher.py` | 5 |
| `tests/test_model_version.py` | 20 |
| `tests/test_tracking_mlflow.py` | 25 |
| `tests/test_estado_tools.py` | 10 |
| `tests/test_overlay.py` | 7 |
| `tests/test_overlay_launcher.py` | 5 |
| `tests/test_predict.py` | 16 |
| `tests/test_results.py` | 10 |
| `tests/test_smoke.py` | 1 |
| `tests/test_tracking.py` | 11 |
| `tests/test_training.py` | 7 |
| `tests/test_yolo_detector.py` | 16 |
| **Total** | **279** |

## 3. Desglose del frontend

| Archivo | Pruebas |
|---------|--------:|
| `src/App.test.tsx` | 16 |
| `src/api/client.test.ts` | 17 |
| `src/config.test.ts` | 5 |
| `src/download.test.ts` | 3 |
| `src/filter.test.ts` | 3 |
| `src/validate.test.ts` | 14 |
| `src/components/AnnotatedCanvas.test.tsx` | 6 |
| `src/components/DetectionTable.test.tsx` | 7 |
| `src/components/SettingsDrawer.test.tsx` | 5 |
| **Total** | **76** |

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
| Actual | **355** (279 pytest + 76 Vitest) |
| Brecha mínima | **45** |
| Objetivo operativo | **430** (115 nuevas) |

> El requisito es un **mínimo**: superar 400 no es un problema. El objetivo operativo
> del plan es **430** para tener margen de descarte en revisión.

> El frente restante es el de Hernán (+75, PR #58 en revisión): con él, el total
> llegaría a **430**.

## 6. Plan para llegar a 400 o más

El reparto por integrante, los archivos propuestos y los casos concretos viven en
[`PLAN-PRUEBAS.md`](PLAN-PRUEBAS.md). Resumen:

| Integrante | Frente | Nuevas |
|------------|--------|--------|
| Hernán Estrada | Evaluación, métricas, contratos y geometría | 75 |
| Jesús Riveros | MLflow, versión del modelo y trazabilidad | 0 (completado) |
| Eliana Cardona | API REST, gRPC y Docker | 0 (completado, 40) |
| Guillermo Zabala | Frontend, visualización y herramientas | 0 (completado, 42) |
| **Total** | | **115** → **430** |

> Jesús completó sus 55 pruebas, Guillermo sus 42 (37 de frontend y 5 de
> overlay/launcher) y Eliana sus 40 (15 REST, 12 gRPC y 13 Docker estáticos).
> El plan restante es 75 (Hernán); el mínimo de 400 exige al menos 45.

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
