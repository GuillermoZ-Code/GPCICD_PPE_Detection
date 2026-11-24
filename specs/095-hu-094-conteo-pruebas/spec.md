# Feature Specification: HU-094 — Conteo reproducible de pruebas (`make pruebas`)

**Feature Branch**: `feature/095-hu-094-conteo-pruebas`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #150 — «Conteo reproducible de pruebas (`make pruebas`)». Asignada a
Jesús (`jesusriverosUAO`), épica `ep-14`, P0, Ola 1, 2 SP, 8 pruebas objetivo. No tiene
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Demostrar el avance hacia 1.200 sin contar a mano (Priority: P0)

Como equipo, quiero un comando que cuente los casos recolectados por pytest y por Vitest
y escriba la tabla por archivo e integrante, para demostrar el avance hacia 1.200
pruebas sin cifras contradictorias entre documentos.

**Why this priority**: hoy conviven 375, 425, 451 y 515 en distintos archivos. El
contador convierte el conteo en una salida reproducible y deja `PRUEBAS.md` como espejo
de `make check`, no como una transcripción manual.

**Independent Test**: `uv run python -m ppe_detection.tools.pruebas` imprime el resumen;
`--write` regenera `docs/curso/PRUEBAS.md`. Las pruebas del módulo usan salidas de pytest
y Vitest simuladas, sin ejecutar la suite real.

**Acceptance Scenarios** (AC de la issue #150):

1. **AC-01**: **Dado** el repositorio, **Cuando** se ejecuta el contador, **Entonces**
   suma los casos recolectados por pytest y por Vitest y muestra el total.
2. **AC-02**: **Dado** el conteo, **Cuando** se escribe el informe, **Entonces** incluye
   la tabla por archivo con su dueño y los totales por integrante.
3. **AC-03**: **Dado** el módulo, **Cuando** se ejecutan las pruebas, **Entonces** los
   parsers se validan con salidas simuladas, sin lanzar pytest ni Vitest.

### Edge Cases

- **`node_modules` ausente**: Vitest no puede listar los casos; el comando falla con un
  mensaje que dice cómo resolverlo, salvo que se use `--skip-frontend`.
- **Salida de pytest con formato doble-quiet** (`archivo.py: N`) o con ids
  (`archivo.py::test`): el parser acepta ambas.
- **Ruta absoluta de Vitest en Windows**: se normaliza a ruta relativa al repositorio.
- **Archivo sin dueño en `propiedad.toml`**: se muestra «sin dueño», no se inventa un
  responsable.
- **Un archivo con cero casos**: no aparece en la tabla; el total no cambia.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El repositorio MUST exponer `python -m ppe_detection.tools.pruebas` y el
  objetivo `make pruebas`.
- **FR-002**: El conteo de pytest MUST ejecutar `pytest --collect-only` y leer los casos
  recolectados, sin ejecutar la suite.
- **FR-003**: El conteo de Vitest MUST ejecutar `vitest list --json` y leer los casos
  listados, sin ejecutar la suite.
- **FR-004**: El informe MUST incluir resumen por suite, desglose por archivo con su
  dueño y totales por integrante.
- **FR-005**: `--write` MUST regenerar `docs/curso/PRUEBAS.md`; sin `--write` el comando
  solo imprime el resumen.
- **FR-006**: Los parsers MUST ser funciones puras que acepten la salida como texto o
  JSON, para probarlas sin subprocesos.
- **FR-007**: No se agregan dependencias: se usa la biblioteca estándar y PyYAML del
  entorno.
- **FR-008**: `--skip-frontend` MUST permitir contar solo pytest cuando Node no está
  disponible.

### Key Entities

- **ConteoPorArchivo**: ruta relativa, suite (`pytest`/`vitest`) y número de casos.
- **FilaDelInforme**: archivo, suite, pruebas y dueño resuelto desde `propiedad.toml`.
- **Informe**: resumen, desglose y totales por integrante en Markdown.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Suma pytest y Vitest | `tests/test_tools_pruebas.py::test_pytest_counter_accepts_both_formats`, `::test_vitest_counter_reads_json` |
| AC-02 Tabla por archivo e integrante | `test_report_maps_owner_from_manifest`, `test_report_has_suite_and_owner_totals` |
| AC-03 Salidas simuladas | `test_report_writes_markdown_to_target` |

## Success Criteria *(mandatory)*

- **SC-001**: `make pruebas` produce el mismo total que `make check` + `make frontend-check`.
- **SC-002**: `PRUEBAS.md` se regenera sin edición manual y sin cifras escritas a mano.
- **SC-003**: Las pruebas del módulo no lanzan pytest ni Vitest ni dependen de Node.
- **SC-004**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Actualizar `PLAN-PRUEBAS.md` a 1.200 (HU-095, #151).
- Cambiar las pruebas existentes o su reparto.
- Ejecutar la suite completa dentro del contador.
- Tocar `frontend/package.json` o `uv.lock`.

## Assumptions

- Vitest 5 admite `vitest list --json`; se verificó en el entorno local.
- El dueño de cada archivo se resuelve con las mismas reglas que
  `ppe_detection.tools.ownership` (`propiedad.toml`).
- `docs/curso/PRUEBAS.md` es `[[locked]]` de `jesusriverosUAO`; el comando lo regenera y
  el dueño lo commitea.
- El Makefile es de Guillermo: se añade un objetivo, no se reordena lo existente.
