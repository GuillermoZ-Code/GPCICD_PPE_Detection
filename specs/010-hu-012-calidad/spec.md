# Feature Specification: HU-012 — Verificaciones automatizadas de calidad

**Feature Branch**: `feature/010-hu-012-calidad`

**Created**: 2026-11-10

**Status**: En revisión (PR #49)

**Input**: Issue #12 — «Ejecutar verificaciones automatizadas de calidad». Asignada a
Hernán (EP-04, Must Have, M3-S2). Depende de los contratos de HU-006, HU-007 y HU-010,
ya fusionados.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ejecutar una suite de calidad con un informe claro (Priority: P1)

Como integrante del equipo, quiero ejecutar una verificación automatizada que informe
el resultado de lint, formato, tipos y pruebas, para detectar regresiones antes de
integrar.

**Why this priority**: es la compuerta previa a cada PR y la evidencia de HU-012.

**Independent Test**: `uv run python -m ppe_detection.tools.calidad` ejecuta las
verificaciones y devuelve 0 si todas pasan; con una verificación fallida devuelve 1 y
la marca como FALLO.

**Acceptance Scenarios** (AC de la issue #12):

1. **AC-01**: **Dada** la suite del proyecto, **Cuando** se ejecuta, **Entonces**
   pytest finaliza satisfactoriamente e informa el resultado.
2. **AC-02**: **Dada** una regresión deliberada, **Cuando** se ejecuta la suite,
   **Entonces** el comando falla con un código distinto de cero.
3. **AC-03**: **Dado** un archivo con una violación configurada de Ruff, **Cuando** se
   ejecuta Ruff, **Entonces** reporta el incumplimiento.
4. **AC-04**: **Dadas** las pruebas unitarias, **Cuando** se ejecutan, **Entonces** no
   requieren GPU, dataset completo ni red.

### Edge Cases

- Una verificación tarda o falla: el informe conserva el nombre y el código de salida.
- `ruff`/`ty`/`pytest` ausentes: la verificación se reporta como fallo, no como éxito.
- Windows: la salida de las herramientas se decodifica en UTF-8 para evitar `cp1252`.
- La suite no debe ejecutarse a sí misma en bucle: el informe se prueba con un runner
  falso y la invocación real queda en el comando.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST exponer un comando de calidad que ejecute, como mínimo,
  `ruff check`, `ruff format --check`, `ty check` y `pytest`.
- **FR-002**: El comando MUST imprimir un informe por verificación con `OK`/`FALLO` y
  un resumen final.
- **FR-003**: El comando MUST devolver 0 si todas pasan y un código distinto de cero si
  alguna falla.
- **FR-004**: Las pruebas del comando MUST ser unitarias y deterministas, con un runner
  inyectable.
- **FR-005**: La suite NO MUST requerir GPU ni dataset completo.
- **FR-006**: La configuración de Ruff del proyecto MUST detectar al menos una
  violación deliberada (por ejemplo, un import sin usar).

## Success Criteria *(mandatory)*

- **SC-001**: AC-01 a AC-04 tienen pruebas pytest que los referencian.
- **SC-002**: `make check` sigue en verde.
- **SC-003**: El comando de calidad se documenta en el README o en `docs/`.
- **SC-004**: Una verificación fallida produce código de salida distinto de cero.

## Out of Scope

- Duplicar el job de CI o el frontend.
- Cobertura mínima (se decide más adelante).
- Pruebas de rendimiento o de carga.
