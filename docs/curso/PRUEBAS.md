# Inventario de pruebas — GPCICD PPE Detection

> **Actualizado:** 2026-11-11.
> **Requisito del curso:** **400 pruebas unitarias o más** (≥ 400) para la entrega
> (indicación del docente; no constaba en el repositorio hasta este documento).

## 1. Resumen

| Suite | Herramienta | Archivos | Pruebas | Comando |
|-------|-------------|---------:|--------:|---------|
| Backend Python | pytest | 13 | **154** | `make test` |
| Frontend | Vitest | 5 | **19** | `make frontend-test` |
| **Total** | | **18** | **173** | `make check` + `make frontend-check` |

Dos pruebas se omiten sin hardware o artefactos: `test_real_weights_smoke` (sin
pesos locales) y la de contenedor de HU-011 (sin Docker/imagen/artefacto,
`@pytest.mark.docker`); la corrida muestra **152 passed + 2 skipped**.

> Incluye HU-005 (#39, +7 pruebas), HU-006 (#42, +9), HU-010 (#46, +9) y
> HU-011 (rama, +9 en `tests/test_docker.py`, 8 estáticas + 1 de contenedor).

## 2. Desglose del backend

| Archivo | Pruebas |
|---------|--------:|
| `tests/test_api.py` | 12 |
| `tests/test_calidad.py` | 5 |
| `tests/test_contracts.py` | 28 |
| `tests/test_estado.py` | 10 |
| `tests/test_grpc.py` | 9 |
| `tests/test_docker.py` | 9 |
| `tests/test_image_validation.py` | 7 |
| `tests/test_launcher.py` | 5 |
| `tests/test_overlay.py` | 7 |
| `tests/test_predict.py` | 16 |
| `tests/test_results.py` | 10 |
| `tests/test_smoke.py` | 1 |
| **Total** | **154** |

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
| Actual | **155** |
| Brecha | **245** |

## 6. Ruta propuesta para llegar a 400 o más

| Frente | Pruebas | Enfoque |
|--------|--------:|---------|
| HU-005 (#39) | 7 | ✅ aplicado: validación de imágenes |
| HU-006 (#42) | 9 | ✅ aplicado: API REST |
| HU-008 evaluación | 60 | IoU, mAP, matrices y métricas por clase |
| HU-009 MLflow | 30 | Runs, parámetros, métricas y artefactos |
| HU-010 gRPC (rama) | 9 | ✅ aplicado: contrato, errores y equivalencia con REST |
| HU-011 Docker CPU | 12 | Build, smoke y ejecución sin GPU |
| HU-012 calidad | 25 | Regresiones y contratos |
| HU-013 versión | 20 | Identificación y distinción de versiones |
| Frontend (ampliación) | 35 | Estados, accesibilidad y API real |
| Contratos y geometría parametrizados | 40 | Casos borde por clase y formato |
| **Pendiente** | **248** | → **403 acumuladas** |

> HU-006 y HU-010 aportaron 9 pruebas cada una, por debajo de lo proyectado. La ruta
> está recalculada: los frentes pendientes deben cubrir **248 casos** para superar los
> 400. El requisito se cumple con pruebas que verifican un AC o un FR, no con duplicados.

## 7. Reglas

- Toda prueba nueva referencia su AC o FR en el nombre o en el docstring (test-first).
- Sin GPU, dataset completo ni red en las pruebas unitarias.
- Sin umbral de cobertura hasta HU-012.
- El conteo se actualiza al cerrar cada HU, en el mismo PR (regla de sincronía).
