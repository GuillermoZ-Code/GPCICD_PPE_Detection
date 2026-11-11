# Feature Specification: HU-009 — Consultar y comparar experimentos en MLflow

**Feature Branch**: `feature/011-hu-009-mlflow`

**Created**: 2026-11-11

**Status**: Implementada — pendiente de PR

**Input**: Issue #9 — «Consultar y comparar experimentos en MLflow». Asignada a Jesús
(EP-04, Must Have, M3-S2). Depende de HU-008 (evaluación instrumentada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registrar una evaluación como run (Priority: P1)

Como integrante del equipo ML, quiero registrar una evaluación terminada como un run de
MLflow, para conservar sus parámetros, métricas y la referencia del modelo evaluado.

**Why this priority**: sin un run identificable no hay trazabilidad ni comparación
posible; es la base de los otros dos criterios de aceptación.

**Independent Test**: con un `summary.json` de HU-008 y un tracker inyectado, el
registro devuelve un `run_id` y el payload contiene modelo, partición, configuración,
métricas globales y métricas por clase.

**Acceptance Scenarios** (AC de la issue #9):

1. **AC-009.1**: **Dada** una evaluación ejecutada correctamente, **Cuando** finaliza el
   proceso instrumentado, **Entonces** existe un run identificable en MLflow, **Y**
   registra parámetros, métricas y referencia del modelo evaluado.
2. **AC-009.2**: **Dados** dos runs registrados con identificadores distintos,
   **Cuando** se consultan mediante MLflow, **Entonces** sus configuraciones y
   resultados pueden distinguirse.
3. **AC-009.3**: **Dado** un run que referencia un artefacto de modelo, **Cuando** se
   consulta su registro, **Entonces** se puede identificar la versión o ubicación
   controlada del artefacto, **Y** el registro no depende de que los pesos estén
   almacenados en Git.

### Edge Cases

- `summary.json` ausente, vacío o sin las claves obligatorias.
- Modelo sin SHA256 o con un hash que no sea hexadecimal de 64 caracteres.
- Partición sin métricas por clase: se registran las clases presentes.
- Intento de registrar pesos (`.pt`, `.pth`, `.onnx`, `.safetensors`) o datasets
  (`.zip`) como artefactos: se rechaza con un error comprensible.
- MLflow no instalado: error que indica el extra `tracking`.
- Run inexistente al comparar: error controlado, sin traza cruda.
- Dos identificadores iguales en la comparación: se rechaza.
- Backend local sin red: la configuración por defecto debe funcionar en local.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST leer un `summary.json` generado por HU-008 y construir un
  payload con parámetros, métricas y etiquetas.
- **FR-002**: El payload MUST incluir la ruta y el SHA256 del modelo, el SHA256 del YAML
  del dataset cuando exista, la partición, `imgsz`, `conf`, `iou`, `seed`, `device`,
  imágenes e instancias.
- **FR-003**: El payload MUST incluir precision, recall, mAP50 y mAP50-95 globales y por
  clase, con nombres de métrica válidos para MLflow.
- **FR-004**: El registro MUST devolver el `run_id` de MLflow y aceptar un nombre de run
  explícito o uno determinista por defecto.
- **FR-005**: El sistema MUST consultar dos o más runs por `run_id` y generar una
  comparación legible que distinga configuración y métricas.
- **FR-006**: El registro MUST rechazar pesos y datasets como artefactos; la referencia
  del modelo se guarda como SHA256 y ruta, no copiando los pesos.
- **FR-007**: La integración con MLflow MUST ser perezosa y opcional: el paquete base y
  las pruebas unitarias no dependen de MLflow; el extra `tracking` lo habilita.
- **FR-008**: El sistema MUST funcionar con un backend local (SQLite o archivo) sin red
  ni servidor remoto.

### Key Entities

- **RunPayload**: parámetros, métricas, etiquetas y artefactos de un run.
- **RunView**: vista de un run consultado: `run_id`, nombre, parámetros, métricas y
  etiquetas.
- **RunTracker**: protocolo de registro y consulta; `MlflowTracker` es la implementación
  real y los tests usan un tracker falso.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-009.1 Registro de ejecución | `tests/test_tracking.py::test_build_run_payload_records_model_partition_and_config` y `test_log_evaluation_run_returns_run_id_and_passes_artifacts` |
| AC-009.2 Consulta de experimentos | `tests/test_tracking.py::test_compare_runs_distinguishes_two_runs` |
| AC-009.3 Vinculación de artefactos | `tests/test_tracking.py::test_build_run_payload_rejects_weights` y `test_render_comparison_includes_model_reference` |
| FR-002 Configuración y dataset | `tests/test_tracking.py::test_build_run_payload_records_dataset_sha_when_provided` |
| FR-007 MLflow opcional | Pruebas con `FakeTracker`, sin importar MLflow |

## Success Criteria *(mandatory)*

- **SC-001**: Un `summary.json` real de HU-008 se registra en un backend local de MLflow
  y devuelve un `run_id`.
- **SC-002**: Dos runs con particiones o configuraciones distintas se comparan y sus
  diferencias son visibles en Markdown.
- **SC-003**: `make check` pasa sin GPU, sin dataset completo, sin red y sin MLflow
  instalado.
- **SC-004**: El run referencia el modelo por SHA256 y no versiona ni copia pesos en Git.

## Out of Scope

- Servidor MLflow remoto, autenticación multiusuario, model registry y despliegue.
- Una interfaz web propia de experimentos; se usa la UI de MLflow.
- Entrenamiento, descarga de pesos o evaluación del detector (HU-008).
- Docker y CI/CD (HU-011 y HU-014).

## Assumptions

- El `summary.json` de HU-008 tiene `model.sha256`, `dataset.split`, `config`, `images`,
  `instances`, `metrics` y `per_class`.
- Los artefactos viven fuera de Git; la carpeta de MLflow (`mlruns/`, `mlartifacts/` o
  `mlflow.db`) está en `.gitignore`.
- MLflow 3.x se instala con el extra `tracking`; el backend local por defecto es
  `sqlite:///mlflow.db`.
