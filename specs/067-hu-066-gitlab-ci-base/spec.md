# Feature Specification: HU-066 — `.gitlab-ci.yml` base: stages, cachés y reglas

**Feature Branch**: `feature/067-hu-066-gitlab-ci-base`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #122 — «HU-066 — `.gitlab-ci.yml` base: stages, cachés y reglas».
Asignada a Guillermo (`GuillermoZ-Code`), épica `ep-06`, P0, ola 3, 2 SP, 8 pruebas
objetivo. Depende de HU-065 (en revisión, PR #218).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Pipeline base trazable por commit (Priority: P0)

Como responsable de CI, quiero un pipeline con lint → test → build → deploy → verify, para
que cada etapa sea trazable por commit y el equipo vea en GitLab el mismo resultado que en
GitHub.

**Why this priority**: el 40 % de la rúbrica del M4 es el pipeline de GitLab. Sin un
`.gitlab-ci.yml` versionado, GitLab ejecuta lo que alguien subió por web y el SHA no se
puede defender.

**Independent Test**: el archivo pasa `glab ci lint`; en un pipeline de MR corren
`quality` y `frontend`, y en `main` corren además `build` y el `deploy` manual.

**Acceptance Scenarios** (AC de la issue #122):

1. **AC-01**: **Dado** el pipeline, **Cuando** corre, **Entonces** las etapas están
   definidas y `uv` y `npm` usan caché.
2. **AC-02**: **Dados** un MR y un push, **Cuando** se dispara, **Entonces** lint y test
   corren en MR y ramas, y `main` ejecuta build y deploy.
3. **AC-03**: **Dado** el archivo, **Cuando** se valida con `glab ci lint`, **Entonces**
   es válido y no usa `pip` ni secretos embebidos.

### Edge Cases

- Un push a `develop` no debe crear dos pipelines (MR + rama): `workflow.rules` lo evita.
- `build` en `develop` no corre; se puede lanzar manual.
- `deploy` es un marcador manual hasta HU-070; no debe romper el pipeline
  (`allow_failure`).
- `uv.lock` o `package-lock.json` desactualizados: la caché cambia de clave y la compuerta
  falla de forma visible.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El pipeline MUST declarar las etapas `quality`, `frontend`, `build` y
  `deploy` en ese orden.
- **FR-002**: `quality` MUST usar `uv sync --frozen` y ejecutar Ruff, `ruff format
  --check`, `ty` y pytest.
- **FR-003**: `frontend` MUST usar Node 24, `npm ci`, lint, pruebas y build.
- **FR-004**: MUST existir caché de `uv` (por `uv.lock`) y de `npm` (por
  `package-lock.json`).
- **FR-005**: `workflow.rules` MUST cubrir MR, `develop`, `main` y ejecución manual, sin
  duplicar pipelines.
- **FR-006**: `build` y `deploy` MUST limitarse a `main` (o manual).
- **FR-007**: `deploy` MUST ser manual y declararse pendiente de HU-070.
- **FR-008**: El archivo MUST NOT usar `pip` ni contener secretos.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `glab ci lint` acepta el archivo.
- **SC-002**: Al menos 8 pruebas estáticas cubren los tres AC.
- **SC-003**: `make check` en verde y el pipeline de GitLab en verde al fusionar.

## Assumptions

- El runner de GitLab es compartido y tiene acceso a `ghcr.io/astral-sh/uv` y
  `node:24-alpine`.
- El despliegue real llega en HU-070; aquí solo se reserva la etapa.
- El espejo de HU-065 entrega este archivo a GitLab con el mismo SHA.
