# Implementation Plan: HU-008 — Evaluación del detector

**Branch**: `feature/009-hu-008-evaluador` | **Date**: 2026-11-10 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/009-hu-008-evaluacion/spec.md` e issue #8.

## Summary

Implementar un evaluador versionado que cargue un artefacto YOLO identificado, evalúe
una partición etiquetada y genere un informe con métricas globales y por clase,
protección de particiones y análisis de errores. El informe de evaluación de esta rama
usa el mismo protocolo y documenta la evidencia.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `ultralytics` como extra `inference`; `numpy`, `opencv-python-headless`

**Storage**: JSON y Markdown en `artifacts/eval/`; pesos y dataset fuera de Git

**Testing**: pytest (AAA), sin GPU, sin dataset completo y sin red

**Target Platform**: CPU

**Project Type**: library + CLI

**Performance Goals**: evaluación completa en CPU; no se fija umbral de latencia aquí

**Constraints**: no entrenar, no descargar pesos, no versionar dataset ni artefactos

**Scale/Scope**: 2 particiones (`test` de 1.094 y `test_original_sin_fuga` de 492),
6 clases y un informe por corrida

## Constitution Check

- [x] `uv` como único gestor.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Contract-first y AGPL-3.0-only.
- [x] Sin LLM en inferencia.
- [x] Test-first: cada AC tendrá una prueba que lo referencia.

## Project Structure

```text
src/ppe_detection/evaluation/
├── __init__.py
└── evaluate.py          # carga del modelo, val, reporte JSON/MD

tests/
└── test_evaluation.py   # pruebas con métricas falsas y configuración

docs/evaluation/
└── HU-008.md            # informe de evaluación y análisis de errores
```

## Phases

1. **Tests first**: reporte, configuración, protección de particiones y errores.
2. **Evaluador**: `evaluate.py` con `YOLO.val`, validación de catálogo y escritura de
   `summary.json`/`summary.md`.
3. **Evidencia**: ejecutar sobre 492 y 1.094; comparar con el baseline de SPI-02.
4. **Informe**: completar FP/FN y limitaciones; enlazar desde `specs/README.md` y el
   backlog.
5. **Cierre**: `make check`, PR y actualización de estado.

## Risks

| Riesgo | Mitigación |
|--------|------------|
| Diferencia de versión Ultralytics 8.4.198 vs 8.4.202 | Fijar la versión de evaluación y declararla en el informe |
| Dataset ausente en otra máquina | Rutas configurables y evidencia de SHA256 |
| `safety_shoe` con muy pocas instancias en eval492 | Reportar conteos y no concluir con 6 objetos |
| Evaluación lenta en CPU | Cachear etiquetas y documentar el tiempo |
| Fuga de datos | Usar `test_original_sin_fuga` y documentar la separación |
