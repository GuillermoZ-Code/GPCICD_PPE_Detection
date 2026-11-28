# Feature Specification: HU-040 — Guía de reproducibilidad del entrenamiento

**Feature Branch**: `feature/041-hu-040-reproducibilidad-entrenamiento`

**Created**: 2026-11-26

**Status**: En implementación

**Input**: Issue #96 — «Guía de reproducibilidad del entrenamiento». Asignada a
Hernán (`HestradaUAO`), épica `ep-15`, P1, ola 3, 1 SP, 4 pruebas objetivo. Depende de
HU-018, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Repetir el entrenamiento y verificar el artefacto (Priority: P1)

Como evaluador externo, quiero una guía con comandos, versiones, semilla, hardware,
tiempos y enlaces a MLflow, para verificar cómo se produjo el modelo sin depender del
conocimiento del equipo.

**Why this priority**: el resultado del M4 se sustenta en un fine-tuning en GPU
externo. Sin una guía reproducible, el jurado no puede distinguir una corrida real de
un resultado manual.

**Independent Test**: leer `docs/evaluation/reproducibilidad.md` y comprobar que tiene
las secciones, versiones, semilla, tiempos, enlaces a MLflow y al artefacto.

**Acceptance Scenarios** (AC de la issue #96):

1. **AC-01**: **Dada** la guía, **Cuando** se revisa, **Entonces** contiene pasos con
   `uv`, versiones, semilla, hardware y tiempos.
2. **AC-02**: **Dada** la guía, **Cuando** se revisa, **Entonces** enlaza los runs de
   MLflow y el paquete/artefacto del modelo.
3. **AC-03**: **Dada** la guía, **Cuando** se ejecuta la prueba estructural,
   **Entonces** las secciones obligatorias están presentes y no se exponen secretos.

### Edge Cases

- El entorno original de Colab no es reproducible exactamente: se declara la limitación.
- El dataset y los pesos están fuera de Git: se documentan rutas externas y SHA256.
- Colab/Kaggle solo se usan como cómputo GPU; no se versionan notebooks.
- Los runs de MLflow se regeneran; la guía enlaza el procedimiento y la comparación.
- La evaluación se ejecuta en CPU, no en la GPU de entrenamiento.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La guía MUST documentar `uv`, Python, Ultralytics, torch y la semilla.
- **FR-002**: MUST registrar hardware de entrenamiento y evaluación, y tiempos.
- **FR-003**: MUST enlazar MLflow, la comparación de runs y `models.lock`.
- **FR-004**: MUST indicar que el artefacto se verifica por SHA256 y vive fuera de Git.
- **FR-005**: MUST declarar las limitaciones de reproducibilidad del entorno GPU.
- **FR-006**: Las pruebas MUST verificar secciones, versiones, enlaces y ausencia de
  secretos.
- **FR-007**: No se agregan dependencias ni se entrena en CI.

### Key Entities

- **Guía de reproducibilidad**: `docs/evaluation/reproducibilidad.md`.
- **Run de entrenamiento**: configuración, versiones, semilla, tiempos y SHA256.
- **Artefacto**: `best.pt`/`best.onnx` fuera de Git, referenciados por `models.lock`.
- **MLflow**: tracking de runs y comparación.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Pasos, versiones y tiempos | `tests/test_reproducibilidad.py::test_guide_documents_uv_versions_seed_hardware_and_time`, `tests/test_reproducibilidad.py::test_guide_has_required_sections` |
| AC-02 MLflow y artefacto | `tests/test_reproducibilidad.py::test_guide_links_mlflow_and_model_package` |
| AC-03 Estructura sin secretos | `tests/test_reproducibilidad.py::test_guide_has_required_sections`, `tests/test_reproducibilidad.py::test_guide_does_not_expose_secrets_or_user_paths` |

## Success Criteria *(mandatory)*

- **SC-001**: La guía se entiende sin abrir el notebook de Colab.
- **SC-002**: El SHA256 del modelo y el manifiesto son verificables.
- **SC-003**: La guía no expone secretos ni rutas personales.
- **SC-004**: La HU añade al menos 4 pruebas al inventario.

## Out of Scope

- Reentrenar el modelo.
- Descargar el dataset o los pesos.
- Cambiar `models.lock` o el artefacto.
- Publicar notebooks.
- Medir latencia o calidad del modelo.

## Assumptions

- El run de referencia es `yolo26` del 2026-11-22.
- El dataset limpio se conserva fuera de Git.
- MLflow y la comparación de runs están documentados.
- El artefacto productivo es YOLO26n con SHA256 `FEFB1F1A…0F27F9`.
