# Feature Specification: HU-055 — Runbook de despliegue y rollback

**Feature Branch**: `docs/059-hu-055-runbook`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #111 — «Runbook de despliegue y rollback». Asignada a Eliana
(`ElianaCardona`), épica `ep-15`, P0, Ola 3, 2 SP, 8 pruebas objetivo. Entregable:
`docs/operacion/despliegue.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Operar el sistema en la sustentación (Priority: P0)

Como integrante del equipo, quiero pasos exactos para desplegar y volver a la versión
anterior, para operar el sistema durante la sustentación sin improvisar.

**Why this priority**: el despliegue en vivo es parte de la rúbrica; un rollback
documentado evita que un fallo delante del docente deje el sitio caído.

**Independent Test**: seguir la sección 4 con un tag real y comprobar `make verify`;
ejecutar `uv run pytest tests/test_runbook_despliegue.py`.

**Acceptance Scenarios** (AC de la issue #111):

1. **AC-01**: **Dado** el runbook, **Cuando** se lee, **Entonces** hay despliegue manual
   y por pipeline con comandos exactos.
2. **AC-02**: **Dado** un fallo, **Cuando** se sigue el rollback, **Entonces** se vuelve
   al tag anterior guardado en `.deployed_env`.
3. **AC-03**: **Dado** el repositorio, **Cuando** se ejecuta la suite, **Entonces** una
   prueba estructural valida el documento.

### Edge Cases

- **Tag de 8 caracteres**: GitLab usa `CI_COMMIT_SHORT_SHA`, no 7.
- **Smoke falla**: el script restaura el tag anterior y sale con error.
- **Rollback también falla**: se conservan los logs y no se silencia.
- **Modelo ausente o SHA distinto**: la API responde 503; se revisa el montaje `:ro`.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El runbook MUST estar en `docs/operacion/despliegue.md`.
- **FR-002**: MUST documentar el despliegue por pipeline y el manual.
- **FR-003**: MUST documentar el rollback por tag y `.deployed_env`.
- **FR-004**: MUST incluir diagnóstico, aprovisionamiento y apagado.
- **FR-005**: MUST registrar el modelo `:ro` y el SHA256.
- **FR-006**: MUST haber una prueba estructural del documento.

### Key Entities

- **Runbook**: secciones de arquitectura, despliegue, rollback y diagnóstico.
- **Tag**: identificador de las imágenes que se despliegan.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Despliegue manual y por pipeline | `tests/test_runbook_despliegue.py::test_pipeline_deploy_is_documented`, `::test_manual_deploy_has_exact_commands` |
| AC-02 Rollback por tag | `tests/test_runbook_despliegue.py::test_rollback_documents_previous_tag`, `tests/test_deploy.py::test_script_keeps_the_previous_tag_for_rollback` |
| AC-03 Prueba estructural | `tests/test_runbook_despliegue.py::test_runbook_has_all_sections` |

## Success Criteria *(mandatory)*

- **SC-001**: Cualquiera puede desplegar y volver atrás siguiendo el documento.
- **SC-002**: El documento no contiene secretos ni hashes reales.
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Cambiar `deploy.sh` (HU-070).
- Provisionar el Droplet (HU-069).
- Repetir el diagrama (HU-086).

## Assumptions

- El Droplet ya está aprovisionado y el pipeline de `main` despliega.
- `docs/operacion/despliegue.md` es la fuente operativa.
