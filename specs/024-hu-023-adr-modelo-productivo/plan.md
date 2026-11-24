# Implementation Plan: HU-023 — ADR del modelo productivo

**Branch**: `feature/024-hu-023-adr-modelo-productivo` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #79 y `specs/024-hu-023-adr-modelo-productivo/spec.md`.

## Summary

Registrar la decisión de modelo con evidencia de calidad, latencia y tamaño. Se
selecciona **YOLO26n + ONNX a 640** y se mantiene **YOLO11s** como rollback hasta el
rollout. La Model Card y la constitución se actualizan para reflejar la decisión sin
afirmar que el nuevo modelo ya está desplegado.

## Evidence

- Calidad: `docs/evaluation/YOLO26.md` y `docs/evaluation/yolo26-training.md`.
- Latencia: `docs/evaluation/latencia.md`.
- Compatibilidad: `docs/spikes/SPI-03-yolo26.md`.
- Pesos: SHA256 `fefb1f1a…f27f9`; tamaño 5.467.973 B.

## Project Structure

```text
docs/adr/0009-modelo-productivo.md
docs/adr/README.md
docs/model-card.md
CONSTITUTION.md
specs/024-hu-023-adr-modelo-productivo/
```

## Decision

- **Modelo seleccionado:** YOLO26n fine-tuneado, ONNX 640.
- **Rollback:** YOLO11s clean, conservando su SHA256 y artefacto.
- **No seleccionado:** YOLO26s por latencia y falta de fine-tuning EPP.
- **Rollout:** actualizar `models.lock`, montar `best.pt`/`best.onnx` verificados y
  volver a ejecutar smoke REST/gRPC.

## Risks

- **Model Card**: debe distinguir “seleccionado” de “desplegado”.
- **CONSTITUTION**: es de Guillermo; requiere su revisión.
- **ADR**: es de Guillermo; requiere su revisión.
- **Rollout**: no se completa en esta HU.
