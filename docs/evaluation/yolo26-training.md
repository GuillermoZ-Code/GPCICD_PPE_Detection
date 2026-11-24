# Entrenamiento YOLO26 — HU-018

**Estado:** YOLO26n completado; YOLO26s pendiente de decisión.

**Fecha:** 2026-11-21

**Responsable:** Hernán Estrada (`HestradaUAO`)

**Issue:** #74

---

## 1. Alcance

Registrar el entrenamiento de YOLO26n con el dataset limpio y compararlo con el modelo
productivo YOLO11s. YOLO26s no se ejecutó todavía: la latencia medida en el spike
SPI-03 lo deja como candidato de investigación, no de producción.

Los pesos y artefactos están fuera de Git.

## 2. Entorno y datos

| Elemento | Valor |
|---|---|
| Entorno | Colab pago, GPU |
| Python | 3.13.16 |
| Ultralytics | 8.4.216 |
| torch | 2.15.0 |
| Dataset | `data_colab.yaml` |
| Evaluación | `data_eval_colab.yaml`, split `test` |
| Train / valid / test | 7.658 / 2.188 / 1.095 imágenes |
| Semilla | 42 |
| `imgsz` | 640 |
| `batch` | -1 |
| Épocas | 100 |

El `run_manifest.json` es la fuente autoritativa de la configuración.

## 3. Run YOLO26n

| Campo | Valor |
|---|---|
| Modelo base | `yolo26n.pt` |
| Run | `yolo26` |
| Inicio | 2026-11-22 00:11 UTC |
| Fin | 2026-11-22 01:36 UTC |
| Duración | ~85 min |
| `best.pt` | 5.467.973 B |
| SHA256 `best.pt` | `fefb1f1a120fb3ac7bc0f4de90e5e594bbef5e936d8168750aa78fc3fb0f27f9` |
| `best.onnx` | 9.857.236 B |
| SHA256 `best.onnx` | `D7983DA28821A116C62843CAEFF774EB8D426141558766AB753C6C43A180ACD9` |
| Clases | 6 EPP (`Gloves, Vest, goggles, helmet, mask, safety_shoe`) |

Los pesos están en:

```text
artifacts/models/yolo26n_clean/weights/
├── best.pt
├── last.pt
└── best.onnx
```

## 4. Evaluación

### 4.1 Test limpio — 1.095 imágenes / 1.920 objetos

Esta es la comparación de referencia contra YOLO11s.

| Clase | YOLO26n P | YOLO26n R | YOLO26n mAP50 | YOLO26n mAP50-95 | YOLO11s mAP50 | YOLO11s mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|
| **all** | **0,893** | **0,842** | **0,892** | **0,614** | 0,810 | 0,516 |
| Gloves | 0,809 | 0,693 | 0,770 | 0,553 | 0,613 | 0,407 |
| Vest | 0,914 | 0,948 | 0,967 | 0,817 | 0,931 | 0,712 |
| goggles | 0,904 | 0,923 | 0,947 | 0,484 | 0,926 | 0,464 |
| helmet | 0,930 | 0,779 | 0,891 | 0,609 | 0,874 | 0,595 |
| mask | 0,928 | 0,894 | 0,923 | 0,676 | 0,894 | 0,600 |
| safety_shoe | 0,869 | 0,816 | 0,852 | 0,546 | 0,623 | 0,318 |

**Lectura:** YOLO26n mejora a YOLO11s en mAP50 (**+0,082**) y mAP50-95
(**+0,098**). La mejora más importante está en `Gloves` y `safety_shoe`, las dos
clases débiles del baseline. `safety_shoe` deja de estar en cero.

### 4.2 Eval sin fuga — 492 imágenes / 1.013 objetos

| Clase | YOLO26n P | YOLO26n R | YOLO26n mAP50 | YOLO26n mAP50-95 | YOLO11s mAP50 | YOLO11s mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|
| **all** | 0,885 | 0,645 | 0,688 | 0,419 | 0,726 | 0,424 |
| Gloves | 0,794 | 0,594 | 0,673 | 0,427 | 0,654 | 0,427 |
| Vest | 0,772 | 0,902 | 0,863 | 0,579 | 0,834 | 0,556 |
| goggles | 0,931 | 0,916 | 0,952 | 0,474 | 0,956 | 0,476 |
| helmet | 0,933 | 0,773 | 0,889 | 0,602 | 0,882 | 0,599 |
| mask | 0,878 | 0,682 | 0,751 | 0,430 | 0,788 | 0,437 |
| safety_shoe | 1,000 | 0,000 | 0,000 | 0,000 | 0,240 | 0,048 |

