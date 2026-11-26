# Tasks: HU-085 — ADR de GitLab CI/CD, espejo y Droplet

**Input**: Design documents from `specs/086-hu-085-adr-gitlab-droplet/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/086-hu-085-adr-gitlab-droplet` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #141.

## Phase 2: Pruebas (test-first)

- [x] T003 [AC-01] `tests/test_adr_m4.py`: existen el ADR 0007 y el ADR 0008 con su
      decisión.
- [x] T004 [AC-02] `tests/test_adr_m4.py`: registran el descarte de Premium, Render y
      Hugging Face.
- [x] T005 [AC-03] `tests/test_adr_m4.py`: `CONSTITUTION.md` enlaza ambos ADR.
- [x] T006 [AC-03] `tests/test_adr_m4.py`: el índice `docs/adr/README.md` los lista.
- [x] T007 [AC-03] `tests/test_adr_m4.py`: los enlaces apuntan a archivos existentes.

## Phase 3: Documentación

- [x] T008 `docs/adr/0007-gitlab-ci-espejo.md` con contexto, decisión, alternativas y
      consecuencias.
- [x] T009 `docs/adr/0008-droplet-caddy.md` con contexto, decisión, alternativas y
      consecuencias.
- [x] T010 `docs/adr/README.md` y `CONSTITUTION.md` (§7 y §11) actualizados.

## Phase 4: Cierre

- [x] T011 `make check` y `make ownership-check` en verde.
- [x] T012 PR con plantilla UAO, `Closes #141`, revisor de otro integrante.
