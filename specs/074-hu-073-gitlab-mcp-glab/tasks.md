# Tasks: HU-073 — MCP de GitLab y `glab` autenticado

**Input**: Design documents from `specs/074-hu-073-gitlab-mcp-glab/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/074-hu-073-gitlab-mcp-glab` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #129.

## Phase 2: Pruebas (test-first)

- [x] T003 [AC-01] `tests/test_herramientas_agente.py`: MCP `gitlab` remoto y habilitado.
- [x] T004 [AC-01] `tests/test_herramientas_agente.py`: Engram se conserva.
- [x] T005 [AC-03] `tests/test_herramientas_agente.py`: sin tokens en la configuración.
- [x] T006 [AC-02] `tests/test_herramientas_agente.py`: comandos de verificación en el
      runbook.
- [x] T007 [AC-02] `tests/test_herramientas_agente.py`: nombre canónico y OAuth.

## Phase 3: Implementación

- [x] T008 `opencode.json`: entrada `gitlab` del MCP remoto.
- [x] T009 `docs/operacion/herramientas-agente.md`: CLI, MCP, verificación y diagnóstico.

## Phase 4: Cierre

- [x] T010 `make check` en verde.
- [x] T011 Rama preparada y pusheada sin PR (modo preparación).
