# Feature Specification: HU-087 — Actualizar CONSTITUTION, AGENTS y README para el M4

**Feature Branch**: `feature/088-hu-087-docs-m4`

**Created**: 2026-11-28

**Status**: En revisión

**Input**: Issue #143 — «HU-087 — Actualizar CONSTITUTION, AGENTS y README para el M4».
Asignada a Guillermo (`GuillermoZ-Code`), épica `ep-15`, P0 · ola 2, 1 SP, 4 pruebas
objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Gobierno técnico al día con el M4 (Priority: P0)

Como equipo, quiero que `CONSTITUTION.md`, `AGENTS.md` y `README.md` describan el stack,
el roadmap, los riesgos y las decisiones del M4, para que la entrega no se contradiga
con el código ni con el despliegue real.

**Why this priority**: la directiva de sincronía de la constitución exige que cada
cambio significativo se refleje en el mismo commit. El M4 cambió el modelo, el CI/CD y
el despliegue; la documentación seguía anclada al M3 (YOLO11s, 451 pruebas, sin Caddy).

**Independent Test**: las cuatro pruebas de `tests/test_docs_m4.py` pasan y verifican
la constitución, la constitución derivada, los enlaces internos y el README.

**Acceptance Scenarios** (AC de la issue #143):

1. **AC-01**: **Dado** el repositorio, **Cuando** se lee `CONSTITUTION.md`, **Entonces**
   declara el stack, roadmap, riesgos y decisiones del M4 (YOLO26n + ONNX, GitLab CI,
   Droplet/Caddy, ADR 0009 y ADR 0013) y el README refleja el modelo y el despliegue
   reales.
2. **AC-02**: **Dada** la constitución fuente, **Cuando** se lee
   `.specify/memory/constitution.md`, **Entonces** es la versión 1.2 sincronizada con
   los principios no negociables y el foco M4.
3. **AC-03**: **Dados** los documentos de gobierno, **Cuando** se validan sus enlaces
   internos, **Entonces** todos resuelven a rutas existentes del repositorio.

### Edge Cases

- El bloque de estado de `AGENTS.md` §0 es generado por `make estado-write` y se
  actualiza en la sesión de cierre; no se edita a mano en esta HU.
- El README no debe prometer HUs abiertas como completadas: el estado del M4 se marca
  como «release v1.0.0 en preparación».
- Los enlaces externos (`https://…`) no se validan; solo los internos.
- La documentación no incluye valores de secretos, solo nombres de variables.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `CONSTITUTION.md` MUST declarar el M4 como módulo activo y el release
  v1.0.0 como estado.
- **FR-002**: `CONSTITUTION.md` MUST incluir el stack M4 (YOLO26n + ONNX, GitLab CI,
  Droplet/Caddy) y las decisiones ADR 0009 y ADR 0013.
- **FR-003**: `.specify/memory/constitution.md` MUST ser la versión 1.2, conservar el
  encabezado de derivado y repetir el foco M4 y el mínimo de 1.200 pruebas.
- **FR-004**: `README.md` MUST describir el modelo `yolo26n-clean`, ONNX, Caddy y la URL
  pública `https://143.198.10.157.sslip.io`, sin referencias a `yolo11s-clean`.
- **FR-005**: Los enlaces internos de `CONSTITUTION.md`, `AGENTS.md` y `README.md` MUST
  resolver a rutas existentes.
- **FR-006**: Al menos 4 pruebas pytest MUST referenciar AC-01, AC-02 y AC-03.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 4/4 pruebas de `tests/test_docs_m4.py` en verde.
- **SC-002**: `make check` en verde con Ruff, formato, `ty` y pytest.
- **SC-003**: `python -m ppe_detection.tools.check_specs --check` acepta esta spec.
- **SC-004**: `make ownership-check` sin bloqueos para la rama.

## Test Mapping

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_docs_m4.py::test_ac01_constitution_documents_m4_stack_roadmap_and_risks` |
| AC-01 | `tests/test_docs_m4.py::test_ac01_readme_reflects_the_m4_model_and_deployment` |
| AC-02 | `tests/test_docs_m4.py::test_ac02_derived_constitution_is_synced_with_m4` |
| AC-03 | `tests/test_docs_m4.py::test_ac03_internal_links_in_governance_docs_resolve` |
