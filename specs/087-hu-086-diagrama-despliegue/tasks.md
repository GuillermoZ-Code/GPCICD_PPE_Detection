# Tasks: HU-086 — Diagrama de arquitectura de despliegue

**Input**: Design documents from `specs/087-hu-086-diagrama-despliegue/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/087-hu-086-diagrama-despliegue` desde `develop`
      actualizado (HU-070 #126 está *Done*).
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #142.
- [x] T003 Verificar dependencia: HU-070 #126 en *Done*; #142 en *In progress* y
      asignada a Eliana.

## Phase 2: Pruebas (test-first)

- [x] T004 [AC-01] `tests/test_arquitectura_despliegue.py`: componentes y conexiones
      `github → gitlab → registry → droplet → usuario`, con Caddy, `web` y `grpc`.
- [x] T005 [AC-02] El JSON documenta `SSH_KEY`, `DOCKERHUB_TOKEN`, `PPE_AUTH_HASH`,
      puertos 80/443, 8000 y 9000, y healthchecks `/health` y `/health/ready`.
- [x] T006 [AC-03] El JSON es válido, `schema_version` ≥ 1 y `meta.output` apunta al HTML.
- [x] T007 [AC-01/03] El HTML regenerado contiene los nodos `GitHub`, `GitLab CI`,
      `Registry`, `Droplet` y `Caddy`.

## Phase 3: Diagrama

- [x] T008 Actualizar `docs/architecture/arquitectura.json` con la cadena de entrega,
      Caddy, SPA, gRPC interno, secretos, puertos y healthchecks.
- [x] T009 Regenerar `docs/architecture/arquitectura.html` con Archify
      (`deliver architecture ... --quality showcase`) desde una copia temporal del skill.
- [x] T010 Ajustar `docs/architecture/README.md` para describir el flujo de despliegue
      sin editar el HTML a mano.

## Phase 4: Cierre

- [x] T011 Ruff, formato, `ty`, pytest y `ownership-check` verificados en local.
- [x] T012 PR con plantilla UAO, `Closes #142`, reviewer Guillermo por propiedad de
      `docs/architecture/`, y CI reportada solo con evidencia. PR #262 abierta; 9/9
      checks en `success` verificados con `gh pr checks 262 --watch`.

## Evidencia local (2026-11-27)

- Test-first: las cuatro pruebas nuevas se ejecutaron antes del cambio; tres fallaron
  (AC-01, AC-02 y AC-01/03) y AC-03 ya pasaba.
- Después del cambio: `uv run pytest -q tests/test_arquitectura_despliegue.py` →
  **4 passed**.
- Archify `deliver architecture docs/architecture/arquitectura.json
  docs/architecture/arquitectura.html --quality showcase --json` → `ok: true`,
  `validation.checksPassed: 9/9`, `errors: 0`, `warnings: 0`, artefacto de 971.227 bytes.
- Archify `finalize` no pudo publicar su recibo en Windows/OneDrive; se usó `deliver`,
  que validó y escribió el artefacto correctamente. No se editó el HTML a mano.
- `docs/architecture/` es propiedad de Guillermo: la futura PR debe pedir su revisión.
  No se modificaron `deploy/*`, `.gitlab-ci.yml` ni `compose.prod.yml`.

## Estado

- Implementación commiteada (`a3c9bd3`) y rebaseada sobre `origin/develop`.
- PR #262 abierta a `develop` con revisor Guillermo; no fusionada ni autoaprobada.
- Issue #142 movida a *In review* para liberar WIP.
- CI en verde: 9/9 checks en `success` (`gh pr checks 262 --watch`, 2026-11-27).
- Suite local tras el rebase: 945 passed, 2 skipped; Ruff, formato, `ty`, propiedad y
  `uv build` correctos.
