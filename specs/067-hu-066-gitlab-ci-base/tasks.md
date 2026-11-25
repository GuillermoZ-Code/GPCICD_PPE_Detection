# Tasks: HU-066 — `.gitlab-ci.yml` base

**Input**: Design documents from `specs/067-hu-066-gitlab-ci-base/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/067-hu-066-gitlab-ci-base` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #122.

## Phase 2: Pruebas (test-first)

- [x] T003 [AC-01] `tests/test_gitlab_ci.py`: etapas en orden.
- [x] T004 [AC-01] `tests/test_gitlab_ci.py`: caché de `uv` y de `npm`.
- [x] T005 [AC-01] `tests/test_gitlab_ci.py`: `uv sync --frozen`, Ruff, `ty` y pytest.
- [x] T006 [AC-02] `tests/test_gitlab_ci.py`: `workflow.rules` cubre MR, ramas y manual.
- [x] T007 [AC-02] `tests/test_gitlab_ci.py`: calidad y frontend sin reglas restrictivas.
- [x] T008 [AC-02] `tests/test_gitlab_ci.py`: build y deploy solo en `main`.
- [x] T009 [AC-02] `tests/test_gitlab_ci.py`: deploy manual y pendiente de HU-070.
- [x] T010 [AC-03] `tests/test_gitlab_ci.py`: sin `pip`, sin `requirements.txt`, sin
      tokens.
- [x] T011 [AC-03] `tests/test_gitlab_ci.py`: el runbook documenta `glab ci lint`.

## Phase 3: Implementación

- [x] T012 `.gitlab-ci.yml` con las cuatro etapas y las reglas.
- [x] T013 `docs/operacion/gitlab-ci.md` con etapas, cachés, reglas y diagnóstico.

## Phase 4: Cierre

- [x] T014 `make check` en verde.
- [x] T015 Rama preparada y pusheada sin PR (modo preparación).