**No usar este eval para decidir:** solo tiene **6 objetos** de `safety_shoe` y su
distribución no representa el test completo. El eval de 492 sirve para comparar
contra el baseline histórico, no para concluir sobre la calidad del modelo.

## 5. Comparación con YOLO11s

| Modelo | Test | P | R | mAP50 | mAP50-95 |
|---|---|---:|---:|---:|---:|
| YOLO11s clean | 1.095 imágenes | 0,800 | 0,767 | 0,810 | 0,516 |
| **YOLO26n clean** | 1.095 imágenes | **0,893** | **0,842** | **0,892** | **0,614** |
| Diferencia | | **+0,093** | **+0,075** | **+0,082** | **+0,098** |

YOLO26n es mejor en el test completo, incluyendo `safety_shoe`, que era la debilidad
principal. La latencia sigue siendo el problema: SPI-03 midió ~160 ms p50 en CPU, por
encima del objetivo de 100 ms.

## 6. Estado de YOLO26s

**No entrenado todavía.**

Razones:

- El spike midió YOLO26s en **514 ms p50** y **800 ms p95** en CPU; es poco viable
  para el servicio.
- YOLO26n ya supera a YOLO11s en el test completo; no hay una necesidad inmediata de
  un modelo más grande.
- Entrenar `s` consume otra sesión de GPU y no cambia la decisión de producción por
  sí solo.

Se entrenará solo si:

1. El equipo exige cumplir el AC de dos modelos, o
2. YOLO26n no alcanza el rendimiento esperado en una clase crítica.

## 7. Calidad de la evidencia

`best.pt` coincide con el SHA256 del `run_manifest.json`. El modelo carga con las 6
clases EPP.

**Advertencia:** `raw/args.yaml` y `raw/results.csv` no coinciden con el manifiesto
(hablan de `coco8.yaml`, `last.pt`, `seed=0` y métricas en cero). Se conservan como
archivos crudos, pero **no se usan** para afirmar la configuración ni las curvas. La
fuente válida es `run_manifest.json` + `eval_test1094/summary.json`.

## 8. Evidencia

```text
dist/analisis/yolo26n/
├── run_manifest.json
├── eval/                 # eval 492, histórico
├── eval_test1094/        # test completo, referencia
│   ├── summary.json
│   ├── summary.md
│   ├── BoxF1_curve.png
│   ├── BoxPR_curve.png
│   ├── BoxP_curve.png
│   ├── BoxR_curve.png
│   ├── confusion_matrix.png
│   └── confusion_matrix_normalized.png
└── raw/
    ├── args.yaml
    ├── results.csv
    └── source-yolo26.zip
```

## 9. Conclusión

1. **YOLO26n es un candidato real**: supera a YOLO11s en el test completo.
2. **YOLO26s no es prioritario**: la latencia en CPU lo hace poco viable.
3. La decisión de producción requiere HU-019 (informe comparativo) y HU-023 (ADR).
4. La latencia debe resolverse en HU-020/HU-022 antes de reemplazar el modelo actual.

## 10. Reproducibilidad

```bash
python -m ppe_detection.training.train \
  --data /content/data_colab.yaml \
  --eval-data /content/data_eval_colab.yaml \
  --model yolo26n.pt \
  --epochs 100 \
  --imgsz 640 \
  --batch -1 \
  --device 0 \
  --seed 42 \
  --name yolo26
```

Evaluación local del test completo:

```bash
uv run --extra inference python -m ppe_detection.evaluation.evaluate \
  --model artifacts/models/yolo26n_clean/weights/best.pt \
  --data dataset_limpio/data.yaml \
  --split test \
  --output artifacts/eval \
  --name yolo26n_test1094
```

No se versionan pesos, datasets ni imágenes.
