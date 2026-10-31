# EDA — Dataset PPE Detection (`51ddhesh/PPE_Detection`)

- **Fecha:** 2026-10-31
- **Estado:** Completado
- **Fuente:** [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection)
- **Evidencia cruda:** `runs/eda/eda_summary.json` y `runs/eda/class_distribution.csv`
  (locales, ignorados por Git)
- **Relacionado:** [ADR 0002](../adr/0002-dataset.md),
  [SPI-01](../spikes/SPI-01-compatibilidad-yolo.md),
  [SPI-02](../spikes/SPI-02-baseline-evaluacion.md)

---

## 0. Resumen ejecutivo

| Hecho | Valor |
|-------|-------|
| Imágenes originales | **12.078** |
| Formato | JPEG **640×640**, YOLO TXT |
| Imágenes corruptas | **0** |
| Objetos con etiqueta válida | **16.011** (la tarjeta declara 16.014) |
| Clases | 6 |
| Desbalance | Vest 4.418 vs goggles 1.431 (**3,1×**) |
| Imágenes vacías (original) | **3.757 (31,1 %)** |
| Duplicados exactos eliminados | **1.137** |
| Grupos exactos entre splits | **969** (corregidos) |
| Conflictos de etiquetas | **47** |
| Líneas inválidas | **1** (polígono) |
| Dataset limpio v1 | **10.941** (7.658 / 2.188 / 1.095) |
| Split corregido (`data/ds_base`) | **10.941** (7.659 / 2.188 / 1.094) |
| Fuga del split corregido | **0** base · **0** exacta · **0** ≤4 |
| Imágenes vacías (limpio) | **2.647 (24,2 %)** |
| Eval inicial (con fuga residual) | **797** imágenes · 1.552 objetos |
| Eval corregido (sin fuga) | **492** imágenes · 1.013 objetos · 22 fondos |
| Baseline inicial (optimista) | mAP50 **0,783** · mAP50-95 **0,486** |
| Baseline corregido | mAP50 **0,639** · mAP50-95 **0,375** |

> ⚠️ **Hallazgo crítico:** el split v1 elimina duplicados **exactos**, pero **no las
> aumentaciones de la misma foto**. Hay **795 grupos de nombre base repartidos entre
> splits** y **235 de las 797 imágenes del eval set (29,5 %)** tienen una variante con
> el mismo nombre base en train/valid. La fuga residual es real y visible.
>
> ✅ **Corrección aplicada:** se regeneró el split con agrupación por **nombre base +
> distancia 4** en `data/ds_base`. La fuga quedó en **0** (base, exacta y ≤4). El eval
> corregido baja a **492 imágenes / 1.013 objetos** y el baseline a **mAP50 0,639 /
> mAP50-95 0,375**. Ver §6.2.

---

## 1. Fuente y licencia

- Un único `PPE.zip` de **667.690.668 bytes** (668 MB), export de Roboflow v3.
- SHA-256 verificado contra Hugging Face:
  `4b10c6da2abc0f9b5ddf0b37513879ae16922b9f3f21e8b75de12f45cd3de9ac`.
- Licencia declarada: **CC-BY-4.0** (requiere atribución).
- La tarjeta no declara la fuente original de las fotos ni consentimiento de las
  personas. Se mantiene como riesgo ético/legal documentado en ADR 0002.

## 2. Estructura y clases

```text
PPE/
├── data.yaml
├── train/{images,labels}   # 8.774 imágenes
├── valid/{images,labels}   # 2.070 imágenes
└── test/{images,labels}    # 1.234 imágenes
```

Orden real del `data.yaml` (manda sobre la lista en prosa de la tarjeta):

```text
0 Gloves · 1 Vest · 2 goggles · 3 helmet · 4 mask · 5 safety_shoe
```

El checkpoint preentrenado usa exactamente el mismo orden; verificado leyendo el
pickle de `best.pt`.

