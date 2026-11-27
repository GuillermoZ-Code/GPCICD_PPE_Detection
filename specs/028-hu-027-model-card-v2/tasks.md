# Tasks: HU-027 — Model Card v2

**Input**: Design documents from `specs/028-hu-027-model-card-v2/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #83.

## Phase 2: Pruebas

- [x] T002 [AC-01] La tarjeta compara YOLO11s y YOLO26 y cita el ADR 0009.
- [x] T003 [AC-02] La tarjeta documenta los sesgos de `safety_shoe` y `Gloves`.
- [x] T004 [AC-02] La tarjeta declara el uso no apto (no certifica cumplimiento).
- [x] T005 [AC-03] La tarjeta enlaza `models.lock`, MLflow y el informe de evaluación.

## Phase 3: Implementación

- [x] T006 `docs/model-card.md` con la versión `yolo26n-clean` y su SHA256.
- [x] T007 Sección de limitaciones y sesgos por clase.
- [x] T008 Sección de reproducibilidad con los enlaces de evidencia.

## Phase 4: Verificación

- [x] T009 `make trazabilidad-check` pasa para HU-027.
- [ ] T010 `make check` en verde.
- [ ] T011 PR con plantilla UAO y revisor de otro integrante.
