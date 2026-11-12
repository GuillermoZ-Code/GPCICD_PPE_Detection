# M3 — Implementación local

> **Periodo:** 31/10/2026 → 14/11/2026. **Peso:** 25 %.
> **Sustentación:** sábado **14/11/2026**.

## 1. Clases y focos

| Fecha | Tema | Impacto en el repo |
|-------|------|--------------------|
| **05/11** | FastAPI / REST | HU-006: API `/predict`, contrato OpenAPI, validación de entrada |
| **07/11** | MLflow + Streamlit | HU-009: experiment tracking; HU-007: interfaz web (React) |

## 2. Sprints

### M3-S1 — 31/10 a 07/11 (11 SP)

| HU | Título | SP | Responsable | Dependencias | Estado |
|----|--------|----|-------------|--------------|--------|
| HU-001 | Cargar una imagen para su análisis | 1 | Hernán | TA-04 | ✅ #28 |
| HU-002 | Detectar las seis categorías de EPP | 3 | Hernán | SPI-01, SPI-02, TA-02, TA-09 | ✅ #30 |
| HU-003 | Visualizar las detecciones sobre la imagen | 1 | Guillermo | HU-002 | ✅ #33 |
| HU-004 | Informar cuando no se detectan EPP | 1 | Eliana | HU-002 | ✅ #34 |
| HU-005 | Validar las imágenes recibidas | 1 | Hernán | HU-001 | ✅ #39 |
| HU-006 | API REST con FastAPI | 2 | Hernán | HU-002, HU-005 | ✅ #42 |
| HU-007 | Interfaz gráfica del detector | 2 | Guillermo | HU-001, 003, 004, 005, 006 | ✅ #35 |

### M3-S2 — 08/11 a 14/11 (8 SP)

| HU | Título | SP | Responsable | Dependencias | Estado |
|----|--------|----|-------------|--------------|--------|
| HU-008 | Evaluar el desempeño del modelo | 2 | Jesús | HU-002, TA-02 | ⏳ |
| HU-009 | Consultar y comparar experimentos en MLflow | 1 | Jesús | HU-008 | 🔍 PR #50 (en revisión) |
| HU-010 | Consumir inferencias mediante gRPC | 1 | Eliana | HU-006 | PR #46 (en revisión) |
| HU-011 | Ejecutar el sistema en Docker CPU | 2 | Eliana | HU-006, HU-007, HU-010 | ⏳ |
| HU-012 | Verificaciones automatizadas de calidad | 1 | Hernán | Contratos de HU-006/007/010 | ⏳ |
| HU-013 | Consultar la versión del modelo | 1 | Jesús | HU-002, HU-009 | ⏳ |

## 3. Entregables del M3

- Contrato `ImageData → list[Detection]` + `FakeDetector`.
- Detector YOLO con inferencia local en CPU.
- API REST FastAPI y servicio gRPC.
- SPA React + Vite + TypeScript.
- MLflow con runs consultables.
- Docker CPU reproducible.
- Suite de pruebas deterministas y `make check` en verde.
- Evidencias y documentación de arquitectura actualizadas.
- Runbook de la demo local API + frontend: [`docs/operacion/demo-local.md`](../../operacion/demo-local.md).

## 4. Decisiones de planificación

**Resuelto el 04/11/2026:** la reestimación fijó HU-002 en **3 SP** y absorbió el
trabajo de las TA/SPI en las actividades de preparación P1–P4 (12 SP). Las TA/SPI no se
crean como issues salvo decisión expresa de Jesús; la incoherencia entre HU-002 (8 SP)
y sus dependencias (14 SP) queda cerrada.

Ver [`docs/curso/backlog.md`](../backlog.md) para el detalle.

## 5. Riesgos y decisiones pendientes

| Riesgo / decisión | Responsable sugerido por rol | Acción |
|-------------------|------------------------------|--------|
| **Entrenamiento en CPU no es viable** | Hernán (modelo) | Usar **Colab/Kaggle solo como cómputo GPU**, ejecutando un script versionado del repo con `uv`, sin `.ipynb`. Documentar la excepción en la Model Card. |
| **Python 3.13 + Ultralytics/torch CPU** | Guillermo (entorno/arquitectura) | **Cerrado en SPI-01:** Ultralytics 8.4.195 + torch 2.15.0+cpu cargan e infieren en Python 3.13.7. Ver [`docs/spikes/SPI-01`](../../spikes/SPI-01-compatibilidad-yolo.md). |
| **EDA y descarga del dataset** | Hernán | **Completado:** 12.078 imágenes, 10.941 tras limpieza, SHA256 del ZIP registrado. Ver [`docs/dataset/EDA.md`](../../dataset/EDA.md). |
| **Latencia en CPU** | Hernán (modelo) + Guillermo (entorno) | SPI-01 midió **136–158 ms** a 640 px en un i5-1235U: no cumple el objetivo de <100 ms. Decidir si se acepta el tradeoff o se reduce resolución/ONNX antes de HU-011. |