## 3. Auditoría del dataset original

### 3.1 Conteos por split

| Split | Imágenes | Vacías | % vacías | Objetos |
|-------|---------:|-------:|---------:|--------:|
| train | 8.774 | 2.632 | 30,0 % | 11.726 |
| valid | 2.070 | 751 | 36,3 % | 2.504 |
| test | 1.234 | 374 | 30,3 % | 1.781 |
| **Total** | **12.078** | **3.757** | **31,1 %** | **16.011** |

### 3.2 Objetos por clase

| Clase | train | valid | test | Total |
|-------|------:|------:|-----:|------:|
| Gloves | 1.837 | 558 | 298 | 2.693 |
| Vest | 3.104 | 842 | 472 | **4.418** |
| goggles | 994 | 298 | 139 | **1.431** |
| helmet | 1.896 | 210 | 596 | 2.702 |
| mask | 2.267 | 408 | 86 | 2.761 |
| safety_shoe | 1.628 | 188 | 190 | 2.006 |
| **Total** | **11.726** | **2.504** | **1.781** | **16.011** |

La tarjeta declara 16.014 objetos; el conteo reproducible da **16.011**. La diferencia
de 3 se explica por líneas inválidas o copias con etiquetas inconsistentes (ver §3.4).

### 3.3 Propiedades de imagen

- **Todas** las imágenes son JPEG de **640×640**.
- **0** imágenes corruptas o ilegibles.
- Esto simplifica el preprocesamiento del dataset, pero no el de imágenes reales, que
  pueden tener otras resoluciones y relaciones de aspecto.

### 3.4 Validez de etiquetas

| Problema | Original | Limpio |
|----------|---------:|-------:|
| Polígono/segmentación | 1 | 0 |
| Clase fuera de rango | 0 | 0 |
| Caja de área cero | 0 | 0 |
| Caja fuera de la imagen | 0 | 0 |
| Línea mal formada | 0 | 0 |

La única línea inválida estaba en `test` y era un polígono
(`VID-20240831-WA0012_mp4-0011_jpg...txt`); se descartó.

### 3.5 Tamaño de las cajas

Umbrales COCO en píxeles: pequeño < 32², mediano 32²–96², grande ≥ 96².

| Split | Objetos | Área norm. mediana | Pequeños | Medianos | Grandes |
|-------|--------:|-------------------:|---------:|---------:|--------:|
| train | 11.726 | 0,0366 | 880 (7,5 %) | 3.715 (31,7 %) | 7.131 (60,8 %) |
| valid | 2.504 | 0,0343 | 307 (12,3 %) | 733 (29,3 %) | 1.464 (58,5 %) |
| test | 1.781 | 0,0256 | 183 (10,3 %) | 660 (37,1 %) | 938 (52,7 %) |
| **Total** | **16.011** | — | **1.370 (8,6 %)** | **5.108 (31,9 %)** | **9.533 (59,5 %)** |

El test original tiene objetos **más pequeños** que train/valid (área mediana 0,0256
frente a 0,0366). Es una dificultad adicional del conjunto de evaluación.

### 3.6 Co-ocurrencia

La mayoría de las imágenes contiene **una sola clase**. Las combinaciones más
frecuentes son `Gloves + helmet` y `helmet + mask`; no hay una clase “persona” que
agrupe el contexto. Esto refuerza que el sistema reporta EPP detectado, no
cumplimiento de un trabajador.

## 4. Duplicados y fuga

### 4.1 Duplicados exactos

- **1.137** imágenes idénticas eliminadas (MD5).
- **969** grupos de imágenes idénticas o con el mismo hash perceptual estaban
  repartidos entre train/valid/test.
- **47** copias idénticas tenían etiquetas distintas; se conservó la versión con más
  cajas.
- Distribución de las copias eliminadas: train 736 · valid 390 · test 11.

Esto confirma que el split original de Roboflow **no era válido para evaluar**.

