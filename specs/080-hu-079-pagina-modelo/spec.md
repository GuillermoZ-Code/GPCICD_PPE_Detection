# Feature Specification: HU-079 — Página «Acerca del modelo» desde `/health`

**Feature Branch**: `feature/080-hu-079-pagina-modelo`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #135 — «Página 'Acerca del modelo' desde `/health`». Asignada a
Eliana (`ElianaCardona`), épica `ep-11`, SP 1, P1, Ola 2, 4 pruebas objetivo.
Depende de HU-045 (contrato `/health/ready`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Identidad del modelo visible (Priority: P1)

Como usuario, quiero ver versión, SHA256, licencia y fuente del modelo, para saber
qué modelo generó el resultado.

**Why this priority**: sin identidad visible, una detección no se puede vincular
al artefacto que la produjo ni a sus condiciones de licencia.

**Independent Test**: `npm test -- --run src/components/ModelInfo.test.tsx` monta
el componente con `fetch` simulado; no requiere API ni red.

**Acceptance Scenarios** (AC de la issue #135):

1. **AC-01**: **Dado** un `GET /health/ready` con respuesta `ready`, **Cuando** se
   abre «Acerca del modelo», **Entonces** se muestran `model_version`,
   `model_reference` (etiquetado como referencia/commit), `model_sha256` y
   `api_version`.
2. **AC-02**: **Dado** el componente visible, **Cuando** se lee el pie, **Entonces**
   hay enlaces al código bajo AGPL-3.0-only y a la atribución CC-BY-4.0 del dataset.
3. **AC-03**: **Dado** que la API no responde o responde con error, **Cuando** se
   intenta cargar la información, **Entonces** se muestra un estado de error con
   mensaje y acción de reintento.

### Edge Cases

- La base de la API se resuelve con `resolveApiBaseUrl()` (`/api` por omisión) y
  se normalizan las barras finales.
- `model_sha256` puede ser `null`; en ese caso se muestra `—`.
- Una respuesta HTTP distinta de 200 se trata como error (incluido `503 not_ready`).
- El componente no provoca la carga del modelo: solo consulta `/health/ready`.
- No se modifica el contrato del backend ni los títulos/AC de la issue.

### Nota de contrato (decisión documentada)

`GET /health/ready` (`src/ppe_detection/api/app.py`, `ReadyResponse`) publica
`status`, `api_version`, `model_loaded`, `model_version`, `model_reference`,
`model_sha256` y `model_artifact`. **No** publica `commit`, `license` ni `source`.
Sin cambiar la issue (requiere aprobación de Jesús):

- «commit» se presenta como `model_reference` / `api_version` de la respuesta;
- licencia y fuente se presentan como enlaces estáticos: repositorio
  AGPL-3.0-only y dataset `51ddhesh/PPE_Detection` CC-BY-4.0, ya usados en el
  pie de `App.tsx`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: el componente MUST consultar `${apiBaseUrl}/health/ready` con `fetch`.
- **FR-002**: MUST mostrar versión del modelo, referencia/commit, SHA256 y versión
  de API cuando la respuesta es correcta.
- **FR-003**: MUST mostrar enlaces al código AGPL y a la atribución CC-BY.
- **FR-004**: MUST mostrar `role="alert"` y botón «Reintentar» si `fetch` falla o
  la respuesta no es `ok`.
- **FR-005**: la SPA MUST ofrecer la vista desde un botón «Acerca del modelo» sin
  cambiar el contrato de inferencia.
- **FR-006**: las 4 pruebas Vitest MUST ser nuevas, AAA y referenciar AC-01/AC-02/AC-03.

### Key Entities

- **ReadyResponse**: espejo tipado del contrato de `/health/ready`.
- **ModelInfo**: componente con estados `loading | ready | error`.
- **Manual**: guía de uso en `docs/operacion/modelo.md`.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `frontend/src/components/ModelInfo.test.tsx::AC-01 …` (dos pruebas: datos y base URL) |
| AC-02 | `frontend/src/components/ModelInfo.test.tsx::AC-02 …` |
| AC-03 | `frontend/src/components/ModelInfo.test.tsx::AC-03 …` |

## Success Criteria *(mandatory)*

- **SC-001**: las 4 pruebas nuevas pasan y las existentes de Vitest siguen verdes.
- **SC-002**: `npm run lint`, `npm test` y `npm run build` pasan.
- **SC-003**: la suite Python y `check_specs` siguen verdes; sin cambios en el backend.

## Out of Scope

- Cambiar `ReadyResponse`, `/health/ready`, títulos o AC de la issue #135.
- Modificar el cliente de inferencia, el compose ni el Dockerfile.
- Añadir dependencias npm (se usan React, Testing Library y Vitest ya instalados).

## Assumptions

- El proxy `/api` de Vite/nginx reenvía `/health/ready` a FastAPI sin reescritura
  adicional (misma base que `/predict`).
- Los enlaces de licencia son los mismos que ya muestra el pie de la SPA.
