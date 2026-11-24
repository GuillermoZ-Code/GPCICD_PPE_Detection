# Implementation Plan: HU-020 — Benchmark de latencia CPU

**Branch**: `feature/021-hu-020-benchmark-latencia` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #76 y `specs/021-hu-020-benchmark-latencia/spec.md`.

## Summary

Medir latencia de inferencia CPU para tres modelos, tres resoluciones y dos formatos.
El entregable es un informe con metodología, tablas p50/p95 y una recomendación de
`imgsz`/formato. No se modifica el modelo productivo.

## Technical Context

**Python**: 3.13.7

**Ultralytics**: 8.4.202

**torch**: 2.15.0+cpu

**ONNX Runtime**: 1.32.0, CPUExecutionProvider

**Hardware**: Intel Core i5-1235U, 10 núcleos / 12 hilos, Windows 11

**Medición**: `model.predict()` completo, batch 1, `conf=0.25`, `iou=0.7`, 5 warm-ups,
20 repeticiones.

## Project Structure

```text
docs/evaluation/latencia.md          # entregable
specs/021-hu-020-benchmark-latencia/
├── spec.md
├── plan.md
└── tasks.md
```

## Modelos

| Nombre | Formato | Clases | Nota |
|---|---|---|---|
| YOLO11s clean | `.pt`, `.onnx` | 6 EPP | baseline productivo |
| YOLO26n clean | `.pt`, `.onnx` | 6 EPP | candidato |
| YOLO26s pretrained | `.pt`, `.onnx` | 80 COCO | solo latencia, no calidad |

## Decisión esperada

- Si YOLO26n ONNX a 640 cumple <100 ms, es el candidato de producción.
- Si no, evaluar 480/416 y documentar el tradeoff.
- YOLO26s solo si su latencia y calidad justifican el costo.

## Risks

- **Imagen sintética**: no mide calidad; solo latencia.
- **Equipo compartido**: p95 puede variar; se documenta.
- **s preentrenado**: su latencia es de arquitectura, no del modelo EPP.
- **Specs/ es de Jesús**: la spec genera aviso de propiedad.
