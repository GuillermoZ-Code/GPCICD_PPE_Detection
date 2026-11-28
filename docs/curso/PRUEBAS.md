# Inventario de pruebas — GPCICD PPE Detection

> **Generado:** 2026-11-28 03:31 UTC · `make pruebas`
> **Requisito del curso:** ≥ 400 pruebas unitarias (mínimo, no techo).
> **Fuente:** casos recolectados por pytest y por Vitest; no se edita a mano.

## 1. Resumen

| Suite | Herramienta | Archivos | Pruebas | Comando |
|-------|-------------|---------:|--------:|---------|
| Backend | pytest | 109 | 1057 | `make test` |
| Frontend | Vitest | 13 | 101 | `make frontend-test` |
| **Total** | | **122** | **1158** | `make check` + `make frontend-check` |

## 2. Desglose por archivo

| Archivo | Suite | Pruebas | Dueño |
|---|---|---:|---|
| tests/test_adr_exposicion_grpc.py | pytest | 4 | sin dueño |
| tests/test_adr_m4.py | pytest | 5 | sin dueño |
| tests/test_agpl_despliegue.py | pytest | 4 | sin dueño |
| tests/test_api.py | pytest | 12 | Eliana Cardona |
| tests/test_api_catalogo_errores.py | pytest | 4 | Eliana Cardona |
| tests/test_api_contract.py | pytest | 15 | Eliana Cardona |
| tests/test_api_health_live_ready.py | pytest | 8 | Eliana Cardona |
| tests/test_api_key.py | pytest | 12 | Eliana Cardona |
| tests/test_api_logs_json.py | pytest | 12 | Eliana Cardona |
| tests/test_api_settings.py | pytest | 8 | Eliana Cardona |
| tests/test_api_upload_limits.py | pytest | 8 | Eliana Cardona |
| tests/test_arquitectura_despliegue.py | pytest | 4 | sin dueño |
| tests/test_artifact_fetch.py | pytest | 8 | sin dueño |
| tests/test_backlog_mirror.py | pytest | 4 | sin dueño |
| tests/test_board_m4.py | pytest | 12 | sin dueño |
| tests/test_caddy.py | pytest | 10 | sin dueño |
| tests/test_caddyfile_cors_ratelimit.py | pytest | 3 | sin dueño |
| tests/test_calidad.py | pytest | 5 | sin dueño |
| tests/test_changelog.py | pytest | 4 | sin dueño |
| tests/test_ci_docker_trivy.py | pytest | 8 | sin dueño |
| tests/test_cierres_m4.py | pytest | 14 | sin dueño |
| tests/test_cobertura_cierre.py | pytest | 48 | sin dueño |
| tests/test_codeowners_hu082.py | pytest | 4 | sin dueño |
| tests/test_compose_prod.py | pytest | 8 | sin dueño |
| tests/test_contracts.py | pytest | 28 | sin dueño |
| tests/test_dataset_card.py | pytest | 4 | sin dueño |
| tests/test_deploy.py | pytest | 18 | sin dueño |
| tests/test_design_system.py | pytest | 9 | sin dueño |
| tests/test_detector_contract.py | pytest | 8 | sin dueño |
| tests/test_docker.py | pytest | 9 | sin dueño |
| tests/test_docker_assets.py | pytest | 15 | sin dueño |
| tests/test_docs_ficha_m4.py | pytest | 9 | sin dueño |
| tests/test_docs_m4.py | pytest | 4 | sin dueño |
| tests/test_docs_readme.py | pytest | 4 | sin dueño |
| tests/test_docs_runbook_fallos.py | pytest | 6 | sin dueño |
| tests/test_dor_dod.py | pytest | 4 | sin dueño |
| tests/test_engram_config.py | pytest | 8 | sin dueño |
| tests/test_engram_protocol.py | pytest | 7 | sin dueño |
| tests/test_estado.py | pytest | 10 | Jesús Riveros |
| tests/test_estado_gitlab.py | pytest | 12 | Jesús Riveros |
| tests/test_estado_tools.py | pytest | 10 | Jesús Riveros |
| tests/test_evaluation.py | pytest | 9 | Hernán Estrada |
| tests/test_evaluation_artifacts.py | pytest | 5 | Hernán Estrada |
| tests/test_evaluation_errors.py | pytest | 8 | Hernán Estrada |
| tests/test_evaluation_report.py | pytest | 10 | Hernán Estrada |
| tests/test_frontend_config.py | pytest | 2 | sin dueño |
| tests/test_geometry.py | pytest | 20 | sin dueño |
| tests/test_gga.py | pytest | 8 | sin dueño |
| tests/test_gitlab_ci.py | pytest | 19 | sin dueño |
| tests/test_gitleaks.py | pytest | 8 | sin dueño |
| tests/test_grpc.py | pytest | 9 | Eliana Cardona |
| tests/test_grpc_contract.py | pytest | 12 | Eliana Cardona |
| tests/test_health.py | pytest | 7 | sin dueño |
| tests/test_healthcheck.py | pytest | 7 | sin dueño |
| tests/test_image_loader.py | pytest | 17 | sin dueño |
| tests/test_image_validation.py | pytest | 7 | sin dueño |
| tests/test_input_stats.py | pytest | 4 | sin dueño |
| tests/test_io_edge_cases.py | pytest | 10 | Eliana Cardona |
| tests/test_issue_template.py | pytest | 6 | sin dueño |
| tests/test_labels.py | pytest | 4 | sin dueño |
| tests/test_launcher.py | pytest | 5 | sin dueño |
| tests/test_load_test.py | pytest | 16 | sin dueño |
| tests/test_make_deploy.py | pytest | 6 | sin dueño |
| tests/test_metrics.py | pytest | 35 | sin dueño |
| tests/test_metrics_golden.py | pytest | 9 | sin dueño |
| tests/test_mirror_gitlab.py | pytest | 13 | sin dueño |
| tests/test_model_card_v2.py | pytest | 11 | sin dueño |
| tests/test_model_manifest.py | pytest | 10 | sin dueño |
| tests/test_model_publish.py | pytest | 8 | sin dueño |
| tests/test_model_version.py | pytest | 21 | sin dueño |
| tests/test_models_lock.py | pytest | 7 | sin dueño |
| tests/test_onnx_backend.py | pytest | 9 | sin dueño |
| tests/test_openapi_publica.py | pytest | 8 | sin dueño |
| tests/test_optimizacion_imagen.py | pytest | 4 | sin dueño |
| tests/test_overlay.py | pytest | 7 | sin dueño |
| tests/test_overlay_launcher.py | pytest | 5 | sin dueño |
| tests/test_ownership.py | pytest | 17 | Guillermo Zabala |
| tests/test_paridad_protocolos.py | pytest | 13 | sin dueño |
| tests/test_plan_pruebas.py | pytest | 4 | sin dueño |
| tests/test_postprocessing_thresholds.py | pytest | 10 | sin dueño |
| tests/test_predict.py | pytest | 16 | sin dueño |
| tests/test_predict_batch.py | pytest | 4 | sin dueño |
| tests/test_preprocessing.py | pytest | 8 | Hernán Estrada |
| tests/test_readme_badges.py | pytest | 4 | sin dueño |
| tests/test_reproducibilidad.py | pytest | 4 | sin dueño |
| tests/test_results.py | pytest | 10 | sin dueño |
| tests/test_retro_m4.py | pytest | 4 | sin dueño |
| tests/test_riesgos_m4.py | pytest | 4 | sin dueño |
| tests/test_robustness.py | pytest | 5 | sin dueño |
| tests/test_segunda_url_publica.py | pytest | 16 | sin dueño |
| tests/test_size_bias.py | pytest | 5 | sin dueño |
| tests/test_skills_repo.py | pytest | 6 | sin dueño |
| tests/test_smoke.py | pytest | 1 | sin dueño |
| tests/test_smoke_remote.py | pytest | 8 | sin dueño |
| tests/test_sprint.py | pytest | 10 | sin dueño |
| tests/test_thresholds.py | pytest | 11 | sin dueño |
| tests/test_tools_check_specs.py | pytest | 13 | Jesús Riveros |
| tests/test_tools_pruebas.py | pytest | 6 | Jesús Riveros |
| tests/test_tools_rubrica.py | pytest | 8 | Jesús Riveros |
| tests/test_tools_trazabilidad.py | pytest | 17 | Jesús Riveros |
| tests/test_tracking.py | pytest | 11 | Jesús Riveros |
| tests/test_tracking_benchmark.py | pytest | 15 | Jesús Riveros |
| tests/test_tracking_comparison.py | pytest | 8 | Jesús Riveros |
| tests/test_tracking_latency_run.py | pytest | 8 | Jesús Riveros |
| tests/test_tracking_mlflow.py | pytest | 25 | Jesús Riveros |
| tests/test_tracking_registry.py | pytest | 9 | Jesús Riveros |
| tests/test_tracking_report.py | pytest | 7 | Jesús Riveros |
| tests/test_training.py | pytest | 15 | sin dueño |
| tests/test_yolo_detector.py | pytest | 20 | sin dueño |
| frontend/src/App.flow.test.tsx | vitest | 8 | Guillermo Zabala |
| frontend/src/App.states.test.tsx | vitest | 5 | Guillermo Zabala |
| frontend/src/App.test.tsx | vitest | 16 | Guillermo Zabala |
| frontend/src/api/client.test.ts | vitest | 19 | Guillermo Zabala |
| frontend/src/api/config.test.ts | vitest | 6 | Guillermo Zabala |
| frontend/src/components/AnnotatedCanvas.test.tsx | vitest | 6 | Guillermo Zabala |
| frontend/src/components/DetectionTable.test.tsx | vitest | 7 | Guillermo Zabala |
| frontend/src/components/ModelInfo.test.tsx | vitest | 4 | Guillermo Zabala |
| frontend/src/components/SettingsDrawer.test.tsx | vitest | 5 | Guillermo Zabala |
| frontend/src/config.test.ts | vitest | 5 | Guillermo Zabala |
| frontend/src/download.test.ts | vitest | 3 | Guillermo Zabala |
| frontend/src/filter.test.ts | vitest | 3 | Guillermo Zabala |
| frontend/src/validate.test.ts | vitest | 14 | Guillermo Zabala |

## 3. Totales por integrante

| Integrante | pytest | Vitest | Total |
|---|---:|---:|---:|
| Eliana Cardona | 110 | 0 | 110 |
| Guillermo Zabala | 17 | 101 | 118 |
| Hernán Estrada | 40 | 0 | 40 |
| Jesús Riveros | 159 | 0 | 159 |
| sin dueño | 731 | 0 | 731 |

## 4. Cómo se actualiza

```bash
make pruebas        # imprime el resumen
make pruebas-write  # regenera este archivo
```

El dueño de `docs/curso/PRUEBAS.md` lo regenera y lo commitea. El plan
hacia 1.200 pruebas vive en `docs/curso/PLAN-PRUEBAS.md`.
