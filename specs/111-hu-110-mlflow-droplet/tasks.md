# Tasks: HU-110 â€” MLflow en el Droplet (decisiÃ³n de alcance)

**Input**: Design documents from `specs/111-hu-110-mlflow-droplet/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias. La prueba verifica la decisiÃ³n de no publicar MLflow.

## Phase 1: DecisiÃ³n

- [x] T001 Revisar el alcance de #166 y la rÃºbrica del M4.
- [x] T002 Confirmar que MLflow local (HU-009) cubre la evaluaciÃ³n y comparaciÃ³n.
- [x] T003 Documentar la decisiÃ³n en `spec.md` y `plan.md`.

## Phase 2: Pruebas

- [x] T004 [AC-01] `compose.prod.yml` no declara un servicio `mlflow`.
- [x] T005 [AC-01/03] `docker/Caddyfile` no publica `/mlflow`.
- [x] T006 [AC-03] `docs/operacion/mlflow.md` documenta el uso local.

## Phase 3: Cierre

- [x] T007 `trazabilidad --check` acepta HU-110.
- [x] T008 `make check` en verde.
- [x] T009 Cerrar #166 con el enlace a esta spec.
