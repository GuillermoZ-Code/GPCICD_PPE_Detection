# Tasks: HU-066 — `.gitlab-ci.yml` base

**Input**: Design documents from `specs/067-hu-066-gitlab-ci/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/067-hu-066-gitlab-ci` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #122.

## Phase 2: Pruebas (test-first)

- [x] T003 [AC-01] El archivo declara los stages `quality`, `test` y `package` en orden.
- [x] T004 [AC-01] El cache de uv usa `pyproject.toml` y `uv.lock` como clave.
- [x] T005 [AC-01] El cache de npm usa `frontend/package-lock.json` como clave.
- [x] T006 [AC-02] Los jobs de calidad corren en ramas y en merge requests.
- [x] T007 [AC-02] `build_image` corre solo en la rama por defecto o de forma manual.
- [x] T008 [AC-02] El pipeline declara `auto_cancel` y jobs `interruptible`.
- [x] T009 [AC-03] El archivo no usa `only:`/`except:` y respeta `UV_FROZEN`.
- [x] T010 [AC-03] El job de pruebas publica `report.xml` como reporte JUnit.

## Phase 3: Implementación

- [x] T011 `.gitlab-ci.yml` con la imagen de uv, `workflow.rules` y `default.cache`.
- [x] T012 Jobs `lint`, `types`, `specs`, `test` y `frontend`.
- [x] T013 Instalación de librerías de sistema para OpenCV en el job de pruebas.

## Phase 4: Verificación

- [x] T014 `glab ci lint` valida el archivo.
- [ ] T015 `make check` en verde.
- [ ] T016 PR con plantilla UAO, `Closes #122`, revisor de otro integrante.
