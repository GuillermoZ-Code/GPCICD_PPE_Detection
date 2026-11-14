# Model Card — Detector de EPP (YOLO11s ajustado)

> Documento de la rúbrica del M3: qué modelo usa el backend, de dónde salió, qué tan
> bien funciona, dónde falla y con qué licencia. Debe coincidir con el artefacto que
> carga la API (`PPE_MODEL_PATH`) y con la versión registrada en MLflow.

| Campo | Valor |
|---|---|
| **Modelo** | `yolo11s-clean` — YOLO11s ajustado para 6 clases de EPP |
| **Tarea** | Detección de objetos (bounding boxes) |
| **Versión** | `yolo11s-clean` (`PPE_MODEL_VERSION`) |
| **SHA256** | `E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959` |
| **Artefacto** | `artifacts/drive/yolo11s_clean/weights/best.pt` (18,3 MB, fuera de Git) |
| **Referencia** | `sha256:E51EB080…D7A9959` (`model_reference` en REST y gRPC) |
| **Responsable** | Hernán Estrada (`@HestradaUAO`) |
| **Última actualización** | 2026-11-13 |
| **Licencia del modelo** | AGPL-3.0 (heredada de Ultralytics) |

---

## 1. Modelo base

| Campo | Valor |
|---|---|
| Nombre | `yolo11s.pt` (Ultralytics YOLO11 small) |
| Autor | Ultralytics |
| Repositorio / distribución | <https://github.com/ultralytics/ultralytics> · <https://huggingface.co/Ultralytics/YOLO11> |
| Arquitectura | CNN de detección en una etapa (YOLO11s) |
| Preentrenamiento | COCO (80 clases), pesos `yolo11s.pt` |
| Versión de Ultralytics del ajuste | 8.4.198 |
| Licencia del modelo base | AGPL-3.0 |

El equipo **no entrena desde cero**: parte de los pesos preentrenados de Ultralytics y
hace *fine-tuning* con el script versionado
[`src/ppe_detection/training/train.py`](../src/ppe_detection/training/train.py) en GPU
(Colab). El backend sirve el artefacto resultante; no entrena en inferencia.

### Configuración del ajuste

Metadatos leídos del propio `best.pt` (`train_args`):

| Parámetro | Valor |
|---|---|
| `model` | `yolo11s.pt` |
| `data` | `data_colab.yaml` (dataset limpio `ds_base`) |
| `epochs` | 100 (`patience` 20) |
| `imgsz` | 640 |
| `batch` | 47 (AutoBatch) |
| `optimizer` | MuSGD, `lr0 = 0.01` |
| `device` | `0` (GPU) |
| `seed` | 42 |
| `date` | 2026-11-02 |
| Clases | `Gloves, Vest, goggles, helmet, mask, safety_shoe` |

> La revisión del modelo base no queda grabada en el `.pt`; la identidad verificable
> del artefacto derivado es su **SHA256**, que es el que publica la API. Para
> reproducir, use `yolo11s.pt` de Ultralytics 8.4.198 y el script del repositorio.

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
- El detalle del EDA y de la limpieza vive en
  [`docs/dataset/EDA.md`](dataset/EDA.md).

---

## 3. Métricas

Evaluación reproducible con `imgsz=640`, `conf=0.001`, `iou=0.7`, `seed=42`,
`device=cpu`. Informe completo:
[`docs/evaluation/HU-008.md`](evaluation/HU-008.md).

### Test limpio — 1.094 imágenes / 1.905 objetos

| Clase | P | R | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| **Global** | **0.800** | **0.767** | **0.810** | **0.516** |
| Gloves | 0.598 | 0.637 | 0.613 | 0.407 |
| Vest | 0.883 | 0.905 | 0.931 | 0.712 |
| goggles | 0.819 | 0.909 | 0.926 | 0.464 |
| helmet | 0.904 | 0.790 | 0.874 | 0.595 |
| mask | 0.917 | 0.833 | 0.894 | 0.600 |
| safety_shoe | 0.679 | 0.530 | 0.623 | 0.318 |

### Eval sin fuga — 492 imágenes / 1.013 objetos

| Clase | P | R | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| **Global** | **0.874** | **0.645** | **0.726** | **0.424** |
| safety_shoe | 1.000 | 0.000 | 0.240 | 0.048 |

