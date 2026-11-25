# Feature Specification: HU-098 — Model Registry con alias champion/challenger

**Feature Branch**: `feature/099-hu-098-registry`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #154 — «Model Registry con alias champion/challenger». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-14`, P1, Ola 3, 2 SP, 8 pruebas objetivo. Depende de HU-097
(fusionada).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Promover un modelo con trazabilidad (Priority: P1)

Como responsable MLOps, quiero alias que indiquen el modelo productivo, para promover o
revertir modelos sin perder el rastro.

**Why this priority**: el ADR 0009 fija YOLO26n como productivo y YOLO11s como rollback;
sin alias, promover o revertir depende de recordar la versión.

**Independent Test**: construir los alias y comprobar que `champion` apunta a
`yolo26n-clean`, que `challenger` apunta al candidato y que la promoción deja el campeón
anterior como rollback.

**Acceptance Scenarios** (AC de la issue #154):

1. **AC-01**: **Dado** el registro, **Cuando** se consulta `champion`, **Entonces** apunta
   al modelo del ADR 0009 (`yolo26n-clean`).
2. **AC-02**: **Dado** el registro, **Cuando** se consulta `challenger`, **Entonces**
   apunta al candidato alternativo y ambos validan su SHA256.
3. **AC-03**: **Dados** los dos alias, **Cuando** se promociona, **Entonces** el
   challenger pasa a champion y el anterior queda como rollback.

### Edge Cases

- **Alias desconocido**: falla.
- **Alias duplicado**: falla.
- **SHA256 inválido**: falla.
- **Candidato igual al campeón**: la promoción es un no-op documentado.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El módulo MUST exponer `ModelAlias`, `build_aliases`, `validate_aliases` y
  `plan_promotion`.
- **FR-002**: `champion` MUST apuntar a `yolo26n-clean` con el SHA del ADR 0009.
- **FR-003**: `challenger` MUST apuntar al candidato indicado.
- **FR-004**: La validación MUST rechazar alias desconocidos, duplicados y SHA inválidos.
- **FR-005**: La promoción MUST devolver el nuevo campeón y el rollback.
- **FR-006**: No se agregan dependencias.

### Key Entities

- **ModelAlias**: alias, versión y SHA256.
- **Plan de promoción**: alias, versión de origen, destino y rollback.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Champion | `tests/test_tracking_registry.py::test_champion_points_to_adr_model`, `::test_champion_sha_matches_adr` |
| AC-02 Challenger | `::test_challenger_points_to_candidate`, `::test_build_aliases_returns_two`, `::test_validate_rejects_unknown_alias`, `::test_validate_rejects_invalid_sha`, `::test_build_aliases_rejects_invalid_candidate` |
| AC-03 Promoción | `::test_plan_promotion_moves_challenger`, `::test_plan_promotion_keeps_rollback` |

## Success Criteria *(mandatory)*

- **SC-001**: Promover o revertir es una operación con plan explícito.
- **SC-002**: `make check` pasa con las pruebas nuevas.
- **SC-003**: No se agregan dependencias.

## Out of Scope

- Llamar a MLflow real (el registro se prueba con lógica pura).
- Cambiar `models.lock`.
- Publicar el paquete en GitLab.

## Assumptions

- El SHA del champion es el de `models.lock`.
- `tracking/` pertenece a Jesús.
