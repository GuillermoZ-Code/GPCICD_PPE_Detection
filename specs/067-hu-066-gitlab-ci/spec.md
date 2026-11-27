# Feature Specification: HU-066 — `.gitlab-ci.yml` base: stages, cachés y reglas

**Feature Branch**: `feature/067-hu-066-gitlab-ci`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #122 — «HU-066 — `.gitlab-ci.yml` base: stages, cachés y reglas».
Asignada a Guillermo (`GuillermoZ-Code`), épica `ep-06`, P0, ola 3, 2 SP, 8 pruebas
objetivo. Depende de HU-065 (espejo GitHub → GitLab), ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cada push valida el código en GitLab (Priority: P0)

Como equipo, quiero que cada push espejado a GitLab ejecute lint, tipos, pruebas y
frontend, para que el SHA que revisa el equipo sea el mismo que pasa por las compuertas.

**Why this priority**: el pipeline de GitLab es el requisito de CI/CD de la rúbrica del
M4. Sin stages ni reglas no hay compuertas, y sin compuertas el build y el deploy no
tienen nada que bloquear.

**Independent Test**: se empuja un cambio a `develop`, GitLab crea el pipeline y los
jobs `lint`, `types`, `specs`, `test` y `frontend` terminan en verde.

**Acceptance Scenarios** (AC de la issue #122):

1. **AC-01**: **Dado** un push, **Cuando** corre el pipeline, **Entonces** hay stages
   definidos y el cache de uv y el de npm están declarados.
2. **AC-02**: **Dado** el pipeline de una rama, **Cuando** se evalúan las reglas,
   **Entonces** lint y test corren en ramas y MR, y build/deploy solo en `main`.
3. **AC-03**: **Dado** el archivo `.gitlab-ci.yml`, **Cuando** se ejecuta `glab ci
   lint`, **Entonces** la sintaxis es válida.

### Edge Cases

- **Dos pushes seguidos**: `auto_cancel` interrumpe el pipeline anterior.
- **Job colgado**: `timeout: 20 minutes` corta el job en vez de consumir una hora.
- **Falta `uv.lock` o cambia `pyproject.toml`**: la clave del cache cambia y se
  reconstruye.
- **Rama con MR abierto**: no se duplica el pipeline del MR.
- **Tag**: no dispara pipeline; el release se construye desde `main`.
- **Sin Docker Hub configurado**: el job de imágenes sigue en verde y solo omite el
  espejo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El pipeline MUST definir los stages `quality`, `test` y `package`, en ese
  orden.
- **FR-002**: El cache de uv MUST usar `pyproject.toml` y `uv.lock` como clave, con
  prefijo por job.
- **FR-003**: El cache de npm MUST usar `frontend/package-lock.json` como clave.
- **FR-004**: Los jobs de calidad MUST correr en ramas y en merge requests.
- **FR-005**: `build_image` MUST correr solo en la rama por defecto o de forma manual.
- **FR-006**: El pipeline MUST cancelar ejecuciones obsoletas (`auto_cancel`) y ser
  `interruptible`.
- **FR-007**: La instalación de dependencias MUST respetar `uv.lock` (`UV_FROZEN=1`).
- **FR-008**: Las pruebas MUST publicarse como reporte JUnit.

### Key Entities

- **Pipeline**: ejecución de los stages sobre un SHA espejado desde GitHub.
- **Cache**: `.uv-cache/` para Python y `frontend/node_modules/` para el frontend,
  versionados por archivo de bloqueo.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `glab ci lint` valida el archivo sin errores.
- **SC-002**: Al menos 8 pruebas estáticas cubren stages, caches y reglas.
- **SC-003**: `make check` en verde y el pipeline de GitLab en verde sobre `develop`.

## Assumptions

- El proyecto GitLab existe y el espejo ya empuja `develop` y `main` (HU-065).
- La rama por defecto de GitLab es `main`, igual que en GitHub.
- Los runners compartidos de gitlab.com tienen Docker disponible para los jobs que lo
  piden.
