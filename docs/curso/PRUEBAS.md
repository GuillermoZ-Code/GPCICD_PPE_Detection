# Inventario de pruebas — GPCICD PPE Detection

> **Actualizado:** 2026-11-12.
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
> HU-011 (#52, +9 en `tests/test_docker.py`: 8 estáticas + 1 de contenedor).

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
| Actual | **173** (154 pytest + 19 Vitest) |
| Brecha | **227** |

> El requisito es un **mínimo**: superar 400 no es un problema. El objetivo operativo
> del plan es **430** para tener margen de descarte en revisión.

## 6. Plan para llegar a 400 o más

El reparto por integrante, los archivos propuestos y los casos concretos viven en
[`PLAN-PRUEBAS.md`](PLAN-PRUEBAS.md). Resumen:

| Integrante | Frente | Nuevas | Total |
|------------|--------|-------:|------:|
| Hernán Estrada | Evaluación, métricas, contratos y geometría | 90 | 110 |
| Jesús Riveros | MLflow, versión del modelo y trazabilidad | 65 | 82 |
| Eliana Cardona | API REST, gRPC y Docker | 50 | 69 |
| Guillermo Zabala | Frontend, visualización y herramientas | 52 | 73 |
| **Total** | | **257** | **430** |

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
