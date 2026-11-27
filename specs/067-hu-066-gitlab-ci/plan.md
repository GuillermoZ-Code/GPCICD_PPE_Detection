# Implementation Plan: HU-066 — `.gitlab-ci.yml` base

**Branch**: `feature/067-hu-066-gitlab-ci` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/067-hu-066-gitlab-ci/spec.md`

## Summary

Crear el pipeline base de GitLab con imagen oficial de `uv`, cache por job y reglas
explícitas: ramas y merge requests validan; solo la rama por defecto empaqueta. Los
jobs nuevos se escriben con el mismo criterio que GitHub Actions, para que un rojo
signifique lo mismo en las dos forjas.

## Technical Context

**Language/Version**: YAML de GitLab CI/CD; Python 3.13; Node 24

**Primary Dependencies**: `ghcr.io/astral-sh/uv:0.13.9-python3.13-trixie-slim`,
`node:24-alpine`, `docker:29.10.0-cli` + `docker:29.10.0-dind`

**Testing**: pytest estático sobre `.gitlab-ci.yml` (sin red y sin runner)

**Target Platform**: gitlab.com, runners compartidos

**Project Type**: infraestructura CI/CD

**Constraints**: sin secretos en el repositorio; sin `only/except` (obsoleto); el
pipeline no debe duplicarse entre rama y MR

**Scale/Scope**: 1 archivo, 5 jobs de validación, 1 job de imágenes

## Constitution Check

- **Sin secretos en el repositorio**: las credenciales son variables de CI/CD. ✅
- **`uv` como único gestor**: el pipeline no usa `pip` ni `requirements.txt`. ✅
- **Test-first**: las pruebas estáticas se escriben antes del YAML. ✅
- **Sin pesos ni datos en Git**: el modelo se monta, no se hornea. ✅
- **Una HU por PR**: este PR cubre el pipeline de GitLab; el deploy va aparte. ✅

## Project Structure

```text
.gitlab-ci.yml                        # nuevo: pipeline base + build + publicación
tests/test_gitlab_ci.py               # nuevo: pruebas estáticas de AC-01 a AC-03
specs/067-hu-066-gitlab-ci/
├── spec.md
├── plan.md
└── tasks.md
```

## Design decisions

1. **Imagen de uv, no Docker, para validar.** El job instala solo lo que necesita y
   arranca en segundos; construir la imagen en cada push sería desperdiciar minutos.
2. **`--only-group dev` en lint.** Ruff no necesita torch ni OpenCV: si el estilo está
   mal, el pipeline falla antes de instalar el entorno completo.
3. **Cache con prefijo por job.** Compartir clave hacía que `lint` pisara el entorno de
   `test`; con `prefix: $CI_JOB_NAME` cada job conserva el suyo.
4. **Reglas explícitas en vez de `only/except`.** `rules` permite combinar rama, MR y
   ejecución manual sin duplicar pipelines.
5. **`auto_cancel` + `timeout`.** Un push nuevo invalida el anterior; un job colgado
   muere a los 20 minutos.
6. **Sin `merge_request_event` obligatorio.** Los MR viven en GitHub; GitLab valida
   ramas. La regla de MR queda por si el equipo migra la revisión.

## Risks

| Riesgo | Mitigación |
|---|---|
| El runner no tiene Docker | `build_image` usa DinD declarado como servicio |
| El cache crece sin control | Clave por archivo de bloqueo; GitLab expira solo |
| Un job nuevo rompe el pipeline de todos | `glab ci lint` + pruebas estáticas antes de fusionar |
| Duplicación rama/MR | Regla `$CI_OPEN_MERGE_REQUESTS` |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_gitlab_ci.py` (stages, cache de uv, cache de npm) |
| AC-02 | `tests/test_gitlab_ci.py` (reglas de ramas/MR y de `main`) |
| AC-03 | `tests/test_gitlab_ci.py` (archivo presente y sin `only/except`); `glab ci lint` en la revisión |
