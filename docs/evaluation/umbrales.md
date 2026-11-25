# Calibración de umbrales por clase — HU-029

**Estado:** Completado.

**Fecha:** 2026-11-23.

**Responsable:** Hernán Estrada (`HestradaUAO`).

**Issue:** #85.

---

## 1. Pregunta

¿Qué umbral de confianza maximiza F1 por clase en validación y cómo cambia el
desempeño en el conjunto de test?

## 2. Configuración

| Parámetro | Valor |
|---|---|
| Modelo | `artifacts/models/yolo26n_clean/weights/best.pt` |
| SHA256 | `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9` |
| `imgsz` | 640 |
| `conf` de recolección | 0,001 |
| `iou` | 0,7 |
| Device | CPU |
| Validación | 2188 imágenes |
| Test | 1095 imágenes |

La calibración usa solo la partición de validación. El test se reserva para la
tabla antes/después y no participa en la elección del umbral.

## 3. Umbrales calibrados en validación

| Clase | Objetos GT | Umbral | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Gloves | 533 | 0,450 | 491 | 24 | 42 | 0,953 | 0,921 | 0,937 |
| Vest | 880 | 0,510 | 821 | 113 | 59 | 0,879 | 0,933 | 0,905 |
| goggles | 286 | 0,300 | 271 | 19 | 15 | 0,934 | 0,948 | 0,941 |
| helmet | 469 | 0,490 | 438 | 23 | 31 | 0,950 | 0,934 | 0,942 |
| mask | 552 | 0,400 | 478 | 35 | 74 | 0,932 | 0,866 | 0,898 |
| safety_shoe | 401 | 0,320 | 315 | 27 | 86 | 0,921 | 0,786 | 0,848 |

Si una clase no tiene etiquetas o predicciones, se conserva el umbral por
defecto de 0,25: no hay evidencia para calibrarla.

## 4. Antes/después en test

| Clase | Objetos GT | Umbral base | P base | R base | F1 base | Umbral calibrado | P calibrada | R calibrada | F1 calibrado | Delta F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Gloves | 267 | 0,250 | 0,748 | 0,745 | 0,747 | 0,450 | 0,847 | 0,682 | 0,755 | 0,008 |
| Vest | 440 | 0,250 | 0,907 | 0,957 | 0,931 | 0,510 | 0,940 | 0,932 | 0,936 | 0,005 |
| goggles | 143 | 0,250 | 0,905 | 0,930 | 0,917 | 0,300 | 0,923 | 0,923 | 0,923 | 0,006 |
| helmet | 593 | 0,250 | 0,881 | 0,799 | 0,838 | 0,490 | 0,944 | 0,745 | 0,833 | -0,005 |
| mask | 276 | 0,250 | 0,892 | 0,902 | 0,897 | 0,400 | 0,946 | 0,891 | 0,918 | 0,021 |
| safety_shoe | 201 | 0,250 | 0,816 | 0,796 | 0,806 | 0,320 | 0,847 | 0,771 | 0,807 | 0,001 |

### 4.1 Global (micro)

| Configuración | TP | FP | FN | Precision | Recall | F1 |
|---|---:|---:|---:|---:|---:|---:|
| Base 0,25 | 1636 | 254 | 284 | 0,866 | 0,852 | 0,859 |
| Calibrado | 1567 | 138 | 353 | 0,919 | 0,816 | 0,865 |

El umbral calibrado sube la precision global (+0,053), baja el recall (-0,036) y
mejora el F1 micro (+0,006). `mask` es la clase que más gana (+0,021); `helmet`
pierde 0,005 por el cambio de 0,25 a 0,49.

## 5. Artefactos

- `configs/thresholds.yaml`: umbrales consumibles por el postprocesamiento.
- `dist/analisis/calibracion/summary.json`: evidencia local fuera de Git.

## 6. Limitaciones

- La calibración depende de la partición de validación y del umbral de IoU 0,5.
- Las clases con pocos objetos, como `safety_shoe`, tienen estimaciones inestables.
- El test se usó solo para reportar; no se usó para elegir los umbrales.

## 7. Reproducción

```bash
uv run pytest tests/test_thresholds.py -q
```

La recolección de detecciones se hizo con YOLO26n y las particiones del dataset limpio.
El cálculo de los umbrales y la exportación del YAML están versionados en
`src/ppe_detection/evaluation/thresholds.py`; `summary.json` conserva los conteos
locales que respaldan las tablas.
