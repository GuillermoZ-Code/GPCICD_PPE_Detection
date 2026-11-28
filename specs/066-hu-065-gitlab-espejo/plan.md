# Implementation Plan: HU-065 — Proyecto GitLab y espejo GitHub → GitLab

**Branch**: `feature/066-hu-065-gitlab-espejo` | **Date**: 2026-11-25 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/066-hu-065-gitlab-espejo/spec.md`

## Summary

Replicar `develop` y `main` de GitHub a GitLab con un workflow de GitHub Actions que
empuja el commit exacto y luego verifica por API que el SHA coincide. El token vive en
`secrets.GITLAB_TOKEN` y se enmascara; no se usa `--force` sobre ramas protegidas.

## Technical Context

**Language/Version**: GitHub Actions (runner `ubuntu-latest`), YAML, shell POSIX

**Primary Dependencies**: `actions/checkout@v7`, `git`, `curl`, `python3` (preinstalados
en el runner); GitLab API v4

**Storage**: N/A (GitLab aloja el espejo)

**Testing**: pytest estático sobre el YAML y el runbook (sin red ni GitLab)

**Target Platform**: GitHub Actions → GitLab.com

**Project Type**: infraestructura CI/CD

**Performance Goals**: el espejo termina en menos de 2 minutos por push

**Constraints**: sin tokens en el repositorio; sin funciones Premium de GitLab; sin
`--force` sobre `main`

**Scale/Scope**: 2 ramas, 1 proyecto GitLab (id 89281003)

## Constitution Check

- **Sin secretos en el repositorio**: el token solo existe como secret y se enmascara. ✅
- **Datos y pesos fuera de Git**: no aplica. ✅
- **Test-first**: cada AC tiene prueba estática antes del workflow. ✅
- **`make check` en verde**: las pruebas nuevas son pytest. ✅
- **Propiedad**: `.github/` y `tests/` del flujo de CI no tienen dueño conflictivo;
  `docs/operacion/` es de Eliana (aviso, no bloqueo). ✅
- **Una HU por PR**: solo el espejo, su runbook y sus pruebas. ✅

## Project Structure

```text
.github/workflows/mirror-gitlab.yml   # nuevo: workflow del espejo
tests/test_mirror_gitlab.py           # nuevo: 12 pruebas estáticas
docs/operacion/gitlab-espejo.md       # nuevo: runbook (token, secret, verificación)
specs/066-hu-065-gitlab-espejo/
├── spec.md
├── plan.md
└── tasks.md
```

## Design decisions

1. **Push desde GitHub Actions, no pull mirror de GitLab.** El espejo *pull* que tenía
   GitLab quedó en `import_status: failed` (`9:Could not update main`) y compite con
   cualquier push: si sigue activo, puede reescribir ramas. GitHub es la fuente de
   verdad; el workflow empuja solo las ramas `develop` y `main`.
2. **Credencial por helper, no en la URL.** El token se pasa con
   `credential.helper` leyendo `GITLAB_TOKEN` del entorno, para que nunca aparezca en la
   URL del remoto ni en un mensaje de error de `git`.
3. **Verificación activa del SHA (AC-02).** El workflow no confía en que el push
   funcione: consulta `GET /projects/:id/repository/commits?ref_name=...` y compara con
   `GITHUB_SHA`. Si no coincide, falla.
4. **Sin `--force`.** El push normal mantiene la protección de `main`. La divergencia
   inicial (commit `7a9b206b` creado por web en GitLab) se resuelve una sola vez, fuera
   del workflow.
5. **Project access token con `write_repository`.** Permiso mínimo para empujar; nada de
   `api` completo ni un PAT personal de larga vida.
6. **`fetch-depth: 0`.** Evita pushes superficiales que GitLab rechaza por falta de
   ancestros.

## Risks

| Riesgo | Mitigación |
|---|---|
| `main` divergió por un commit creado en GitLab | Alineación única documentada; después el workflow solo avanza |
| Rama protegida rechaza el push | Token con rol Maintainer y `write_repository`; `main` solo cambia en release |
| Token en logs | `::add-mask::` + credencial por helper, nunca en la URL |
| El espejo *pull* vuelve a activarse | Runbook indica deshabilitarlo y por qué |
| Push de una rama no espejada | El workflow solo escucha `develop` y `main` |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_mirror_gitlab.py` (disparadores, checkout completo, push a la rama y al remoto correcto) |
| AC-02 | `tests/test_mirror_gitlab.py` (consulta de la API y comparación con `GITHUB_SHA`) |
| AC-03 | `tests/test_mirror_gitlab.py` (secret, `::add-mask::`, ausencia de `glpat-` y de tokens en URL, `permissions: contents: read`) |
