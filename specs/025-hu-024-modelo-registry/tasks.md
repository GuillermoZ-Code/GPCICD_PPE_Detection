# Tasks: HU-024 — Modelo en GitLab Generic Packages

**Input**: Design documents from `specs/025-hu-024-modelo-registry/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #80.

## Phase 2: Pruebas

- [x] T002 [AC-01] `models.lock` apunta a `packages/generic/`.
- [x] T003 [AC-02] El SHA256 del manifiesto tiene 64 hex en mayúsculas.
- [x] T004 [AC-02] La versión del manifiesto coincide con la de la URL.
- [x] T005 [AC-03] El pipeline descarga con `JOB-TOKEN` y verifica con `sha256sum -c`.
- [x] T006 [AC-03] El compose monta el artefacto `:ro`.

## Phase 3: Implementación

- [x] T007 Publicar `best.pt` de YOLO26n con `deploy/model/publish.sh`.
- [x] T008 Actualizar `url` en `models.lock` al paquete publicado.
- [x] T009 Verificar el tamaño y el SHA del archivo publicado.

## Phase 4: Verificación

- [ ] T010 `make check` en verde.
- [ ] T011 PR con plantilla UAO, `Closes #80`.