### 4.2 Fuga residual por aumentaciones (crítico)

El script de limpieza agrupó por **MD5 y hash perceptual exacto** (distancia 0). Las
aumentaciones de Roboflow de una misma foto tienen hashes distintos y **no** quedaron
agrupadas. Señales medidas:

| Nivel | Grupos con nombre base cruzando splits | Imágenes involucradas |
|-------|----------------------------------------:|----------------------:|
| Original | 1.322 de 7.373 bases (17,9 %) | 4.008 de 12.078 (33,2 %) |
| Limpio | **795 de 7.373 bases (10,8 %)** | **2.831 de 10.941 (25,9 %)** |
| Eval vs train/valid | **235 de 797 imágenes (29,5 %)** | — |

El “nombre base” es el nombre antes del sufijo `.rf.<hash>` de Roboflow. Dos archivos
con el mismo base son, con altísima probabilidad, la misma foto aumentada.

Además, con distancia de Hamming ≤ 4 entre hashes perceptuales:

| Comparación | Pares entre splits |
|-------------|-------------------:|
| train–valid | 21.563 |
| test–train | 5.780 |
| test–valid | 1.138 |
| **Total** | **28.481** |

No son 28.481 imágenes únicas: un grupo con varias aumentaciones genera muchos pares.
Pero confirman que la fuga no es marginal. En el eval set, **152 de 797 imágenes
(19,1 %)** tienen un casi-duplicado (≤ 4) en train/valid.

**Verificación visual:** se compararon pares como `00027_jpg` (eval vs train) y
`00059_jpg` (eval vs train). Son la **misma escena**, con variaciones mínimas de
compresión/aumento y las mismas etiquetas. No es un falso positivo del hash.

### 4.3 Implicación

El `dataset_limpio` actual es **“sin duplicados exactos”**, no **“sin fuga”**. Para
una evaluación defendible hay que agrupar también las aumentaciones antes de dividir:

- re-ejecutar `limpiar_y_redividir.py` con `--distancia-hash 4` (mantiene las
  aumentaciones, pero las fuerza al mismo split); o
- agrupar por nombre base (más robusto para este export de Roboflow); o
- ambas cosas.

El eval set resultante será más pequeño (probablemente ~560 imágenes si se eliminan
las 235 con mismo base) y el baseline debe recalcularse.

## 5. Limpieza y re-división v1 (histórica)

> Este split conserva la fuga por aumentaciones. La corrección canónica está en §6.2.

### 5.1 Método aplicado

`limpiar_y_redividir.py` con semilla 42, proporciones 70/20/10 y
`--distancia-hash 0`:

1. Agrupa por MD5 y hash perceptual exacto.
2. Elimina copias idénticas conservando la de más cajas.
3. Reparte cada grupo completo en un solo split.
4. Corrige etiquetas inválidas y cajas fuera de borde.
5. Genera `test_original_sin_fuga` para evaluar modelos ya entrenados con el train
   original.

### 5.2 Resultado

| Split | Imágenes | Vacías | % vacías | Objetos |
|-------|---------:|-------:|---------:|--------:|
| train | 7.658 | 1.970 | 25,7 % | 10.921 |
| valid | 2.188 | 583 | 26,6 % | 3.121 |
| test | 1.095 | 94 | 8,6 % | 1.920 |
| **Total** | **10.941** | **2.647** | **24,2 %** | **15.962** |

### 5.3 Objetos por clase después de limpiar

| Clase | train | valid | test | Total |
|-------|------:|------:|-----:|------:|
| Gloves | 1.865 | 533 | 267 | 2.665 |
| Vest | 3.077 | 880 | 440 | 4.397 |
| goggles | 1.002 | 286 | 143 | 1.431 |
| helmet | 1.640 | 469 | 593 | 2.702 |
| mask | 1.933 | 552 | 276 | 2.761 |
| safety_shoe | 1.404 | 401 | 201 | 2.006 |
| **Total** | **10.921** | **3.121** | **1.920** | **15.962** |

