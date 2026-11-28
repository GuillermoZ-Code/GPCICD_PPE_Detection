# Tasks: HU-043 — Escaneo de secretos con gitleaks

**Input**: Design documents from `specs/044-hu-043-gitleaks/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #99.

## Phase 2: Pruebas

- [x] T002 [AC-01] La configuración hereda las reglas por defecto.
- [x] T003 [AC-01] Las exclusiones son explícitas y acotadas.
- [x] T004 [AC-02] El job existe, corre en push y PR y pide `contents: read`.
- [x] T005 [AC-02] El checkout es completo (`fetch-depth: 0`).
- [x] T006 [AC-03] `make secrets` ejecuta el mismo escaneo.
- [x] T007 [AC-03] Ningún archivo versionado tiene tokens con formato conocido.

## Phase 3: Implementación

- [x] T008 `.gitleaks.toml` con `useDefault` y lista de exclusión.
- [x] T009 Job `Secretos` en `.github/workflows/ci.yml`.
- [x] T010 Objetivo `secrets` en el `Makefile`.

## Phase 4: Verificación

- [ ] T011 `make check` en verde.
- [ ] T012 PR con plantilla UAO, `Closes #99`.
