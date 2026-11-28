# Feature Specification: HU-064 — Notas de versión v1.0.0 y CHANGELOG

**Feature Branch**: `feature/065-hu-064-release-notes`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #120 — «Notas de versión v1.0.0 y CHANGELOG». Asignada a Eliana
(`ElianaCardona`), épica `ep-15`, SP 1, P2, Ola 3, 4 pruebas objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Trazar la evolución entregada (Priority: P2)

Como evaluador, quiero un CHANGELOG con lo entregado por módulo, para trazar la
evolución del proyecto desde M2 hasta v1.0.0.

**Why this priority**: el curso exige evidencia de qué cambió en cada entrega y cómo
se enlaza con historias y PRs; sin formato consistente la trazabilidad se pierde.

**Independent Test**: `uv run pytest -v tests/test_changelog.py` valida encabezados,
secciones, categorías y enlaces sin depender de red.

**Acceptance Scenarios** (AC de la issue #120):

1. **AC-01**: **Dado** el archivo `CHANGELOG.md`, **Cuando** se abre, **Entonces**
   sigue Keep a Changelog con `Unreleased` antes que `1.0.0` y categorías estándar.
2. **AC-02**: **Dado** el bloque de `v1.0.0`, **Cuando** se revisan las notas,
   **Entonces** cada cambio relevante enlaza su HU y su PR reales del repositorio.
3. **AC-03**: **Dado** el formato, **Cuando** corren las pruebas, **Entonces** se
   comprueban encabezados, fechas ISO y que las entradas usan viñetas.

### Edge Cases

- La versión 1.0.0 está planificada para la entrega del 27/11/2026: se documenta
  como fecha prevista, no como release publicado.
- No se inventan números de PR: solo se enlazan PRs confirmados en el repositorio.
- No se modifica `docs/curso/` (un solo escritor) ni la rúbrica generada.
- Los enlaces son absolutos al repositorio del curso, sin rutas personales.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `CHANGELOG.md` MUST declarar `Keep a Changelog` y `Semantic Versioning`.
- **FR-002**: El archivo MUST contener `## [Unreleased]` antes de `## [1.0.0] - YYYY-MM-DD`.
- **FR-003**: `## [1.0.0]` MUST incluir al menos cuatro enlaces a `issues/` y cuatro
  a `pull/` dentro de sus notas.
- **FR-004**: Las secciones MUST usar `### Added`, `### Changed`, `### Fixed` y
  viñetas `- ` bajo cada categoría.
- **FR-005**: `tests/test_changelog.py` MUST tener al menos 4 pruebas con AC en el
  docstring, ejecutadas antes de crear el CHANGELOG.

### Key Entities

- **ReleaseBlock**: versión → fecha → categorías → entradas.
- **Entry**: texto → HU enlazada → PR enlazado.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_changelog.py::test_keep_a_changelog_header_is_present`, `::test_unreleased_precedes_release_section` |
| AC-02 | `tests/test_changelog.py::test_release_notes_link_real_hus_and_prs` |
| AC-03 | `tests/test_changelog.py::test_categories_and_iso_date_are_valid` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 4 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: ruff, formato y ty pasan sin hallazgos.
- **SC-003**: `ownership --base origin/develop` no bloquea los archivos tocados.
- **SC-004**: La PR queda abierta con revisor de otro integrante.

## Out of Scope

- Crear el tag `v1.0.0` o publicar un release en GitHub: requiere aprobación del
  equipo y la entrega oficial.
- Actualizar `docs/curso/ESTADO.md`, `backlog.md` ni `PRUEBAS.md` (un solo escritor).
- Reescribir `docs/entrega/FICHA-M3.md` ni la rúbrica generada.

## Assumptions

- Los PRs citados están fusionados o abiertos y se identifican por su número real.
- La fecha de entrega prevista es 2026-11-27 según `RUBRICA-M4.md`.
