# Feature Specification: HU-020 — Benchmark de latencia CPU

**Feature Branch**: `feature/021-hu-020-benchmark-latencia`

**Created**: 2026-11-23

**Status**: Completado

**Input**: Issue #76 — «Benchmark de latencia CPU por resolución y formato». Asignada
a Hernán (`HestradaUAO`), épica `ep-09`, P1, Ola 3, 3 SP. Depende de HU-018.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Elegir resolución y formato (Priority: P1)

Como responsable técnico, quiero medir latencia CPU a 640/480/416 en PyTorch y ONNX,
para decidir `imgsz` y formato frente al objetivo de 100 ms.

**Why this priority**: el modelo YOLO26n es más preciso que YOLO11s, pero la latencia
sigue siendo el riesgo principal. La decisión de producción necesita datos, no
impresiones.

**Independent Test**: ejecutar el benchmark sobre una imagen sintética con los tres
modelos, tres resoluciones y dos formatos; comparar p50/p95 y emitir una
recomendación explícita.

**Acceptance Scenarios** (AC de la issue #76):

1. **AC-01**: **Dados** YOLO11s, YOLO26n y YOLO26s, **Cuando** se miden en CPU,
   **Entonces** hay p50/p95 para 640/480/416 en PyTorch y ONNX.
2. **AC-02**: **Dado** el entorno, **Cuando** se ejecuta el benchmark, **Entonces**
   hardware, hilos, versiones y configuración quedan registrados.
3. **AC-03**: **Dados** los resultados, **Cuando** se cierra el informe, **Entonces**
   hay una recomendación explícita de `imgsz` y formato.

### Edge Cases

- ONNX con entrada fija: Ultralytics reescala; se verifica que las tres resoluciones
  funcionen.
- Modelo `s` sin fine-tuning EPP: se etiqueta como preentrenado COCO y se usa solo
  para latencia, no para calidad.
- Imagen sintética: sirve para latencia, no para mAP.
- Variabilidad del equipo: se reportan p50/p95 y se advierte que no es producción.
- Resolución 416: puede ser más lenta que 480 por overhead; se reporta el dato real.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST medir YOLO11s, YOLO26n y YOLO26s en CPU.
- **FR-002**: MUST medir 640, 480 y 416 en PyTorch y ONNX.
- **FR-003**: MUST usar 5 warm-ups y 20 repeticiones por combinación.
- **FR-004**: MUST registrar Python, Ultralytics, torch, hardware, hilos, `conf` e
  `iou`.
- **FR-005**: MUST reportar p50, media, p95, mínimo y máximo.
- **FR-006**: MUST comparar con el objetivo de 100 ms.
- **FR-007**: MUST recomendar `imgsz` y formato.
- **FR-008**: MUST NOT versionar pesos ni imágenes.

## Acceptance → Evidence

| AC | Evidencia |
|----|-----------|
| AC-01 p50/p95 | Tablas de `docs/evaluation/latencia.md` |
| AC-02 entorno | §2 del informe |
| AC-03 recomendación | §5 del informe |

## Success Criteria *(mandatory)*

- **SC-001**: El informe permite decidir entre 640/480/416.
- **SC-002**: La recomendación distingue PyTorch y ONNX.
- **SC-003**: Se identifica si se cumple <100 ms.
- **SC-004**: No se versionan pesos ni imágenes.

## Out of Scope

- Evaluar mAP o calidad (HU-019).
- Medir la API, gRPC o la SPA.
- Optimizar el modelo o exportar variantes nuevas.
- Cambiar `models.lock` o el modelo productivo.

## Assumptions

- Los pesos de YOLO11s y YOLO26n están fine-tuneados con EPP.
- `yolo26s` no está fine-tuneado; se usa como referencia de arquitectura.
- El hardware es el mismo de SPI-01/SPI-03: i5-1235U, CPU, Windows 11.
- El benchmark mide `model.predict()` completo, no solo el forward.
