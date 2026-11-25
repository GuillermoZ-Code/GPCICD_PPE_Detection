# Comparación de runs

> **Generado:** 2026-11-24
> **Tracking URI:** `file:./mlruns`
> **Fuente:** runs registrados en MLflow; el artefacto se referencia por SHA256.

| Run | mAP50 | mAP50-95 | Precision | Recall | Artefacto | Enlace |
|---|---:|---:|---:|---:|---|---|
| eval-test-yolo26n | 0.892 | 0.614 | 0.893 | 0.842 | `artifacts/models/yolo26n_clean/weights/best.pt` sha256:FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9 | [eval-test-yolo26n](file:./mlruns/#/runs/a1b2c3d4e5f6) |
| eval-test-yolo11s | 0.810 | 0.516 | 0.800 | 0.767 | `artifacts/models/yolo11s_clean/weights/best.pt` sha256:E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959 | [eval-test-yolo11s](file:./mlruns/#/runs/f6e5d4c3b2a1) |

## Cómo se regenera

```bash
python -m ppe_detection.tracking comparar --runs <id> <id> --output docs/evaluation/mlflow-comparacion.md
```

> **Nota:** esta muestra se construyó con los resúmenes de la evaluación de HU-019
> (`docs/evaluation/YOLO26.md`); se regenera contra MLflow cuando los runs existen en
> el Droplet.
