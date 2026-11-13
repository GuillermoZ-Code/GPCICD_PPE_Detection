# Implementation Plan: HU-004 — Informe sin detecciones

**Branch**: `feature/004-hu-004-informe-sin-detecciones` | **Date**: 2026-11-10 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/006-hu-004-informe-sin-detecciones/spec.md`
e issue #4.

## Summary

Agregar el contrato de resultado vacío: un `InferenceResult` que envuelva la colección
de `Detection` producida por HU-002 (incluida la vacía con `FakeDetector`), clasifique
éxito/fallo y entregue un mensaje en español que distinga “no se detectaron” de un
error y no afirme incumplimiento ni ausencia real de EPP. API, interfaz y gRPC
(HU-006/007/010) consumen este contrato.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `numpy` (contrato existente); sin dependencias nuevas.

**Storage**: n/a (sin datos ni pesos).

**Testing**: pytest (AAA), `FakeDetector` determinista; sin GPU, sin red.

**Target Platform**: CPU

**Project Type**: library

**Performance Goals**: n/a (sin inferencia aquí).

**Constraints**: reutilizar el contrato de `contracts.py`; sin LLM; español en
mensajes; nombres de clase canónicos del catálogo.

**Scale/Scope**: 1 módulo nuevo (~60 líneas), 1 archivo de pruebas (~9 pruebas).

## Constitution Check

- [x] `uv` como único gestor; no hay dependencias nuevas.
- [x] src-layout y pruebas en `tests/` con patrón AAA.
- [x] Ruff, `ty`, pytest y `make check` (equivalente por comandos bajo PowerShell).
- [x] Sin datos ni pesos en Git.
- [x] Contract-first: reutiliza `Detection`, `FakeDetector` y `CLASSES`.
- [x] Sin LLM en inferencia.
- [x] Test-first: pruebas antes de la implementación (rojo → verde).
- [x] Uso responsable: reporta detecciones, no cumplimiento.

## Project Structure

```text
src/ppe_detection/
├── contracts.py        # existente: Detection, FakeDetector, CLASSES
└── results.py          # nuevo: InferenceResult + constantes de mensaje

tests/
└── test_results.py     # nuevo: AC-004.1 . AC-004.3 + FR

specs/006-hu-004-informe-sin-detecciones/
├── spec.md · plan.md · tasks.md · checklists/requirements.md
```

**Structure Decision**: un módulo plano `results.py` al lado de `contracts.py`. El
resultado envuelve el contrato y no lo modifica. La CLI de `detection/predict.py`
integra el mensaje vacío en `format_summary` (única superficie de consulta
disponible en este sprint); API/UI/gRPC la reutilizarán en HU-006/007/010.

## Phase 0 — Investigación

Sin preguntas abiertas (`/speckit.clarify` termina sin marcadores):

- **Wording**: se fija en la spec el mensaje exacto
  `NO_DETECTIONS_MESSAGE = "No se detectaron objetos EPP en la imagen."`; la nota de
  uso responsable es una constante aparte para no contaminar el mensaje que verificará
  AC-004.3.
- **`None` vs `[]`**: la respuesta vacía es `[]`; `None` es violación del contrato y
  se clasifica como error (FR-004), no se normaliza a vacío.
- **Ámbito**: presentación HTTP/gráfica es tarea de HU-006/HU-007/HU-010 (se documenta
  en la spec para que el análisis de cobertura no la exija aquí).

## Phase 1 — Diseño

- `InferenceResult(frozen=True)`: `detections: tuple[Detection, ...]`, `is_empty`,
  `is_error`, `message`.
- `build_inference_result(detections: Sequence[Detection] | None) -> InferenceResult`:
  - `None` → resultado de error (“la inferencia no devolvió una colección”).
  - vacío → `is_empty=True`, `is_error=False`, `NO_DETECTIONS_MESSAGE`.
  - con objetos → resumen singular/plural con recuento por clase en orden canónico.
- `build_error_result(error: BaseException) -> InferenceResult`: `is_error=True`,
  `is_empty=False`, mensaje `Error de inferencia: {tipo}`.
- `RESPONSIBLE_USE_NOTE`: constante para API/UI (HU-006/007/010), no parte del
  mensaje vacío.
- Recuento por clase en orden `CLASSES` (índice del `data.yaml`), estable y
  determinista.

## Complexity Tracking

No hay violaciones a la constitución. Ningún suplente técnico nuevo: arranca el
módulo desde el contrato ya validado en producción por HU-001/HU-002.
