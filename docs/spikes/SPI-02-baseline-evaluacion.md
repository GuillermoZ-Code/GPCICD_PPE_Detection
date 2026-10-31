# SPI-02 — Baseline y protocolo de evaluación sin fuga

- **Fecha:** 2026-10-31
- **Estado:** Baseline inicial y corregido completados; fine-tuning pendiente
- **Responsable sugerido:** Hernán (modelo) + Guillermo (entorno)
- **Habilita:** HU-002, HU-008, ADR 0001, ADR 0002
- **Timebox:** 2 días

## 1. Pregunta

¿Cuál es el desempeño **honesto** del modelo preentrenado en este dataset y qué
protocolo de evaluación evita la fuga de datos?

## 2. Dataset verificado

Fuente: [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection),
un único `PPE.zip` de Roboflow v3.

| Hecho | Valor |
|-------|-------|
| Imágenes originales | **12.078** |
| Splits originales | train 8.774 · valid 2.070 · test 1.234 |
| Clases | 6 |
| Objetos declarados en la tarjeta | 16.014 |
| Formato | YOLO (`images/` + `labels/`) |
| Licencia | **CC-BY-4.0** |
| SHA-256 del ZIP | `4b10c6da2abc0f9b5ddf0b37513879ae16922b9f3f21e8b75de12f45cd3de9ac` |

Orden de clases del `data.yaml` (coincide con el checkpoint):

```text
0 Gloves · 1 Vest · 2 goggles · 3 helmet · 4 mask · 5 safety_shoe
```

> La tarjeta del dataset no publica el número de imágenes; este spike lo verificó
> contando los archivos del ZIP. ADR 0002 queda como decisión y este documento como
> evidencia de conteo.

## 3. Fuga detectada y corrección

El dataset original **no es apto para evaluar** sin limpieza:

- **1.137 duplicados exactos** (mismo MD5).
- **969 grupos** de imágenes idénticas o con el mismo hash perceptual repartidos
  entre train/valid/test.
- **47** copias idénticas con etiquetas distintas.
- **1** línea de etiqueta inválida/corregida.

**Split v1 (histórico):** se ejecutó `limpiar_y_redividir.py` (script local,
pendiente de versionar en TA-EDA) con semilla 42 y proporciones 70/20/10:

| Resultado | Valor |
|-----------|-------|
| Imágenes finales | **10.941** |
| train / valid / test | **7.658 / 2.188 / 1.095** |
| Imágenes vacías | 2.647 (**24 %**) |
| Grupos exactos repartidos entre splits | **0** |
| Grupos de aumentaciones entre splits | **795** (ver §3.1) |
| Test para modelos preentrenados | **797** imágenes (`test_original_sin_fuga`) |
| Objetos en ese test | **1.552** |
| Fondos en ese test | 62 |

**Regla:** el test re-dividido **no** sirve para evaluar modelos entrenados con el
train original. Para ellos se usa `test_original_sin_fuga`, que excluye duplicados
exactos, pero **no** las aumentaciones de la misma foto. El EDA completo está en
[`docs/dataset/EDA.md`](../dataset/EDA.md).

### 3.1 Fuga residual por aumentaciones (crítico)

El split con `--distancia-hash 0` agrupa solo hashes exactos. Las aumentaciones de
Roboflow de una misma foto tienen hashes distintos y quedaron repartidas:

| Señal | Valor |
|-------|-------|
| Grupos con nombre base cruzando splits (limpio) | **795** |
| Imágenes involucradas | **2.831 de 10.941 (25,9 %)** |
| Imágenes del eval con mismo base en train/valid | **235 de 797 (29,5 %)** |
| Pares con distancia Hamming ≤ 4 entre splits | **28.481** |
| Imágenes del eval con casi-duplicado ≤ 4 en train/valid | **152 de 797 (19,1 %)** |

Verificación visual: `00027_jpg` y `00059_jpg` son la misma escena en eval y train.
El baseline de §4.1 es **optimista**. La corrección se aplicó en §3.2 y el baseline
recalculado está en §4.2. Detalle en [`docs/dataset/EDA.md`](../dataset/EDA.md).

