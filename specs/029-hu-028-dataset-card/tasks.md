---
description: "Task list for HU-028 — Dataset Card y atribución CC-BY-4.0"
---

# Tasks: HU-028 — Dataset Card y atribución CC-BY-4.0

**Input**: `specs/029-hu-028-dataset-card/spec.md` y `plan.md`.

**Prerequisites**: issue #84, rama `feature/029-hu-028-dataset-card`,
`develop` actualizado.

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-028.
- [ ] T002 Mover #84 a **In progress** en el tablero.
- [x] T003 Ejecutar `make ownership-check` antes del primer cambio.

## Phase 2: Tests

- [x] T004 [P] `test_dataset_card_has_source_license_and_counts` → AC-01.
- [x] T005 [P] `test_dataset_card_declares_missing_origin_and_consent` → AC-02.
- [x] T006 [P] `test_dataset_card_has_reusable_attribution` → AC-03.
- [x] T007 [P] `test_dataset_card_links_to_evidence` → AC-01.
- [x] T008 Ejecutar `uv run pytest tests/test_dataset_card.py -q`.

## Phase 3: Implementation

- [x] T009 Escribir `docs/dataset/README.md` con identidad, licencia y clases.
- [x] T010 Añadir particiones, limpieza y enlaces al EDA/ADR.
- [x] T011 Añadir limitaciones de fuente, consentimiento y ausencia de `person`/`no-EPP`.
- [x] T012 Añadir bloque de atribución CC-BY-4.0 reutilizable.

## Phase 4: Verification and close

- [x] T013 Ejecutar `make specs-check`.
- [x] T014 Ejecutar `make check`.
- [x] T015 Ejecutar `uv build`.
- [ ] T016 Solicitar a Jesús la actualización de `docs/curso/PRUEBAS.md` con las
  4 pruebas nuevas.
- [ ] T017 Abrir PR a `develop` con la plantilla UAO y `Closes #84`.
- [ ] T018 Tras el merge, cerrar #84 a mano y moverla a Done.

## Notes

- Solo se versiona documentación y pruebas; no se descarga el dataset.
- La ficha no publica imágenes ni recortes.
- La atribución debe conservarse en la SPA y en el README.
