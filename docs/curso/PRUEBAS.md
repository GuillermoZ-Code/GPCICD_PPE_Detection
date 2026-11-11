# Inventario de pruebas — GPCICD PPE Detection

> **Actualizado:** 2026-11-10.
> **Requisito del curso:** **400 pruebas unitarias o más** (≥ 400) para la entrega
> (indicación del docente; no constaba en el repositorio hasta este documento).

## 1. Resumen

| Suite | Herramienta | Archivos | Pruebas | Comando |
|-------|-------------|---------:|--------:|---------|
| Backend Python | pytest | 11 | **127** | `make test` |
| Frontend | Vitest | 5 | **19** | `make frontend-test` |
| **Total** | | **16** | **146** | `make check` + `make frontend-check` |

Una prueba del backend se omite cuando no hay artefactos locales
(`test_real_weights_smoke`), por eso la corrida muestra **126 passed + 1 skipped**.

> Incluye HU-005 (#39, +7 pruebas) y HU-006 (#42, +9 pruebas).

## 2. Desglose del backend

| Archivo | Pruebas |
|---------|--------:|
| `tests/test_contracts.py` | 28 |
| `tests/test_image_loader.py` | 17 |
| `tests/test_predict.py` | 16 |
| `tests/test_yolo_detector.py` | 15 |
| `tests/test_estado.py` | 10 |
| `tests/test_results.py` | 10 |
| `tests/test_api.py` | 9 |
| `tests/test_image_validation.py` | 7 |
| `tests/test_overlay.py` | 7 |
| `tests/test_training.py` | 7 |
| `tests/test_smoke.py` | 1 |
| **Total** | **127** |

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
| Requisito | **≥ 400** |
| Actual | **146** |
| Brecha | **254** |

## 6. Ruta propuesta para llegar a 400 o más

| Frente | Pruebas | Enfoque |
|--------|--------:|---------|
| HU-005 (#39) | 7 | ✅ aplicado: validación de imágenes |
| HU-006 (#42) | 9 | ✅ aplicado: API REST |
| HU-008 evaluación | 60 | IoU, mAP, matrices y métricas por clase |
| HU-009 MLflow | 30 | Runs, parámetros, métricas y artefactos |
| HU-010 gRPC | 35 | Contrato, errores y equivalencia con REST |
| HU-011 Docker CPU | 12 | Build, smoke y ejecución sin GPU |
| HU-012 calidad | 25 | Regresiones y contratos |
| HU-013 versión | 20 | Identificación y distinción de versiones |
| Frontend (ampliación) | 35 | Estados, accesibilidad y API real |
| Contratos y geometría parametrizados | 40 | Casos borde por clase y formato |
| **Pendiente** | **257** | → **403 acumuladas** |

> HU-006 aportó 9 pruebas, por debajo de las 60 que se habían proyectado. La ruta está
> recalculada: los frentes pendientes deben cubrir **257 casos** para superar los 400.
> El requisito se cumple con pruebas que verifican un AC o un FR, no con duplicados.

## 7. Reglas

- Toda prueba nueva referencia su AC o FR en el nombre o en el docstring (test-first).
- Sin GPU, dataset completo ni red en las pruebas unitarias.
- Sin umbral de cobertura hasta HU-012.
- El conteo se actualiza al cerrar cada HU, en el mismo PR (regla de sincronía).