### 3.2 Split corregido (aplicado)

Se regeneró el split con **agrupación por nombre base + distancia 4** en
`data/ds_base` (extensión local del script, pendiente de versionar):

| Resultado | Valor |
|-----------|-------|
| Imágenes finales | **10.941** |
| train / valid / test | **7.659 / 2.188 / 1.094** |
| Fuga base / exacta / ≤4 | **0 / 0 / 0** |
| Eval | **492** imágenes · **1.013** objetos · 22 fondos |
| Clases en eval | helmet 573 · Gloves 187 · goggles 132 · mask 74 · Vest 41 · safety_shoe 6 |

El eval corregido es **source-disjoint**, pero **no está balanceado**: helmet 56,6 %
y safety_shoe 0,6 %. El test limpio (1.094 imágenes, 1.905 objetos) se usa para el
modelo fine-tuneado; el eval de 492 se reserva para comparar preentrenado vs
fine-tuned en las mismas condiciones.

## 4. Baseline preentrenado

### 4.1 Baseline inicial (eval v1)

Modelo: `Tanishjain9/yolov8n-ppe-detection-6classes` (`best.pt`, YOLOv8n, 6 clases).
Evaluación en CPU, `imgsz=640`, `conf=0.001`, `iou=0.7`, `seed=42`.

| Clase | Imágenes | Instancias | P | R | mAP50 | mAP50-95 |
|-------|---------:|-----------:|---:|---:|------:|---------:|
| **all** | 797 | 1.552 | 0,802 | 0,732 | **0,783** | **0,486** |
| Gloves | 132 | 239 | 0,647 | 0,499 | 0,556 | 0,376 |
| Vest | 157 | 313 | 0,858 | 0,948 | 0,960 | 0,752 |
| goggles | 124 | 137 | 0,870 | 0,928 | 0,953 | 0,488 |
| helmet | 281 | 593 | 0,883 | 0,801 | 0,896 | 0,580 |
| mask | 43 | 86 | 0,885 | 0,628 | 0,700 | 0,382 |
| safety_shoe | 91 | 184 | 0,669 | 0,587 | 0,636 | 0,339 |

Comparación con la card del modelo:

| Métrica | Card | Medido (eval actual) | Diferencia |
|---------|-----:|---------------------:|-----------:|
| mAP50 | ~0,81 | **0,783** | −0,027 |
| mAP50-95 | ~0,53 | **0,486** | −0,044 |
| Precisión | ~0,80 | 0,802 | ≈0 |
| Recall | ~0,74 | 0,732 | −0,008 |

Lecturas:

- **Vest**, **goggles** y **helmet** son sólidos (mAP50 ≥ 0,896).
- **Gloves**, **safety_shoe** y **mask** son las clases débiles; las dos primeras
  también tienen el menor soporte y el menor recall.
- La caída frente a la card es moderada, pero confirma que las métricas publicadas
  estaban infladas por la fuga.
- `mask` tiene solo 86 objetos: sus métricas tienen alta incertidumbre.

> ⚠️ **Cautela:** 235 imágenes del eval set tienen una aumentación con el mismo
> nombre base en train/valid. Estas métricas son una **referencia preliminar**, no
> una medida final libre de fuga.

### 4.2 Baseline corregido (eval sin fuga)

Evaluado sobre `data/ds_base/test_original_sin_fuga` (492 imágenes, 1.013 objetos),
misma configuración y mismo checkpoint:

| Clase | Instancias | P | R | mAP50 | mAP50-95 |
|-------|-----------:|--:|---:|------:|---------:|
| **all** | 1.013 | 0,681 | 0,564 | **0,639** | **0,375** |
| Gloves | 187 | 0,659 | 0,385 | 0,468 | 0,291 |
| Vest | 41 | 0,649 | 0,780 | 0,804 | 0,530 |
| goggles | 132 | 0,919 | 0,859 | 0,950 | 0,482 |
| helmet | 573 | 0,929 | 0,766 | 0,895 | 0,579 |
| mask | 74 | 0,933 | 0,595 | 0,682 | 0,357 |
| safety_shoe | 6 | 0,000 | 0,000 | 0,037 | 0,011 |

