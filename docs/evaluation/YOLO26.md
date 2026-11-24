# Evaluación comparativa YOLO26 vs YOLO11s — HU-019

**Estado:** Completado.

**Fecha:** 2026-11-23.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #75.

---

## 1. Pregunta

¿YOLO26n mejora a YOLO11s en el mismo conjunto de evaluación y justifica el cambio
de modelo productivo?

## 2. Artefactos comparados

| Modelo | Artefacto | SHA256 | Clases |
|---|---|---|---|
| YOLO11s clean | `artifacts/models/yolo11s_clean/weights/best.pt` | `E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959` | 6 EPP |
| YOLO26n clean | `artifacts/models/yolo26n_clean/weights/best.pt` | `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9` | 6 EPP |

Los pesos están fuera de Git.

## 3. Configuración

| Parámetro | Valor |
|---|---|
| `imgsz` | 640 |
| `conf` | 0.001 |
| `iou` | 0.7 |
| `seed` | 42 |
| `device` | CPU |
| Evaluación | `ppe_detection.evaluation.evaluate` |
| YOLO11s | entrenado con 8.4.198; evaluado con 8.4.202 |
| YOLO26n | entrenado con 8.4.216; evaluado con 8.4.202 |

Ambos modelos se evalúan con la misma configuración y las mismas particiones.

## 4. Eval sin fuga — 492 imágenes / 1.013 objetos

### 4.1 Global

| Modelo | P | R | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| YOLO11s | **0,874** | **0,645** | **0,726** | **0,424** |
| YOLO26n | 0,885 | 0,645 | 0,688 | 0,419 |
| Diferencia | +0,011 | 0,000 | **−0,038** | **−0,005** |

En esta partición YOLO26n **no mejora** el mAP global: sube ligeramente la precisión,
mantiene el recall y baja mAP50/mAP50-95.

### 4.2 Por clase

| Clase | YOLO11s P | YOLO11s R | YOLO11s mAP50 | YOLO11s mAP50-95 | YOLO26n P | YOLO26n R | YOLO26n mAP50 | YOLO26n mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Gloves | 0,726 | 0,626 | 0,654 | 0,427 | 0,794 | 0,594 | 0,673 | 0,427 |
| Vest | 0,751 | 0,854 | 0,834 | 0,556 | 0,772 | 0,902 | 0,863 | 0,579 |
| goggles | 0,939 | 0,894 | 0,956 | 0,476 | 0,931 | 0,916 | 0,952 | 0,474 |
| helmet | 0,947 | 0,751 | 0,882 | 0,599 | 0,933 | 0,773 | 0,889 | 0,602 |
| mask | 0,880 | 0,743 | 0,788 | 0,437 | 0,878 | 0,682 | 0,751 | 0,430 |
| safety_shoe | 1,000 | 0,000 | 0,240 | 0,048 | 1,000 | 0,000 | 0,000 | 0,000 |

**Lectura:** `safety_shoe` tiene solo **6 objetos** en esta partición y ambos modelos
tienen recall 0. Su AP no es una medida estable. `mask` baja; `Vest` y `helmet`
mejoran ligeramente. La conclusión de esta tabla no debe generalizarse.

## 5. Test completo — 1.095 imágenes / 1.920 objetos

Esta es la referencia de calidad del modelo ajustado.

| Modelo | P | R | mAP50 | mAP50-95 |
|---|---:|---:|---:|---:|
| YOLO11s | 0,800 | 0,767 | 0,810 | 0,516 |
| **YOLO26n** | **0,893** | **0,842** | **0,892** | **0,614** |
| Diferencia | **+0,093** | **+0,075** | **+0,082** | **+0,098** |

### 5.1 Por clase

| Clase | YOLO11s mAP50 | YOLO11s mAP50-95 | YOLO26n mAP50 | YOLO26n mAP50-95 |
|---|---:|---:|---:|---:|
| Gloves | 0,613 | 0,407 | **0,770** | **0,553** |
| Vest | 0,931 | 0,712 | **0,967** | **0,817** |
| goggles | 0,926 | 0,464 | **0,947** | **0,484** |
| helmet | 0,874 | 0,595 | **0,891** | **0,609** |
| mask | 0,894 | 0,600 | **0,923** | **0,676** |
| safety_shoe | 0,623 | 0,318 | **0,852** | **0,546** |

YOLO26n mejora las seis clases. La mejora más importante está en `Gloves` y
`safety_shoe`, justamente las dos clases débiles del baseline.

## 6. Latencia

Del benchmark HU-020, en CPU y batch 1:

| Modelo | Formato | 640 p50 / p95 |
|---|---|---:|
| YOLO11s | ONNX | 183,52 / 280,63 ms |
| **YOLO26n** | **ONNX** | **53,92 / 88,05 ms** |
| YOLO26s | ONNX | 123,69 / 190,80 ms |

YOLO26n ONNX a 640 cumple <100 ms en el equipo de referencia. YOLO11s no cumple.

## 7. Reproducibilidad

Evaluación del eval 492:

```bash
uv run --extra inference python -m ppe_detection.evaluation.evaluate \
  --model artifacts/models/yolo11s_clean/weights/best.pt \
  --data dataset_limpio/data_eval_preentrenados.yaml \
  --split test \
  --output artifacts/eval \
  --name yolo11s_eval492
```

```bash
uv run --extra inference python -m ppe_detection.evaluation.evaluate \
  --model artifacts/models/yolo26n_clean/weights/best.pt \
  --data dataset_limpio/data_eval_preentrenados.yaml \
  --split test \
  --output artifacts/eval \
  --name yolo26n_eval492
```

Evaluación del test completo:

```bash
uv run --extra inference python -m ppe_detection.evaluation.evaluate \
  --model artifacts/models/yolo26n_clean/weights/best.pt \
  --data dataset_limpio/data.yaml \
  --split test \
  --output artifacts/eval \
  --name yolo26n_test1094
```

Los resúmenes están en `dist/analisis/yolo26n/` y en `artifacts/eval/`. No se
versionan pesos ni imágenes.

## 8. Decisión preliminar

1. **YOLO26n es mejor en el test completo**: +0,082 mAP50 y +0,098 mAP50-95.
2. **YOLO26n ONNX 640 cumple <100 ms** en CPU; YOLO11s no.
3. **El eval de 492 no es suficiente para decidir**: solo 6 objetos de
   `safety_shoe`.
4. **YOLO26s no se justifica**: es más lento y no está fine-tuneado.
5. La decisión final está en el **ADR 0009 (HU-023)**; `models.lock` ya apunta a
   YOLO26n y el rollout del artefacto queda pendiente.

## 9. Limitaciones

- El test 1.095 tiene 1.920 objetos; el eval 492 tiene 1.013 y está desbalanceado.
- La latencia es de una máquina de desarrollo, no del Droplet.
- No se midió la latencia de la API completa.
- Las diferencias de versión de Ultralytics entre entrenamiento y evaluación se
  declaran, pero no se corrigen retroactivamente.
- No se analizaron videos ni escenas fuera del dataset.