### 5.4 Anomalías de estratificación

- **Helmet** quedó **60,7 / 17,4 / 21,9** en train/valid/test, no 70/20/10. El test
  original concentraba el 22,1 % de los helmets y se forzó completo a test para
  proteger el eval set.
- El **test limpio tiene solo 8,6 % de imágenes vacías**, frente a 25,7 % en train y
  26,6 % en valid. Es un cambio de distribución: el test es más “denso” en objetos.
- El eval set tiene 7,8 % de fondos (62 de 797).

### 5.5 Composición del eval set (`test_original_sin_fuga`)

| Clase | Objetos | % del total |
|-------|--------:|------------:|
| helmet | 593 | 38,2 % |
| Vest | 313 | 20,2 % |
| Gloves | 239 | 15,4 % |
| safety_shoe | 184 | 11,9 % |
| goggles | 137 | 8,8 % |
| mask | 86 | 5,5 % |
| **Total** | **1.552** | **100 %** |

- 797 imágenes · **62 fondos**.
- Área norm. mediana **0,0194** (objetos más pequeños que en train: 0,0366).
- Pequeños 178 (11,5 %) · medianos 637 (41,0 %) · grandes 737 (47,5 %).
- Las 797 imágenes están presentes en el test limpio, con el mismo número de cajas;
  el eval set es un subconjunto consistente del test limpio.

## 6. Baseline preentrenado

### 6.1 Baseline inicial (eval con fuga residual)

Modelo: `Tanishjain9/yolov8n-ppe-detection-6classes` (YOLOv8n, 6 clases).
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

- **Vest**, **goggles** y **helmet** son sólidos (mAP50 ≥ 0,896).
- **Gloves**, **safety_shoe** y **mask** son las clases débiles.
- El eval set tiene objetos más pequeños y está sobrerrepresentado en helmet; las
  métricas por clase no son directamente comparables entre sí.
- **Cautela:** 235 imágenes del eval set tienen una aumentación con mismo base en
  train/valid. El baseline es **optimista** y no debe presentarse como métrica final.
- Latencia CPU: **157,5 ms/imagen** a 640 px (~6,3 FPS), por encima del objetivo
  <100 ms. Ver SPI-01.

### 6.2 Baseline corregido (split sin fuga)

Se regeneró el split con `--agrupar-por-base --distancia-hash 4` en `data/ds_base`.
Verificación independiente: **0 grupos base cruzados, 0 duplicados exactos, 0
casi-duplicados ≤4** entre train/valid/test. El eval set es un subconjunto de 492
imágenes del test limpio, sin base compartido con train/valid.

| Clase | Instancias | P | R | mAP50 | mAP50-95 |
|-------|-----------:|--:|---:|------:|---------:|
| **all** | 1.013 | 0,681 | 0,564 | **0,639** | **0,375** |
| Gloves | 187 | 0,659 | 0,385 | 0,468 | 0,291 |
| Vest | 41 | 0,649 | 0,780 | 0,804 | 0,530 |
| goggles | 132 | 0,919 | 0,859 | 0,950 | 0,482 |
| helmet | 573 | 0,929 | 0,766 | 0,895 | 0,579 |
| mask | 74 | 0,933 | 0,595 | 0,682 | 0,357 |
| safety_shoe | 6 | 0,000 | 0,000 | 0,037 | 0,011 |

Lecturas:

- La caída global (**0,783 → 0,639** mAP50; **0,486 → 0,375** mAP50-95) confirma que el
  eval inicial era optimista.
- El eval corregido está dominado por **helmet (573/1.013 = 56,6 %)**; **Vest (41)** y
  **safety_shoe (6)** tienen soporte insuficiente para conclusiones.
- `safety_shoe` con 6 objetos y AP50 0,037 es **anecdótico**: no debe reportarse como
  desempeño del modelo.
