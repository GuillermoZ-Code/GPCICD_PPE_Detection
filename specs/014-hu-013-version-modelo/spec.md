# Feature Specification: HU-013 — Consultar la versión del modelo utilizado

**Feature Branch**: `feature/014-hu-013-version-modelo`

**Created**: 2026-11-12

**Status**: Fusionada (PR #54)

**Input**: Issue #13 — «Consultar la versión del modelo utilizado». Asignada a Jesús
(EP-04, Should Have, M3-S2). Depende de HU-002 y HU-009, ambas fusionadas.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Identificar el modelo de una inferencia (Priority: P1)

Como evaluador técnico del sistema, quiero identificar la versión del modelo que generó
una inferencia, para relacionar los resultados con su configuración y desempeño
documentado.

**Why this priority**: sin una referencia verificable no se puede reproducir ni explicar
un resultado; la API y gRPC ya devuelven un nombre de versión, pero no el artefacto.

**Independent Test**: con un `ModelIdentity` inyectado, `POST /predict` y `Detect`
devuelven versión, SHA256, ruta del artefacto y referencia; dos identidades distintas
producen respuestas distinguibles.

**Acceptance Scenarios** (AC de la issue #13):

1. **AC-013.1**: **Dado** un modelo cargado, **Cuando** se ejecuta una inferencia,
   **Entonces** queda disponible una referencia verificable de la versión utilizada,
   **Y** dicha referencia puede relacionarse con el artefacto correspondiente.
2. **AC-013.2**: **Dadas** dos versiones diferentes del detector, **Cuando** se comparan
   resultados generados por cada una, **Entonces** se pueden distinguir las versiones
   que produjeron esos resultados.
3. **AC-013.3**: **Dada** una versión cuyos pesos se almacenan fuera de Git, **Cuando**
   se consulta su referencia, **Entonces** es posible identificar su ubicación controlada
   o su identificador de artefacto, **Y** no se requiere almacenar los pesos en el
   repositorio.

### Edge Cases

- `PPE_MODEL_PATH` ausente: la identidad existe con versión `unknown`, sin artefacto.
- `PPE_MODEL_SHA256` con formato inválido: error de configuración explícito.
- Artefacto configurado que no existe: no se inventa un SHA; la referencia cae a la
  versión o al artefacto.
- Dos modelos con el mismo nombre pero distinto SHA256: se distinguen por el hash.
- Modelo sin SHA y sin ruta: la referencia es `version:<versión>`.
- Petición REST/gRPC sin identidad inyectada: se usa la configuración del entorno.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST definir `ModelIdentity` con `version`, `sha256` y
  `artifact`, y una propiedad `reference` determinista.
- **FR-002**: `default_model_identity()` MUST leer `PPE_MODEL_PATH`,
  `PPE_MODEL_VERSION` y `PPE_MODEL_SHA256`; si no hay SHA explícito y el artefacto
  existe, MUST calcularlo.
- **FR-003**: `PPE_MODEL_SHA256` MUST validarse como SHA256 hexadecimal de 64
  caracteres cuando se usa.
- **FR-004**: `POST /predict` MUST incluir `model_version`, `model_sha256`,
  `model_artifact` y `model_reference`.
- **FR-005**: El contrato gRPC `ppe.v1.PredictResponse` MUST incluir los mismos campos
  de identidad del modelo.
- **FR-006**: REST y gRPC MUST aceptar una identidad inyectada para pruebas y MUST NOT
  acoplarse a un artefacto concreto.
- **FR-007**: La referencia MUST usar el formato `sha256:<hash>` cuando hay SHA; es el
  mismo formato que usa el tag `model_reference` de MLflow (HU-009).
- **FR-008**: La identidad MUST NOT copiar ni versionar los pesos; solo registra su
  ruta y su hash.

### Key Entities

- **ModelIdentity**: versión legible, SHA256 opcional y ruta/URI del artefacto.
- **PredictResponse**: respuesta REST/gRPC con la identidad del modelo y las
  detecciones.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-013.1 Identificación del modelo | `tests/test_model_version.py::test_api_response_includes_model_identity`, `test_grpc_response_includes_model_identity`, `test_model_identity_reference_uses_sha256` |
| AC-013.2 Distinción de versiones | `test_api_two_versions_are_distinguishable`, `test_grpc_two_versions_are_distinguishable` |
| AC-013.3 Artefactos externos | `test_model_identity_exposes_artifact_path`, `test_default_model_identity_reads_version_and_artifact` |
| FR-002 Configuración | `test_default_model_identity_reads_explicit_sha`, `test_default_model_identity_computes_sha_from_path` |
| FR-003 SHA válido | `test_default_model_identity_rejects_invalid_sha_env` |
| FR-007 Enlace MLflow | `test_model_identity_reference_uses_sha256_format` |

## Success Criteria *(mandatory)*

- **SC-001**: Una inferencia REST y una gRPC del mismo modelo devuelven la misma
  referencia de identidad.
- **SC-002**: Dos identidades con versiones o SHA distintos se distinguen sin ambigüedad.
- **SC-003**: `make check` pasa sin GPU, sin dataset y sin red.
- **SC-004**: El contrato documenta los campos nuevos y el artefacto sigue fuera de Git.

## Out of Scope

- Model registry, promoción de versiones o despliegue multi-modelo.
- Cambiar el detector, el entrenamiento o las métricas de HU-008.
- Autenticación o control de acceso a la información del modelo.

## Assumptions

- El SHA256 del artefacto es el mismo que usa HU-008 y el tag `model_reference` de
  HU-009.
- La ruta del artefacto se recibe por `PPE_MODEL_PATH`; el hash puede venir por
  `PPE_MODEL_SHA256` o calcularse del archivo.
- La identidad se calcula una vez al crear la app o el servidor, no por petición.
