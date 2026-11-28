# Feature Specification: HU-111 — Release v1.0.0 `develop → main`

**Feature Branch**: `docs/112-hu-111-release`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #167 — «Release v1.0.0 `develop → main`». Asignada a Jesús
(`jesusriverosUAO`), épica `ep-15`, P0, Ola 3, 2 SP, 8 pruebas objetivo. Entregable:
tag `v1.0.0` + `docs/entrega/`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Entregar una versión identificada (Priority: P0)

Como equipo, queremos una release con merge commit y tag, para entregar una versión
identificada y reproducible.

**Why this priority**: la rúbrica del M4 exige un despliegue en vivo y un release; sin
tag no hay forma de volver a un estado conocido.

**Independent Test**: abrir `docs/entrega/RELEASE-V1.0.0.md` y comprobar el checklist, el
tag y la verificación de `/health`; ejecutar `uv run pytest tests/test_release_v1.py`.

**Acceptance Scenarios** (AC de la issue #167):

1. **AC-01**: **Dado** el release, **Cuando** se revisa, **Entonces** el checklist está
   completo y sin ambigüedades.
2. **AC-02**: **Dado** el repositorio, **Cuando** se consulta, **Entonces** existen el tag
   `v1.0.0` y el CI verde en `main`.
3. **AC-03**: **Dado** el despliegue, **Cuando** se consulta, **Entonces** la imagen y el
   modelo quedan asociados al tag.

### Edge Cases

- **Tag anterior**: el rollback debe indicar cómo volver.
- **Modelo distinto**: el SHA256 del modelo desplegado debe coincidir con ADR 0009.
- **Suite incompleta**: se declara el pending en lugar de afirmar que se cumplió.
- **main avanza después del tag**: se publica `v1.0.1`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST existir `docs/entrega/RELEASE-V1.0.0.md` con el checklist.
- **FR-002**: El documento MUST registrar tag, commit, fecha y release.
- **FR-003**: MUST registrar la imagen (tag por SHA) y el modelo (SHA256).
- **FR-004**: MUST registrar la verificación de `/health` y `/health/ready`.
- **FR-005**: MUST declarar licencia AGPL, atribución CC-BY y rollback.
- **FR-006**: MUST declarar el pending de la suite si no llega a 1.200.

### Key Entities

- **Release**: tag, commit, fecha y notas.
- **Checklist**: items verificados y pendientes declarados.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Checklist completo | `tests/test_release_v1.py::test_release_doc_has_complete_checklist`, `::test_release_doc_declares_test_gap` |
| AC-02 Tag y CI en main | `tests/test_release_v1.py::test_release_doc_records_tag_and_merge_commit`, `::test_changelog_has_release_notes` |
| AC-03 Imagen y modelo del tag | `tests/test_release_v1.py::test_release_doc_associates_image_and_model`, `::test_release_doc_verifies_health` |

## Success Criteria *(mandatory)*

- **SC-001**: Cualquiera puede reconstruir el release con el tag y el checklist.
- **SC-002**: El modelo desplegado (YOLO26n, SHA256) queda trazado.
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Re-cortar el tag en esta HU (se hace en `v1.0.1` si `main` cambia).
- Despliegue nuevo.
- Cambiar el CHANGELOG de HU-064.

## Assumptions

- El tag `v1.0.0` apunta al merge commit de la PR #265.
- El Droplet responde en `https://143.198.10.157.sslip.io`.
