---
description: "Task list for HU-020 — Benchmark de latencia CPU"
---

# Tasks: HU-020 — Benchmark de latencia CPU

**Input**: `specs/021-hu-020-benchmark-latencia/spec.md` y `plan.md`.

**Prerequisites**: issue #76, rama `feature/021-hu-020-benchmark-latencia`, modelos de
HU-018.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-020.
- [ ] T002 Mover #76 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: Benchmark

- [x] T004 Verificar modelos y formatos disponibles.
- [x] T005 Exportar YOLO26s preentrenado a ONNX para la comparación de arquitectura.
- [x] T006 Generar imagen sintética y medir 5 warm-ups + 20 repeticiones.
- [x] T007 Medir 640/480/416 en PyTorch y ONNX.
- [x] T008 Registrar hardware, hilos, versiones y configuración.
- [x] T009 Guardar JSON de resultados en `artifacts/eval/latency_yolo26.json`.

## Phase 3: Informe y cierre

- [x] T010 Escribir `docs/evaluation/latencia.md` con tablas p50/p95.
- [x] T011 Emitir recomendación de `imgsz` y formato.
- [x] T012 Verificar que los pesos no aparecen en `git status`.
- [x] T013 Ejecutar `make check` (410 passed, 1 skipped).
- [ ] T014 Abrir PR a `develop` con la plantilla UAO y `Closes #76`.
- [ ] T015 Tras el merge, cerrar #76 a mano y moverla a Done.

## Notes

- Benchmark documental; no se modifica código de producción.
- YOLO26s es preentrenado COCO; se usa solo para latencia.
- El objetivo de 100 ms se evalúa por modelo, resolución y formato.
