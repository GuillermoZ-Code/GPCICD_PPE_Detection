---
description: "Task list for HU-102 — Protocolo de Engram y ADR"
---

# Tasks: HU-102 — Protocolo de Engram y ADR

**Input**: `specs/103-hu-102-protocolo-engram/spec.md` y `plan.md`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas.
- [x] T002 Mover #158 a **In progress** en el tablero.
- [x] T003 Crear la rama `feature/103-hu-102-protocolo-engram`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_adr_exists_with_decision` → AC-02.
- [x] T005 [P] `test_adr_says_what_is_stored` → AC-01.
- [x] T006 [P] `test_adr_forbids_secrets_and_personal_data` → AC-01.
- [x] T007 [P] `test_adr_documents_sync_and_export` → AC-01.
- [x] T008 [P] `test_adr_is_subordinate_to_repository` → AC-02.
- [x] T009 [P] `test_agents_links_the_adr` → AC-03.
- [x] T010 [P] `test_adr_index_lists_0011` → AC-02.

## Phase 3: Implementation

- [x] T011 Escribir `docs/adr/0011-memoria-agentes.md`.
- [x] T012 Indexar el ADR y actualizar `AGENTS.md`.
- [x] T013 Ejecutar las pruebas en verde.

## Phase 4: Evidence and close

- [x] T014 Ejecutar `make check` y `make ownership-check`.
- [ ] T015 Abrir PR y cerrar #158 tras el merge.

## Notes

- La memoria es local y subordinada al repositorio.
- No se guardan secretos ni datos personales.