La partición de 492 está dominada por `helmet` (573 de 1.013 objetos) y solo tiene 6
objetos de `safety_shoe`; sus métricas minoritarias no son representativas.

### Comparación con el baseline

| Modelo | Partición | P | R | mAP50 | mAP50-95 |
|---|---|---:|---:|---:|---:|
| YOLOv8n preentrenado (SPI-02) | Eval 492 | 0.681 | 0.564 | 0.639 | 0.375 |
| **YOLO11s ajustado** | Eval 492 | **0.874** | **0.645** | **0.726** | **0.424** |

La diferencia incluye arquitectura, datos y ajuste; no es una comparación pura de
fine-tuning.

### Latencia de servicio (CPU)

| Medición | Valor |
|---|---|
| Inferencia a 640 px (i5-1235U, SPI-01) | **136–158 ms/imagen** |
| Validación a 640 px (i9-13900H, HU-008) | 300,7 ms/imagen |
| Sesión medida con `tracking benchmark` (640 px, equipo de desarrollo) | **82,4 ms media · 90,3 ms p95 · 12,1 fps** |
| Sesión medida con `tracking benchmark` (416 px, equipo de desarrollo) | **41,4 ms media · 44,4 ms p95 · 24,1 fps** |

**No se cumple el objetivo de <100 ms a 640 px.** El tradeoff y las alternativas
(ONNX, `imgsz` menor) están documentados en
[`docs/spikes/SPI-01`](spikes/SPI-01-compatibilidad-yolo.md).

---

## 4. Limitaciones y sesgos

- **`safety_shoe` es la clase más débil** (mAP50 0.623, R 0.530) y en el eval de 492
  solo hay 6 objetos. No se deben sacar conclusiones fuertes sobre ella.
- **`Gloves`** es la segunda clase más débil (mAP50 0.613): guantes pequeños, ocluidos o
  de bajo contraste.
- **Falsos negativos en `Vest`** cuando hay dos chalecos solapados o uno parcialmente
  ocluido.
- **Falsos positivos de `goggles`** sobre patrones de chalecos o imágenes de producto.
- **Dominio:** imágenes del dataset; no se evaluaron cámaras, video ni escenas
  industriales reales.
- **Sesgos de representatividad:** el dataset no documenta su procedencia, la
  distribución por género, edad o etnia es desconocida y el desbalance favorece a
  `Vest`.
- **Uso no previsto:** vigilancia, certificación de cumplimiento o decisiones
  disciplinarias. El sistema es asistivo y reporta presencia de EPP.

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
# 1. Obtener el artefacto (fuera de Git) y verificar su identidad
#    Ruta esperada: artifacts/drive/yolo11s_clean/weights/best.pt
#    SHA256: E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959

# 2. Servir la API con el artefacto
export PPE_MODEL_PATH=artifacts/drive/yolo11s_clean/weights/best.pt
uv run --extra inference uvicorn ppe_detection.api.app:app --port 8000

# 3. Verificar la identidad publicada
curl http://127.0.0.1:8000/health

# 4. Repetir una medición y registrarla en MLflow
uv run --extra tracking --extra inference python -m ppe_detection.tracking benchmark \
  --model "$PPE_MODEL_PATH" --images artifacts/samples --iterations 30 --imgsz 640
```

- **Pesos y dataset nunca se versionan en Git.** La identidad se fija por SHA256.
- El entrenamiento se ejecuta solo en GPU (Colab/Kaggle) con el script versionado; no
  se usan notebooks.
- Cada inferencia de la API publica `model_version`, `model_sha256`,
  `model_artifact` y `model_reference`.

---

## 7. Enlaces

- [Informe de evaluación HU-008](evaluation/HU-008.md)
- [EDA y limpieza del dataset](dataset/EDA.md)
- [SPI-01 — compatibilidad y latencia](spikes/SPI-01-compatibilidad-yolo.md)
- [SPI-02 — baseline y entrenamiento](spikes/SPI-02-baseline-evaluacion.md)
- [ADR 0001 — modelo base](adr/0001-modelo-base.md)
- [ADR 0002 — dataset](adr/0002-dataset.md)
- [ADR 0003 — licencia](adr/0003-licencia-agpl.md)
- [Dataset en Hugging Face](https://huggingface.co/datasets/51ddhesh/PPE_Detection)
