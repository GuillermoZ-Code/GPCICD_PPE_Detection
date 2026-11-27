# Feature Specification: HU-043 — Escaneo de secretos con gitleaks

**Feature Branch**: `feature/044-hu-043-gitleaks`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #99 — «HU-043 — Escaneo de secretos con gitleaks». Épica `ep-08`,
P0, 1 SP, 4 pruebas objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Un token real no llega al repositorio (Priority: P0)

Como equipo, quiero que cada push y cada PR se escaneen en busca de credenciales, para
que un token pegado por error no termine en el historial ni en la entrega.

**Why this priority**: durante el M4 apareció un token de DigitalOcean en un archivo
temporal del repo; no se versionó por suerte, no por una compuerta.

**Independent Test**: se introduce una cadena con formato de token en el escaneo y el
job `Secretos` falla con la ruta y la regla.

**Acceptance Scenarios** (AC de la issue #99):

1. **AC-01**: **Dado** el repositorio, **Cuando** se configura gitleaks, **Entonces**
   usa las reglas por defecto y una lista de exclusiones justificada.
2. **AC-02**: **Dado** un push o una PR, **Cuando** corre la CI, **Entonces** el job
   `Secretos` escanea el histórico completo con permisos de solo lectura.
3. **AC-03**: **Dado** el equipo en local, **Cuando** ejecuta `make secrets`, **Entonces**
   obtiene el mismo escaneo sin depender de GitHub.

## Requirements *(mandatory)*

- **FR-001**: La configuración MUST vivir en `.gitleaks.toml` en la raíz.
- **FR-002**: Las exclusiones MUST limitarse a documentación, fixtures y artefactos.
- **FR-003**: El job MUST correr en `push` y `pull_request` con `contents: read`.
- **FR-004**: El escaneo MUST usar `fetch-depth: 0` para revisar el histórico.
- **FR-005**: `make secrets` MUST permitir repetirlo en local.
- **FR-006**: Ningún archivo versionado MUST contener tokens con formato conocido.

## Success Criteria *(mandatory)*

- **SC-001**: El job `Secretos` aparece en la CI y termina en verde sobre `develop`.
- **SC-002**: 8 pruebas estáticas cubren configuración, workflow y superficie.
- **SC-003**: `make check` sigue en verde.

## Assumptions

- El repositorio es público y de una cuenta personal: la acción oficial no exige
  licencia.
- Las claves ficticias de `tests/` no son secretos reales y quedan excluidas.
