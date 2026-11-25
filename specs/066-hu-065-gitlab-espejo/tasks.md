# Tasks: HU-065 — Proyecto GitLab y espejo GitHub → GitLab

**Input**: Design documents from `specs/066-hu-065-gitlab-espejo/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/066-hu-065-gitlab-espejo` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #121.

## Phase 2: Pruebas (test-first)

- [ ] T003 [AC-01] El workflow existe, se dispara en `push` a `develop`/`main` y admite
      `workflow_dispatch`.
- [ ] T004 [AC-01] El checkout usa `fetch-depth: 0`.
- [ ] T005 [AC-01] El push apunta a `gitlab.com/educacional-group/GPCICD_PPE_Detection`
      y a `HEAD:refs/heads/${GITHUB_REF_NAME}`.
- [ ] T006 [AC-01] El push no usa `--force`.
- [ ] T007 [AC-02] El workflow consulta la API de commits y compara con `GITHUB_SHA`.
- [ ] T008 [AC-03] El token viene de `secrets.GITLAB_TOKEN`.
- [ ] T009 [AC-03] El token se enmascara con `::add-mask::`.
- [ ] T010 [AC-03] No hay tokens literales (`glpat-`) ni credenciales en URLs.
- [ ] T011 [AC-03] El workflow declara `permissions: contents: read`.
- [ ] T012 Concurrencia definida y sin cancelación de pushes.
- [ ] T013 El runbook `docs/operacion/gitlab-espejo.md` documenta token, secret,
      verificación y diagnóstico.
- [ ] T014 La documentación declara que GitHub es la fuente de verdad y que el espejo
      *pull* debe estar deshabilitado.

## Phase 3: Implementación

- [ ] T015 `.github/workflows/mirror-gitlab.yml` con checkout completo, credencial por
      helper, push y verificación del SHA.
- [ ] T016 `docs/operacion/gitlab-espejo.md` con creación del token, secret, alineación
      de `main` y diagnóstico.

## Phase 4: Configuración remota (requiere autorización)

- [ ] T017 Deshabilitar el espejo *pull* del proyecto GitLab 89281003.
- [ ] T018 Crear el project access token con `write_repository` y guardarlo como
      `GITLAB_TOKEN` en GitHub Secrets.
- [ ] T019 Alinear `main` una vez y verificar `develop` y `main` con el mismo SHA.

## Phase 5: Cierre

- [ ] T020 `make check` y `make ownership-check` en verde.
- [ ] T021 PR con plantilla UAO, `Closes #121`, revisor de otro integrante.
