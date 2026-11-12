# Plan de pruebas — llegar a ≥ 400 en la entrega del M3

> **Requisito del curso:** **mínimo 400 pruebas unitarias**. No es un techo: el
> objetivo operativo es **430**, para tener margen si alguna prueba se descarta en
> revisión.
>
> **Para qué sirve este archivo:** cada integrante (y la IA que lo asiste) lee su
> sección, crea las pruebas que le corresponden, actualiza el conteo y lo demuestra en
> su PR. No se reparte por “escribir muchas pruebas”, sino por **AC y FR sin cubrir**.

## 1. Punto de partida (12/11/2026)

| Suite | Herramienta | Archivos | Pruebas |
|-------|-------------|---------:|--------:|
| Backend Python | pytest | 20 | **234** |
| Frontend | Vitest | 8 | **39** |
| **Total** | | **28** | **273** |

Brecha contra el mínimo: **127**. Brecha contra el objetivo operativo (430): **157**.

Comando de conteo:

```bash
# Backend: casos recogidos (cada parametrización cuenta)
uv run pytest --collect-only -q

# Frontend: total que informa Vitest
cd frontend && npm run test
```

## 2. Reglas del plan

- **Test-first:** la prueba se escribe antes de la implementación y referencia su AC o
  FR en el nombre o en el docstring (`AC-008.2`, `FR-013.1`, etc.).
- **Sin GPU, sin dataset completo y sin red.** Se usan `FakeDetector`, arrays
  sintéticos y `tmp_path`.
- **Sin duplicados.** Una prueba debe verificar comportamiento, no repetir otra con
  otro nombre. Prohibido `assert True`, comparar una constante consigo misma o
  “probar” que un mock devuelve lo que se le configuró sin pasar por el código real.
- **Patrón AAA** (*Arrange · Act · Assert*) y nombres descriptivos en inglés.
- **Cada PR actualiza** `docs/curso/PRUEBAS.md` con el conteo antes/después.
- **Cierre de una HU:** su PR no se aprueba si el frente de pruebas asignado no está
  cubierto o si el conteo baja.

## 3. Reparto por integrante

| Integrante | Frente principal | Nuevas |
|------------|------------------|-------:|
| **Hernán Estrada** | Evaluación, métricas, contratos y geometría | **75** |
| **Jesús Riveros** | MLflow, versión del modelo y trazabilidad | **0 (completado)** |
| **Eliana Cardona** | API REST, gRPC y Docker | **40** |
| **Guillermo Zabala** | Frontend, visualización y herramientas | **42** |
| **Total** | | **157** → **430** |

> Jesús completó sus 55 pruebas: 20 de HU-013 (`test_model_version.py`) y 35 de
> tracking/estado (`test_tracking_mlflow.py` y `test_estado_tools.py`). El plan
> restante es 157; el mínimo de 400 exige 127.

## 4. Frentes y casos concretos

### 4.1 Hernán — 75 pruebas

| Archivo propuesto | Casos | Qué debe cubrir | AC/FR |
|-------------------|------:|-----------------|-------|
| `tests/test_metrics.py` | 35 | IoU (idénticas, disjuntas, borde, anidadas, área cero, `float32` vs `float64`); emparejamiento por clase; AP con 1 y varios puntos; mAP@0.5 y @0.5:0.95; precisión/recall/F1 por clase; listas vacías de predicción y de ground truth; cajas fuera de rango | AC-008.1, AC-008.2 |
| `tests/test_evaluation_report.py` | 10 | Configuración y partición registradas; reproducibilidad con la misma semilla; CSV/JSON con las seis clases; partición de test protegida; modelo y SHA256 en el manifiesto | AC-008.1, AC-008.4 |
| `tests/test_geometry.py` | 20 | `xyxy` ↔ `xywh`; escalado letterbox; recorte a límites; cajas degeneradas; tipos y formas inválidas; seis clases parametrizadas | AC-003.2, contrato `Detection` |
| `tests/test_io_edge_cases.py` | 10 | Grayscale, RGBA, EXIF rotado, archivo truncado, MIME falso, tamaño límite, nombre con espacios, `Path` vs `bytes` | AC-005.1, AC-005.3 |

**Cómo lo ejecuta su IA:** crear los archivos, correr
`uv run pytest tests/test_metrics.py -q` y luego `make check`; actualizar
`docs/curso/PRUEBAS.md`; PR `test(eval): ampliar la suite de evaluación y geometría`.

### 4.2 Jesús — 0 pruebas restantes (frente completo)

