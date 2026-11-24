---
description: "Task list for HU-101 — Engram: memoria persistente para los agentes"
---

# Tasks: HU-101 — Engram: memoria persistente para los agentes

**Input**: `specs/102-hu-101-engram/spec.md` y `plan.md`.

**Prerequisites**: issue #157, rama `feature/102-hu-101-engram`.

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Crear la spec, el plan y las tareas de HU-101.
- [x] T002 Mover #157 a **In progress** en el tablero (WIP 1).
- [x] T003 Crear la rama `feature/102-hu-101-engram` desde `develop`.

## Phase 2: Tests first (deben fallar)

- [x] T004 [P] `test_opencode_json_is_valid_json` → AC-01.
- [x] T005 [P] `test_opencode_declares_engram_mcp` → AC-01.
- [x] T006 [P] `test_opencode_engram_is_enabled` → AC-01.
- [x] T007 [P] `test_runbook_documents_installation` → AC-01.
- [x] T008 [P] `test_runbook_documents_how_to_disable` → AC-01.
- [x] T009 [P] `test_runbook_documents_save_and_search` → AC-02.
- [x] T010 [P] `test_runbook_documents_local_database` → AC-03.
- [x] T011 [P] `test_gitignore_covers_engram_database` → AC-03.
- [x] T012 Ejecutar `uv run pytest tests/test_engram_config.py` y confirmar rojo.
      *(1 fallo: `opencode.json` no declaraba el MCP; el runbook no existía.)*

## Phase 3: Implementation

- [x] T013 Añadir `mcp.engram` a `opencode.json`.
- [x] T014 Escribir `docs/operacion/engram.md`.
- [x] T015 Enlazar la spec 102 en `docs/curso/backlog.md`.

## Phase 4: Evidence and close

- [x] T016 Ejecutar `make check`.
- [x] T017 Ejecutar `make ownership-check`.
- [ ] T018 Abrir PR a `develop` con la plantilla UAO y `Closes #157`.
- [ ] T019 Tras el merge, cerrar #157 a mano y moverla a Done.

## Notes

- La ruta del binario es `engram` (PATH), no una ruta absoluta de una máquina.
- La base vive en `~/.engram/engram.db` y `.gitignore` ya cubre `*.db` y `*.sqlite`.
- `opencode.json` es de Guillermo y `docs/operacion/` de Eliana: aviso, no bloqueo.