- La caída global (**0,783 → 0,639** mAP50; **0,486 → 0,375** mAP50-95) cuantifica el
  sesgo optimista del eval con fuga.
- **Vest (41)** y **safety_shoe (6)** no tienen soporte para conclusiones. El AP50 de
  safety_shoe (0,037 con 6 objetos) es anecdótico y no debe reportarse como desempeño.
- El eval está dominado por helmet (56,6 % de los objetos); el mAP global no es
  representativo de las seis clases.
- El test limpio del split corregido (1.094 imágenes, 1.905 objetos) es el conjunto
  adecuado para medir el modelo fine-tuneado.

## 5. Protocolo de evaluación

1. **Preentrenado:** evaluar solo en el eval corregido
   (`data/ds_base/test_original_sin_fuga`, 492 imágenes).
2. **Fine-tuned:** evaluar en el test limpio de `data/ds_base` (1.094 imágenes) y,
   para comparación apples-to-apples, en el eval corregido de 492.
3. **Configuración fija:** `imgsz=640`, `conf=0.001` para mAP, `iou=0.7`, `seed=42`,
   `deterministic=True`.
4. **Reporte obligatorio:** mAP50, mAP50-95, P, R globales; AP50 y AP50-95 por clase;
   número de instancias; matriz de confusión; latencia CPU.
5. **Prohibido:** ajustar umbrales o épocas mirando el test. La selección se hace con
   `valid`.
6. **Artefactos:** pesos, JSON de métricas y gráficas fuera de Git, con SHA-256.

## 6. Riesgos y limitaciones

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| 24 % de imágenes vacías | Precisión/recall sesgados | Reportar el porcentaje; limitar vacías solo en train/valid, nunca en test |
| `helmet` no queda 70/20/10 | Test sobrerrepresenta helmet | Documentarlo; no comparar clases como si fueran independientes |
| Eval corregido desbalanceado | `safety_shoe` 6 y `Vest` 41 | No reportar métricas por clase para esas clases; usar el test limpio para el modelo fine-tuned |
| Clases minoritarias | Métricas inestables | Reportar conteos; considerar intervalos de confianza |
| Sin clase `person`/`no-EPP` | No se puede afirmar cumplimiento | El sistema reporta EPP detectado, no cumplimiento |
| Procedencia/consentimiento del dataset | Riesgo ético/legal | Declararlo en la Model Card; atribuir CC-BY-4.0 |
| Latencia 136–158 ms a 640 | No cumple <100 ms | ONNX + `imgsz` menor; ver SPI-01 |

## 7. Próximos pasos

- [ ] Versionar `limpiar_y_redividir.py`, la opción `--agrupar-por-base` y el
      evaluador en `src/ppe_detection/` (TA-EDA / HU-008), sin `.ipynb`.
- [x] Rehacer el split con `--distancia-hash 4` + agrupación por nombre base;
      regenerar `test_original_sin_fuga` y recalcular el baseline (`data/ds_base`).
- [x] Script de entrenamiento versionado (`src/ppe_detection/training/train.py`).
- [ ] Fine-tuning de YOLOv8n sobre `data/ds_base` en Colab Pro con ese script.
- [ ] Evaluar el modelo fine-tuneado en el test limpio (1.094) y en el eval corregido
      (492) para comparar con el preentrenado.
- [ ] Exportar a ONNX y medir latencia.
- [ ] Registrar runs en MLflow (HU-009).
- [ ] Documentar métricas, fuga residual y límites en la Model Card (Hernán),
      incluyendo que `safety_shoe` tiene 6 objetos en el eval corregido.

### 7.1 Entrenamiento en Colab Pro

Script versionado: `src/ppe_detection/training/train.py` (sin `.ipynb`).

1. Subir `data/ds_base/` a Google Drive (o generarlo desde el ZIP con el script de
   limpieza).
2. En Colab, clonar el repo e instalar `uv`:

   ```bash
   git clone https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection.git
   cd GPCICD_PPE_Detection
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync
   ```

