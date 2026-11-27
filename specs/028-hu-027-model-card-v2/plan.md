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
docs/model-card.md                  # entregable existente (Hernán)
tests/test_model_card_v2.py         # nuevo: AC-01 a AC-03
specs/028-hu-027-model-card-v2/
├── spec.md
├── plan.md
└── tasks.md
```

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
| Métricas desactualizadas | Se citan de `docs/evaluation/YOLO26.md` y del run de MLflow |
| Confundir seleccionado con desplegado | El encabezado del documento lo aclara |
| Sesgos subestimados | Sección propia con las dos clases débiles y la procedencia desconocida |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_model_card_v2.py` (comparación y ADR 0009) |
| AC-02 | `tests/test_model_card_v2.py` (sesgos y uso no apto) |
| AC-03 | `tests/test_model_card_v2.py` (`models.lock`, MLflow y evaluación) |
