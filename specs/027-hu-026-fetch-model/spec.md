# Feature Specification: HU-026 — Descarga y verificación del modelo por SHA256

**Feature Branch**: `feature/027-hu-026-fetch-model`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #82 — «Descarga y verificación del modelo por SHA256». Asignada a
Hernán (`HestradaUAO`), épica `ep-06`, P0, Ola 1, 2 SP, 8 pruebas objetivo. Depende de
HU-025, ya fusionada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Descargar un artefacto confiable (Priority: P0)

Como pipeline de despliegue, quiero descargar el modelo declarado en `models.lock` y
verificar su SHA256, para impedir desplegar un artefacto alterado o incompleto.

**Why this priority**: el despliegue no puede depender de una URL sin integridad. El
manifiesto ya existe (HU-025); ahora falta el paso que materializa el artefacto.

**Independent Test**: con un manifiesto temporal y un archivo local servido por
`file://`, ejecutar `fetch`; el destino debe existir y coincidir con el SHA256. Con un
SHA incorrecto, el comando debe fallar y no dejar un archivo parcial.

**Acceptance Scenarios** (AC de la issue #82):

1. **AC-01**: **Dado** `models.lock`, **Cuando** se ejecuta
   `python -m ppe_detection.detection.artifact fetch`, **Entonces** lee el manifiesto y
   descarga el archivo en el destino indicado.
2. **AC-02**: **Dado** un archivo cuyo SHA256 no coincide, **Cuando** se verifica,
   **Entonces** el proceso aborta con código de salida distinto de cero y elimina el
   archivo temporal.
3. **AC-03**: **Dados** los tests, **Cuando** se ejecutan, **Entonces** usan
   `tmp_path` y un servidor/archivo simulado, sin red externa.

### Edge Cases

- URL `file://`: se copia el archivo local; no hay descarga HTTP.
- URL `http://` o `https://`: se descarga por bloques con timeout.
- Esquema no soportado: error explícito.
- Archivo origen inexistente: error explícito.
- SHA256 en mayúsculas o minúsculas: se compara en mayúsculas.
- Destino existente: se reemplaza solo después de verificar el SHA256.
- Fallo a mitad de descarga: se elimina el `.part`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El módulo MUST leer `models.lock` y construir la URL y el SHA256.
- **FR-002**: El comando `fetch` MUST aceptar `--manifest`, `--output` y `--timeout`.
- **FR-003**: MUST soportar `file://`, `http://` y `https://`.
- **FR-004**: MUST escribir en un archivo temporal y verificar antes de reemplazar.
- **FR-005**: MUST abortar con código no cero si el SHA256 no coincide.
- **FR-006**: MUST limpiar el temporal ante cualquier fallo.
- **FR-007**: MUST funcionar sin red en los tests, usando `file://` o un `urlopen`
  simulado.
- **FR-008**: No se agregan dependencias; se usa `urllib` de la biblioteca estándar.

### Key Entities

- **ModelManifest**: nombre, versión, SHA256 y URL.
- **ArtifactFetchResult**: ruta destino, SHA256 verificado y tamaño.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Descarga desde manifiesto | `test_fetch_from_manifest_file_url`, `test_cli_fetch_success` |
| AC-02 SHA inválido | `test_fetch_rejects_sha_mismatch`, `test_cli_fetch_sha_mismatch` |
| AC-03 Sin red | `test_fetch_http_uses_injected_urlopen`, `test_fetch_cleans_temp_file` |
| FR-003 Esquemas | `test_fetch_rejects_unsupported_scheme` |
| FR-004/006 Temporal | `test_fetch_does_not_replace_existing_on_failure` |

## Success Criteria *(mandatory)*

- **SC-001**: El comando descarga y verifica un archivo local sin red.
- **SC-002**: Un SHA incorrecto deja el destino intacto y devuelve código 1.
- **SC-003**: El archivo descargado tiene el mismo SHA256 del manifiesto.
- **SC-004**: `make check` pasa sin GPU, dataset ni red.

## Out of Scope

- Publicar el modelo en GitLab Generic Packages (HU-024).
- Descargar datasets o imágenes.
- Cambiar `models.lock` o el modelo productivo.
- Validar la firma criptográfica del manifiesto.

## Assumptions

- `models.lock` tiene `sha256` y `url` válidos.
- `file:///models/best.pt` es la URL provisional del contenedor; en local se usará un
  manifiesto temporal para probar.
- El destino se elige por CLI; el valor por defecto es `artifacts/models/best.pt`.
