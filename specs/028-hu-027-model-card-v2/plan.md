# Implementation Plan: HU-027 — Model Card v2 con YOLO26, sesgos y limitaciones

**Branch**: `feature/028-hu-027-model-card-v2` | **Date**: 2026-11-26

**Spec**: [spec.md](spec.md)

**Input**: Issue #83 y `specs/028-hu-027-model-card-v2/spec.md`.

## Summary

Actualizar y proteger la Model Card de YOLO26n. La ficha ya existe; se añaden los
enlaces a `models.lock`, MLflow, errores y comparación, y se fijan con 8 pruebas
estructurales los AC de modelo, sesgos, uso responsable y licencia.

## Technical Context

**Language/Version**: Python 3.13 para las pruebas de documentación

**Primary Dependencies**: pytest y stdlib; sin dependencias nuevas

**Storage**: Markdown versionado; sin datos ni imágenes

**Testing**: pytest AAA; lectura del Markdown y aserciones de contenido

**Target Platform**: CPU / CI

**Project Type**: documentación del modelo

**Constraints**: no cambiar el modelo, sus métricas ni el artefacto

**Scale/Scope**: 8 pruebas, seis clases, dos modelos comparados

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red.
- [x] La ficha declara licencia, sesgos y límites.
- [x] No se versionan datos ni pesos.
- [x] No se cambia el contrato de detección.

## Project Structure

```text
docs/model-card.md
tests/test_model_card_v2.py
specs/028-hu-027-model-card-v2/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

La ficha mantiene su estructura y añade enlaces verificables:

- `models.lock` para la identidad del artefacto;
- `docs/operacion/mlflow.md` y `docs/evaluation/mlflow-comparacion.md`;
- `docs/evaluation/errores.md` para FP/FN;
- `docs/evaluation/YOLO26.md` para la comparación.

Las pruebas verifican selección, comparación, sesgos, uso responsable, enlaces y
licencia sin cargar el modelo.

## Phases

1. **Documento:** añadir enlaces y revisar el estado del rollout.
2. **Pruebas:** ocho casos estructurales.
3. **Verificación:** `make specs-check`, `make check`, `uv build`.
4. **Cierre:** PR con `Closes #83`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Ficha obsoleta | Pruebas de selección y comparación |
| Ocultar sesgos | Casos específicos para `safety_shoe` y `Gloves` |
| Afirmar cumplimiento | Prueba de uso no previsto |
| Enlaces rotos | Se enlazan archivos versionados existentes |
| Datos personales | Solo texto y métricas |

## Verification

```bash
uv run pytest tests/test_model_card_v2.py -q
make specs-check
make check
uv build
```
