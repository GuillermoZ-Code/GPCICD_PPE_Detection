# Feature Specification: HU-082 — CODEOWNERS y checks obligatorios

**Feature Branch**: `feature/083-hu-082-codeowners-checks`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #138 — «CODEOWNERS y checks obligatorios». Asignada a Eliana
(`ElianaCardona`), épica `ep-14`, SP 1, P1, Ola 2, 4 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Revisión por dueño y checks verificables (Priority: P1)

Como Code Reviewer, quiero revisión obligatoria por dueño de archivo y checks
verdes, para cumplir el estándar de PR del M4.

**Why this priority**: cuatro agentes escriben en paralelo; sin una mapping
generada y checks enumerados, una PR puede fusionarse sin la revisión de quien
posee la ruta.

**Independent Test**: `uv run pytest -v tests/test_codeowners_hu082.py` comprueba
el archivo generado, los checks exigidos y el ADR, sin red ni servicios.

**Acceptance Scenarios** (AC de la issue #138):

1. **AC-01**: **Dado** `docs/curso/propiedad.toml`, **Cuando** se compara con
   `.github/CODEOWNERS`, **Entonces** el archivo versionado coincide con el
   contenido generado por `ppe_detection.tools.ownership`.
2. **AC-02**: **Dado** el ADR de protección, **Cuando** se consultan los checks
   requeridos, **Entonces** enumera los siete jobs del flujo y deja explícito que
   la protección técnica sigue pendiente de aprobación del equipo.
3. **AC-03**: **Dado** el ADR 0004, **Cuando** se lee la decisión vigente,
   **Entonces** el ADR 0012 la actualiza sin reescribirla y queda indexado.

### Edge Cases

- El generador ordena patrones por especificidad: el test compara el texto
  completo, no solo la presencia de líneas.
- Un check renombrado en un workflow debe actualizar el ADR y la prueba.
- La aprobación de protección técnica no se puede simular: se registra como
  pendiente, no se afirma que está activa.
- El ADR es append-only: 0004 no se modifica.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `.github/CODEOWNERS` MUST ser generado desde `propiedad.toml` con
  `python -m ppe_detection.tools.ownership --write-codeowners`; nadie lo edita a mano.
- **FR-002**: El ADR 0012 MUST documentar los siete checks requeridos y el estado
  de la protección de `develop`/`main`.
- **FR-003**: `docs/adr/README.md` MUST indexar el ADR 0012.
- **FR-004**: Las 4 pruebas MUST referenciar AC-01, AC-02 y AC-03 por nombre o
  docstring, sin red, Docker ni servicios externos.
- **FR-005**: No se MUST cambiar `propiedad.toml`, los workflows ni la configuración
  de ramas de GitHub sin aprobación del equipo.

### Key Entities

- **Manifest**: dueños y rutas bloqueadas leídos de `propiedad.toml`.
- **CODEOWNERS**: proyección determinista del manifiesto.
- **ADR 0012**: decisión de gobierno técnico que actualiza ADR 0004.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_codeowners_hu082.py::test_codeowners_refleja_el_manifiesto_ac_01`, `::test_codeowners_cubre_duenos_y_bloqueos_ac_01` |
| AC-02 | `tests/test_codeowners_hu082.py::test_adr_lista_checks_requeridos_ac_02` |
| AC-03 | `tests/test_codeowners_hu082.py::test_adr_actualiza_proteccion_escrita_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 4 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: `ruff`, formato, ty y la compuerta de propiedad pasan sin hallazgos.
- **SC-003**: La PR queda abierta con revisión del dueño de `.github/` y `docs/adr/`.

## Out of Scope

- Activar branch protection en GitHub: requiere aprobación del equipo y permisos de
  administrador (AC-02 condicionado en la issue).
- Cambiar `docs/curso/propiedad.toml` ni `docs/curso/M4/ASIGNACION.md`.
- Modificar workflows: los checks ya existen y solo se enumeran.

## Assumptions

- `properties.toml` es la fuente única y `render_codeowners` es determinista.
- ADR 0012 está libre: los ADR 0007/0008 pertenecen a la PR #221 de Guillermo.
- La protección escrita de ADR 0004 sigue vigente hasta nueva decisión.
