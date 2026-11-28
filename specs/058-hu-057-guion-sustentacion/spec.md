# Feature Specification: HU-057 — Guion de la sustentación M4 y checklist

**Feature Branch**: `feature/058-hu-057-guion-sustentacion`

**Created**: 2026-11-24

**Status**: En implementación

**Input**: Issue #113 — «Guion de la sustentación M4 y checklist del entorno».
Asignada a Eliana (`ElianaCardona`), épica `ep-15`, SP 2, P0, Ola 2, 8 pruebas objetivo.
Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Sustentar en 15 minutos (Priority: P0)

Como equipo, quiero un guion minuto a minuto y un checklist del entorno, para cumplir
los 15 minutos de la prueba en vivo sin omitir evidencias ni responsables.

**Why this priority**: la evaluación individual y grupal depende de mostrar evidencia
 verificable en el tiempo asignado; improvisar el orden cuesta minutos y deja huecos.

**Independent Test**: `uv run pytest -v tests/test_docs_ficha_m4.py` valida el guion,
el checklist y el registro de ensayo sin ejecutar la sustentación.

**Acceptance Scenarios** (AC de la issue #113):

1. **AC-01**: **Dado** el guion, **Cuando** se recorre de 0:00 a 15:00, **Entonces**
   cada bloque indica responsable, evidencia y mensaje central alineado a la rúbrica.
2. **AC-02**: **Dado** el checklist del entorno (§5.4 de la rúbrica), **Cuando** se
   revisa antes de la prueba, **Entonces** cada ítem tiene responsable, comando de
   verificación y criterio de éxito.
3. **AC-03**: **Dado** el ensayo cronometrado, **Cuando** se consulta el registro,
   **Entonces** hay una fila por bloque con duración objetivo, duración real y estado;
   la ejecución real del equipo se marca como pendiente hasta realizarse.

### Edge Cases

- El guion no afirma que el ensayo del equipo ya ocurrió: separa validación estática
  de ejecución real.
- No incluye credenciales, rutas personales ni IPs del Droplet.
- El checklist distingue evidencia versionada en `develop` de evidencia local
  (pesos fuera de Git).
- La ficha no presenta el detector como certificación normativa.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/entrega/FICHA-M4.md` MUST contener seis bloques continuos que
  cubran 0:00–15:00 con responsable y evidencia por bloque.
- **FR-002**: El documento MUST incluir `## Checklist del entorno (§5.4)` con columna
  de responsable y al menos seis ítems verificables.
- **FR-003**: El documento MUST incluir un registro de ensayo cronometrado con
  `Objetivo`, `Real` y `Estado` por bloque.
- **FR-004**: El registro MUST distinguir la validación estática del documento del
  ensayo real del equipo, marcando este último como pendiente si no se ejecutó.
- **FR-005**: No se MUST modificar `docs/curso/`, `.github/`, `Makefile` ni código de
  producción; la entrega es documentación y pruebas.

### Key Entities

- **ScriptBlock**: intervalo → responsable → evidencia → mensaje.
- **ChecklistItem**: ítem → comando → criterio → responsable.
- **Rehearsal**: bloque → objetivo → real → estado.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_docs_ficha_m4.py::test_script_has_six_time_blocks`, `::test_each_block_has_speaker_and_evidence`, `::test_script_covers_required_topics` |
| AC-02 | `tests/test_docs_ficha_m4.py::test_checklist_has_responsible_column`, `::test_checklist_covers_environment_items` |
| AC-03 | `tests/test_docs_ficha_m4.py::test_timed_rehearsal_log_exists`, `::test_rehearsal_rows_have_goal_real_and_status`, `::test_rehearsal_distinguishes_static_and_team_execution` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 8 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: ruff, formato y ty pasan sin hallazgos.
- **SC-003**: `ownership --base origin/develop` no bloquea los archivos tocados.
- **SC-004**: La PR queda abierta con revisor de otro integrante.

## Out of Scope

- Cambios en `docs/curso/ESTADO.md`, `backlog.md` ni `PRUEBAS.md` (un solo escritor).
- Ejecutar la sustentación real: requiere sala, equipo y entorno de despliegue.
- Modificar la rúbrica generada (`docs/entrega/RUBRICA-M4.md`).

## Assumptions

- La rúbrica M4 externa define bloques de 15 minutos y un checklist de entorno §5.4;
  se usa la estructura publicada en la issue y la ficha M3 como referencia local.
- Cada integrante confirmará su responsable al ensayar; los nombres son los del equipo.
