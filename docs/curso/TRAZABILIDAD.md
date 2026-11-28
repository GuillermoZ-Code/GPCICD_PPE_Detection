# Matriz de trazabilidad — GPCICD PPE Detection

> **Generado:** 2026-11-28 04:31 UTC · `make trazabilidad-write`
> **HU:** 113 · completas: 108 · incompletas: 5
> **Fuente:** GitHub Issues y PRs, `specs/` y referencias `HU-NNN` en las pruebas.
> **Exenciones:** HU-016 (spike documental (SPI)), HU-018 (entrenamiento en GPU; sin pruebas unitarias), HU-019 (informe de evaluación; evidencia documental), HU-023 (ADR; decisión documental), HU-089 (creación de issues; entregable en GitHub)

| HU | Issue | Estado | Spec | PR | Pruebas | Falta |
|---|---|---|---|---|---|---|
| HU-001 | [#1](../../issues/1) | cerrada | [002-hu-001-carga-imagen](../../specs/002-hu-001-carga-imagen/) | [#28](../../pull/28) | `tests/test_image_loader.py` | — |
| HU-002 | [#2](../../issues/2) | cerrada | [003-hu-002-deteccion](../../specs/003-hu-002-deteccion/) | [#30](../../pull/30) | `test_predict.py`, `tests/test_yolo_detector.py` | — |
| HU-003 | [#3](../../issues/3) | cerrada | [004-hu-003-visualizacion](../../specs/004-hu-003-visualizacion/) | [#33](../../pull/33) | `tests/test_geometry.py`, `tests/test_overlay.py` | — |
| HU-004 | [#4](../../issues/4) | cerrada | [006-hu-004-informe-sin-detecciones](../../specs/006-hu-004-informe-sin-detecciones/) | [#34](../../pull/34), [#37](../../pull/37) | `tests/test_grpc_contract.py`, `tests/test_results.py` | — |
| HU-005 | [#5](../../issues/5) | cerrada | [007-hu-005-validacion-imagenes](../../specs/007-hu-005-validacion-imagenes/) | [#39](../../pull/39) | `tests/test_image_validation.py`, `tests/test_io_edge_cases.py` | — |
| HU-006 | [#6](../../issues/6) | cerrada | [008-hu-006-api-rest](../../specs/008-hu-006-api-rest/) | [#42](../../pull/42) | `tests/test_api.py`, `tests/test_api_contract.py` | — |
| HU-007 | [#7](../../issues/7) | cerrada | [005-hu-007-interfaz](../../specs/005-hu-007-interfaz/) | [#35](../../pull/35), [#37](../../pull/37) | `AnnotatedCanvas.test.tsx`, `DetectionTable.test.tsx` | — |
| HU-008 | [#8](../../issues/8) | cerrada | [009-hu-008-evaluacion](../../specs/009-hu-008-evaluacion/) | [#45](../../pull/45), [#51](../../pull/51) | `test_evaluation.py`, `tests/test_evaluation_report.py`, `tests/test_geometry.py`, `tests/test_metrics.py` | — |
| HU-009 | [#9](../../issues/9) | cerrada | [012-hu-009-mlflow](../../specs/012-hu-009-mlflow/) | [#50](../../pull/50) | `tests/test_tracking.py`, `tests/test_tracking_mlflow.py` | — |
| HU-010 | [#10](../../issues/10) | cerrada | [010-hu-010-consumo-grpc](../../specs/010-hu-010-consumo-grpc/) | [#46](../../pull/46) | `tests/test_grpc.py`, `tests/test_grpc_contract.py` | — |
| HU-011 | [#11](../../issues/11) | cerrada | [013-hu-011-docker-cpu](../../specs/013-hu-011-docker-cpu/) | [#52](../../pull/52) | `tests/test_docker.py`, `tests/test_docker_assets.py` | — |
| HU-012 | [#12](../../issues/12) | cerrada | [011-hu-012-calidad](../../specs/011-hu-012-calidad/) | [#49](../../pull/49) | `tests/test_calidad.py` | — |
| HU-013 | [#13](../../issues/13) | cerrada | [014-hu-013-version-modelo](../../specs/014-hu-013-version-modelo/) | [#54](../../pull/54), [#55](../../pull/55) | `tests/test_model_version.py` | — |
| HU-014 | [#14](../../issues/14) | cerrada | [015-hu-014-compuertas](../../specs/015-hu-014-compuertas/) | [#255](../../pull/255) | `tests/test_cierres_m4.py` | — |
| HU-015 | [#15](../../issues/15) | cerrada | [016-hu-015-verificacion](../../specs/016-hu-015-verificacion/) | [#255](../../pull/255) | `tests/test_cierres_m4.py` | — |
| HU-016 | [#72](../../issues/72) | cerrada | [017-hu-016-spike-yolo26](../../specs/017-hu-016-spike-yolo26/) | [#173](../../pull/173) | — | pruebas |
| HU-017 | [#73](../../issues/73) | cerrada | [018-hu-017-train-yolo26](../../specs/018-hu-017-train-yolo26/) | [#181](../../pull/181) | `tests/test_training.py` | — |
| HU-018 | [#74](../../issues/74) | cerrada | [019-hu-018-entrenar-yolo26](../../specs/019-hu-018-entrenar-yolo26/) | [#174](../../pull/174) | — | pruebas |
| HU-019 | [#75](../../issues/75) | cerrada | [020-hu-019-comparar-yolo26-yolo11](../../specs/020-hu-019-comparar-yolo26-yolo11/) | [#178](../../pull/178) | — | pruebas |
| HU-020 | [#76](../../issues/76) | cerrada | [021-hu-020-benchmark-latencia](../../specs/021-hu-020-benchmark-latencia/) | [#176](../../pull/176) | `tests/test_tracking_benchmark.py` | — |
| HU-021 | [#77](../../issues/77) | cerrada | [022-hu-021-detector-nms-free](../../specs/022-hu-021-detector-nms-free/) | [#177](../../pull/177) | `tests/test_yolo_detector.py` | — |
| HU-022 | [#78](../../issues/78) | cerrada | [023-hu-022-export-onnx](../../specs/023-hu-022-export-onnx/) | [#185](../../pull/185) | `tests/test_onnx_backend.py` | — |
| HU-023 | [#79](../../issues/79) | cerrada | [024-hu-023-adr-modelo-productivo](../../specs/024-hu-023-adr-modelo-productivo/) | [#184](../../pull/184) | — | pruebas |
| HU-024 | [#80](../../issues/80) | cerrada | [025-hu-024-modelo-registry](../../specs/025-hu-024-modelo-registry/) | [#249](../../pull/249) | `tests/test_model_publish.py`, `tests/test_models_lock.py` | — |
| HU-025 | [#81](../../issues/81) | cerrada | [026-hu-025-models-lock](../../specs/026-hu-025-models-lock/) | [#171](../../pull/171) | `tests/test_model_manifest.py` | — |
| HU-026 | [#82](../../issues/82) | cerrada | [027-hu-026-fetch-model](../../specs/027-hu-026-fetch-model/) | [#175](../../pull/175) | `tests/test_artifact_fetch.py` | — |
| HU-027 | [#83](../../issues/83) | cerrada | [028-hu-027-model-card-v2](../../specs/028-hu-027-model-card-v2/) | [#242](../../pull/242), [#243](../../pull/243) | `test_model_card_v2.py`, `tests/test_model_card_v2.py` | — |
| HU-028 | [#84](../../issues/84) | cerrada | [029-hu-028-dataset-card](../../specs/029-hu-028-dataset-card/) | [#235](../../pull/235) | `tests/test_dataset_card.py` | — |
| HU-029 | [#85](../../issues/85) | cerrada | [030-hu-029-umbrales-por-clase](../../specs/030-hu-029-umbrales-por-clase/) | [#204](../../pull/204) | `tests/test_thresholds.py` | — |
| HU-030 | [#86](../../issues/86) | cerrada | [031-hu-030-analisis-fp-fn](../../specs/031-hu-030-analisis-fp-fn/) | [#207](../../pull/207) | `tests/test_evaluation_errors.py` | — |
| HU-031 | [#87](../../issues/87) | cerrada | [032-hu-031-artefactos-evaluacion](../../specs/032-hu-031-artefactos-evaluacion/) | [#206](../../pull/206) | `tests/test_evaluation_artifacts.py` | — |
| HU-032 | [#88](../../issues/88) | cerrada | [033-hu-032-robustez](../../specs/033-hu-032-robustez/) | [#258](../../pull/258) | `tests/test_robustness.py` | — |
| HU-033 | [#89](../../issues/89) | cerrada | [034-hu-033-regresion-metricas](../../specs/034-hu-033-regresion-metricas/) | [#172](../../pull/172) | `test_metrics_golden.py`, `tests/test_metrics_golden.py` | — |
| HU-034 | [#90](../../issues/90) | cerrada | [035-hu-034-contrato-yolo26](../../specs/035-hu-034-contrato-yolo26/) | [#205](../../pull/205) | `test_detector_contract.py`, `tests/test_detector_contract.py` | — |
| HU-035 | [#91](../../issues/91) | cerrada | [036-hu-035-preprocessing](../../specs/036-hu-035-preprocessing/) | [#238](../../pull/238) | `tests/test_preprocessing.py` | — |
| HU-036 | [#92](../../issues/92) | cerrada | [037-hu-036-postprocessing](../../specs/037-hu-036-postprocessing/) | [#233](../../pull/233) | `tests/test_postprocessing_thresholds.py` | — |
| HU-037 | [#93](../../issues/93) | cerrada | [038-hu-037-sesgo-tamano](../../specs/038-hu-037-sesgo-tamano/) | [#246](../../pull/246) | `tests/test_size_bias.py` | — |
| HU-038 | [#94](../../issues/94) | cerrada | [039-hu-038-drift-entrada](../../specs/039-hu-038-drift-entrada/) | [#260](../../pull/260) | `tests/test_input_stats.py` | — |
| HU-039 | [#95](../../issues/95) | cerrada | [040-hu-039-predict-lotes](../../specs/040-hu-039-predict-lotes/) | [#239](../../pull/239) | `test_predict.py`, `tests/test_predict_batch.py` | — |
| HU-040 | [#96](../../issues/96) | cerrada | [041-hu-040-reproducibilidad-entrenamiento](../../specs/041-hu-040-reproducibilidad-entrenamiento/) | [#237](../../pull/237) | `tests/test_reproducibilidad.py` | — |
| HU-041 | [#97](../../issues/97) | cerrada | [042-hu-041-caddy](../../specs/042-hu-041-caddy/) | [#241](../../pull/241) | `tests/test_caddy.py` | — |
| HU-042 | [#98](../../issues/98) | cerrada | [043-hu-042-variables-ci](../../specs/043-hu-042-variables-ci/) | [#255](../../pull/255) | `tests/test_cierres_m4.py` | — |
| HU-043 | [#99](../../issues/99) | cerrada | [044-hu-043-gitleaks](../../specs/044-hu-043-gitleaks/) | [#254](../../pull/254) | `tests/test_gitleaks.py` | — |
| HU-044 | [#100](../../issues/100) | cerrada | [045-hu-044-config-entorno](../../specs/045-hu-044-config-entorno/) | [#210](../../pull/210) | `test_api_settings.py`, `tests/test_api_settings.py` | — |
| HU-045 | [#101](../../issues/101) | cerrada | [046-hu-045-health-live-ready](../../specs/046-hu-045-health-live-ready/) | [#209](../../pull/209) | `test_api_health_live_ready.py`, `tests/test_api_health_live_ready.py` | — |
| HU-046 | [#102](../../issues/102) | cerrada | [047-hu-046-healthcheck](../../specs/047-hu-046-healthcheck/) | [#241](../../pull/241) | `tests/test_healthcheck.py` | — |
| HU-047 | [#103](../../issues/103) | cerrada | [048-hu-047-logs-json](../../specs/048-hu-047-logs-json/) | [#211](../../pull/211) | `test_api_logs_json.py`, `tests/test_api_logs_json.py` | — |
| HU-048 | [#104](../../issues/104) | cerrada | [049-hu-048-limites-carga](../../specs/049-hu-048-limites-carga/) | [#212](../../pull/212) | `test_api_upload_limits.py`, `tests/test_api_upload_limits.py` | — |
| HU-049 | [#105](../../issues/105) | cerrada | [050-hu-049-exposicion-grpc](../../specs/050-hu-049-exposicion-grpc/) | [#263](../../pull/263) | `test_adr_exposicion_grpc.py`, `tests/test_adr_exposicion_grpc.py` | — |
| HU-050 | [#106](../../issues/106) | cerrada | [051-hu-050-smoke-remoto](../../specs/051-hu-050-smoke-remoto/) | [#222](../../pull/222) | `conftest.py`, `test_smoke_remote.py`, `tests/test_smoke_remote.py` | — |
| HU-051 | [#107](../../issues/107) | cerrada | [052-hu-051-api-key](../../specs/052-hu-051-api-key/) | [#229](../../pull/229) | `test_api_key.py`, `tests/test_api_key.py` | — |
| HU-052 | [#108](../../issues/108) | cerrada | [053-hu-052-openapi-publica](../../specs/053-hu-052-openapi-publica/) | [#228](../../pull/228) | `test_openapi_publica.py`, `tests/test_openapi_publica.py` | — |
| HU-053 | [#109](../../issues/109) | cerrada | [054-hu-053-hf-spaces](../../specs/054-hu-053-hf-spaces/) | [#230](../../pull/230) | `test_segunda_url_publica.py`, `tests/test_segunda_url_publica.py` | — |
| HU-054 | [#110](../../issues/110) | cerrada | [055-hu-054-cors-ratelimit](../../specs/055-hu-054-cors-ratelimit/) | [#259](../../pull/259) | `test_caddyfile_cors_ratelimit.py`, `tests/test_caddyfile_cors_ratelimit.py` | — |
| HU-055 | [#111](../../issues/111) | cerrada | [059-hu-055-runbook-despliegue](../../specs/059-hu-055-runbook-despliegue/) | [#279](../../pull/279) | `test_runbook_despliegue.py`, `tests/test_runbook_despliegue.py` | — |
| HU-056 | [#112](../../issues/112) | cerrada | [057-hu-056-runbook-fallos](../../specs/057-hu-056-runbook-fallos/) | [#213](../../pull/213) | `test_docs_runbook_fallos.py`, `tests/test_docs_runbook_fallos.py` | — |
| HU-057 | [#113](../../issues/113) | cerrada | [058-hu-057-guion-sustentacion](../../specs/058-hu-057-guion-sustentacion/) | [#214](../../pull/214) | `test_docs_ficha_m4.py`, `tests/test_docs_ficha_m4.py` | — |
| HU-058 | [#114](../../issues/114) | cerrada | [059-hu-058-manual-usuario](../../specs/059-hu-058-manual-usuario/) | [#272](../../pull/272) | `tests/test_manual_usuario_spa.py` | — |
| HU-059 | [#115](../../issues/115) | cerrada | [060-hu-059-catalogo-errores](../../specs/060-hu-059-catalogo-errores/) | [#234](../../pull/234), [#236](../../pull/236) | `test_api_catalogo_errores.py`, `tests/test_api_catalogo_errores.py` | — |
| HU-060 | [#116](../../issues/116) | cerrada | [061-hu-060-agpl-despliegue](../../specs/061-hu-060-agpl-despliegue/) | [#227](../../pull/227) | `test_agpl_despliegue.py`, `tests/test_agpl_despliegue.py` | — |
| HU-061 | [#117](../../issues/117) | cerrada | [062-hu-061-readme-badges](../../specs/062-hu-061-readme-badges/) | [#231](../../pull/231) | `test_readme_badges.py`, `tests/test_readme_badges.py` | — |
| HU-062 | [#118](../../issues/118) | cerrada | [063-hu-062-paridad-rest-grpc](../../specs/063-hu-062-paridad-rest-grpc/) | [#216](../../pull/216) | `test_paridad_protocolos.py`, `tests/test_paridad_protocolos.py` | — |
| HU-063 | [#119](../../issues/119) | cerrada | [064-hu-063-prueba-carga](../../specs/064-hu-063-prueba-carga/) | [#264](../../pull/264) | `tests/test_load_test.py` | — |
| HU-064 | [#120](../../issues/120) | cerrada | [065-hu-064-release-notes](../../specs/065-hu-064-release-notes/) | [#217](../../pull/217) | `test_changelog.py`, `tests/test_changelog.py` | — |
| HU-065 | [#121](../../issues/121) | cerrada | [066-hu-065-gitlab-espejo](../../specs/066-hu-065-gitlab-espejo/) | [#218](../../pull/218) | `tests/test_mirror_gitlab.py` | — |
| HU-066 | [#122](../../issues/122) | cerrada | [067-hu-066-gitlab-ci](../../specs/067-hu-066-gitlab-ci/) | [#240](../../pull/240) | `tests/test_gitlab_ci.py` | — |
| HU-067 | [#123](../../issues/123) | cerrada | [068-hu-067-build-image](../../specs/068-hu-067-build-image/) | [#240](../../pull/240) | `tests/test_gitlab_ci.py` | — |
| HU-068 | [#124](../../issues/124) | cerrada | [069-hu-068-registry](../../specs/069-hu-068-registry/) | [#240](../../pull/240) | `tests/test_gitlab_ci.py` | — |
| HU-069 | [#125](../../issues/125) | cerrada | [070-hu-069-droplet](../../specs/070-hu-069-droplet/) | [#241](../../pull/241), [#247](../../pull/247) | `tests/test_deploy.py` | — |
| HU-070 | [#126](../../issues/126) | cerrada | [071-hu-070-deploy](../../specs/071-hu-070-deploy/) | [#241](../../pull/241) | `tests/test_deploy.py`, `tests/test_make_deploy.py` | — |
| HU-071 | [#127](../../issues/127) | cerrada | [072-hu-071-compose-prod](../../specs/072-hu-071-compose-prod/) | [#241](../../pull/241) | `tests/test_compose_prod.py` | — |
| HU-072 | [#128](../../issues/128) | cerrada | [073-hu-072-spa-api-relativa](../../specs/073-hu-072-spa-api-relativa/) | [#215](../../pull/215) | `tests/test_frontend_config.py` | — |
| HU-073 | [#129](../../issues/129) | cerrada | [074-hu-073-gitlab-mcp](../../specs/074-hu-073-gitlab-mcp/) | [#255](../../pull/255) | `tests/test_cierres_m4.py` | — |
| HU-074 | [#130](../../issues/130) | cerrada | [075-hu-074-skills-repo](../../specs/075-hu-074-skills-repo/) | [#219](../../pull/219), [#255](../../pull/255) | `tests/test_skills_repo.py` | — |
| HU-075 | [#131](../../issues/131) | cerrada | [076-hu-075-gga](../../specs/076-hu-075-gga/) | [#261](../../pull/261) | `tests/test_gga.py` | — |
| HU-076 | [#132](../../issues/132) | cerrada | [077-hu-076-rediseno](../../specs/077-hu-076-rediseno/) | [#252](../../pull/252) | `tests/test_design_system.py` | — |
| HU-077 | [#133](../../issues/133) | cerrada | [078-hu-077-rediseno-flujo](../../specs/078-hu-077-rediseno-flujo/) | [#267](../../pull/267) | `App.flow.test.tsx` | — |
| HU-078 | [#134](../../issues/134) | cerrada | [079-hu-078-export](../../specs/079-hu-078-export/) | [#255](../../pull/255) | `tests/test_cierres_m4.py` | — |
| HU-079 | [#135](../../issues/135) | cerrada | [080-hu-079-pagina-modelo](../../specs/080-hu-079-pagina-modelo/) | [#226](../../pull/226) | `ModelInfo.test.tsx` | — |
| HU-080 | [#136](../../issues/136) | cerrada | [081-hu-080-accesibilidad](../../specs/081-hu-080-accesibilidad/) | [#275](../../pull/275) | `App.a11y.test.tsx` | — |
| HU-081 | [#137](../../issues/137) | cerrada | [082-hu-081-estados-ui](../../specs/082-hu-081-estados-ui/) | [#220](../../pull/220), [#255](../../pull/255) | `App.states.test.tsx`, `tests/test_cierres_m4.py` | — |
| HU-082 | [#138](../../issues/138) | cerrada | [083-hu-082-codeowners-checks](../../specs/083-hu-082-codeowners-checks/) | [#223](../../pull/223) | `test_codeowners_hu082.py`, `tests/test_codeowners_hu082.py`, `tests/test_ownership.py` | — |
| HU-083 | [#139](../../issues/139) | cerrada | [084-hu-083-ci-docker-trivy](../../specs/084-hu-083-ci-docker-trivy/) | [#224](../../pull/224) | `test_ci_docker_trivy.py`, `tests/test_ci_docker_trivy.py` | — |
| HU-084 | [#140](../../issues/140) | cerrada | [085-hu-084-optimizar-imagen](../../specs/085-hu-084-optimizar-imagen/) | [#225](../../pull/225) | `test_optimizacion_imagen.py`, `tests/test_optimizacion_imagen.py` | — |
| HU-085 | [#141](../../issues/141) | cerrada | [086-hu-085-adr-gitlab-droplet](../../specs/086-hu-085-adr-gitlab-droplet/) | [#221](../../pull/221) | `tests/test_adr_m4.py` | — |
| HU-086 | [#142](../../issues/142) | cerrada | [087-hu-086-diagrama-despliegue](../../specs/087-hu-086-diagrama-despliegue/) | [#262](../../pull/262) | `tests/test_arquitectura_despliegue.py` | — |
| HU-087 | [#143](../../issues/143) | cerrada | [088-hu-087-docs-m4](../../specs/088-hu-087-docs-m4/) | [#266](../../pull/266) | `test_docs_m4.py`, `tests/test_docs_m4.py` | — |
| HU-088 | [#144](../../issues/144) | cerrada | [089-hu-088-historial-sesion](../../specs/089-hu-088-historial-sesion/) | [#276](../../pull/276) | `App.history.test.tsx` | — |
| HU-089 | [#145](../../issues/145) | cerrada | — | — | — | spec, pr, pruebas |
| HU-090 | [#146](../../issues/146) | cerrada | [091-hu-090-tablero](../../specs/091-hu-090-tablero/) | [#270](../../pull/270) | `test_board_m4.py`, `tests/test_board_m4.py` | — |
| HU-091 | [#147](../../issues/147) | cerrada | [092-hu-091-plantilla-hu](../../specs/092-hu-091-plantilla-hu/) | [#179](../../pull/179) | `test_issue_template.py`, `tests/test_issue_template.py` | — |
| HU-092 | [#148](../../issues/148) | cerrada | [093-hu-092-backlog-espejo](../../specs/093-hu-092-backlog-espejo/) | [#188](../../pull/188) | `test_backlog_mirror.py`, `tests/test_backlog_mirror.py` | — |
| HU-093 | [#149](../../issues/149) | cerrada | [094-hu-093-matriz-trazabilidad](../../specs/094-hu-093-matriz-trazabilidad/) | [#189](../../pull/189) | `...test.tsx`, `tests/test_tools_trazabilidad.py` | — |
| HU-094 | [#150](../../issues/150) | cerrada | [095-hu-094-conteo-pruebas](../../specs/095-hu-094-conteo-pruebas/) | [#183](../../pull/183) | `tests/test_tools_pruebas.py` | — |
| HU-095 | [#151](../../issues/151) | cerrada | [096-hu-095-corregir-pruebas-md](../../specs/096-hu-095-corregir-pruebas-md/) | [#186](../../pull/186) | `test_plan_pruebas.py`, `tests/test_plan_pruebas.py` | — |
| HU-096 | [#152](../../issues/152) | cerrada | [097-hu-096-validador-specs](../../specs/097-hu-096-validador-specs/) | [#191](../../pull/191) | `tests/test_tools_check_specs.py` | — |
| HU-097 | [#153](../../issues/153) | cerrada | [098-hu-097-runs-mlflow](../../specs/098-hu-097-runs-mlflow/) | [#198](../../pull/198) | `tests/test_tracking_comparison.py` | — |
| HU-098 | [#154](../../issues/154) | cerrada | [099-hu-098-registry](../../specs/099-hu-098-registry/) | [#201](../../pull/201) | `tests/test_tracking_registry.py` | — |
| HU-099 | [#155](../../issues/155) | cerrada | [100-hu-099-informe-runs](../../specs/100-hu-099-informe-runs/) | [#202](../../pull/202) | `tests/test_tracking_report.py` | — |
| HU-100 | [#156](../../issues/156) | cerrada | [101-hu-100-latencia-mlflow](../../specs/101-hu-100-latencia-mlflow/) | [#199](../../pull/199) | `tests/test_tracking_latency_run.py` | — |
| HU-101 | [#157](../../issues/157) | cerrada | [102-hu-101-engram](../../specs/102-hu-101-engram/) | [#192](../../pull/192) | `tests/test_engram_config.py` | — |
| HU-102 | [#158](../../issues/158) | cerrada | [103-hu-102-protocolo-engram](../../specs/103-hu-102-protocolo-engram/) | [#203](../../pull/203) | `test_engram_protocol.py`, `tests/test_engram_protocol.py` | — |
| HU-103 | [#159](../../issues/159) | cerrada | [104-hu-103-informe-sprint](../../specs/104-hu-103-informe-sprint/) | [#271](../../pull/271) | `test_sprint.py`, `tests/test_sprint.py` | — |
| HU-104 | [#160](../../issues/160) | cerrada | [105-hu-104-riesgos](../../specs/105-hu-104-riesgos/) | [#193](../../pull/193) | `test_riesgos_m4.py`, `tests/test_riesgos_m4.py` | — |
| HU-105 | [#161](../../issues/161) | cerrada | [106-hu-105-milestones-labels](../../specs/106-hu-105-milestones-labels/) | [#182](../../pull/182) | `test_labels.py`, `tests/test_labels.py` | — |
| HU-106 | [#162](../../issues/162) | cerrada | [107-hu-106-estado-gitlab](../../specs/107-hu-106-estado-gitlab/) | [#268](../../pull/268) | `tests/test_estado_gitlab.py` | — |
| HU-107 | [#163](../../issues/163) | cerrada | [108-hu-107-dor-dod](../../specs/108-hu-107-dor-dod/) | [#180](../../pull/180) | `test_dor_dod.py`, `tests/test_dor_dod.py` | — |
| HU-108 | [#164](../../issues/164) | cerrada | [109-hu-108-retrospectiva](../../specs/109-hu-108-retrospectiva/) | [#194](../../pull/194) | `test_retro_m4.py`, `tests/test_retro_m4.py` | — |
| HU-109 | [#165](../../issues/165) | cerrada | [110-hu-109-capacidad](../../specs/110-hu-109-capacidad/) | [#273](../../pull/273) | `test_capacidad.py`, `tests/test_capacidad.py` | — |
| HU-110 | [#166](../../issues/166) | cerrada | [111-hu-110-mlflow-droplet](../../specs/111-hu-110-mlflow-droplet/) | [#277](../../pull/277) | `test_mlflow_droplet.py`, `tests/test_mlflow_droplet.py` | — |
| HU-111 | [#167](../../issues/167) | cerrada | [112-hu-111-release](../../specs/112-hu-111-release/) | [#265](../../pull/265), [#274](../../pull/274) | `test_release_v1.py`, `tests/test_release_v1.py` | — |
| HU-112 | [#168](../../issues/168) | cerrada | [113-hu-112-glosario](../../specs/113-hu-112-glosario/) | [#195](../../pull/195) | `test_docs_readme.py`, `tests/test_docs_readme.py` | — |
| HU-113 | [#169](../../issues/169) | cerrada | [114-hu-113-rubrica](../../specs/114-hu-113-rubrica/) | [#196](../../pull/196) | `tests/test_tools_rubrica.py` | — |

## Cómo se actualiza

```bash
make trazabilidad        # imprime la matriz
make trazabilidad-write  # regenera este archivo
make trazabilidad-check  # compuerta de CI
```

No se edita a mano. La compuerta falla si una HU cerrada no tiene spec o
pruebas; las exenciones documentales se declaran en el módulo con su motivo.
