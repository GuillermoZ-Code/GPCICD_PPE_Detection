# Tasks: HU-087 — Actualizar CONSTITUTION, AGENTS y README para el M4

**Input**: Design documents from `specs/088-hu-087-docs-m4/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/088-hu-087-docs-m4` desde `develop` actualizado.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #143.
- [x] T003 Verificar el alcance: no tocar `docs/curso/PRUEBAS.md`,
      `docs/curso/backlog.md` ni el bloque generado de `AGENTS.md` §0.

## Phase 2: Pruebas (test-first)

- [x] T004 [AC-01] `test_ac01_constitution_documents_m4_stack_roadmap_and_risks`:
      módulo activo M4, YOLO26n, ONNX, GitLab CI, Droplet, Caddy, ADR 0009, ADR 0013 y
      1.200 pruebas.
- [x] T005 [AC-02] `test_ac02_derived_constitution_is_synced_with_m4`: derivado v1.2
      con el encabezado y el foco M4.
- [x] T006 [AC-03] `test_ac03_internal_links_in_governance_docs_resolve`: enlaces
      internos de CONSTITUTION, AGENTS y README.
- [x] T007 [AC-01] `test_ac01_readme_reflects_the_m4_model_and_deployment`: YOLO26n,
      ONNX, Caddy y URL pública; sin `yolo11s-clean`.

## Phase 3: Documentación

- [x] T008 `CONSTITUTION.md`: módulo activo M4, CI/CD con GitLab/Caddy, ADR 0013 y
      release v1.0.0.
- [x] T009 `.specify/memory/constitution.md` v1.2: stack, roadmap, riesgos y decisiones
      del M4; mínimo de 1.200 pruebas.
- [x] T010 `README.md`: YOLO26n + ONNX, Caddy, URL pública, registry, métricas y
      roadmap.
- [x] T011 `AGENTS.md`: comandos `make deploy` y `make verify`.

## Phase 4: Cierre

- [x] T012 `uv run pytest -q tests/test_docs_m4.py` (4 passed).
- [x] T013 `make check`, `check_specs --check` y `ownership-check` en verde.
- [ ] T014 PR con plantilla UAO, `Closes #143`, revisión de otro integrante.
