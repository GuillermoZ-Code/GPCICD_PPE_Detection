---
description: "Task list for HU-023 — ADR del modelo productivo"
---

# Tasks: HU-023 — ADR del modelo productivo

**Input**: `specs/024-hu-023-adr-modelo-productivo/spec.md` y `plan.md`.

**Prerequisites**: issue #79, rama `feature/024-hu-023-adr-modelo-productivo`,
HU-019 cerrada.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-023.
- [ ] T002 Mover #79 a **In progress** en el tablero.
- [x] T003 Crear la rama desde `develop`.

## Phase 2: ADR

- [x] T004 Escribir `docs/adr/0009-modelo-productivo.md`.
- [x] T005 Incluir mAP50-95, recall por clase, latencia y tamaño.
- [x] T006 Enlazar HU-019, HU-020 y SPI-03.
- [x] T007 Definir rollback a YOLO11s.
- [x] T008 Añadir el ADR al índice `docs/adr/README.md`.

## Phase 3: Documentos derivados

- [x] T009 Actualizar `docs/model-card.md` al modelo seleccionado.
- [x] T010 Aclarar que el despliegue actual sigue siendo YOLO11s hasta el rollout.
- [x] T011 Actualizar `CONSTITUTION.md` con la decisión y el enlace al ADR.
- [x] T012 Verificar que no se versionan pesos.

## Phase 4: Verificación y cierre

- [x] T013 Ejecutar `make check` (446 passed, 1 skipped).
- [ ] T014 Ejecutar `make ownership-check`.
- [ ] T015 Abrir PR a `develop` con la plantilla UAO y `Closes #79`.
- [ ] T016 Tras el merge, cerrar #79 a mano y moverla a Done.

## Notes

- No se actualiza `models.lock` en esta HU; eso pertenece al rollout.
- El ADR es append-only.
- Model Card y CONSTITUTION distinguen modelo seleccionado vs. desplegado.
