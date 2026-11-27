# Model Card — Detector de EPP (YOLO26n seleccionado)

> Documento de la rúbrica del M4: qué modelo se selecciona, de dónde sale, cómo
> funciona, dónde falla y con qué licencia. **YOLO26n es el modelo seleccionado; el
> modelo actualmente desplegado sigue siendo YOLO11s hasta completar el rollout**
> descrito en el [ADR 0009](adr/0009-modelo-productivo.md).

| Campo | Valor |
|---|---|
| **Modelo seleccionado** | `yolo26n-clean` — YOLO26n ajustado para 6 clases de EPP |
| **Estado** | Seleccionado; manifiesto actualizado, rollout del artefacto pendiente |
| **Tarea** | Detección de objetos (bounding boxes) |
| **Versión** | `yolo26n-clean` |
| **SHA256 del `best.pt`** | `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9` |
| **Artefacto** | `artifacts/models/yolo26n_clean/weights/best.pt` (5,47 MB, fuera de Git) |
| **Formato de servicio** | ONNX 640 (`best.onnx`, 9,86 MB) |
| **Referencia** | `sha256:FEFB1F1A…0F27F9` |
| **Fallback** | YOLO11s clean — `E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959` |
| **Responsable** | Hernán Estrada (`@HestradaUAO`) |
| **Última actualización** | 2026-11-23 |
| **Licencia del modelo** | AGPL-3.0 (heredada de Ultralytics) |

---

## 1. Modelo base

| Campo | Valor |
|---|---|
| Nombre | `yolo26n.pt` (Ultralytics YOLO26 nano) |
| Autor | Ultralytics |
| Repositorio / distribución | <https://github.com/ultralytics/ultralytics> |
| Arquitectura | CNN de detección en una etapa (YOLO26n) |
| Preentrenamiento | COCO (80 clases) |
| Versión de Ultralytics del ajuste | 8.4.216 |
| Licencia del modelo base | AGPL-3.0 |

El equipo **no entrena desde cero**: parte de `yolo26n.pt` y hace *fine-tuning* con el
script versionado [`src/ppe_detection/training/train.py`](../src/ppe_detection/training/train.py)
en GPU (Colab pagado). El backend sirve el artefacto resultante; no entrena en
inferencia.

### Configuración del ajuste

Metadatos del `run_manifest.json` del run `yolo26`:

| Parámetro | Valor |
|---|---|
| `model` | `yolo26n.pt` |
| `data` | `data_colab.yaml` (dataset limpio) |
| `eval_data` | `data_eval_colab.yaml` |
| `epochs` | 100 (`patience` 20) |
| `imgsz` | 640 |
| `batch` | -1 (AutoBatch) |
| `device` | `0` (GPU) |
| `seed` | 42 |
| `fecha` | 2026-11-22 |
| Clases | `Gloves, Vest, goggles, helmet, mask, safety_shoe` |

La identidad verificable del artefacto es su **SHA256**; coincide con el
`run_manifest.json`.

---

## 2. Dataset de origen

| Campo | Valor |
|---|---|
| Dataset | [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection) |
| Licencia | **CC-BY-4.0** (requiere atribución) |
| Empaquetado | `PPE.zip` (668 MB), estructura YOLO (`train/valid/test`) |
| Imágenes originales | 12.078 |
| Objetos anotados | 16.011 verificados (la tarjeta declara 16.014) |
| Tras limpieza | 10.941 imágenes → 7.659 / 2.188 / 1.094 |
| Clases | 6: `Gloves, Vest, goggles, helmet, mask, safety_shoe` |
| Desbalance | Vest 4.418 vs goggles 1.431 (3,1×) |
| SHA256 del ZIP | `3D1AE47B7F1401B02A05A997E413765D8F15529FB1944F2A5B1ADF536E909432` |

Hechos que condicionan el uso:

- **No existe clase `person` ni `no-EPP`.** El modelo reporta qué EPP aparecen, no si
  una persona cumple o incumple.
- La tarjeta del dataset **no declara la fuente original** ni el consentimiento de las
  personas que aparecen en las imágenes.
- El detalle del EDA y de la limpieza vive en [`docs/dataset/EDA.md`](dataset/EDA.md).

---

## 3. Métricas

Evaluación reproducible con `imgsz=640`, `conf=0.001`, `iou=0.7`, `seed=42`,
`device=cpu`. Informe completo: [`docs/evaluation/YOLO26.md`](evaluation/YOLO26.md).

### Test completo — 1.095 imágenes / 1.920 objetos

| Clase | P | R | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| **Global** | **0.893** | **0.842** | **0.892** | **0.614** |
| Gloves | 0.809 | 0.693 | 0.770 | 0.553 |
| Vest | 0.914 | 0.948 | 0.967 | 0.817 |
| goggles | 0.904 | 0.923 | 0.947 | 0.484 |
| helmet | 0.930 | 0.779 | 0.891 | 0.609 |
| mask | 0.928 | 0.894 | 0.923 | 0.676 |
| safety_shoe | 0.869 | 0.816 | 0.852 | 0.546 |

### Comparación con YOLO11s en test completo

| Modelo | P | R | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| YOLO11s | 0.800 | 0.767 | 0.810 | 0.516 |
| **YOLO26n** | **0.893** | **0.842** | **0.892** | **0.614** |

### Eval sin fuga — 492 imágenes / 1.013 objetos

| Clase | P | R | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| **Global** | **0.885** | **0.645** | **0.688** | **0.419** |
| safety_shoe | 1.000 | 0.000 | 0.000 | 0.000 |

