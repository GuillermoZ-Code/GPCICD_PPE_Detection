# Implementation Plan: HU-019 — Comparación YOLO26 vs YOLO11s

**Branch**: `feature/020-hu-019-comparar-yolo26-yolo11` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #75 y `specs/020-hu-019-comparar-yolo26-yolo11/spec.md`.

## Summary

Producir un informe comparativo a partir de los resúmenes de evaluación de ambos
modelos. Se incluyen el eval de 492 (AC de la issue) y el test completo de 1.095
(evidencia complementaria) para no basar la decisión en una partición con solo 6
objetos de `safety_shoe`.

## Technical Context

**Modelos**:
- `yolo11s_clean/weights/best.pt` (SHA256 `E51EB080…A9959`)
- `yolo26n_clean/weights/best.pt` (SHA256 `FEFB1F1A…F27F9`)

**Evaluación**: `imgsz=640`, `conf=0.001`, `iou=0.7`, `seed=42`, `device=cpu`.

**Datos**: eval 492 (1.013 objetos) y test 1.095 (1.920 objetos).

**Entregable**: `docs/evaluation/YOLO26.md`.

## Project Structure

```text
docs/evaluation/YOLO26.md
specs/020-hu-019-comparar-yolo26-yolo11/
├── spec.md
├── plan.md
└── tasks.md
```

## Decisiones

- La tabla del eval 492 se conserva porque es el AC literal.
- El test 1.095 se presenta como referencia de calidad; no reemplaza el AC.
- La recomendación es preliminar; el ADR 0009 decide.
- No se modifica el modelo productivo ni `models.lock`.

## Risks

- **Partición 492 desbalanceada**: `safety_shoe` tiene 6 objetos; se advierte.
- **Versiones de Ultralytics**: el entrenamiento usó 8.4.216 y la evaluación local
  8.4.202; se declara.
- **Sin imágenes en Git**: la evidencia visual queda fuera del repo.
- **Specs/ es de Jesús**: la spec genera aviso de propiedad.
