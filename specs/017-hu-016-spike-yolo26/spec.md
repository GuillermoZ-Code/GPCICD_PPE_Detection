# Feature Specification: HU-016 — Spike de compatibilidad de YOLO26

**Feature Branch**: `feature/017-hu-016-spike-yolo26`

**Created**: 2026-11-21

**Status**: Completado

**Input**: Issue #72 — «Spike: compatibilidad de YOLO26 con el entorno CPU». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P0, Ola 2, 2 SP. No tiene dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decidir si YOLO26 es viable (Priority: P0)

Como evaluador técnico, quiero confirmar que YOLO26 carga e infiere con Ultralytics,
torch CPU y Python 3.13, para decidir si la migración es viable sin romper el entorno
ni el despliegue actual.

**Why this priority**: YOLO26 es la apuesta de mejora del modelo; si no carga, no
infiere o no mejora la latencia, la cadena HU-017 a HU-023 no debe consumir tiempo del
M4. El modelo actual YOLO11s sigue siendo el fallback.

**Independent Test**: cargar `yolo26n.pt` y `yolo26s.pt`, ejecutar inferencia CPU
sobre una imagen sintética y comparar versiones, latencia, número de parámetros y
forma de salida con el `best.pt` de YOLO11s.

**Acceptance Scenarios** (AC de la issue #72):

1. **AC-01**: **Dados** `yolo26n.pt` y `yolo26s.pt`, **Cuando** se cargan en CPU,
   **Entonces** ambos infieren sobre una imagen de muestra sin error.
2. **AC-02**: **Dado** el entorno de ejecución, **Cuando** se ejecuta el spike,
   **Entonces** se documentan versiones de Ultralytics/torch, latencia p50/p95 y
   diferencias de salida frente a YOLO11s.
3. **AC-03**: **Dados** los resultados, **Cuando** se cierra el spike, **Entonces**
   existe una conclusión go/no-go en `docs/spikes/SPI-03-yolo26.md`.

### Edge Cases

- Peso no disponible o descarga fallida: se documenta como no-go de entorno.
- Clases COCO (80) frente a las 6 clases EPP: no se comparan clases; se compara el
  contrato de salida y la latencia.
- Imagen sintética sin objetos EPP: sirve para compatibilidad y latencia, no para
  calidad.
- CPU compartida o con carga: la latencia se reporta como orden de magnitud y se
  repite si hay outliers.
- `torch` CPU sin GPU: no se usan CUDA ni drivers.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El spike MUST ejecutarse con Python 3.13, torch CPU y Ultralytics
  instalado por `uv`.
- **FR-002**: MUST cargar e inferir con `yolo26n.pt` y `yolo26s.pt`.
- **FR-003**: MUST medir latencia p50/p95 con warm-up y al menos 20 repeticiones.
- **FR-004**: MUST comparar parámetros, número de clases y forma de salida con el
  `best.pt` de YOLO11s.
- **FR-005**: MUST documentar el hardware, las versiones y los SHA256 de los pesos
  usados.
- **FR-006**: MUST concluir go/no-go para la cadena YOLO26 y registrar el fallback.
- **FR-007**: MUST NOT versionar pesos ni imágenes; los pesos quedan fuera de Git.

## Acceptance → Evidence

| AC | Evidencia |
|----|-----------|
| AC-01 Carga e inferencia | Tabla de SPI-03 y comando de ejecución |
| AC-02 Versiones, latencia y salida | SPI-03 §3 y §4 |
| AC-03 Go/no-go | SPI-03 §5 |

## Success Criteria *(mandatory)*

- **SC-001**: El informe se reproduce con un comando documentado.
- **SC-002**: La decisión go/no-go es explícita y tiene fallback.
- **SC-003**: No se versionan pesos ni imágenes.
- **SC-004**: La conclusión permite decidir si se abren HU-017/018/019.

## Out of Scope

- Entrenar YOLO26 con el dataset EPP.
- Evaluar mAP o calidad por clase.
- Exportar a ONNX o cambiar el detector.
- Modificar `Dockerfile`, `compose.yml` o dependencias del proyecto.

## Assumptions

- Los pesos preentrenados COCO de YOLO26 son suficientes para probar compatibilidad y
  latencia; la calidad EPP requiere fine-tuning.
- El hardware de referencia es el mismo equipo de SPI-01: Intel Core i5-1235U, CPU,
  Windows 11.
- La imagen sintética es solo una entrada reproducible; no representa el dataset.