La partición de 492 está dominada por `helmet` (573 de 1.013 objetos) y solo tiene 6
objetos de `safety_shoe`; sus métricas minoritarias no son representativas. No se usa
sola para decidir.

### Latencia CPU

| Medición | YOLO26n | YOLO11s |
|---|---:|---:|
| ONNX 640 p50 | **53,92 ms** | 183,52 ms |
| ONNX 640 p95 | **88,05 ms** | 280,63 ms |
| PyTorch 640 p50 | 80,42 ms | 194,80 ms |

YOLO26n ONNX 640 cumple el objetivo de **<100 ms** en el equipo de referencia
(i5-1235U, Windows 11). YOLO11s no cumple.

---

## 4. Limitaciones y sesgos

- **`safety_shoe` mejora** de mAP50 0.623 (YOLO11s) a **0.852**, pero sigue siendo una
  clase con menos soporte que `Vest` o `helmet`.
- **`Gloves`** es la clase más débil en mAP50-95 (0.553): guantes pequeños, ocluidos
  o de bajo contraste.
- **`helmet`** baja levemente el recall frente a YOLO11s (0.790 → 0.779).
- **Dominio:** imágenes del dataset; no se evaluaron cámaras, video ni escenas
  industriales reales.
- **Sesgos de representatividad:** el dataset no documenta su procedencia; la
  distribución por género, edad o etnia es desconocida y el desbalance favorece a
  `Vest`.
- **Uso no previsto:** vigilancia, certificación de cumplimiento o decisiones
  disciplinarias. El sistema es asistivo y reporta presencia de EPP.
- **Estado del despliegue:** YOLO26n está seleccionado, pero el servicio actual sigue
  ejecutando YOLO11s hasta el rollout.

---

## 5. Licencia y uso

| Elemento | Licencia | Obligación |
|---|---|---|
| Código del proyecto | **AGPL-3.0-only** | Compartir el código si se usa como servicio en red |
| Modelo base y derivado (Ultralytics) | **AGPL-3.0** | Misma obligación de red |
| Dataset | **CC-BY-4.0** | Atribuir `51ddhesh/PPE_Detection` |

> El proyecto **no usa MIT**: la licencia AGPL es una decisión registrada en el
> [ADR 0003](adr/0003-licencia-agpl.md) y es obligatoria por el detector Ultralytics.
> La interfaz y la API deben enlazar el código fuente cuando el sistema se publique.

**Uso responsable:** los resultados no certifican cumplimiento normativo. Una
detección ausente no prueba que falte el EPP; un falso positivo no prueba que esté
presente.

---

## 6. Reproducibilidad

```bash
# 1. Artefacto esperado (fuera de Git)
#    artifacts/models/yolo26n_clean/weights/best.pt
#    SHA256: FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9

# 2. Entrenamiento reproducible (Colab/Kaggle con GPU)
uv run python -m ppe_detection.training.train \
  --config configs/train/yolo26n.yaml --device 0

# 3. Evaluación local
uv run --extra inference python -m ppe_detection.evaluation.evaluate \
  --model artifacts/models/yolo26n_clean/weights/best.pt \
  --data dataset_limpio/data.yaml --split test \
  --output artifacts/eval --name yolo26n_test1094

# 4. Servir el modelo seleccionado (tras el rollout)
export PPE_MODEL_PATH=artifacts/models/yolo26n_clean/weights/best.pt
export PPE_MODEL_VERSION=yolo26n-clean
uv run --extra inference uvicorn ppe_detection.api.app:app --port 8000
```

- **Pesos y dataset nunca se versionan en Git.** La identidad se fija por SHA256.
- El entrenamiento se ejecuta solo en GPU con el script versionado; no se usan
  notebooks.
- Cada inferencia de la API publica `model_version`, `model_sha256`,
  `model_artifact` y `model_reference`.

---

## 7. Rollout y rollback

**Rollout:**

1. Publicar `best.pt` y `best.onnx` con SHA256.
2. Actualizar `models.lock` a `yolo26n-clean` (hecho).
3. Verificar la descarga con `ppe_detection.detection.artifact fetch`.
4. Montar el `best.pt` nuevo y reiniciar API/gRPC.
5. Ejecutar smoke REST/gRPC y medir latencia de servicio.

**Rollback:** restaurar `models.lock` a `yolo11s-clean`, montar el `best.pt` anterior,
reiniciar y repetir el smoke. No se reentrena.

---

## 8. Enlaces

- [ADR 0009 — modelo productivo](adr/0009-modelo-productivo.md)
- [Manifiesto del modelo (`models.lock`)](../models.lock)
- [Comparación YOLO26 vs YOLO11s](evaluation/YOLO26.md)
- [Entrenamiento YOLO26n](evaluation/yolo26-training.md)
- [Benchmark de latencia](evaluation/latencia.md)
- [MLflow: runbook](../operacion/mlflow.md)
- [MLflow: comparación de runs](evaluation/mlflow-comparacion.md)
- [Análisis de errores FP/FN](evaluation/errores.md)
- [SPI-03 — compatibilidad YOLO26](spikes/SPI-03-yolo26.md)
- [EDA y limpieza del dataset](dataset/EDA.md)
- [ADR 0001 — modelo base](adr/0001-modelo-base.md)
- [ADR 0002 — dataset](adr/0002-dataset.md)
- [ADR 0003 — licencia](adr/0003-licencia-agpl.md)
- [Dataset en Hugging Face](https://huggingface.co/datasets/51ddhesh/PPE_Detection)