| Archivo propuesto | Casos | Qué debe cubrir | AC/FR |
|-------------------|------:|-----------------|-------|
| `tests/test_tracking_mlflow.py` | **25 (hecho)** | Run con parámetros, métricas y referencia al artefacto; dos runs distinguibles; comparación ordenada; fallback sin MLflow instalado; `mlruns/` fuera de Git; SHA256 del modelo; errores de conexión controlados | AC-009.1, AC-009.2, AC-009.3 |
| `tests/test_model_version.py` | **20 (hecho)** | Identificador verificable por inferencia; dos versiones distintas se distinguen; artefacto externo referenciado; versión en la respuesta REST y gRPC; versión ausente → error controlado; hash y ruta configurable | AC-013.1, AC-013.2, AC-013.3 |
| `tests/test_estado_tools.py` | **10 (hecho)** | Parser de SP, issues por milestone, rama y PRs, `--write` con y sin `gh`, bloque generado idempotente | FR de `tools/estado.py` |

**Dependencia:** frente completo; no quedan pruebas de Jesús en el plan.

### 4.3 Eliana — 40 pruebas

| Archivo propuesto | Casos | Qué debe cubrir | AC/FR |
|-------------------|------:|-----------------|-------|
| `tests/test_api_contract.py` | 15 | Esquema OpenAPI; `conf` por petición fuera de rango; imagen inválida → 4xx sin caída; sin detecciones → 200 con mensaje; CORS; límite de tamaño; detector inyectado | AC-006.1, AC-006.2, AC-006.3, AC-004.1 |
| `tests/test_grpc_contract.py` | 12 | Contrato `ppe.v1`; seis clases; error definido para bytes inválidos; servidor sigue disponible; equivalencia semántica REST/gRPC; metadatos de versión | AC-010.1, AC-010.2, AC-010.3 |
| `tests/test_docker_assets.py` | 13 | `Dockerfile` multietapa; usuario no root; `uv sync --frozen`; `.dockerignore` excluye pesos y `.venv`; `compose.yml` monta el modelo `:ro`; `PPE_SERVICES`; healthcheck; nginx sirve la SPA | AC-011.1, AC-011.3, AC-011.4 |

**Nota:** la prueba de contenedor real sigue marcada `@pytest.mark.docker` y no cuenta
para las 400 si el entorno no tiene Docker; las 13 propuestas son estáticas.

### 4.4 Guillermo — 42 pruebas

| Archivo propuesto | Casos | Qué debe cubrir | AC/FR |
|-------------------|------:|-----------------|-------|
| `frontend/src/api/client.test.ts` | 10 | Multipart, `conf`, errores HTTP, timeout, respuesta vacía, tipos de detección, cliente simulado | AC-007.1, AC-007.4 |
| `frontend/src/validate.test.ts` | 5 | JPEG/PNG/JFIF, tamaño, vacío, MIME falso, extensión vs contenido | AC-005.1, AC-005.2 |
| `frontend/src/App.test.tsx` | 8 | Estados cargando/error/vacío/resultado; reintento; mensaje sin EPP; cambio de tema | AC-007.1, AC-007.3, AC-007.4 |
| `frontend/src/components/AnnotatedCanvas.test.tsx` | 4 | Escalado proporcional, sin detecciones, cajas fuera de límites, DPR | AC-003.2, AC-003.3 |
| `frontend/src/components/DetectionTable.test.tsx` | 4 | Orden por confianza, confianza formateada, seis clases, vacío | AC-007.2 |
| `frontend/src/components/SettingsPanel.test.tsx` | 5 | Tema claro/oscuro/sistema, umbral válido e inválido, persistencia | FR de configuración |
| `tests/test_overlay_launcher.py` | 6 | Etiquetas en español, color por clase, imagen sin cajas, argumentos del launcher | AC-003.1 |

## 5. Calendario de la entrega

| Fecha | Hito |
|-------|------|
| **12/11** | HU-013 + 35 de tracking/estado completadas (+55 de Jesús); cada integrante abre su rama `test/*` |
| **13/11** | Cada frente en verde y `PRUEBAS.md` actualizado; PRs a `develop` |
| **14/11 (mañana)** | `make calidad` + `make frontend-check`; conteo final ≥ 400; release del M3 |
| **14/11 (sustentación)** | Evidencia del conteo y de la suite en verde |

## 6. Definición de terminado

- [ ] `uv run pytest --collect-only -q` + Vitest suman **≥ 400**.
- [ ] `make check` y `make frontend-check` en verde, sin pruebas rojas.
- [ ] Cada prueba nueva referencia un AC o FR.
- [ ] `docs/curso/PRUEBAS.md` refleja el conteo final y el desglose por archivo.
- [ ] No hay pruebas triviales, duplicadas ni dependientes de red, GPU o dataset.

## 7. Instrucción para las IA de cada integrante

1. Lee este archivo y ubica la sección de tu integrante.
2. Abre una rama `test/<frente>` desde `develop` y escribe **primero** las pruebas.
3. Ejecuta solo tu archivo, luego `make check` (y `make frontend-check` si aplica).
4. Actualiza `docs/curso/PRUEBAS.md` con el conteo antes/después.
5. Abre la PR a `develop` con la plantilla UAO y evidencia del conteo.
6. Si un caso no se puede probar sin GPU, red o dataset, **no lo inventes**: sustitúyelo
   por uno equivalente con `FakeDetector` o datos sintéticos y anótalo en la PR.
