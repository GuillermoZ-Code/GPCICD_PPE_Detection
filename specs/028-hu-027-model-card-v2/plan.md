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
# Implementation Plan: HU-027 — Model Card v2

**Branch**: `docs/m4-plan-real` | **Date**: 2026-11-27 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/028-hu-027-model-card-v2/spec.md`

## Summary

Documento único (`docs/model-card.md`) que declara el modelo seleccionado, lo compara
con la alternativa, expone sus sesgos por clase y enlaza la evidencia (manifiesto,
MLflow y evaluación). No hay código de producto: la entrega es la tarjeta y sus pruebas
estáticas.

## Technical Context

**Language/Version**: Markdown

**Primary Dependencies**: ninguna en ejecución; enlaces a `docs/evaluation/` y
`models.lock`

**Testing**: pytest estático sobre el Markdown

**Target Platform**: repositorio (GitHub y GitLab)

**Project Type**: documentación técnica

**Constraints**: las métricas se citan de los informes versionados; no se inventan

**Scale/Scope**: 1 documento, 3 AC

## Constitution Check

- **Datos y pesos fuera de Git**: la tarjeta declara los SHA256 y no copia pesos. ✅
- **Uso responsable**: declara que el sistema reporta EPP, no cumplimiento. ✅
- **AGPL y CC-BY**: declara licencias y atribución. ✅
- **Test-first**: pruebas estáticas sobre el documento. ✅

## Project Structure

```text
docs/model-card.md
tests/test_model_card_v2.py
docs/model-card.md                  # entregable existente (Hernán)
tests/test_model_card_v2.py         # nuevo: AC-01 a AC-03
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
## Design decisions

1. **Una tarjeta, dos modelos.** Declara YOLO26n como seleccionado y YOLO11s como
   desplegado hasta el rollout; evita prometer lo que aún no corre.
2. **Sesgos por clase, no genéricos.** `safety_shoe` y `Gloves` son las clases débiles y
   el documento lo cuantifica con mAP y recall.
3. **Enlaces en vez de copias.** `models.lock`, MLflow y el informe de evaluación son la
   fuente; la tarjeta no duplica valores que puedan quedar viejos.
4. **Spec retroactiva.** La HU se cerró sin spec y rompía la compuerta de trazabilidad;
   este directorio la deja auditable.

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
| Métricas desactualizadas | Se citan de `docs/evaluation/YOLO26.md` y del run de MLflow |
| Confundir seleccionado con desplegado | El encabezado del documento lo aclara |
| Sesgos subestimados | Sección propia con las dos clases débiles y la procedencia desconocida |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_model_card_v2.py` (comparación y ADR 0009) |
| AC-02 | `tests/test_model_card_v2.py` (sesgos y uso no apto) |
| AC-03 | `tests/test_model_card_v2.py` (`models.lock`, MLflow y evaluación) |
