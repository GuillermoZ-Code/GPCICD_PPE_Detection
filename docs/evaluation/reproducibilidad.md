# Reproducibilidad del entrenamiento — HU-040

**Estado:** Documentado.

**Fecha:** 2026-11-26.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #96.

---

## 1. Alcance

Esta guía permite repetir el fine-tuning de **YOLO26n** y verificar el artefacto que
usa el servicio. No descarga ni versiona el dataset, los pesos ni las imágenes: solo
documenta comandos, versiones y evidencias.

Fuentes de verdad:

- [Entrenamiento YOLO26n](yolo26-training.md)
- [Model Card](../model-card.md)
- [Runbook de MLflow](../operacion/mlflow.md)
- [Comparación de runs](mlflow-comparacion.md)

## 2. Entorno y hardware

| Elemento | Entrenamiento | Evaluación/servicio |
|---|---|---|
| Plataforma | Colab pago con GPU | CPU local / CI |
| Python | 3.13.16 | 3.13.7+ |
| Ultralytics | 8.4.216 | 8.4.202+ |
| torch | 2.15.0 | 2.15.0+cpu |
| GPU/CPU | GPU del entorno Colab | Intel Core i5-1235U, 10 núcleos / 12 hilos |
| `imgsz` | 640 | 640 |
| `batch` | -1 (AutoBatch) | 1 (servicio) |
| Semilla | 42 | 42 |
| Épocas | 100 (`patience=20`) | No aplica |

El entrenamiento **no se ejecuta en CPU local**: la CPU no es viable para este
fine-tuning. Colab/Kaggle se usan solo como cómputo GPU y ejecutan el script
versionado; no se versionan notebooks.

## 3. Datos y versiones

| Dato | Valor |
|---|---|
| Dataset | `51ddhesh/PPE_Detection`, CC-BY-4.0 |
| YAML de entrenamiento | `data_colab.yaml` |
| YAML de evaluación | `data_eval_colab.yaml` |
| SHA256 del YAML de train | `da1fc5d0d33427b1578dbf3fa10b789bb02218bcfb4762b46f284bf8f7e6750d` |
| SHA256 del YAML de eval | `1bf9a9157734b30f5b3312375e15d1bc43e972ddb94b0a84d9086bb5df55c96c` |
| Modelo base | `yolo26n.pt` (COCO) |
| Clases | `Gloves, Vest, goggles, helmet, mask, safety_shoe` |
| Particiones | 7.658 train / 2.188 valid / 1.095 test |

Los YAML y los pesos viven fuera de Git; la ficha del dataset está en
[`docs/dataset/README.md`](../dataset/README.md).

## 4. Pasos con `uv`

Desde la raíz del repositorio:

```bash
# 1. Sincronizar el entorno y las herramientas de entrenamiento
uv sync --all-extras

# 2. Exportar las rutas externas al repositorio
export DATASET_DIR=/ruta/al/dataset
export MLFLOW_TRACKING_URI=file:/ruta/a/mlruns

# 3. Ejecutar el script versionado (GPU)
uv run --extra inference python -m ppe_detection.training.train \
  --config configs/train/yolo26n.yaml \
  --data "$DATASET_DIR/data_colab.yaml" \
  --eval-data "$DATASET_DIR/data_eval_colab.yaml" \
  --device 0 \
  --name yolo26 \
  --seed 42
```

El comando no usa `pip`, `requirements.txt` ni notebooks. El manifiesto de la corrida
se escribe junto a los pesos y conserva la configuración, versiones y SHA256.

## 5. Tiempos de referencia

| Fase | Tiempo |
|---|---|
| Fine-tuning YOLO26n (GPU Colab) | **~85 min** (00:11 → 01:36 UTC) |
| Evaluación test 1.095 imágenes (CPU) | minutos; depende del equipo |
| Inferencia ONNX 640 (CPU i5-1235U) | p50 33,94 ms / p95 40,90 ms |

La medición de latencia es del equipo de referencia, no del Droplet.

## 6. MLflow

El entrenamiento registra la corrida en el tracking configurado:

```bash
uv run --extra tracking mlflow ui --backend-store-uri "$MLFLOW_TRACKING_URI"
```

La comparación reproducible de los runs de YOLO26n y YOLO11s está en
[`docs/evaluation/mlflow-comparacion.md`](mlflow-comparacion.md). El procedimiento
para registrar una evaluación y adjuntar figuras está en
[`docs/operacion/mlflow.md`](../operacion/mlflow.md).

En el entorno local, el tracking por defecto es `sqlite:///mlflow.db`; en Colab se
puede usar un directorio de Drive como `file:.../mlruns`. Los runs no se versionan.

## 7. Paquete y artefacto del modelo

El manifiesto canónico es [`models.lock`](../../models.lock):

```toml
version = "yolo26n-clean"
sha256 = "FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9"
```

Artefactos fuera de Git:

```text
artifacts/models/yolo26n_clean/weights/best.pt
artifacts/models/yolo26n_clean/weights/best.onnx
```

Para descargar y verificar el artefacto:

```bash
uv run python -m ppe_detection.detection.artifact fetch --manifest models.lock
```

Los pesos no se suben al repositorio; la identidad se referencia por SHA256.

## 8. Verificación

```bash
# Comprobar que el artefacto coincide con el manifiesto
uv run python -m ppe_detection.detection.artifact fetch \
  --manifest models.lock \
  --output artifacts/models/yolo26n_clean/weights/best.pt

# Evaluación reproducible del test
uv run --extra inference python -m ppe_detection.evaluation.evaluate \
  --model artifacts/models/yolo26n_clean/weights/best.pt \
  --data "$DATASET_DIR/data.yaml" \
  --split test \
  --output artifacts/eval \
  --name yolo26n_test1094
```

Las métricas de referencia están en [`docs/evaluation/YOLO26.md`](YOLO26.md) y en la
[Model Card](../model-card.md).

## 9. Límites

- La corrida original se ejecutó en Colab; no se conserva el entorno exacto de la GPU.
- El dataset no se publica; se documenta su origen, licencia y SHA256 del ZIP.
- Los resultados dependen de la versión de Ultralytics, CUDA y la GPU.
- La latencia de entrenamiento no es la latencia del servicio.
- No se publican imágenes ni datos personales.
