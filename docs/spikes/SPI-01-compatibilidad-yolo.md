# SPI-01 — Compatibilidad de YOLO con Python 3.13 + torch CPU

- **Fecha:** 2026-10-31
- **Estado:** Completado
- **Responsable sugerido:** Guillermo (entorno/arquitectura)
- **Habilita:** HU-002, ADR 0001
- **Timebox:** 1 día

## 1. Pregunta

¿Funciona Ultralytics YOLO con **Python 3.13 + PyTorch CPU**, qué variante y versión
son viables, y se cumple el objetivo de **<100 ms por imagen** en CPU?

## 2. Método

- Entorno efímero con `uv` (sin modificar las dependencias del proyecto todavía):

  ```bash
  uv run --no-project --with ultralytics python evaluar.py
  ```

- Modelo: `best.pt` de
  [`Tanishjain9/yolov8n-ppe-detection-6classes`](https://huggingface.co/Tanishjain9/yolov8n-ppe-detection-6classes).
- Dataset de evaluación: `dataset_limpio/data_eval_preentrenados.yaml`
  (`test_original_sin_fuga`, 797 imágenes).
- Hardware: Intel Core i5-1235U, **sin GPU NVIDIA**.
- Configuración: `imgsz=640`, `batch=16`, `device=cpu`, `workers=0`,
  `conf=0.001`, `iou=0.7`, `seed=42`, `deterministic=True`.

## 3. Resultados

### 3.1 Compatibilidad

| Componente | Versión | Resultado |
|------------|---------|-----------|
| Python | 3.13.7 | ✅ |
| Ultralytics | 8.4.195 | ✅ |
| torch | 2.15.0+cpu | ✅ |
| Modelo | YOLOv8n PPE, 6 clases | ✅ carga e infiere |

- El checkpoint tiene **2.685.538 parámetros**, **6,8 GFLOPs** y pesa **5,6 MB**.
- `model.names` coincide exactamente con el `data.yaml`:

  ```text
  {0: Gloves, 1: Vest, 2: goggles, 3: helmet, 4: mask, 5: safety_shoe}
  ```

- **No fue necesario bajar a Python 3.12.** El plan B del riesgo de la constitución
  no se activa.

### 3.2 Latencia en CPU (640 px)

| Etapa | ms/imagen (rango de 2 corridas) |
|-------|--------------------------------:|
| Preprocesamiento | 2,4 |
| **Inferencia** | **136,2 – 157,5** |
| Postprocesamiento | 2,2 – 2,4 |
| **Total aproximado** | **140,8 – 162,3** |

- Equivale a **~6,2 – 7,3 FPS** por imagen.
- **No cumple** el objetivo de <100 ms en esta máquina a 640 px.
- La variación depende de la carga del equipo y del tamaño del lote; el orden de
  magnitud se mantiene.
- La latencia es solo inferencia; API, serialización y UI añaden overhead.

### 3.3 Calidad

El detalle está en [SPI-02](SPI-02-baseline-evaluacion.md). Resumen:

| Eval | mAP50 | mAP50-95 | Nota |
|------|------:|---------:|------|
| Inicial (797) | 0,783 | 0,486 | Con fuga residual por aumentaciones |
| Corregido (492) | **0,639** | **0,375** | Source-disjoint; dominado por helmet |

## 4. Conclusión

1. **YOLOv8n es viable** con Python 3.13 + torch CPU y confirma la decisión de
   ADR 0001 (detector especializado nivel 3).
2. La variante **nano** es la única que deja margen para acercarse a <100 ms; una
   variante `small` o mayor queda descartada para CPU salvo que ONNX cambie el
   resultado.
3. **La latencia es el riesgo principal.** Antes de fijar la versión definitiva hay
   que medir:
   - export ONNX + ONNX Runtime;
   - `imgsz` 640, 480 y 320;
   - batch 1 (caso API) y batch N (caso evaluación).
4. Hasta completar esas mediciones, la versión de Ultralytics queda **candidata**
   (8.4.195), no fijada.

## 5. Próximos pasos

- [ ] Exportar `best.pt` a ONNX (`opset=17`, `simplify=True`, `dynamic=False`).
- [ ] Benchmark ONNX Runtime en CPU a 640/480/320.
- [ ] Repetir con `yolov8n.pt` fine-tuneado para comparar latencia.
- [ ] Decidir si se acepta el objetivo <100 ms o se documenta el tradeoff.
- [ ] Fijar versión de Ultralytics en `pyproject.toml` y `uv.lock` vía `uv add`.

## 6. Evidencia

- `runs/val/pretrained_eval/summary.json` (ignorado por Git).
- Curvas PR/F1, matriz de confusión y lotes de validación en el mismo directorio.
- Este spike no versiona pesos ni imágenes.

## 7. Referencias

- [ADR 0001](../adr/0001-modelo-base.md)
- [SPI-02](SPI-02-baseline-evaluacion.md)
- `docs/curso/backlog.md` — SPI-01, HU-002
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics)
- [Modelo en Hugging Face](https://huggingface.co/Tanishjain9/yolov8n-ppe-detection-6classes)