- El test limpio del split corregido tiene **1.094 imágenes y 1.905 objetos**; úsalo
  para el modelo fine-tuneado. El eval de 492 imágenes se reserva para comparar
  preentrenado vs fine-tuned en condiciones equivalentes.

## 7. Conclusiones y recomendaciones

1. **Usar `data/ds_base` como dataset canónico.** `dataset_limpio` v1 se conserva solo
   como evidencia histórica; no usar sus métricas como finales.
2. **No afirmar “sin fuga” sin calificar.** El split v1 tenía fuga por aumentaciones;
   el corregido tiene **0 fuga** base/exacta/≤4. Documentar la diferencia.
3. **Métricas:** usar el eval corregido (492) para comparar preentrenado vs
   fine-tuned; usar el test limpio (1.094 imágenes, 1.905 objetos) para el modelo
   fine-tuneado. No mezclar tablas de ambos conjuntos.
4. **No usar el test para tuning.** Mantener `valid` para épocas/hiperparámetros.
5. **Vacías:** 24,2 % en el dataset limpio. Si se limita con `--pct-vacias`, aplicarlo
   solo a train/valid, nunca a test.
6. **Distribución:** el eval corregido sobrerrepresenta helmet (56,6 %) y tiene solo
   41 objetos de Vest y 6 de safety_shoe. No comparar clases como si fueran
   independientes.
7. **Clases pequeñas:** reportar siempre conteos; `safety_shoe` (6) y `Vest` (41) no
   permiten conclusiones; `mask` (74) y `goggles` (132) son moderadas.
8. **Latencia:** **136–158 ms/imagen** a 640 px según corrida; medir ONNX y `imgsz`
   menor antes de fijar la variante.
9. **Versionar** el script de limpieza/EDA y la opción `--agrupar-por-base` en `src/`
   o `scripts/` (sin `.ipynb`), y adjuntar SHA-256 del ZIP y del dataset generado.

## 8. Reproducibilidad

```bash
# Descarga y verificación
curl -L -o data/raw/PPE.zip \
  https://huggingface.co/datasets/51ddhesh/PPE_Detection/resolve/main/PPE.zip
# SHA-256 esperado:
# 4b10c6da2abc0f9b5ddf0b37513879ae16922b9f3f21e8b75de12f45cd3de9ac

# Split v1 (histórico, con fuga residual por aumentaciones)
uv run --no-project --with pandas --with pillow --with pyyaml --with tabulate \
  python limpiar_y_redividir.py --data data/raw/PPE.zip --salida dataset_limpio

# Split corregido (canónico, sin fuga base/exacta/≤4)
uv run --no-project --with pandas --with pillow --with pyyaml --with tabulate \
  python limpiar_y_redividir_base.py --data _original --salida data/ds_base \
  --distancia-hash 4 --agrupar-por-base

# EDA (script local, pendiente de versionar)
uv run --no-project --with pillow --with pyyaml python eda_dataset.py
```

> `limpiar_y_redividir_base.py` es una extensión local del script original que añade
> `--agrupar-por-base`. Está pendiente de versionar en el repo (TA-EDA).

Artefactos locales (ignorados por Git): `data/ds_base/`, `dataset_limpio/`,
`runs/eda/`, `runs/val/pretrained_eval/`, `runs/val/pretrained_eval_base/`.

## 9. Referencias

- [ADR 0002 — Dataset](../adr/0002-dataset.md)
- [SPI-01 — Compatibilidad YOLO](../spikes/SPI-01-compatibilidad-yolo.md)
- [SPI-02 — Baseline y evaluación](../spikes/SPI-02-baseline-evaluacion.md)
- [Dataset en Hugging Face](https://huggingface.co/datasets/51ddhesh/PPE_Detection)
- [Modelo en Hugging Face](https://huggingface.co/Tanishjain9/yolov8n-ppe-detection-6classes)
