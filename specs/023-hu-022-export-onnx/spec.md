# Feature Specification: HU-022 — Exportación ONNX y backend opcional

**Feature Branch**: `feature/023-hu-022-export-onnx`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #78 — «Exportación ONNX y backend de inferencia opcional». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P2, Ola 3, 5 SP, 16 pruebas objetivo. Depende de
HU-020, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Elegir backend sin cambiar el código (Priority: P2)

Como responsable técnico, quiero exportar el modelo a ONNX e inferir con él, para
reducir la latencia en CPU si el benchmark lo justifica.

**Why this priority**: el benchmark de HU-020 demostró que YOLO26n ONNX 640 cumple
<100 ms y PyTorch no. Falta un mecanismo reproducible para exportar y seleccionar el
backend por configuración.

**Independent Test**: resolver la ruta del backend con `PPE_MODEL_FORMAT=onnx`,
exportar un `.pt` a `.onnx` con un exportador simulado y verificar el manifiesto con
`opset` e `imgsz`.

**Acceptance Scenarios** (AC de la issue #78):

1. **AC-01**: **Dado** un checkpoint, **Cuando** se exporta, **Entonces** se registran
   `opset` e `imgsz` y se produce un `.onnx`.
2. **AC-02**: **Dados** PyTorch y ONNX, **Cuando** se comparan detecciones,
   **Entonces** coinciden dentro de una tolerancia documentada.
3. **AC-03**: **Dado** `PPE_MODEL_FORMAT`, **Cuando** se construye el detector,
   **Entonces** se elige el artefacto `.pt` o `.onnx`.

### Edge Cases

- `PPE_MODEL_FORMAT` ausente: se usa PyTorch (`.pt`).
- Formato desconocido: error explícito.
- `.onnx` ausente: error explícito, sin fallback silencioso.
- Ruta ya `.onnx`: se respeta.
- Exportación sin `onnx`/`onnxslim`: error con instrucciones.
- Comparación de detecciones con cajas o confianza fuera de tolerancia: se reporta.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `resolve_backend_path()` MUST elegir `.pt` o `.onnx` según
  `PPE_MODEL_FORMAT`.
- **FR-002**: `export_onnx()` MUST aceptar `opset` e `imgsz` y escribir un manifiesto
  JSON con hashes, versión y configuración.
- **FR-003**: `build_detector()` MUST usar `resolve_backend_path()` cuando
  `PPE_MODEL_FORMAT` esté definido.
- **FR-004**: MUST comparar detecciones con tolerancia documentada.
- **FR-005**: MUST NOT agregar dependencias obligatorias; `onnx`/`onnxruntime` son
  opcionales y se validan al usar.
- **FR-006**: Los tests MUST usar archivos temporales y un exportador simulado.
- **FR-007**: No se versionan pesos ni ONNX.

## Acceptance → Evidence

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Exportación | `test_export_onnx_writes_manifest` |
| AC-02 Paridad | `test_compare_detections_within_tolerance` |
| AC-03 Backend | `test_resolve_backend_prefers_onnx`, `test_build_detector_uses_onnx` |

## Success Criteria *(mandatory)*

- **SC-001**: `PPE_MODEL_FORMAT=onnx` usa el `.onnx` correcto.
- **SC-002**: El manifiesto de exportación es reproducible.
- **SC-003**: La comparación reporta una tolerancia explícita.
- **SC-004**: `make check` pasa sin GPU ni red.

## Out of Scope

- Entrenar o evaluar de nuevo.
- Cambiar `models.lock` o el modelo productivo.
- Instalar dependencias en el paquete base.
- Optimizar el grafo ONNX.

## Assumptions

- El `.onnx` se exporta con Ultralytics `opset=17`, `imgsz=640`, `dynamic=False`.
- `onnxruntime` se instala en el entorno de inferencia, no en el paquete base.
- La tolerancia de comparación es de 1e-4 en confianza y 1e-3 en coordenadas.
