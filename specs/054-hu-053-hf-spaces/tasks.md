# Tareas — HU-053 (spec 054)

**Rama**: `feature/054-hu-053-hf-spaces` · **Issue**: #109

## Trazabilidad

| AC | Tareas | Pruebas |
|----|--------|---------|
| AC-01 (destino justificado) | T004–T009 | `test_decision_hf_spaces_justificada_ac_01`, `test_space_card_identifica_destino_ac_01`, `test_dockerfile_expone_puerto_spaces_ac_01`, `test_sin_dominio_inventado_ac_01`, `test_documento_registra_limitaciones_ac_01`, `test_secretos_como_variables_de_entorno_ac_01` |
| AC-02 (atribución visible) | T010–T013 | `test_card_atribuye_dataset_cc_by_ac_02`, `test_card_enlaza_codigo_agpl_ac_02`, `test_doc_explica_atribucion_visible_ac_02`, `test_licencias_no_se_relicencian_ac_02` |
| AC-03 (despliegue reproducible y sin secretos) | T014–T019 | `test_dockerfile_congela_lock_ac_03`, `test_dockerfile_no_copia_secretos_ac_03`, `test_dockerignore_excluye_pesos_y_entorno_ac_03`, `test_runbook_incluye_build_y_arranque_ac_03`, `test_modelo_fuera_de_la_imagen_ac_03`, `test_pasos_publicacion_reproducibles_ac_03` |

## Tareas

- [x] T001 Crear `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #109.
- [x] T002 Aplicar WIP 1: issue #109 a *In progress* y crear la rama desde `develop`.
- [x] T003 Escribir `tests/test_segunda_url_publica.py` con 16 pruebas AAA (AC-01 ×6, AC-02 ×4, AC-03 ×6) y ejecutarlas en rojo.
- [x] T004 `test_decision_hf_spaces_justificada_ac_01` → AC-01.
- [x] T005 `test_space_card_identifica_destino_ac_01` → AC-01.
- [x] T006 `test_dockerfile_expone_puerto_spaces_ac_01` → AC-01.
- [x] T007 `test_sin_dominio_inventado_ac_01` → AC-01.
- [x] T008 `test_documento_registra_limitaciones_ac_01` → AC-01.
- [x] T009 `test_secretos_como_variables_de_entorno_ac_01` → AC-01.
- [x] T010 `test_card_atribuye_dataset_cc_by_ac_02` → AC-02.
- [x] T011 `test_card_enlaza_codigo_agpl_ac_02` → AC-02.
- [x] T012 `test_doc_explica_atribucion_visible_ac_02` → AC-02.
- [x] T013 `test_licencias_no_se_relicencian_ac_02` → AC-02.
- [x] T014 `test_dockerfile_congela_lock_ac_03` → AC-03.
- [x] T015 `test_dockerfile_no_copia_secretos_ac_03` → AC-03.
- [x] T016 `test_dockerignore_excluye_pesos_y_entorno_ac_03` → AC-03.
- [x] T017 `test_runbook_incluye_build_y_arranque_ac_03` → AC-03.
- [x] T018 `test_modelo_fuera_de_la_imagen_ac_03` → AC-03.
- [x] T019 `test_pasos_publicacion_reproducibles_ac_03` → AC-03.
- [x] T020 Crear `deploy/maas-alt/Dockerfile` y `.dockerignore`.
- [x] T021 Crear la tarjeta `deploy/maas-alt/README.md` con licencias y enlaces.
- [x] T022 Crear `docs/maas/segunda-url.md` con decisión, runbook y límites.
- [x] T023 Registrar en la issue #109 el bloqueo de credenciales HF para publicar el Space (comentario `7170284743`).
- [x] T024 Ejecutar pytest completo, ruff, pre-commit, ty, check_specs y propiedad.
- [ ] T025 Commitear test-first y docs/deploy por separado, pushear y abrir PR a `develop` con `Closes #109`, plantilla UAO y revisores ajenos; mover #109 a *In review*.
