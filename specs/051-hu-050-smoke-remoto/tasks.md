# Tareas — HU-050 (spec 051)

- [x] T001 Crear `spec.md` con AC-01, AC-02 y AC-03 de la issue #106.
- [x] T002 Crear `plan.md` con el enfoque de transportes inyectables.
- [x] T003 Crear `tasks.md` con trazabilidad AC → prueba.
- [x] T004 `test_ready_reports_model_version_ac_01` → AC-01.
- [x] T005 `test_valid_rest_prediction_reports_latency_ac_01` → AC-01.
- [x] T006 `test_grpc_prediction_reports_version_and_latency_ac_01` → AC-01.
- [x] T007 `test_invalid_rest_image_returns_400_ac_02` → AC-02.
- [x] T008 `test_invalid_grpc_image_is_rejected_ac_02` → AC-02.
- [x] T009 `test_failed_check_returns_nonzero_ac_02` → AC-02.
- [x] T010 `test_service_stays_ready_after_rejection_ac_02` → AC-02.
- [x] T011 `test_simulated_transports_need_no_network_ac_03` → AC-03.
- [x] T012 Implementar `src/ppe_detection/tools/smoke_remote.py` y su CLI.
- [x] T013 Documentar el uso en `docs/operacion/fallos.md`.
- [x] T014 Ejecutar ruff, formato, ty, pytest y `uv build`.
- [x] T015 Verificar `ownership --base origin/develop`.
- [ ] T016 Abrir PR a `develop` con plantilla UAO, `Closes #106` y revisor ajeno.
