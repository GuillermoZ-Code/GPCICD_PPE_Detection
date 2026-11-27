# Feature Specification: HU-028 — Dataset Card y atribución CC-BY-4.0

**Feature Branch**: `feature/029-hu-028-dataset-card`

**Created**: 2026-11-26

**Status**: En implementación

**Input**: Issue #84 — «Dataset Card y atribución CC-BY-4.0». Asignada a Hernán
(`HestradaUAO`), épica `ep-15`, P1, ola 2, 1 SP, 4 pruebas objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Atribuir el dataset y declarar sus límites (Priority: P1)

Como auditor de licencias, quiero una ficha del dataset con origen, licencia,
particiones y limitaciones, para cumplir la atribución CC-BY-4.0 y no presentar el
dataset como si tuviera consentimiento o procedencia verificada.

**Why this priority**: el sistema se apoya en un dataset de terceros con licencia
CC-BY-4.0, fuente original no declarada y posibles imágenes de personas. La ficha es
la evidencia que acompaña al README, la SPA y el documento del curso.

**Independent Test**: leer `docs/dataset/README.md` y verificar que contiene la
fuente, la licencia, las particiones, la limpieza, los riesgos y un bloque de
atribución reutilizable.

**Acceptance Scenarios** (AC de la issue #84):

1. **AC-01**: **Dada** la ficha, **Cuando** se revisa, **Entonces** declara origen,
   licencia, particiones y limpieza.
2. **AC-02**: **Dada** la ficha, **Cuando** se revisa, **Entonces** declara la
   ausencia de fuente original y de consentimiento de rostros.
3. **AC-03**: **Dada** la ficha, **Cuando** se publica, **Entonces** incluye un texto
   de atribución reutilizable por la UI y el README.

### Edge Cases

- El número de imágenes originales no está publicado en la tarjeta: se reporta el
  conteo auditado y se declara la diferencia con la tarjeta.
- La variante de split corregida difiere en una imagen de `dataset_limpio`: se
  documentan ambas cifras y se enlaza el EDA.
- La fuente original es desconocida: no se inventa un autor ni una URL.
- El dataset no tiene clase `person` ni `no-EPP`: se declara la consecuencia.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/dataset/README.md` MUST declarar fuente, licencia y SHA-256 del
  ZIP.
- **FR-002**: MUST declarar las seis clases en orden canónico.
- **FR-003**: MUST declarar particiones y conteos de limpieza con enlace al EDA.
- **FR-004**: MUST declarar ausencia de fuente original y consentimiento de rostros.
- **FR-005**: MUST incluir un bloque de atribución CC-BY-4.0 reutilizable.
- **FR-006**: MUST declarar que no hay clase `person` ni `no-EPP`.
- **FR-007**: No se publican imágenes ni recortes con personas.
- **FR-008**: No se agregan dependencias.

### Key Entities

- **Dataset Card**: documento `docs/dataset/README.md`.
- **Atribución**: bloque de texto con nombre, URL, licencia y modificaciones.
- **EDA**: evidencia de conteos, duplicados y fuga.
- **Model Card**: documento de métricas y limitaciones del detector.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Origen, licencia, particiones y limpieza | `tests/test_dataset_card.py::test_dataset_card_has_source_license_and_counts`, `tests/test_dataset_card.py::test_dataset_card_links_to_evidence` |
| AC-02 Fuente y consentimiento | `tests/test_dataset_card.py::test_dataset_card_declares_missing_origin_and_consent` |
| AC-03 Atribución reutilizable | `tests/test_dataset_card.py::test_dataset_card_has_reusable_attribution` |

## Success Criteria *(mandatory)*

- **SC-001**: La ficha se entiende sin abrir el dataset ni los pesos.
- **SC-002**: La atribución se puede copiar sin reescribir el enlace ni la licencia.
- **SC-003**: Los riesgos de fuente y consentimiento no se ocultan.
- **SC-004**: La HU añade al menos 4 pruebas al inventario.

## Out of Scope

- Descargar o redistribuir el dataset.
- Cambiar las particiones o las etiquetas.
- Reentrenar el modelo.
- Publicar imágenes o recortes.
- Modificar la licencia AGPL del repositorio.

## Assumptions

- El EDA y el ADR 0002 son la fuente de los conteos.
- La licencia declarada por la tarjeta es CC-BY-4.0.
- La ausencia de fuente y consentimiento se mantiene como riesgo documentado.
- El dataset y los pesos están fuera de Git.
