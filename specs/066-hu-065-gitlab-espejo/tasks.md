# Tasks: HU-065 â€” Proyecto GitLab y espejo GitHub â†’ GitLab

**Input**: Design documents from `specs/066-hu-065-gitlab-espejo/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/066-hu-065-gitlab-espejo` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #121.

## Phase 2: Pruebas (test-first)

- [x] T003 [AC-01] El workflow existe, se dispara en `push` a `develop`/`main` y admite
      `workflow_dispatch`.
- [x] T004 [AC-01] El checkout usa `fetch-depth: 0`.
- [x] T005 [AC-01] El push apunta a `gitlab.com/educacional-group/GPCICD_PPE_Detection`
      y a `HEAD:refs/heads/${GITHUB_REF_NAME}`.
- [x] T006 [AC-01] El push no usa `--force`.
- [x] T007 [AC-02] El workflow consulta la API de commits y compara con `GITHUB_SHA`.
- [x] T008 [AC-03] El token viene de `secrets.GITLAB_TOKEN`.
- [x] T009 [AC-03] El token se enmascara con `::add-mask::`.
- [x] T010 [AC-03] No hay tokens literales (`glpat-`) ni credenciales en URLs.
- [x] T011 [AC-03] El workflow declara `permissions: contents: read`.
- [x] T012 Concurrencia definida y sin cancelaciÃ³n de pushes.
- [x] T013 El runbook `docs/operacion/gitlab-espejo.md` documenta token, secret,
      verificaciÃ³n y diagnÃ³stico.
- [x] T014 La documentaciÃ³n declara que GitHub es la fuente de verdad y que el espejo
      *pull* debe estar deshabilitado.

## Phase 3: ImplementaciÃ³n

- [x] T015 `.github/workflows/mirror-gitlab.yml` con checkout completo, credencial por
      helper, push y verificaciÃ³n del SHA.
- [x] T016 `docs/operacion/gitlab-espejo.md` con creaciÃ³n del token, secret, alineaciÃ³n
      de `main` y diagnÃ³stico.

## Phase 4: ConfiguraciÃ³n remota (requiere autorizaciÃ³n)

- [x] T017 Deshabilitar el espejo *pull* del proyecto GitLab 89281003.
- [x] T018 Crear el project access token con `write_repository` y guardarlo como
      `GITLAB_TOKEN` en GitHub Secrets.
- [x] T019 Alinear `main` una vez y verificar `develop` y `main` con el mismo SHA.

## Phase 5: Cierre

- [x] T020 `make check` y `make ownership-check` en verde.
- [x] T021 PR con plantilla UAO, `Closes #121`, revisor de otro integrante.
