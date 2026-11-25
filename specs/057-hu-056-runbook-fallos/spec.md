# Feature Specification: HU-056 — Runbook de diagnóstico de fallos

**Feature Branch**: `feature/057-hu-056-runbook-fallos`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #112 — «Runbook de diagnóstico de fallos». Asignada a Eliana
(`ElianaCardona`), épica `ep-15`, SP 1, P0, Ola 2, 4 pruebas objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Responder ante un fallo de despliegue (Priority: P0)

Como integrante del equipo, quiero una guía de qué revisar si el deploy falla, para
responder la pregunta individual de fallo simulado sin improvisar ni perder tiempo.

**Why this priority**: la sustentación M4 exige diagnosticar un fallo en vivo; sin un
árbol de decisión y comandos verificables, la respuesta depende de la memoria de quien
esté de turno.

**Independent Test**: `uv run pytest -v tests/test_docs_runbook_fallos.py` valida el
contenido de `docs/operacion/fallos.md` sin infraestructura externa.

**Acceptance Scenarios** (AC de la issue #112):

1. **AC-01**: **Dado** un fallo reportado, **Cuando** sigo el runbook, **Entonces**
   encuentro un árbol de diagnóstico con las etapas pipeline, registry, SSH,
   contenedor, proxy y modelo.
2. **AC-02**: **Dado** cualquier etapa del árbol, **Cuando** aplico el runbook,
   **Entonces** dispongo de comandos `glab`, `docker logs`, `docker inspect` y `curl`
   con el criterio para interpretarlos.
3. **AC-03**: **Dado** el ensayo de fallos simulados, **Cuando** reviso el runbook,
   **Entonces** encuentro tres escenarios simulados con síntoma, verificación, acción
   y resultado esperado, y un registro para la ejecución del equipo.

### Edge Cases

- El runbook no contiene tokens, contraseñas, IPs privadas ni rutas personales.
- Los comandos son ejemplos parametrizables; no ejecutan cambios destructivos sin
  advertencia explícita.
- El registro de ensayos distingue «verificación estática del documento» de
  «ejecución con el equipo», para no afirmar una prueba no realizada.
- El runbook no presenta detecciones como cumplimiento normativo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/operacion/fallos.md` MUST existir y contener un árbol de decisión
  con las seis etapas declaradas en AC-01.
- **FR-002**: El runbook MUST incluir comandos `glab`, `docker logs`,
  `docker inspect` y `curl` con una interpretación esperada para cada uno.
- **FR-003**: El runbook MUST describir tres fallos simulados con síntoma,
  verificación, acción y resultado esperado, además de un registro de ensayo.
- **FR-004**: El runbook MUST evitar secretos y acciones destructivas no advertidas.
- **FR-005**: No se MUST modificar código de producción ni archivos de propiedad
  ajena; la única entrega es documentación y sus pruebas.

### Key Entities

- **DecisionTree**: etapa → síntoma → comando → interpretación → acción.
- **Drill**: fallo simulado → señal → verificación → corrección → resultado esperado.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_docs_runbook_fallos.py::test_runbook_has_six_stage_decision_tree`, `::test_each_stage_has_symptom_and_action` |
| AC-02 | `tests/test_docs_runbook_fallos.py::test_required_commands_are_documented`, `::test_commands_have_expected_interpretation` |
| AC-03 | `tests/test_docs_runbook_fallos.py::test_three_drills_are_documented`, `::test_drill_log_distinguishes_static_and_team_validation` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 4 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: ruff, formato y ty pasan sin hallazgos.
- **SC-003**: `ownership --base origin/develop` no bloquea los archivos tocados.
- **SC-004**: La PR queda abierta con revisor de otro integrante.

## Out of Scope

- Cambios en `deploy/`, `compose*.yml`, `.gitlab-ci.yml` ni en el pipeline de GitLab.
- Ejecución real de los fallos simulados: requiere el entorno de despliegue; se deja
  registro explícito para el equipo.
- Modificar `docs/curso/ESTADO.md`, `backlog.md` ni `PRUEBAS.md` (un solo escritor).

## Assumptions

- La documentación existente de `docs/operacion/` es la fuente de los comandos.
- El equipo ejecutará los ensayos en la sesión de sustentación y registrará resultado.
