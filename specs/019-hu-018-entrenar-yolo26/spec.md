# Feature Specification: HU-018 — Entrenar YOLO26n y YOLO26s

**Feature Branch**: `feature/019-hu-018-entrenar-yolo26`

**Created**: 2026-11-21

**Status**: Parcial — YOLO26n entrenado; YOLO26s pendiente de decisión

**Input**: Issue #74 — «Entrenar YOLO26n y YOLO26s en GPU gratuita». Asignada a
Hernán (`HestradaUAO`), épica `ep-09`, P0, Ola 3, 5 SP, 16 pruebas objetivo. Depende
de HU-017.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Entrenar los candidatos YOLO26 (Priority: P0)

Como evaluador del modelo, quiero pesos YOLO26 entrenados con el dataset limpio, para
comparar contra el modelo productivo actual y decidir si conviene migrar.

**Why this priority**: sin pesos fine-tuneados no se puede comparar YOLO26 con YOLO11s
ni justificar el costo de latencia en CPU. El modelo actual sigue siendo el fallback.

**Independent Test**: cargar `yolo26n_clean/weights/best.pt`, verificar que tiene las
6 clases EPP y ejecutar inferencia; revisar `run_manifest.json`, `eval/summary.json`
y las curvas del run.

**Acceptance Scenarios** (AC de la issue #74):

1. **AC-01**: **Dados** los dos modelos, **Cuando** se entrenan, **Entonces** usan la
   misma semilla, `imgsz=640` y la partición de `yolo11s-clean`.
2. **AC-02**: **Dados** los pesos resultantes, **Cuando** se registran, **Entonces**
   quedan fuera de Git con SHA256 y tamaño.
3. **AC-03**: **Dado** cada run, **Cuando** se archiva, **Entonces** sus curvas,
   `results.csv` y manifiesto quedan como artefactos del run.

### Edge Cases

- Una sesión de Colab se corta a mitad de entrenamiento: el backup cada 5 épocas
  permite reanudar con `last.pt`.
- El run no produce `results.csv` coherente con el manifiesto: se conserva como
  archivo crudo y se marca la inconsistencia; el manifiesto y `summary.json` mandan.
- Una clase no tiene verdaderos positivos: se reporta explícitamente; no se oculta en
  el promedio.
- El modelo `s` no cabe en el tiempo o no mejora: se documenta la decisión y se
  mantiene `n` como candidato.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El run de YOLO26n MUST usar `yolo26n.pt`, `imgsz=640`, `seed=42` y la
  misma partición que `yolo11s-clean`.
- **FR-002**: El run de YOLO26s MUST usar la misma configuración, si se ejecuta.
- **FR-003**: Los pesos MUST quedar fuera de Git, con SHA256 y tamaño.
- **FR-004**: El run MUST archivar `run_manifest.json`, `eval/summary.json`,
  `eval/summary.md`, curvas y `results.csv`.
- **FR-005**: El informe MUST comparar el resultado con YOLO11s y declarar el estado
  de `safety_shoe`.
- **FR-006**: Si YOLO26s no se entrena, el informe MUST explicar la decisión con
  evidencia de latencia/tiempo y dejar el AC marcado como pendiente.
- **FR-007**: No se versionan pesos, datasets ni imágenes.

## Acceptance → Evidence

| AC | Evidencia actual |
|----|------------------|
| AC-01 YOLO26n | `run_manifest.json`: `yolo26n.pt`, 100 épocas, `imgsz=640`, `seed=42` |
| AC-01 YOLO26s | Pendiente de decisión |
| AC-02 Pesos fuera de Git | `artifacts/models/yolo26n_clean/weights/` + SHA256 |
| AC-03 Curvas y CSV | `dist/analisis/yolo26n/eval/` y `raw/results.csv` |

## Success Criteria *(mandatory)*

- **SC-001**: El modelo YOLO26n carga con las 6 clases EPP.
- **SC-002**: El SHA256 de `best.pt` coincide con el manifiesto.
- **SC-003**: El informe permite decidir si se entrena YOLO26s.
- **SC-004**: No se versionan pesos ni artefactos pesados.

## Out of Scope

- Evaluación comparativa formal (HU-019).
- Calibración de umbrales (HU-029).
- Export ONNX como decisión de producción (HU-020/HU-022).
- Cambiar `models.lock` o el modelo productivo.

## Assumptions

- El dataset limpio y los YAML de Colab son los usados para `yolo11s-clean`.
- La GPU de Colab es suficiente para 100 épocas de YOLO26n en una sesión.
- El modelo `s` se decide después de ver el resultado y la latencia de `n`.
