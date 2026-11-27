# Tasks: HU-068 — Publicar imágenes en GitLab Registry y Docker Hub

**Input**: Design documents from `specs/069-hu-068-registry/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #124.

## Phase 2: Pruebas (test-first)

- [x] T002 [AC-01] El login al registry usa `CI_JOB_TOKEN` y `CI_REGISTRY_USER`.
- [x] T003 [AC-01] El push va a `$CI_REGISTRY_IMAGE/api` y `$CI_REGISTRY_IMAGE/web`.
- [x] T004 [AC-02] El espejo de Docker Hub depende de `DOCKERHUB_USER` y
      `DOCKERHUB_TOKEN`.
- [x] T005 [AC-02] No hay contraseñas literales en el archivo.
- [x] T006 [AC-03] Los digests se escriben y se publican como artefactos.

## Phase 3: Implementación

- [x] T007 Login con `--password-stdin` y salida silenciada.
- [x] T008 Push de `api` y `web` con SHA corto y `latest`.
- [x] T009 Bloque condicional de Docker Hub con `if [ -n ... ]`.

## Phase 4: Verificación

- [x] T010 `glab ci lint` valida el archivo.
- [ ] T011 `make check` en verde.
- [ ] T012 PR con plantilla UAO, `Closes #124`, revisor de otro integrante.
