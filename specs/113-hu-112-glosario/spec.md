# Feature Specification: HU-112 — Glosario y mapa de documentación

**Feature Branch**: `feature/113-hu-112-glosario`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #168 — «Glosario y mapa de documentación». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-15`, P2, Ola 3, 1 SP, 4 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Encontrar cada documento en un minuto (Priority: P2)

Como lector nuevo, quiero un índice de la documentación y un glosario, para encontrar
cada documento rápido y entender los términos del proyecto.

**Why this priority**: el repositorio tiene ADR, curso, operación, evaluación, dataset y
specs; sin un mapa, el evaluador se pierde en la sustentación.

**Independent Test**: abrir `docs/README.md`, seguir tres enlaces al azar y comprobar que
resuelven; ejecutar `uv run pytest tests/test_docs_readme.py`.

**Acceptance Scenarios** (AC de la issue #168):

1. **AC-01**: **Dado** `docs/README.md`, **Cuando** se revisa, **Entonces** hay un mapa de
   la documentación por tema.
2. **AC-02**: **Dado** el glosario, **Cuando** se busca un término, **Entonces** aparecen
   al menos MaaS, SDD y DinD, con los demás términos del proyecto.
3. **AC-03**: **Dado** el repositorio, **Cuando** se ejecuta la suite, **Entonces** una
   prueba valida que los enlaces resuelven.

### Edge Cases

- **Enlace a carpeta**: se acepta si el directorio existe.
- **Enlace externo** (`https://`): la prueba no lo descarga; solo verifica el formato.
- **Término sin definición**: la prueba falla si falta uno de los obligatorios.
- **Documento nuevo**: se añade al mapa o queda fuera del índice.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/README.md` MUST existir con un mapa por tema.
- **FR-002**: El mapa MUST cubrir gobierno, curso, operación, evaluación, arquitectura y
  specs.
- **FR-003**: El glosario MUST definir al menos MaaS, SDD y DinD, además de los términos
  del dominio.
- **FR-004**: Los enlaces relativos MUST resolver a un archivo o directorio existente.
- **FR-005**: Una prueba MUST validar enlaces y términos.

### Key Entities

- **Entrada del mapa**: tema, descripción y enlace.
- **Término**: nombre y definición.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Mapa | `tests/test_docs_readme.py::test_readme_exists`, `::test_map_covers_key_areas` |
| AC-02 Glosario | `::test_glossary_has_required_terms` |
| AC-03 Enlaces | `::test_relative_links_resolve` |

## Success Criteria *(mandatory)*

- **SC-001**: Un lector nuevo llega a cualquier documento en un minuto.
- **SC-002**: `make check` pasa con las pruebas nuevas.
- **SC-003**: `make ownership-check` sin bloqueos.

## Out of Scope

- Reescribir los documentos enlazados.
- Traducir la documentación.
- Generar el mapa automáticamente.

## Assumptions

- `docs/README.md` no tiene dueño en `propiedad.toml`: archivo libre.
- Los enlaces son relativos a `docs/`.
