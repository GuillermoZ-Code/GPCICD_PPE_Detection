# Tareas — HU-084 (spec 085)

- [x] T001 Crear `spec.md` con AC-01, AC-02 y AC-03 de la issue #140.
- [x] T002 Crear `plan.md` con separación de etapas y usuario no root.
- [x] T003 Crear `tasks.md` con trazabilidad AC → prueba.
- [x] T004 `test_runtime_usa_usuario_no_root_ac_01` → AC-01.
- [x] T005 `test_capas_ordenadas_sin_uv_en_runtime_ac_01` → AC-01.
- [x] T006 `test_runbook_documenta_tamano_antes_despues_ac_02` → AC-02.
- [x] T007 `test_directiva_user_se_verifica_estaticamente_ac_03` → AC-03.
- [x] T008 Añadir `runtime-deps` y optimizar `runtime` en `Dockerfile`.
- [x] T009 Medir tamaño antes/después y documentarlo en `docs/operacion/docker.md` (1034.2 → 549.4 MB, −484.8 MB / −46.9 %; Actions run 45657387570).
- [x] T010 Ejecutar ruff, formato, ty, pytest, check_specs y `uv build`.
- [x] T011 Verificar `ownership --base origin/develop` (0 bloqueos, 4 avisos).
- [ ] T012 Abrir PR a `develop` con `Closes #140` y revisión de Guillermo.