3. Entrenar:

   ```bash
   uv run --with ultralytics --with onnx --with onnxruntime --with onnxslim --with mlflow \
     python -m ppe_detection.training.train \
     --data /content/drive/MyDrive/ppe/ds_base/data.yaml \
     --eval-data /content/drive/MyDrive/ppe/ds_base/data_eval_preentrenados.yaml \
     --device 0 --epochs 100 --imgsz 640 --batch -1 \
     --project /content/runs/train --name yolov8n_clean \
     --backup-dir /content/drive/MyDrive/ppe/runs --export-onnx \
     --mlflow-uri file:/content/drive/MyDrive/ppe/mlruns
   ```

   - `--device 0` usa la GPU; `--batch -1` activa AutoBatch.
   - `--backup-dir` copia `last.pt`, `args.yaml` y `results.csv` cada
     `--save-period` épocas.
   - `--export-onnx` requiere `onnx` y `onnxslim`.
   - `--mlflow-uri` es opcional; puede ser local (`file:...`) o remoto.

4. Reanudar tras una desconexión:

   ```bash
   mkdir -p /content/runs/train/yolov8n_clean/weights
   cp /content/drive/MyDrive/ppe/runs/yolov8n_clean/last.pt \
      /content/runs/train/yolov8n_clean/weights/
   cp /content/drive/MyDrive/ppe/runs/yolov8n_clean/args.yaml \
      /content/runs/train/yolov8n_clean/
   cp /content/drive/MyDrive/ppe/runs/yolov8n_clean/results.csv \
      /content/runs/train/yolov8n_clean/
   uv run --with ultralytics python -m ppe_detection.training.train \
     --data /content/drive/MyDrive/ppe/ds_base/data.yaml \
     --resume --project /content/runs/train --name yolov8n_clean
   ```

5. Salidas:
   - `project/name/weights/best.pt`, `last.pt`, `results.csv`, `args.yaml`.
   - `project/eval/best/summary.json`, `summary.md` y matriz de confusión.
   - `run_manifest.json` con configuración, versiones, commit y SHA-256.
   - ONNX junto a `best.pt` y copia en `--backup-dir`.

> El script no añade `ultralytics` a `pyproject.toml`: se instala con `uv run --with`
> solo en el entorno de cómputo GPU. La versión exacta se fijará cuando SPI-01 cierre
> la medición de latencia ONNX.

> **Lanzador one-click (local, no versionado):** `dist/colab/PPE_Colab_Train.ipynb`
> + `dist/colab/ppe_colab_bundle.zip`. Se suben a `MyDrive/ppe/`, se abre el notebook
> en Colab, se elige GPU y se ejecutan las celdas. El notebook monta Drive, instala
> `uv`, descomprime el bundle, prepara el dataset (Drive o limpieza desde HF) y lanza
> el entrenamiento con respaldo cada `save-period`.

**Prueba de humo:** ejecutado con un dataset sintético (4 train / 2 valid / 2 test,
6 clases, 1 época, `imgsz=64`, CPU). Entrenamiento, evaluación, export ONNX
(`11,5 MB`), manifiesto y respaldo en `--backup-dir` terminaron correctamente. Las
pruebas unitarias del parser y del orden de clases están en
`tests/test_training.py`.

## 8. Evidencia

- `dataset_limpio/reporte_limpieza.md` (v1 histórico, local, ignorado por Git).
- `data/ds_base/reporte_limpieza.md` (split corregido, local, ignorado por Git).
- `runs/eda/verify_ds_base.json` (verificación de fuga: 0 base/exacta/≤4).
- `runs/val/pretrained_eval/summary.json` (baseline inicial).
- `runs/val/pretrained_eval_base/summary.json` (baseline corregido).
- SHA-256 del ZIP verificado contra Hugging Face.

## 9. Referencias

- [ADR 0001](../adr/0001-modelo-base.md)
- [ADR 0002](../adr/0002-dataset.md)
- [SPI-01](SPI-01-compatibilidad-yolo.md)
- `docs/curso/backlog.md` — SPI-02, HU-002, HU-008
- [Dataset en Hugging Face](https://huggingface.co/datasets/51ddhesh/PPE_Detection)
- [Modelo en Hugging Face](https://huggingface.co/Tanishjain9/yolov8n-ppe-detection-6classes)
