# Feature Specification: HU-081 — Estados de carga, error y reintento

**Feature Branch**: `feature/082-hu-081-estados-ui`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #137 — «HU-081 — Estados de carga, error y reintento». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-11`, P1, ola 1, 1 SP, 4 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Saber qué pasa sin recargar la página (Priority: P1)

Como usuario, quiero mensajes claros mientras se analiza la imagen o si algo falla, y
poder reintentar sin volver a seleccionar el archivo, para no perder el trabajo ni
quedarme mirando un indicador que no avanza.

**Why this priority**: con la API relativa de HU-072, el primer arranque sin backend o una
red lenta dejan la interfaz en «Analizando…» sin explicación; el usuario recarga y pierde
la selección. Además, la observación del M3 pedía estados explícitos en la SPA.

**Independent Test**: con un cliente que nunca resuelve, el aviso de espera aparece tras
el umbral configurado; con un cliente que falla una vez, el botón «Reintentar» repite el
análisis y termina en éxito, sin volver a subir la imagen.

**Acceptance Scenarios** (AC de la issue #137):

1. **AC-01**: **Dado** un análisis en curso, **Cuando** supera el tiempo de espera
   configurable, **Entonces** la interfaz muestra el progreso y un aviso de que sigue
   procesando.
2. **AC-02**: **Dado** un error de red, **Cuando** el usuario pulsa «Reintentar»,
   **Entonces** se repite el análisis con el mismo archivo y la misma imagen.
3. **AC-03**: **Dado** el ciclo de la pantalla, **Cuando** se ejecutan las pruebas,
   **Entonces** los estados inactivo, seleccionado, carga y error son distinguibles.

### Edge Cases

- Error de validación (tipo o tamaño): no hay archivo asociado, así que **no** se ofrece
  reintento; se corrige eligiendo otra imagen.
- El aviso de espera no aparece si la inferencia termina antes del umbral.
- Un reintento vuelve a estado de carga y oculta el botón mientras está en curso.
- El umbral por omisión es 8 s y se puede cambiar por prop (pruebas y demos).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La interfaz MUST mostrar un indicador de progreso con `role="status"`
  mientras el análisis está en curso.
- **FR-002**: Transcurrido `slowAfterMs` (8 s por omisión), MUST mostrar un aviso de que
  el análisis sigue en curso y cuánto lleva.
- **FR-003**: El estado de error MUST mostrar el mensaje y, si hay archivo e imagen, un
  botón «Reintentar» que repita el análisis.
- **FR-004**: El reintento MUST reutilizar el archivo y la URL ya seleccionados, sin pedir
  de nuevo la imagen.
- **FR-005**: Mientras se reintenta, el botón MUST ocultarse y volver el indicador de
  progreso.
- **FR-006**: Un error de validación (sin archivo) MUST NOT ofrecer reintento.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El usuario distingue inactivo, seleccionado, carga y error sin recargar.
- **SC-002**: Al menos 4 pruebas de Vitest cubren los tres AC.
- **SC-003**: `make frontend-check` y `make check` en verde.

## Assumptions

- El cliente de inferencia sigue el contrato `DetectorClient` (ADR 0005); no cambia.
- El umbral de espera es de presentación, no un timeout de red: la petición no se aborta.
- El estado de error conserva archivo y URL desde HU-007; solo se añade la acción.
