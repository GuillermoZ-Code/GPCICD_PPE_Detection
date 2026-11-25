# Tareas — HU-083 (spec 084)

- [x] T001 Crear `spec.md` con AC-01, AC-02 y AC-03 de la issue #139.
- [x] T002 Crear `plan.md` con build → smoke → Trivy → artefacto.
- [x] T003 Crear `tasks.md` con trazabilidad AC → prueba.
- [x] T004 `test_job_construye_imagen_runtime_ac_01` → AC-01.
- [x] T005 `test_smoke_no_monta_modelo_ac_01` → AC-01.
- [x] T006 `test_smoke_construye_la_api_sin_pesos_ac_01` → AC-01.
- [x] T007 `test_trivy_escanea_la_imagen_del_job_ac_02` → AC-02.
- [x] T008 `test_trivy_reporta_high_y_critical_en_sarif_ac_02` → AC-02.
- [x] T009 `test_reporte_se_publica_como_artefacto_ac_03` → AC-03.
- [x] T010 `test_job_tiene_permisos_para_artefactos_ac_03` → AC-03.
- [x] T011 Añadir el job `docker` a `.github/workflows/ci.yml`.
- [x] T012 Documentar el job en `docs/operacion/docker.md`.
- [x] T013 Ejecutar ruff, formato, ty, pytest, check_specs y `uv build`.
- [x] T014 Verificar `ownership --base origin/develop`.
- [ ] T015 Abrir PR a `develop` con `Closes #139` y revisión de Guillermo.
