---
description: "Task list for HU-016 — Spike de compatibilidad de YOLO26"
---

# Tasks: HU-016 — Spike de compatibilidad de YOLO26

**Input**: `specs/017-hu-016-spike-yolo26/spec.md` y `plan.md`.

**Prerequisites**: issue #72, rama `feature/017-hu-016-spike-yolo26`, `develop`
actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-016.
- [ ] T002 Mover #72 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: Ejecución del spike

- [x] T004 Descargar `yolo26n.pt` y `yolo26s.pt` fuera de Git.
- [x] T005 Confirmar Python 3.13.7, Ultralytics 8.4.202 y torch 2.15.0+cpu.
- [x] T006 Generar la imagen sintética y ejecutar 5 warm-ups + 20 inferencias.
- [x] T007 Medir p50/p95, parámetros, clases y cajas de cada modelo.
- [x] T008 Comparar con `best.pt` de YOLO11s.
- [x] T009 Calcular SHA256 y tamaño de los pesos descargados.

## Phase 3: Informe y cierre

- [x] T010 Escribir `docs/spikes/SPI-03-yolo26.md` con método, resultados y go/no-go.
- [x] T011 Verificar que los pesos no aparecen en `git status`.
- [x] T012 Ejecutar `make check` (391 passed, 1 skipped).
- [ ] T013 Abrir PR a `develop` con la plantilla UAO y `Closes #72`.
- [ ] T014 Tras el merge, cerrar #72 a mano y moverla a Done.

## Notes

- Spike documental: no se modifica código de producción.
- La comparación de calidad EPP queda para HU-017/018/019; este spike solo decide
  compatibilidad y latencia.
- Los pesos se descargan en la raíz pero están ignorados por Git; se eliminan o se
  mueven fuera del árbol al cerrar.
