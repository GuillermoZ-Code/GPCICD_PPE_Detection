---
description: "Task list for HU-018 — Entrenar YOLO26n y YOLO26s"
---

# Tasks: HU-018 — Entrenar YOLO26n y YOLO26s

**Input**: `specs/019-hu-018-entrenar-yolo26/spec.md` y `plan.md`.

**Prerequisites**: issue #74, rama `feature/019-hu-018-entrenar-yolo26`, spike #173.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-018.
- [ ] T002 Mover #74 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: Run YOLO26n

- [x] T004 Verificar dataset, `data_colab.yaml` y `data_eval_colab.yaml`.
- [x] T005 Entrenar `yolo26n.pt` con 100 épocas, `imgsz=640`, `seed=42`.
- [x] T006 Guardar backup y run completo fuera de Git.
- [x] T007 Verificar SHA256 de `best.pt` contra `run_manifest.json`.
- [x] T008 Verificar que el modelo carga y tiene las 6 clases EPP.
- [x] T009 Recolectar `eval/summary.json`, curvas y `results.csv`.

## Phase 3: Run YOLO26s

- [x] T010 Decidir si se entrena YOLO26s con la evidencia de latencia.
- [ ] T011 Si se decide, ejecutar el mismo pipeline con `yolo26s.pt`.
- [x] T012 Si no se ejecuta, documentar la decisión y dejar el AC pendiente.

## Phase 4: Informe y cierre

- [x] T013 Escribir `docs/evaluation/yolo26-training.md` con el run de `n`.
- [ ] T014 Actualizar el informe con el run de `s`, si se ejecuta.
- [x] T015 Ejecutar `make check` (410 passed, 1 skipped).
- [ ] T016 Abrir PR a `develop` con la plantilla UAO y `Closes #74`.
- [ ] T017 Tras el merge, cerrar #74 o dejarla parcial con aprobación de Jesús.

## Notes

- Los pesos están en `artifacts/models/yolo26n_clean/weights/` y no se versionan.
- `raw/args.yaml` y `raw/results.csv` no coinciden con el manifiesto; se conservan y
  se advierte en el informe.
- `safety_shoe` tiene recall 0; no se debe ocultar en el promedio.
