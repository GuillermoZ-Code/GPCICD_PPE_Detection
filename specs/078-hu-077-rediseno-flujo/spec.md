# Feature Specification: HU-077 — Rediseño del flujo de carga y resultados

**Feature Branch**: `feature/078-hu-077-rediseno-flujo`

**Created**: 2026-11-28

**Status**: En implementación

**Input**: Issue #133 — «HU-077 — Rediseño del flujo de carga y resultados». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-11`, P1 · ola 1, 2 SP, 8 pruebas objetivo.
Depende de HU-076 (#132, *Done*).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cargar y analizar con un flujo claro (Priority: P1)

Como usuario, quiero arrastrar o seleccionar una imagen, ver su vista previa y saber en
qué paso está el análisis, para no perderme entre la carga y los resultados.

**Why this priority**: el flujo de carga es la primera interacción de la SPA y el
requisito de HU-077; sin él, el usuario no sabe si la imagen se cargó ni si el detector
está trabajando.

**Independent Test**: las pruebas de `frontend/src/App.flow.test.tsx` cargan una imagen
por arrastre y por selector, comprueban la vista previa y el paso activo.

**Acceptance Scenarios**:

1. **AC-01**: **Dado** el flujo, **Cuando** el usuario arrastra una imagen o la elige
   con el selector, **Entonces** ve la vista previa, el nombre del archivo y un
   indicador de pasos (01 selección → 02 análisis → 03 resultados); durante la
   inferencia se muestra el progreso.

### User Story 2 - Entender los resultados de un vistazo (Priority: P1)

Como usuario, quiero un resumen y una leyenda por clase, para entender cuántos EPP se
detectaron y de qué categorías sin leer toda la tabla.

**Why this priority**: los resultados son el entregable del detector; un resumen y una
leyenda por clase hacen legible la salida y complementan la tabla existente.

**Independent Test**: las pruebas comprueban el resumen (detecciones, clases, confianza
media, tiempo y modelo) y la leyenda con el conteo por clase.

**Acceptance Scenarios**:

1. **AC-02**: **Dado** un resultado con detecciones, **Cuando** termina el análisis,
   **Entonces** se muestra un resumen con totales y una leyenda por clase con su color y
   conteo, además de la tabla de detecciones.

### User Story 3 - Probar el flujo con Testing Library (Priority: P1)

Como equipo, queremos pruebas de interacción que cubran el flujo completo, para evitar
regresiones en la SPA.

**Acceptance Scenarios**:

1. **AC-03**: **Dada** la suite de Vitest, **Cuando** se ejecuta, **Entonces** hay al
   menos 8 pruebas de interacción con Testing Library que cubren los AC-01 y AC-02.

### Edge Cases

- Si el archivo no es JPEG/PNG, se mantiene el mensaje de validación de HU-005 y el
  flujo sigue disponible.
- Si no hay detecciones, el resumen muestra 0 y la leyenda no se renderiza; se conserva
  el aviso de HU-004.
- Si los filtros visuales ocultan todas las detecciones, el resumen refleja 0 y se
  mantiene el aviso de filtros.
- La vista previa se revoca al cambiar de imagen o desmontar el componente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El flujo MUST aceptar imágenes por arrastre y por selector, con vista
  previa y nombre del archivo.
- **FR-002**: El flujo MUST mostrar tres pasos (01 selección, 02 análisis, 03
  resultados) con el paso activo identificable por `aria-current="step"`.
- **FR-003**: Durante la inferencia MUST existir un `progressbar` accesible y el paso 02
  MUST quedar activo.
- **FR-004**: Al terminar MUST mostrarse un resumen con detecciones, clases, confianza
  media, tiempo y modelo.
- **FR-005**: Cuando haya detecciones visibles MUST mostrarse una leyenda por clase con
  color, nombre, conteo y confianza media.
- **FR-006**: Al menos 8 pruebas de interacción con Testing Library MUST cubrir AC-01,
  AC-02 y AC-03.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 8/8 pruebas de `App.flow.test.tsx` en verde.
- **SC-002**: `make frontend-check` en verde (ESLint + Vitest + build).
- **SC-003**: Las pruebas existentes de HU-076/HU-081 siguen en verde.

## Test Mapping

| AC | Prueba |
|---|---|
| AC-01 | `App.flow.test.tsx::AC-01 acepta una imagen por arrastre` |
| AC-01 | `App.flow.test.tsx::AC-01 acepta una imagen por el selector` |
| AC-01 | `App.flow.test.tsx::AC-01 marca la selección como paso activo` |
| AC-01 | `App.flow.test.tsx::AC-01 activa el análisis y muestra progreso` |
| AC-01 | `App.flow.test.tsx::AC-01 mantiene la vista previa durante el análisis` |
| AC-02 | `App.flow.test.tsx::AC-02 muestra el resumen de detecciones` |
| AC-02 | `App.flow.test.tsx::AC-02 muestra la leyenda por clase` |
| AC-03 | `App.flow.test.tsx::AC-03 completa el flujo y activa resultados` |
