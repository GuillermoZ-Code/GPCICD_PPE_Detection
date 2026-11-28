# Feature Specification: HU-088 — Historial de análisis de la sesión

**Feature Branch**: `feature/089-hu-088-historial-sesion`

**Created**: 2026-11-28

**Status**: En implementación

**Input**: Issue #144 — «HU-088 — Historial de análisis de la sesión en la SPA». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-11`, P2 · ola 2, 3 SP, 12 pruebas objetivo.
Depende de HU-077 (#133, *Done*).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Comparar análisis de la sesión (Priority: P2)

Como usuario, quiero ver los análisis realizados en la sesión, para comparar resultados
de varias imágenes sin volver a subirlas.

**Acceptance Scenarios**:

1. **AC-01**: **Dado** el flujo, **Cuando** termina un análisis, **Entonces** aparece en
   una lista con miniatura, nombre, conteo de detecciones y modelo; al seleccionarlo se
   ve el detalle de clases.
2. **AC-02**: **Dado** el historial, **Cuando** se guarda o recupera, **Entonces** vive
   solo en `localStorage`; ninguna petición lo envía al servidor.
3. **AC-03**: **Dadas** las funciones de almacenamiento y la lista, **Cuando** se
   ejecutan las pruebas, **Entonces** cubren agregar, limitar, limpiar, recuperar y
   tolerar datos corruptos.

### Edge Cases

- Sin análisis, la sección muestra un estado vacío.
- El historial se limita a 8 entradas; las más recientes van primero.
- Un JSON corrupto en `localStorage` no rompe la SPA: se devuelve una lista vacía.
- Las miniaturas `blob:` se muestran en la sesión pero no se persisten; al recargar, la
  entrada conserva nombre, conteo y modelo y muestra el marcador de respaldo.
- `localStorage` lleno o bloqueado no debe romper la inferencia.

## Requirements *(mandatory)*

- **FR-001**: Debe existir un módulo de almacenamiento con `loadHistory`, `saveHistory`,
  `addHistoryEntry`, `clearHistory` y `makeHistoryEntry`.
- **FR-002**: El historial debe limitarse a `MAX_HISTORY = 8` y ordenar lo más reciente
  primero.
- **FR-003**: La lista debe mostrar miniatura (o marcador), nombre, conteo y modelo.
- **FR-004**: Al seleccionar una entrada debe mostrarse el detalle de clases y conteos.
- **FR-005**: Debe existir un botón «Limpiar historial» que vacíe la lista y el storage.
- **FR-006**: Ninguna función del historial debe llamar a `fetch` ni a la API.
- **FR-007**: Al menos 12 pruebas deben cubrir AC-01, AC-02 y AC-03.

## Success Criteria

- **SC-001**: 12/12 pruebas de `App.history.test.tsx` en verde.
- **SC-002**: `make frontend-check` en verde.
- **SC-003**: Las pruebas de HU-077/HU-080/HU-081 siguen en verde.

## Test Mapping

| AC | Prueba |
|---|---|
| AC-02 | `historial vacío sin storage` |
| AC-02 | `agrega y recupera el más reciente primero` |
| AC-02 | `limita a MAX_HISTORY` |
| AC-02 | `tolera JSON corrupto` |
| AC-02 | `limpia el storage` |
| AC-02 | `no llama a fetch` |
| AC-01 | `estado vacío antes de analizar` |
| AC-01 | `lista el análisis con miniatura, conteo y modelo` |
| AC-01 | `conserva varios análisis` |
| AC-01 | `muestra el detalle de clases` |
| AC-03 | `limpia el historial desde la interfaz` |
| AC-03 | `persiste al remontar` |
