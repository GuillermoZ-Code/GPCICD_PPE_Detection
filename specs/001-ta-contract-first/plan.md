# Implementation Plan: TA Contract-first

**Branch**: `feature/001-ta-11-contract-first` | **Date**: 2026-10-31 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-ta-contract-first/spec.md`

**Note**: Este plan se completa con `/speckit.plan`; la implementación no inicia hasta
la aprobación de planificación de Jesús.

## Summary

Definir `ImageData`, `Detection`, el protocolo `Detector` y un `FakeDetector`
determinista. Documentar el contrato y probarlo sin YOLO, dataset ni GPU. Esto
desbloquea API, UI y gRPC mientras HU-002 implementa el detector real.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: biblioteca estándar; Pydantic solo si FastAPI lo requiere

**Storage**: N/A

**Testing**: pytest (patrón AAA), `make check`

**Target Platform**: Linux/Windows; CPU

**Project Type**: library (paquete `ppe_detection`)

**Performance Goals**: N/A; el fake debe ser O(1) o O(n) trivial

**Constraints**: sin GPU, sin dataset, sin pesos, sin red

**Scale/Scope**: 1 contrato, 2 tipos, 1 protocolo, 1 fake, ~6 pruebas

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] `uv` como único gestor.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Contract-first y AGPL-3.0-only.
- [x] Sin LLM en inferencia.

## Project Structure

### Documentation (this feature)

```text
specs/001-ta-contract-first/
├── spec.md
├── plan.md
└── tasks.md
```

### Source Code (repository root)

```text
src/ppe_detection/
├── __init__.py
└── contracts.py          # ImageData, Detection, Detector, FakeDetector

tests/
└── test_contracts.py     # pruebas AAA del contrato
```

**Structure Decision**: paquete único `src/ppe_detection/`; el contrato vive en
`contracts.py` para que API, UI y gRPC lo importen sin acoplarse al detector real.

## Complexity Tracking

No hay violaciones a la constitución. No se requiere justificación adicional.
