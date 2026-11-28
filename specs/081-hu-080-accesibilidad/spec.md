# Feature Specification: HU-080 — Accesibilidad WCAG 2.2 AA en la SPA

**Feature Branch**: `feature/081-hu-080-accesibilidad`

**Created**: 2026-11-28

**Status**: En implementación

**Input**: Issue #136 — «HU-080 — Accesibilidad WCAG 2.2 AA en la SPA». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-11`, P1 · ola 2, 2 SP, 8 pruebas objetivo.
Depende de HU-076 (#132, *Done*).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Navegar sin barreras (Priority: P1)

Como usuario con discapacidad, quiero navegar con teclado y lector de pantalla, para
usar el detector sin depender del ratón ni de la vista.

**Acceptance Scenarios**:

1. **AC-01**: **Dado** el flujo, **Cuando** el usuario navega con teclado, **Entonces**
   hay un enlace para saltar al contenido, el foco es visible y lógico, y los resultados
   se anuncian por `aria-live`.
2. **AC-02**: **Dado** el tema claro u oscuro, **Cuando** se mide el contraste de los
   textos y estados, **Entonces** cumple AA (4,5:1 para texto y 3:1 para UI).
3. **AC-03**: **Dados** los componentes, **Cuando** se consultan sus roles y etiquetas,
   **Entonces** el archivo, el diálogo, la tabla, el progreso, el resumen y la leyenda
   tienen nombres accesibles.

### Edge Cases

- El enlace de salto solo se ve al recibir foco; no ocupa espacio en reposo.
- El foco se mueve al título de resultados al terminar el análisis, sin robar el foco
  durante la carga.
- El diálogo de configuración recibe el foco al abrirse y el botón Cerrar es el primero.
- Los estados de error usan `role="alert"`; los informativos, `role="status"`.

## Requirements *(mandatory)*

- **FR-001**: Debe existir un enlace «Saltar al contenido» que apunte a `#main`.
- **FR-002**: `<main>` debe ser un landmark con `id="main"` y foco programático.
- **FR-003**: Al pasar a `ready`, el foco debe ir al título de resultados.
- **FR-004**: El resumen de resultados debe tener `aria-live="polite"`.
- **FR-005**: El panel de resultados debe exponer `aria-busy` durante la carga.
- **FR-006**: Los tokens de texto y estados deben cumplir contraste AA en ambos temas.
- **FR-007**: El diálogo, la tabla, el progreso, el resumen y la leyenda deben tener
  nombre accesible y rol correcto.
- **FR-008**: Al menos 8 pruebas deben cubrir AC-01, AC-02 y AC-03.

## Success Criteria

- **SC-001**: 8/8 pruebas de `App.a11y.test.tsx` en verde.
- **SC-002**: `make frontend-check` en verde.
- **SC-003**: Las pruebas existentes de HU-076/HU-077/HU-081 siguen en verde.

## Test Mapping

| AC | Prueba |
|---|---|
| AC-01 | `App.a11y.test.tsx::AC-01 ofrece un enlace para saltar al contenido` |
| AC-01 | `App.a11y.test.tsx::AC-01 mantiene un landmark principal enfocable` |
| AC-01 | `App.a11y.test.tsx::AC-01 mueve el foco al título de resultados` |
| AC-01 | `App.a11y.test.tsx::AC-01 anuncia los resultados con aria-live` |
| AC-01 | `App.a11y.test.tsx::AC-01 marca el panel como ocupado durante la carga` |
| AC-02 | `App.a11y.test.tsx::AC-02 cumple contraste AA en el tema oscuro` |
| AC-02 | `App.a11y.test.tsx::AC-02 cumple contraste AA en el tema claro` |
| AC-03 | `App.a11y.test.tsx::AC-03 expone roles y etiquetas accesibles` |
