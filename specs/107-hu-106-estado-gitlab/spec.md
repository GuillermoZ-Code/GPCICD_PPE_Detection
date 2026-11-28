# Feature Specification: HU-106 — `make estado` con el estado del pipeline de GitLab

**Feature Branch**: `feature/107-hu-106-estado-gitlab`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #162 — «`make estado` con el estado del pipeline de GitLab». Asignada a
Jesús (`jesusriverosUAO`), épica `ep-14`, P2, Ola 3, 3 SP, 12 pruebas objetivo. Depende
de HU-073 (MCP de GitLab y `glab` autenticado), ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver el pipeline sin abrir el navegador (Priority: P2)

Como integrante del equipo, quiero ver el último pipeline de GitLab en `make estado`,
para conocer el estado del despliegue sin abrir el navegador.

**Why this priority**: el M4 se cierra con el pipeline de GitLab como evidencia de la
rúbrica; si `make estado` no lo muestra, hay que saltar a la web de GitLab en cada
revisión y el estado operativo queda incompleto.

**Independent Test**: ejecutar `uv run python -m ppe_detection.tools.estado` y comprobar
la línea `**GitLab:**`; sin `glab` instalado debe indicarlo sin fallar.

**Acceptance Scenarios** (AC de la issue #162):

1. **AC-01**: **Dado** un equipo sin `glab`, **Cuando** se ejecuta `make estado`,
   **Entonces** lo indica sin fallar.
2. **AC-02**: **Dado** un pipeline disponible, **Cuando** se ejecuta `make estado`,
   **Entonces** muestra SHA, estado y URL.
3. **AC-03**: **Dado** la suite de pruebas, **Cuando** se ejecuta, **Entonces** hay
   pruebas con salida simulada de `glab`.

### Edge Cases

- **Sin `glab` en el PATH**: se devuelve una nota y una advertencia; no hay excepción.
- **`glab` falla o no responde**: se avisa «no se pudo consultar el pipeline».
- **Respuesta vacía o sin campos**: `parse_pipeline` devuelve `None`, no rompe el informe.
- **Sin red**: el comando agota su tiempo de espera y se comporta como fallo controlado.
- **Varios pipelines**: se usa el más reciente (primer elemento de la respuesta).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `make estado` MUST consultar el último pipeline de `develop` con `glab`.
- **FR-002**: MUST mostrar SHA corto, estado y URL del pipeline.
- **FR-003**: Si `glab` no está instalado o falla, MUST indicarlo sin lanzar excepción.
- **FR-004**: El parseo MUST aceptar una lista o un objeto JSON de la API de GitLab.
- **FR-005**: MUST existir una prueba por cada AC con salida simulada.

### Key Entities

- **Pipeline**: estado (`success`, `failed`, `running`…), SHA y URL web.
- **Report**: informe de `make estado` con git, PRs, issues y pipeline.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 Consulta `glab` y degrada | `tests/test_estado_gitlab.py::test_collect_gitlab_without_glab_returns_note`, `::test_render_without_pipeline_shows_note` |
| AC-02 Muestra SHA, estado y URL | `tests/test_estado_gitlab.py::test_render_shows_pipeline`, `::test_render_shows_short_sha` |
| AC-03 Salida simulada de `glab` | `tests/test_estado_gitlab.py::test_parse_pipeline_reads_first_run`, `::test_collect_gitlab_with_glab_parses` |

## Success Criteria *(mandatory)*

- **SC-001**: `make estado` muestra la línea `**GitLab:**` con SHA, estado y URL.
- **SC-002**: sin `glab`, `make estado` termina en cero y explica por qué no hay datos.
- **SC-003**: `make check` pasa con las pruebas nuevas.

## Out of Scope

- Autenticar `glab` en la máquina de cada integrante (lo cubre HU-073).
- Consultar jobs, artefactos o logs del pipeline.
- Sustituir el panel de GitLab.

## Assumptions

- La rama de integración es `develop` y el proyecto es
  `educacional-group/GPCICD_PPE_Detection` (ADR 0007).
- `glab` puede no estar instalado en local; CI no lo necesita para estas pruebas.
