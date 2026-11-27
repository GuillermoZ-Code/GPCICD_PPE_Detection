# Tasks: HU-067 — Job `build_image` con Docker-in-Docker

**Input**: Design documents from `specs/068-hu-067-build-image/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #123.

## Phase 2: Pruebas (test-first)

- [x] T002 [AC-01] El job usa `docker:29.10.0-cli` y `docker:29.10.0-dind`.
- [x] T003 [AC-01] El job construye los targets `runtime` y `web`.
- [x] T004 [AC-01] El job usa `--cache-from` y `BUILDKIT_INLINE_CACHE`.
- [x] T005 [AC-02] Las imágenes llevan `$CI_COMMIT_SHORT_SHA` y `latest`.
- [x] T006 [AC-03] El `Dockerfile` no copia pesos y el compose los monta `:ro`.
- [x] T007 [AC-03] El job corre el smoke de importación antes de publicar.

## Phase 3: Implementación

- [x] T008 Job `build_image` con `needs` de las compuertas de calidad.
- [x] T009 Regla de rama por defecto y ejecución manual.
- [x] T010 Cache deshabilitado en el job (no usa uv).

## Phase 4: Verificación

- [x] T011 `glab ci lint` valida el archivo.
- [ ] T012 `make check` en verde.
- [ ] T013 PR con plantilla UAO, `Closes #123`, revisor de otro integrante.
