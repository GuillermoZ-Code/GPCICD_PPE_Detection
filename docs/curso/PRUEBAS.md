# Inventario de pruebas — GPCICD PPE Detection

> **Generado:** 2026-11-24 01:48 UTC · `make pruebas`
> **Requisito del curso:** ≥ 400 pruebas unitarias (mínimo, no techo).
> **Fuente:** casos recolectados por pytest y por Vitest; no se edita a mano.

## 1. Resumen

| Suite | Herramienta | Archivos | Pruebas | Comando |
|-------|-------------|---------:|--------:|---------|
| Backend | pytest | 38 | 453 | `make test` |
| Frontend | Vitest | 9 | 76 | `make frontend-test` |
| **Total** | | **47** | **529** | `make check` + `make frontend-check` |

## 2. Desglose por archivo

| Archivo | Suite | Pruebas | Dueño |
|---|---|---:|---|
| tests/test_api.py | pytest | 12 | Eliana Cardona |
| tests/test_api_contract.py | pytest | 15 | Eliana Cardona |
| tests/test_artifact_fetch.py | pytest | 8 | sin dueño |
| tests/test_calidad.py | pytest | 5 | sin dueño |
| tests/test_contracts.py | pytest | 28 | sin dueño |
| tests/test_docker.py | pytest | 9 | sin dueño |
| tests/test_docker_assets.py | pytest | 13 | sin dueño |
| tests/test_dor_dod.py | pytest | 4 | sin dueño |
| tests/test_estado.py | pytest | 10 | Jesús Riveros |
| tests/test_estado_tools.py | pytest | 10 | Jesús Riveros |
| tests/test_evaluation.py | pytest | 9 | Hernán Estrada |
| tests/test_evaluation_report.py | pytest | 10 | Hernán Estrada |
| tests/test_geometry.py | pytest | 20 | sin dueño |
| tests/test_grpc.py | pytest | 9 | Eliana Cardona |
| tests/test_grpc_contract.py | pytest | 12 | Eliana Cardona |
| tests/test_health.py | pytest | 7 | sin dueño |
| tests/test_image_loader.py | pytest | 17 | sin dueño |
| tests/test_image_validation.py | pytest | 7 | sin dueño |
| tests/test_io_edge_cases.py | pytest | 10 | Eliana Cardona |
| tests/test_issue_template.py | pytest | 6 | sin dueño |
| tests/test_labels.py | pytest | 4 | sin dueño |
| tests/test_launcher.py | pytest | 5 | sin dueño |
| tests/test_metrics.py | pytest | 35 | sin dueño |
| tests/test_metrics_golden.py | pytest | 9 | sin dueño |
| tests/test_model_manifest.py | pytest | 10 | sin dueño |
| tests/test_model_version.py | pytest | 21 | sin dueño |
| tests/test_overlay.py | pytest | 7 | sin dueño |
| tests/test_overlay_launcher.py | pytest | 5 | sin dueño |
| tests/test_ownership.py | pytest | 17 | Guillermo Zabala |
| tests/test_predict.py | pytest | 16 | sin dueño |
| tests/test_results.py | pytest | 10 | sin dueño |
| tests/test_smoke.py | pytest | 1 | sin dueño |
| tests/test_tools_pruebas.py | pytest | 6 | Jesús Riveros |
| tests/test_tracking.py | pytest | 11 | Jesús Riveros |
| tests/test_tracking_benchmark.py | pytest | 15 | Jesús Riveros |
| tests/test_tracking_mlflow.py | pytest | 25 | Jesús Riveros |
| tests/test_training.py | pytest | 15 | sin dueño |
| tests/test_yolo_detector.py | pytest | 20 | sin dueño |
| frontend/src/App.test.tsx | vitest | 16 | Guillermo Zabala |
| frontend/src/api/client.test.ts | vitest | 17 | Guillermo Zabala |
| frontend/src/components/AnnotatedCanvas.test.tsx | vitest | 6 | Guillermo Zabala |
| frontend/src/components/DetectionTable.test.tsx | vitest | 7 | Guillermo Zabala |
| frontend/src/components/SettingsDrawer.test.tsx | vitest | 5 | Guillermo Zabala |
| frontend/src/config.test.ts | vitest | 5 | Guillermo Zabala |
| frontend/src/download.test.ts | vitest | 3 | Guillermo Zabala |
| frontend/src/filter.test.ts | vitest | 3 | Guillermo Zabala |
| frontend/src/validate.test.ts | vitest | 14 | Guillermo Zabala |

## 3. Totales por integrante

| Integrante | pytest | Vitest | Total |
|---|---:|---:|---:|
| Eliana Cardona | 58 | 0 | 58 |
| Guillermo Zabala | 17 | 76 | 93 |
| Hernán Estrada | 19 | 0 | 19 |
| Jesús Riveros | 77 | 0 | 77 |
| sin dueño | 282 | 0 | 282 |

## 4. Cómo se actualiza

```bash
make pruebas        # imprime el resumen
make pruebas-write  # regenera este archivo
```

El dueño de `docs/curso/PRUEBAS.md` lo regenera y lo commitea. El plan
hacia 1.200 pruebas vive en `docs/curso/PLAN-PRUEBAS.md`.
