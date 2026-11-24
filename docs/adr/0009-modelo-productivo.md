# ADR 0009 — Modelo productivo: YOLO26n con ONNX

- **Fecha:** 2026-11-23
- **Estado:** Aceptada (PR #184)
- **Decisores:** Grupo 4
- **Evidencia:** HU-019, HU-020, SPI-03
- **Rollout:** `models.lock` actualizado; artefacto y servicio pendientes

## Contexto

El sistema debe detectar seis categorías de EPP en CPU y mantener el objetivo de
latencia de 100 ms. El modelo desplegado hasta ahora es **YOLO11s clean**, con
mAP50-95 0,516 en el test completo y una latencia ONNX 640 de 183,52 ms p50.

YOLO26n fue entrenado con el mismo dataset y evaluado con la misma configuración. El
benchmark ONNX mostró una mejora simultánea de calidad y latencia. La decisión debe
quedar registrada antes de cambiar `models.lock` o el artefacto montado.

## Decisión

**Adoptar YOLO26n fine-tuneado con exportación ONNX a `imgsz=640` como modelo
productivo objetivo.**

- **Modelo:** `yolo26n_clean/weights/best.pt`
- **SHA256:** `FEFB1F1A120FB3AC7BC0F4DE90E5E594BBEF5E936D8168750AA78FC3FB0F27F9`
- **Formato de servicio:** ONNX 640
- **Fallback:** YOLO11s clean, conservando su artefacto y SHA256
  `E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959`.

El modelo **seleccionado** es YOLO26n; el modelo **actualmente desplegado** sigue
siendo YOLO11s hasta completar el rollout. Esta distinción es obligatoria en la Model
Card y en la operación.

## Criterios y evidencia

### Calidad en test completo — 1.095 imágenes / 1.920 objetos

| Criterio | YOLO11s | YOLO26n | Diferencia |
|---|---:|---:|---:|
| mAP50 | 0,810 | **0,892** | **+0,082** |
| mAP50-95 | 0,516 | **0,614** | **+0,098** |
| Precision | 0,800 | **0,893** | +0,093 |
| Recall | 0,767 | **0,842** | +0,075 |

### Recall por clase

| Clase | YOLO11s | YOLO26n |
|---|---:|---:|
| Gloves | 0,637 | **0,693** |
| Vest | 0,905 | **0,948** |
| goggles | 0,909 | **0,923** |
| helmet | 0,790 | 0,779 |
| mask | 0,833 | **0,894** |
| safety_shoe | 0,530 | **0,816** |

`safety_shoe` deja de ser una clase sin recall útil; `helmet` baja 0,011, dentro de la
variabilidad esperada.

### Latencia CPU — batch 1, ONNX 640

| Modelo | p50 | p95 | ¿<100 ms? |
|---|---:|---:|---|
| YOLO11s | 183,52 ms | 280,63 ms | No |
| **YOLO26n** | **53,92 ms** | **88,05 ms** | **Sí** |
| YOLO26s (preentrenado) | 123,69 ms | 190,80 ms | No |

### Tamaño

| Artefacto | YOLO11s | YOLO26n |
|---|---:|---:|
| `best.pt` | 19,19 MB | **5,47 MB** |
| `best.onnx` | 37,94 MB | **9,86 MB** |

## Alternativas consideradas

### Mantener YOLO11s

- **A favor:** ya está desplegado y validado; rollback trivial.
- **En contra:** menor mAP50-95 (0,516) y no cumple <100 ms en ONNX 640.
- **Decisión:** se conserva como rollback, no como modelo objetivo.

### YOLO26s

- **A favor:** mayor capacidad potencial.
- **En contra:** p50 123,69 ms en ONNX 640; no cumple el objetivo. No está
  fine-tuneado para EPP; su latencia es de arquitectura.
- **Decisión:** no se selecciona. Solo se consideraría si YOLO26n fallara en una
  clase crítica.

### Modelo de mayor tamaño o LLM/VLM

- **En contra:** latencia y costo incompatibles con CPU y el objetivo de 100 ms.
- **Decisión:** descartado por ADR 0001.

## Consecuencias

- `models.lock` debe actualizarse en el rollout con `version`, `sha256` y `url` de
  YOLO26n.
- El artefacto montado en `/models/best.pt` debe ser el `best.pt` de YOLO26n,
  verificado por SHA256.
- El servicio debe usar el ONNX 640 para cumplir la latencia; PyTorch queda para
  desarrollo/evaluación.
- El pipeline debe descargar y verificar el artefacto antes de desplegar (HU-026).
- La Model Card debe declarar el modelo seleccionado y el estado del despliegue.
- La decisión no cambia el contrato `ImageData → list[Detection]`.
- Si el rollout falla, se restaura YOLO11s sin reentrenar.

## Plan de rollout

1. Publicar `yolo26n_clean/weights/best.pt` y `best.onnx` fuera de Git, con SHA256.
2. Actualizar `models.lock` a la versión `yolo26n-clean`.
3. Verificar la descarga con `python -m ppe_detection.detection.artifact fetch`.
4. Montar el nuevo `best.pt` en el contenedor y reiniciar API/gRPC.
5. Ejecutar smoke REST y gRPC; comprobar `/health` y una inferencia real.
6. Medir latencia de servicio; si supera 100 ms o falla el smoke, hacer rollback.

## Rollback

- Restaurar `models.lock` a:
  - `version = "yolo11s-clean"`
  - `sha256 = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"`
  - `url` anterior.
- Montar de nuevo el `best.pt` de YOLO11s.
- Reconstruir/reiniciar el servicio y repetir el smoke.
- No se requiere reentrenar ni recuperar datasets.

## Referencias

- [HU-019 — comparación YOLO26 vs YOLO11s](../evaluation/YOLO26.md)
- [HU-020 — benchmark de latencia](../evaluation/latencia.md)
- [HU-018 — entrenamiento YOLO26n](../evaluation/yolo26-training.md)
- [SPI-03 — compatibilidad YOLO26](../spikes/SPI-03-yolo26.md)
- [ADR 0001 — detector especializado](0001-modelo-base.md)
- [Model Card](../model-card.md)
