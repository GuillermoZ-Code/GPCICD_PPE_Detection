# Tareas — HU-051 (spec 052)

**Rama**: `feature/052-hu-051-api-key` · **Issue**: #107

## Trazabilidad

| AC | Tareas | Pruebas |
|----|--------|---------|
| AC-01 (401 sin clave válida) | T004–T009 | `test_sin_cabecera_devuelve_401_ac_01`, `test_clave_incorrecta_devuelve_401_ac_01`, `test_clave_correcta_devuelve_200_ac_01`, `test_multiples_claves_separadas_por_coma_ac_01`, `test_configured_keys_acepta_legacy_y_ignora_vacios_ac_01`, `test_openapi_documenta_401_ac_01` |
| AC-02 (sin variable, sin cambios) | T010–T012 | `test_sin_variable_no_exige_clave_ac_02`, `test_variable_vacia_no_exige_clave_ac_02`, `test_solo_predict_esta_protegido_ac_02` |
| AC-03 (tiempo constante y sin logs) | T013–T015 | `test_comparacion_no_corta_circuito_ac_03`, `test_clave_correcta_por_digest_ac_03`, `test_secretos_nunca_se_registran_ac_03` |

## Tareas

- [x] T001 Crear `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #107.
- [x] T002 Aplicar WIP 1: issue #107 a *In progress* y crear la rama desde `develop`.
- [x] T003 Escribir `tests/test_api_key.py` con 12 pruebas AAA (AC-01 ×6, AC-02 ×3, AC-03 ×3) y ejecutarlas en rojo (error de importación del módulo nuevo).
- [x] T004 `test_sin_cabecera_devuelve_401_ac_01` → AC-01.
- [x] T005 `test_clave_incorrecta_devuelve_401_ac_01` → AC-01.
- [x] T006 `test_clave_correcta_devuelve_200_ac_01` → AC-01.
- [x] T007 `test_multiples_claves_separadas_por_coma_ac_01` → AC-01.
- [x] T008 `test_configured_keys_acepta_legacy_y_ignora_vacios_ac_01` → AC-01.
- [x] T009 `test_openapi_documenta_401_ac_01` → AC-01.
- [x] T010 `test_sin_variable_no_exige_clave_ac_02` → AC-02.
- [x] T011 `test_variable_vacia_no_exige_clave_ac_02` → AC-02.
- [x] T012 `test_solo_predict_esta_protegido_ac_02` → AC-02.
- [x] T013 `test_comparacion_no_corta_circuito_ac_03` → AC-03.
- [x] T014 `test_clave_correcta_por_digest_ac_03` → AC-03.
- [x] T015 `test_secretos_nunca_se_registran_ac_03` → AC-03.
- [x] T016 Crear `src/ppe_detection/api/security.py` con resolución y comparación en tiempo constante.
- [x] T017 Conectar la guarda a `/predict` en `src/ppe_detection/api/app.py` y documentar 401.
- [x] T018 Documentar `PPE_API_KEYS` y `PPE_API_KEY` en `.env.example`.
- [x] T019 Ejecutar pytest completo, ruff, pre-commit, ty, check_specs y propiedad.
- [ ] T020 Commitear test-first y feat/docs por separado, pushear y abrir PR a `develop` con `Closes #107`, plantilla UAO y revisores ajenos; mover #107 a *In review*.
