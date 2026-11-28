# Tasks: HU-074 — Instalar skills de GitLab y frontend-design

**Input**: Design documents from `specs/075-hu-074-skills-repo/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/075-hu-074-skills-repo` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #130.

## Phase 2: Instalación de skills

- [x] T003 [AC-01] Instalar la skill oficial `glab` en `.agents/skills/` con
      `glab skills install`.
- [x] T004 [AC-01] Copiar `frontend-design` con su `LICENSE.txt` a `.agents/skills/`.

## Phase 3: Pruebas (test-first)

- [x] T005 [AC-01] `tests/test_skills_repo.py`: la skill `glab` está versionada.
- [x] T006 [AC-01] `tests/test_skills_repo.py`: `frontend-design` y su licencia están
      versionadas.
- [x] T007 [AC-02] `tests/test_skills_repo.py`: la tabla de `AGENTS.md` lista ambas
      skills y remite a `.agents/skills/`.
- [x] T008 [AC-03] `tests/test_skills_repo.py`: cada `SKILL.md` expone `name` y
      `description`.
- [x] T009 [AC-03] `tests/test_skills_repo.py`: el README documenta origen y
      actualización.
- [x] T010 [AC-03] `tests/test_skills_repo.py`: las skills de usuario no se duplican.

## Phase 4: Documentación

- [x] T011 [AC-02] Actualizar la tabla de skills de `AGENTS.md`.
- [x] T012 [AC-03] Escribir `.agents/skills/README.md` con origen, licencia, alcance y
      comandos de actualización.

## Phase 5: Cierre

- [x] T013 `make check` y `make ownership-check` en verde.
- [x] T014 PR con plantilla UAO, `Closes #130`, revisor de otro integrante.
