# Tareas — HU-052 (spec 053)

**Rama**: `feature/053-hu-052-openapi-publica` · **Issue**: #108

## Trazabilidad

| AC | Tareas | Pruebas |
|----|--------|---------|
| AC-01 (descripciones, ejemplos y códigos de error) | T004–T007 | `test_predict_summary_y_descripcion_ac_01`, `test_predict_codigos_de_error_ac_01`, `test_health_summary_y_descripcion_ac_01`, `test_conf_documented_limits_ac_01` |
| AC-02 (guía pública con URL, ejemplos y límites) | T008–T009 | `test_guia_incluye_url_y_ejemplos_ac_02`, `test_guia_documenta_limites_ac_02` |
| AC-03 (OpenAPI incluye los ejemplos) | T010–T011 | `test_openapi_ejemplo_de_respuesta_ac_03`, `test_info_y_swagger_ac_03` |

## Tareas

- [x] T001 Crear `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #108.
- [x] T002 Aplicar WIP 1: issue #108 a *In progress* y crear la rama desde `develop`.
- [x] T003 Escribir `tests/test_openapi_publica.py` con 8 pruebas AAA (AC-01 ×4, AC-02 ×2, AC-03 ×2) y ejecutarlas en rojo (7 fallaron, 1 pasó por el docstring previo de `/health`).
- [x] T004 `test_predict_summary_y_descripcion_ac_01` → AC-01.
- [x] T005 `test_predict_codigos_de_error_ac_01` → AC-01.
- [x] T006 `test_health_summary_y_descripcion_ac_01` → AC-01.
- [x] T007 `test_conf_documented_limits_ac_01` → AC-01.
- [x] T008 `test_guia_incluye_url_y_ejemplos_ac_02` → AC-02.
- [x] T009 `test_guia_documenta_limites_ac_02` → AC-02.
- [x] T010 `test_openapi_ejemplo_de_respuesta_ac_03` → AC-03.
- [x] T011 `test_info_y_swagger_ac_03` → AC-03.
- [x] T012 Enriquecer metadatos de `/predict`, `/health`, `conf` y descripción global en `src/ppe_detection/api/app.py` sin cambiar contratos ni validaciones.
- [x] T013 Escribir `docs/maas/README.md` con URL configurable (`PPE_MAAS_URL` / `<URL_PUBLICA>`), curl, Python, límites y HU pendientes.
- [x] T014 Ejecutar pytest completo, ruff, pre-commit, ty, check_specs y propiedad.
- [x] T015 Commitear test-first y feat/docs por separado, pushear y abrir PR #228 a `develop` con `Closes #108`, plantilla UAO y revisores ajenos; mover #108 a *In review*.
