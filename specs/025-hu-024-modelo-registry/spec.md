# Feature Specification: HU-024 — Modelo en GitLab Generic Packages

**Feature Branch**: `feature/025-hu-024-modelo-registry`

**Created**: 2026-11-27

**Status**: Implementado

**Input**: Issue #80 — «HU-024 — Publicar el modelo en GitLab Generic Packages».
Épica `ep-06`, P0, 2 SP, 8 pruebas objetivo. Depende de HU-023 (ADR del modelo).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - El peso sale de un almacén versionado, no de un pendrive (Priority: P0)

Como responsable del despliegue, quiero que el artefacto del modelo viva en el registry
de paquetes del proyecto y que el pipeline lo verifique por SHA256, para que cualquier
servidor pueda reconstruir el sistema sin copiar archivos a mano.

**Why this priority**: sin un artefacto publicado no hay despliegue reproducible y el
servidor depende de que alguien recuerde subir el `best.pt`.

**Independent Test**: `models.lock` apunta al paquete genérico del proyecto; el job
`deploy` lo descarga, compara el SHA256 y lo monta en `/opt/ppe/models/best.pt`.

**Acceptance Scenarios** (AC de la issue #80):

1. **AC-01**: **Dado** el registro de paquetes, **Cuando** se publica el peso,
   **Entonces** queda en `packages/generic/ppe-detection-models/<versión>/best.pt`.
2. **AC-02**: **Dado** el paquete publicado, **Cuando** se descarga, **Entonces** su
   SHA256 coincide con `models.lock`.
3. **AC-03**: **Dado** el despliegue, **Cuando** arranca la API, **Entonces** monta el
   artefacto verificado en modo lectura.

### Edge Cases

- **Paquete inexistente**: el job de deploy falla antes de tocar el servidor.
- **SHA distinto**: se aborta el despliegue y no se reemplaza el modelo bueno.
- **Token sin permisos**: la publicación falla con 401/403 y no deja un paquete a medias.

## Requirements *(mandatory)*

- **FR-001**: El manifiesto MUST apuntar a la URL del paquete genérico del proyecto.
- **FR-002**: La versión del manifiesto MUST coincidir con la del paquete.
- **FR-003**: El SHA256 MUST estar en mayúsculas y coincidir con el archivo publicado.
- **FR-004**: El job de despliegue MUST verificar el SHA256 antes de copiar al servidor.
- **FR-005**: El peso MUST montarse `:ro`; nunca dentro de la imagen.

## Success Criteria *(mandatory)*

- **SC-001**: El paquete `ppe-detection-models/yolo26n-clean/best.pt` existe (5,21 MB).
- **SC-002**: Las pruebas estáticas verifican la URL, la versión y el SHA del manifiesto.
- **SC-003**: El sistema desplegado reporta `model_version = yolo26n-clean`.

## Assumptions

- El proyecto GitLab es privado: el pipeline usa `CI_JOB_TOKEN` para descargar.
- Los pesos de YOLO26n se publican una vez por versión; no se regeneran en CI.
