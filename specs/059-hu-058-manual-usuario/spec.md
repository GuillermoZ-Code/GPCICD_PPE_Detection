# Feature Specification: HU-058 — Manual de usuario de la SPA

**Feature Branch**: `feature/059-hu-058-manual-usuario`

**Created**: 2026-11-28

**Status**: En implementación (issue #114 en *In progress*)

**Input**: Issue #114 — «HU-058 — Manual de usuario de la SPA». Asignada a Eliana
(`ElianaCardona`), épica `ep-15`, P2 · ola 3, 1 SP, 4 pruebas objetivo. Depende de
HU-077 (#133), integrada por el PR #267 (`d81b996`) en `develop`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Seguir el flujo rediseñado sin ayuda (Priority: P2)

Como usuario sin conocimientos técnicos, quiero un manual con capturas del flujo
01 Selección → 02 Análisis → 03 Resultados, para usar el detector sin ayuda.

**Why this priority**: HU-077 cambió la interfaz y el manual anterior no describía los
pasos visibles ni el resumen por clase; sin guía, el usuario no sabe qué esperar en cada
pantalla.

**Independent Test**: `tests/test_manual_usuario_spa.py::test_ac_01_flujo_con_capturas_reales`
comprueba que el manual nombra los tres pasos, enlaza cuatro capturas versionadas y que
los archivos son PNG reales generados desde la SPA local.

**Acceptance Scenarios** (AC de la issue #114):

1. **AC-01**: **Dado** el manual, **Cuando** se abre, **Entonces** describe el flujo
   completo con capturas de la interfaz rediseñada y aclara que se tomaron en ejecución
   local con API simulada, no en el sitio remoto.

### User Story 2 - Interpretar «sin detecciones» y sus límites (Priority: P2)

Como usuario, quiero entender qué significa un resultado vacío y qué no puede afirmar el
detector, para no confundir ausencia de EPP con falta de evidencia.

**Why this priority**: la SPA informa «sin detecciones» cuando la lista está vacía; el
modelo no tiene clase `person` ni `no-EPP`, por lo que el manual debe exigir cautela.

**Independent Test**:
`tests/test_manual_usuario_spa.py::test_ac_02_sin_detecciones_y_limites_explicitos`.

**Acceptance Scenarios**:

1. **AC-02**: **Dado** un resultado vacío, **Cuando** se lee el manual, **Entonces**
   explica que la inferencia terminó sin hallar las clases reconocidas, que los filtros y
   el umbral pueden ocultar detecciones y que no es una certificación de cumplimiento.

### User Story 3 - Verificar la estructura del documento (Priority: P2)

Como equipo, queremos una prueba estructural del manual, para evitar enlaces rotos o
capturas ausentes en la entrega.

**Why this priority**: el entregable es documental; la evidencia debe ser reproducible y
no depender de una revisión visual manual.

**Independent Test**:
`tests/test_manual_usuario_spa.py::test_ac_03_estructura_y_enlaces_del_manual`.

**Acceptance Scenarios**:

1. **AC-03**: **Dado** el repositorio, **Cuando** se ejecuta pytest, **Entonces** una
   prueba valida secciones, enlaces, fecha de verificación y procedencia de las capturas.

### Edge Cases

- Si la imagen no es JPEG/PNG o supera 10 MB, el manual remite al catálogo de errores
  (`docs/manual/errores.md`) en vez de duplicar códigos HTTP.
- Si los filtros visuales ocultan todas las detecciones, el resumen muestra 0 y la
  leyenda desaparece; el manual lo explica dentro de «sin detecciones».
- Las capturas usan una API simulada para que el flujo sea reproducible sin modelo ni
  Droplet; el manual no las presenta como medición de producción.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/manual/README.md` MUST existir y describir los pasos 01, 02 y 03 con
  los textos visibles de `FlowSteps`, `UploadPanel`, `DetectionSummary` y
  `DetectionLegend`.
- **FR-002**: El manual MUST enlazar cuatro capturas PNG versionadas en
  `docs/manual/capturas/`: selección, análisis, resultados y sin detecciones.
- **FR-003**: Cada captura MUST generarse desde la SPA local y el manual MUST declarar
  el origen (API simulada, sin validación remota).
- **FR-004**: El manual MUST explicar «sin detecciones» y tres límites: clases del modelo,
  umbral/filtros y ausencia de certificación de cumplimiento.
- **FR-005**: El manual MUST enlazar `docs/manual/errores.md` y declarar una fecha de
  verificación.
- **FR-006**: Al menos 4 pruebas pytest MUST referenciar AC-01, AC-02 y AC-03.

### Non-Functional Requirements

- No se modifica `frontend/`: el manual documenta la interfaz ya fusionada en #267.
- No se toca HU-055 ni `docs/operacion/despliegue.md`; Guillermo conserva esa HU.
- No se publican credenciales ni datos personales en capturas o texto.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 4/4 pruebas nuevas en verde.
- **SC-002**: `make check` y `make frontend-check` en verde sin cambios de dependencias.
- **SC-003**: Cuatro PNG válidos, legibles y enlazados desde el manual.
- **SC-004**: CI remota se reporta solo con evidencia de GitHub; local se declara como tal.

## Acceptance → evidencia

| AC | Evidencia |
|---|---|
| AC-01 | `tests/test_manual_usuario_spa.py::test_ac_01_flujo_con_capturas_reales`, `docs/manual/README.md` §3, `docs/manual/capturas/01-seleccion.png`, `docs/manual/capturas/02-analisis.png`, `docs/manual/capturas/03-resultados.png` |
| AC-02 | `tests/test_manual_usuario_spa.py::test_ac_02_sin_detecciones_y_limites_explicitos`, `docs/manual/README.md` §5, `docs/manual/capturas/04-sin-detecciones.png` |
| AC-03 | `tests/test_manual_usuario_spa.py::test_ac_03_estructura_y_enlaces_del_manual`, `tests/test_manual_usuario_spa.py::test_capturas_declaran_origen_local` |
