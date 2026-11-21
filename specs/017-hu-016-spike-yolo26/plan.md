# Implementation Plan: HU-016 — Spike de compatibilidad de YOLO26

**Branch**: `feature/017-hu-016-spike-yolo26` | **Date**: 2026-11-21

**Spec**: [spec.md](spec.md)

**Input**: Issue #72 y `specs/017-hu-016-spike-yolo26/spec.md`.

## Summary

Verificar en CPU que `yolo26n.pt` y `yolo26s.pt` cargan e infieren con Python 3.13,
torch 2.15.0+cpu y Ultralytics 8.4.202. Medir latencia p50/p95 con una imagen
sintética y comparar el contrato de salida con el `best.pt` de YOLO11s. El entregable
es un informe de decisión, no código de producción.

## Technical Context

**Language/Version**: Python 3.13.7

**Primary Dependencies**: Ultralytics 8.4.202, torch 2.15.0+cpu, OpenCV, NumPy

**Storage**: pesos descargados fuera de Git; no se versionan

**Testing**: spike documental; no requiere pytest (excepción de SPI en la constitución)

**Target Platform**: CPU, Windows 11, Intel Core i5-1235U

**Constraints**: no entrenar, no evaluar mAP, no tocar Docker ni dependencias

**Scale/Scope**: una imagen sintética, 5 warm-ups + 20 repeticiones por modelo

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias al proyecto.
- [x] Sin GPU, dataset completo ni red en la suite de pruebas normal.
- [x] Los pesos quedan fuera de Git.
- [x] Se documentan versiones, hardware y SHA256.
- [x] El resultado es una decisión, no una implementación prematura.

## Project Structure

```text
docs/spikes/SPI-03-yolo26.md          # entregable
specs/017-hu-016-spike-yolo26/
├── spec.md
├── plan.md
└── tasks.md
```

## Method

1. Ejecutar con `uv run --extra inference` para usar el entorno lockeado.
2. Descargar `yolo26n.pt` y `yolo26s.pt` desde Ultralytics Assets.
3. Generar una imagen sintética 640×640 con OpenCV.
4. Hacer 5 warm-ups y 20 inferencias por modelo con `imgsz=640`, `device=cpu`.
5. Registrar p50, p95, mínimo, máximo, parámetros, número de clases y cajas.
6. Comparar con `artifacts/models/yolo11s_clean/weights/best.pt`.
7. Escribir la conclusión go/no-go y el fallback.

## Risks

- **Latencia variable**: el equipo no está aislado; se reporta p50/p95 y se repite si
  hay outliers.
- **Comparación injusta**: YOLO26 usa 80 clases COCO y YOLO11s 6 clases EPP; se
  compara formato y latencia, no precisión.
- **Pesos fuera de Git**: se documenta SHA256, pero no se versionan.
- **Descarga**: si falla, el spike se cierra como no-go de entorno.
