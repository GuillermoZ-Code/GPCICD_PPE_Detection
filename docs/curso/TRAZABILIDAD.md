# Matriz de trazabilidad — GPCICD PPE Detection

> **Generado:** 2026-11-24 02:14 UTC · `make trazabilidad-write`
> **HU:** 113 · completas: 26 · incompletas: 87
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
| HU-014 | [#14](../../issues/14) | abierta | — | — | — | spec, pr, pruebas |
| HU-015 | [#15](../../issues/15) | abierta | — | — | — | spec, pr, pruebas |
| HU-016 | [#72](../../issues/72) | cerrada | [017-hu-016-spike-yolo26](../../specs/017-hu-016-spike-yolo26/) | [#173](../../pull/173) | — | pruebas |
| HU-017 | [#73](../../issues/73) | cerrada | [018-hu-017-train-yolo26](../../specs/018-hu-017-train-yolo26/) | [#181](../../pull/181) | `tests/test_training.py` | — |
| HU-018 | [#74](../../issues/74) | cerrada | [019-hu-018-entrenar-yolo26](../../specs/019-hu-018-entrenar-yolo26/) | [#174](../../pull/174) | — | pruebas |
| HU-019 | [#75](../../issues/75) | cerrada | [020-hu-019-comparar-yolo26-yolo11](../../specs/020-hu-019-comparar-yolo26-yolo11/) | [#178](../../pull/178) | — | pruebas |
| HU-020 | [#76](../../issues/76) | cerrada | [021-hu-020-benchmark-latencia](../../specs/021-hu-020-benchmark-latencia/) | [#176](../../pull/176) | `tests/test_tracking_benchmark.py` | — |
| HU-021 | [#77](../../issues/77) | cerrada | [022-hu-021-detector-nms-free](../../specs/022-hu-021-detector-nms-free/) | [#177](../../pull/177) | `tests/test_yolo_detector.py` | — |
| HU-022 | [#78](../../issues/78) | cerrada | [023-hu-022-export-onnx](../../specs/023-hu-022-export-onnx/) | [#185](../../pull/185) | `tests/test_onnx_backend.py` | — |
| HU-023 | [#79](../../issues/79) | cerrada | [024-hu-023-adr-modelo-productivo](../../specs/024-hu-023-adr-modelo-productivo/) | [#184](../../pull/184) | — | pruebas |
| HU-024 | [#80](../../issues/80) | abierta | — | — | — | spec, pr, pruebas |
| HU-025 | [#81](../../issues/81) | cerrada | [026-hu-025-models-lock](../../specs/026-hu-025-models-lock/) | [#171](../../pull/171) | `tests/test_model_manifest.py` | — |
| HU-026 | [#82](../../issues/82) | cerrada | [027-hu-026-fetch-model](../../specs/027-hu-026-fetch-model/) | [#175](../../pull/175) | `tests/test_artifact_fetch.py` | — |
| HU-027 | [#83](../../issues/83) | abierta | — | — | — | spec, pr, pruebas |
| HU-028 | [#84](../../issues/84) | abierta | — | — | — | spec, pr, pruebas |
| HU-029 | [#85](../../issues/85) | abierta | — | — | — | spec, pr, pruebas |
| HU-030 | [#86](../../issues/86) | abierta | — | — | — | spec, pr, pruebas |
| HU-031 | [#87](../../issues/87) | abierta | — | — | — | spec, pr, pruebas |
| HU-032 | [#88](../../issues/88) | abierta | — | — | — | spec, pr, pruebas |
| HU-033 | [#89](../../issues/89) | cerrada | [034-hu-033-regresion-metricas](../../specs/034-hu-033-regresion-metricas/) | [#172](../../pull/172) | `test_metrics_golden.py`, `tests/test_metrics_golden.py` | — |
| HU-034 | [#90](../../issues/90) | abierta | — | — | — | spec, pr, pruebas |
| HU-035 | [#91](../../issues/91) | abierta | — | — | — | spec, pr, pruebas |
| HU-036 | [#92](../../issues/92) | abierta | — | — | — | spec, pr, pruebas |
| HU-037 | [#93](../../issues/93) | abierta | — | — | — | spec, pr, pruebas |
| HU-038 | [#94](../../issues/94) | abierta | — | — | — | spec, pr, pruebas |
| HU-039 | [#95](../../issues/95) | abierta | — | — | — | spec, pr, pruebas |
| HU-040 | [#96](../../issues/96) | abierta | — | — | — | spec, pr, pruebas |
| HU-041 | [#97](../../issues/97) | abierta | — | — | — | spec, pr, pruebas |
| HU-042 | [#98](../../issues/98) | abierta | — | — | — | spec, pr, pruebas |
| HU-043 | [#99](../../issues/99) | abierta | — | — | — | spec, pr, pruebas |
| HU-044 | [#100](../../issues/100) | abierta | — | — | — | spec, pr, pruebas |
| HU-045 | [#101](../../issues/101) | abierta | — | — | — | spec, pr, pruebas |
| HU-046 | [#102](../../issues/102) | abierta | — | — | — | spec, pr, pruebas |
| HU-047 | [#103](../../issues/103) | abierta | — | — | — | spec, pr, pruebas |
| HU-048 | [#104](../../issues/104) | abierta | — | — | — | spec, pr, pruebas |
| HU-049 | [#105](../../issues/105) | abierta | — | — | — | spec, pr, pruebas |
| HU-050 | [#106](../../issues/106) | abierta | — | — | — | spec, pr, pruebas |
| HU-051 | [#107](../../issues/107) | abierta | — | — | — | spec, pr, pruebas |
| HU-052 | [#108](../../issues/108) | abierta | — | — | — | spec, pr, pruebas |
| HU-053 | [#109](../../issues/109) | abierta | — | — | — | spec, pr, pruebas |
| HU-054 | [#110](../../issues/110) | abierta | — | — | — | spec, pr, pruebas |
| HU-055 | [#111](../../issues/111) | abierta | — | — | — | spec, pr, pruebas |
| HU-056 | [#112](../../issues/112) | abierta | — | — | — | spec, pr, pruebas |
| HU-057 | [#113](../../issues/113) | abierta | — | — | — | spec, pr, pruebas |
| HU-058 | [#114](../../issues/114) | abierta | — | — | — | spec, pr, pruebas |
| HU-059 | [#115](../../issues/115) | abierta | — | — | — | spec, pr, pruebas |
| HU-060 | [#116](../../issues/116) | abierta | — | — | — | spec, pr, pruebas |
| HU-061 | [#117](../../issues/117) | abierta | — | — | — | spec, pr, pruebas |
| HU-062 | [#118](../../issues/118) | abierta | — | — | — | spec, pr, pruebas |
| HU-063 | [#119](../../issues/119) | abierta | — | — | — | spec, pr, pruebas |
| HU-064 | [#120](../../issues/120) | abierta | — | — | — | spec, pr, pruebas |
| HU-065 | [#121](../../issues/121) | abierta | — | — | — | spec, pr, pruebas |
| HU-066 | [#122](../../issues/122) | abierta | — | — | — | spec, pr, pruebas |
| HU-067 | [#123](../../issues/123) | abierta | — | — | — | spec, pr, pruebas |
| HU-068 | [#124](../../issues/124) | abierta | — | — | — | spec, pr, pruebas |
| HU-069 | [#125](../../issues/125) | abierta | — | — | — | spec, pr, pruebas |
| HU-070 | [#126](../../issues/126) | abierta | — | — | — | spec, pr, pruebas |
| HU-071 | [#127](../../issues/127) | abierta | — | — | — | spec, pr, pruebas |
| HU-072 | [#128](../../issues/128) | abierta | — | — | — | spec, pr, pruebas |
| HU-073 | [#129](../../issues/129) | abierta | — | — | — | spec, pr, pruebas |
| HU-074 | [#130](../../issues/130) | abierta | — | — | — | spec, pr, pruebas |
| HU-075 | [#131](../../issues/131) | abierta | — | — | — | spec, pr, pruebas |
| HU-076 | [#132](../../issues/132) | abierta | — | — | — | spec, pr, pruebas |
| HU-077 | [#133](../../issues/133) | abierta | — | — | — | spec, pr, pruebas |
| HU-078 | [#134](../../issues/134) | abierta | — | — | — | spec, pr, pruebas |
| HU-079 | [#135](../../issues/135) | abierta | — | — | — | spec, pr, pruebas |
| HU-080 | [#136](../../issues/136) | abierta | — | — | — | spec, pr, pruebas |
| HU-081 | [#137](../../issues/137) | abierta | — | — | — | spec, pr, pruebas |
| HU-082 | [#138](../../issues/138) | abierta | — | — | `tests/test_ownership.py` | spec, pr |
| HU-083 | [#139](../../issues/139) | abierta | — | — | — | spec, pr, pruebas |
| HU-084 | [#140](../../issues/140) | abierta | — | — | — | spec, pr, pruebas |
| HU-085 | [#141](../../issues/141) | abierta | — | — | — | spec, pr, pruebas |
| HU-086 | [#142](../../issues/142) | abierta | — | — | — | spec, pr, pruebas |
| HU-087 | [#143](../../issues/143) | abierta | — | — | — | spec, pr, pruebas |
| HU-088 | [#144](../../issues/144) | abierta | — | — | — | spec, pr, pruebas |
| HU-089 | [#145](../../issues/145) | cerrada | — | — | — | spec, pr, pruebas |
| HU-090 | [#146](../../issues/146) | abierta | — | — | — | spec, pr, pruebas |
| HU-091 | [#147](../../issues/147) | cerrada | [092-hu-091-plantilla-hu](../../specs/092-hu-091-plantilla-hu/) | [#179](../../pull/179) | `test_issue_template.py`, `tests/test_issue_template.py` | — |
| HU-092 | [#148](../../issues/148) | cerrada | [093-hu-092-backlog-espejo](../../specs/093-hu-092-backlog-espejo/) | [#188](../../pull/188) | `test_backlog_mirror.py`, `tests/test_backlog_mirror.py` | — |
| HU-093 | [#149](../../issues/149) | abierta | [094-hu-093-matriz-trazabilidad](../../specs/094-hu-093-matriz-trazabilidad/) | — | `...test.tsx`, `tests/test_tools_trazabilidad.py` | pr |
| HU-094 | [#150](../../issues/150) | cerrada | [095-hu-094-conteo-pruebas](../../specs/095-hu-094-conteo-pruebas/) | [#183](../../pull/183) | `tests/test_tools_pruebas.py` | — |
| HU-095 | [#151](../../issues/151) | cerrada | [096-hu-095-corregir-pruebas-md](../../specs/096-hu-095-corregir-pruebas-md/) | [#186](../../pull/186) | `test_plan_pruebas.py`, `tests/test_plan_pruebas.py` | — |
| HU-096 | [#152](../../issues/152) | abierta | — | — | — | spec, pr, pruebas |
| HU-097 | [#153](../../issues/153) | abierta | — | — | — | spec, pr, pruebas |
| HU-098 | [#154](../../issues/154) | abierta | — | — | — | spec, pr, pruebas |
| HU-099 | [#155](../../issues/155) | abierta | — | — | — | spec, pr, pruebas |
| HU-100 | [#156](../../issues/156) | abierta | — | — | — | spec, pr, pruebas |
| HU-101 | [#157](../../issues/157) | abierta | — | — | — | spec, pr, pruebas |
| HU-102 | [#158](../../issues/158) | abierta | — | — | — | spec, pr, pruebas |
| HU-103 | [#159](../../issues/159) | abierta | — | — | — | spec, pr, pruebas |
| HU-104 | [#160](../../issues/160) | abierta | — | — | — | spec, pr, pruebas |
| HU-105 | [#161](../../issues/161) | cerrada | [106-hu-105-milestones-labels](../../specs/106-hu-105-milestones-labels/) | [#182](../../pull/182) | `test_labels.py`, `tests/test_labels.py` | — |
| HU-106 | [#162](../../issues/162) | abierta | — | — | — | spec, pr, pruebas |
| HU-107 | [#163](../../issues/163) | cerrada | [108-hu-107-dor-dod](../../specs/108-hu-107-dor-dod/) | [#180](../../pull/180) | `test_dor_dod.py`, `tests/test_dor_dod.py` | — |
| HU-108 | [#164](../../issues/164) | abierta | — | — | — | spec, pr, pruebas |
| HU-109 | [#165](../../issues/165) | abierta | — | — | — | spec, pr, pruebas |
| HU-110 | [#166](../../issues/166) | abierta | — | — | — | spec, pr, pruebas |
| HU-111 | [#167](../../issues/167) | abierta | — | — | — | spec, pr, pruebas |
| HU-112 | [#168](../../issues/168) | abierta | — | — | — | spec, pr, pruebas |
| HU-113 | [#169](../../issues/169) | abierta | — | — | — | spec, pr, pruebas |

## Cómo se actualiza

```bash
make trazabilidad        # imprime la matriz
make trazabilidad-write  # regenera este archivo
make trazabilidad-check  # compuerta de CI
```

No se edita a mano. La compuerta falla si una HU cerrada no tiene spec o
pruebas; las exenciones documentales se declaran en el módulo con su motivo.
