# M3 — Implementación local

> **Periodo:** 31/10/2026 → 14/11/2026. **Peso:** 25 %.
> **Sustentación:** sábado **14/11/2026**.

## 1. Clases y focos

| Fecha | Tema | Impacto en el repo |
|-------|------|--------------------|
| **05/11** | FastAPI / REST | HU-006: API `/predict`, contrato OpenAPI, validación de entrada |
| **07/11** | MLflow + Streamlit | HU-009: experiment tracking; HU-007: interfaz Streamlit |

## 2. Sprints

### M3-S1 — 31/10 a 07/11 (28 SP)

| HU | Título | SP | Dependencias |
|----|--------|----|--------------|
| HU-001 | Cargar una imagen para su análisis | 3 | TA-04 |
| HU-002 | Detectar las seis categorías de EPP | 8 | SPI-01, SPI-02, TA-02, TA-09 |
| HU-003 | Visualizar las detecciones sobre la imagen | 3 | HU-002 |
| HU-004 | Informar cuando no se detectan EPP | 2 | HU-002 |
| HU-005 | Validar las imágenes recibidas | 2 | HU-001 |
| HU-006 | API REST con FastAPI | 5 | HU-002, HU-005 |
| HU-007 | Interfaz gráfica del detector | 5 | HU-001, 003, 004, 005, 006 |

### M3-S2 — 08/11 a 14/11 (26 SP)

| HU | Título | SP | Dependencias |
|----|--------|----|--------------|
| HU-008 | Evaluar el desempeño del modelo | 5 | HU-002, TA-02 |
| HU-009 | Consultar y comparar experimentos en MLflow | 3 | HU-008 |
| HU-010 | Consumir inferencias mediante gRPC | 5 | HU-006 |
| HU-011 | Ejecutar el sistema en Docker CPU | 5 | HU-006, HU-007, HU-010 |
| HU-012 | Verificaciones automatizadas de calidad | 5 | Contratos de HU-006/007/010 |
| HU-013 | Consultar la versión del modelo | 3 | HU-002, HU-009 |

## 3. Entregables del M3

- Contrato `ImageData → list[Detection]` + `FakeDetector`.
- Detector YOLO con inferencia local en CPU.
- API REST FastAPI y servicio gRPC.
- Interfaz Streamlit.
- MLflow con runs consultables.
- Docker CPU reproducible.
- Suite de pruebas deterministas y `make check` en verde.
- Evidencias y documentación de arquitectura actualizadas.

## 4. Pendiente de validación (Jesús)

- Creación de TA-04, TA-11, SPI-01, TA-02, TA-09, SPI-02 y TA-10.
- Criterio de SP para TA/SPI: desglose dentro de la HU padre o alcance adicional.
- Incoherencia detectada: **HU-002 = 8 SP**, pero sus dependencias
  (SPI-01 + SPI-02 + TA-02 + TA-09) suman **14 SP**.

Ver [`docs/curso/backlog.md`](../backlog.md) para el detalle.
