# Feature Specification: HU-025 — Manifiesto canónico del modelo

**Feature Branch**: `feature/026-hu-025-models-lock`

**Created**: 2026-11-21

**Status**: En implementación

**Input**: Issue #81 — «Manifiesto canónico del modelo (`models.lock`)». Asignada a
Hernán (`HestradaUAO`), épica `ep-14`, P0, Ola 1, 1 SP, 4 pruebas objetivo. No tiene
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Identificar el artefacto desplegado (Priority: P0)

Como evaluador técnico, quiero un manifiesto con nombre, versión, SHA256 y URL del
modelo, para saber exactamente qué artefacto se despliega y poder verificar su
integridad sin versionar los pesos en Git.

**Why this priority**: sin un manifiesto canónico, `/health`, la evaluación y MLflow
pueden reportar versiones distintas. Además, HU-026 necesita una fuente estable para
descargar y verificar el modelo.

**Independent Test**: cargar `models.lock`, construir la identidad del modelo y
comparar la referencia `sha256:<hash>` con la que exponen `/health` y el payload de
MLflow. Un manifiesto inválido debe fallar con un mensaje explícito.

**Acceptance Scenarios** (AC de la issue #81):

1. **AC-01**: **Dado** el repositorio, **Cuando** se lee `models.lock`, **Entonces**
   contiene los campos obligatorios `name`, `version`, `sha256` y `url`, **Y** el
   SHA256 es hexadecimal de 64 caracteres.
2. **AC-02**: **Dado** un manifiesto al que le falta un campo o cuyo SHA256 no tiene
   64 caracteres hexadecimales, **Cuando** se carga, **Entonces** falla con un error
   claro que identifica el problema.
3. **AC-03**: **Dado** un manifiesto válido, **Cuando** se consulta `/health` o se
   construye el payload de MLflow, **Entonces** ambos usan la misma versión y la misma
   referencia `sha256:<hash>` del manifiesto.

### Edge Cases

- `models.lock` ausente: la identidad cae al comportamiento anterior basado en
  `PPE_MODEL_PATH`, `PPE_MODEL_VERSION` y `PPE_MODEL_SHA256`.
- `models.lock` con TOML inválido: error explícito; no se ignora en silencio.
- SHA256 en minúsculas: se normaliza a mayúsculas, igual que `sha256_file`.
- `PPE_MODEL_SHA256` explícito: prevalece sobre el manifiesto y se valida igual.
- `PPE_MODEL_PATH` explícito: prevalece como ruta del artefacto, pero la versión y el
  SHA del manifiesto siguen siendo la referencia canónica cuando no hay valores
  explícitos equivalentes.
- `PPE_MODEL_MANIFEST` apunta a una ruta inexistente: error explícito; no se usa el
  manifiesto por defecto.
- URL local (`file://`) o remota (`https://`): el manifiesto solo la registra; la
  descarga y verificación pertenecen a HU-026.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El repositorio MUST incluir un `models.lock` versionado con `name`,
  `version`, `sha256` y `url`.
- **FR-002**: El sistema MUST exponer un cargador de manifiesto que valide campos
  obligatorios, tipos, SHA256 y TOML.
- **FR-003**: `default_model_identity()` MUST usar el manifiesto como fuente de
  versión y SHA cuando no haya valores explícitos equivalentes en el entorno.
- **FR-004**: `PPE_MODEL_MANIFEST` MUST permitir indicar una ruta alternativa; si se
  define y no existe, MUST fallar.
- **FR-005**: `/health` MUST reportar la versión, SHA256, artefacto y referencia del
  manifiesto cuando este sea la fuente activa.
- **FR-006**: El payload de MLflow MUST usar la misma referencia `sha256:<hash>` que
  el manifiesto.
- **FR-007**: Los pesos MUST seguir fuera de Git; el manifiesto solo registra su
  ubicación y su hash.
- **FR-008**: No se agregan dependencias: se usa `tomllib` de la biblioteca estándar.

### Key Entities

- **ModelManifest**: nombre, versión, SHA256 y URL del artefacto.
- **ModelIdentity**: identidad consumida por REST, gRPC, `/health` y MLflow.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Manifiesto completo | `tests/test_model_manifest.py::test_models_lock_has_required_fields` |
| AC-02 Manifiesto inválido | `test_models_lock_rejects_missing_field`, `test_models_lock_rejects_invalid_sha` |
| AC-03 Health y MLflow | `test_health_uses_manifest_identity`, `test_mlflow_payload_uses_manifest_reference` |
| FR-002 Cargador | `test_load_model_manifest_reads_toml`, `test_load_model_manifest_rejects_invalid_toml` |
| FR-004 Ruta explícita | `test_explicit_manifest_path_is_required_to_exist` |
| FR-003 Precedencia | `test_default_model_identity_uses_manifest`, `test_explicit_environment_wins_over_manifest` |

## Success Criteria *(mandatory)*

- **SC-001**: `models.lock` se carga sin red, GPU ni dataset.
- **SC-002**: Un manifiesto inválido falla antes de construir el detector.
- **SC-003**: `/health` y MLflow reportan la misma referencia de modelo.
- **SC-004**: `make check` y `make ownership-check` pasan; los pesos siguen fuera de
  Git.

## Out of Scope

- Descargar el modelo o verificar el archivo contra el SHA256 (HU-026).
- Publicar el modelo en GitLab Generic Packages (HU-024).
- Cambiar el detector, el contrato de detecciones o la UI.
- Editar el Dockerfile o `compose.yml`; la integración de contenedor se coordina en
  HU-024/HU-026.

## Assumptions

- El SHA256 canónico del modelo actual es el de
  `artifacts/models/yolo11s_clean/weights/best.pt`.
- La URL del manifiesto puede ser `file://` mientras HU-024 publica el paquete en
  GitLab; HU-026 verificará el contenido.
- El manifiesto se lee una vez al construir la app/servidor, no por petición.
- `PPE_MODEL_VERSION`, `PPE_MODEL_PATH` y `PPE_MODEL_SHA256` conservan su
  compatibilidad; el manifiesto es la fuente por defecto cuando no hay override.
