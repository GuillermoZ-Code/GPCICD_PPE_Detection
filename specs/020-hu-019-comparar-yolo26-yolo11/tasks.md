---
description: "Task list for HU-019 — Comparación YOLO26 vs YOLO11s"
---

# Tasks: HU-019 — Comparación YOLO26 vs YOLO11s

**Input**: `specs/020-hu-019-comparar-yolo26-yolo11/spec.md` y `plan.md`.

**Prerequisites**: issue #75, rama `feature/020-hu-019-comparar-yolo26-yolo11`,
resúmenes de HU-008 y HU-018.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-019.
- [ ] T002 Mover #75 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: Datos

- [x] T004 Verificar SHA256 de YOLO11s y YOLO26n.
- [x] T005 Confirmar `conf=0.001`, `iou=0.7`, `imgsz=640`, `seed=42`.
- [x] T006 Extraer tablas del eval 492.
- [x] T007 Extraer tablas del test 1.095.
- [x] T008 Comparar latencia ONNX de HU-020.

## Phase 3: Informe

- [x] T009 Escribir `docs/evaluation/YOLO26.md`.
- [x] T010 Incluir análisis de `safety_shoe` y límites del eval 492.
- [x] T011 Emitir recomendación preliminar.
- [x] T012 Documentar comandos de reproducción.
- [x] T013 Verificar que no se versionan pesos ni imágenes.
- [x] T014 Ejecutar `make check` (424 passed, 1 skipped).

## Phase 4: Cierre

- [ ] T015 Ejecutar `make ownership-check`.
- [ ] T016 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md`.
- [ ] T017 Abrir PR a `develop` con la plantilla UAO y `Closes #75`.
- [ ] T018 Tras el merge, cerrar #75 a mano y moverla a Done.

## Notes

- El informe es documental; no modifica modelo ni código de producción.
- El eval 492 se conserva por el AC, pero no se usa solo para decidir.
