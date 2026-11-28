# Implementation Plan: HU-068 — Publicar imágenes en GitLab Registry y Docker Hub

**Branch**: `feature/067-hu-066-gitlab-ci` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/069-hu-068-registry/spec.md`

## Summary

Publicar las imágenes del build en el Container Registry del proyecto con el token
efímero del job y, si existen credenciales, replicarlas en Docker Hub. El digest de cada
imagen queda como artefacto para desplegar exactamente lo construido.

## Technical Context

**Language/Version**: Docker 29, YAML de GitLab CI/CD

**Primary Dependencies**: Container Registry de gitlab.com, Docker Hub (opcional)

**Testing**: pytest estático sobre `.gitlab-ci.yml`

**Target Platform**: gitlab.com + Docker Hub

**Project Type**: infraestructura CI/CD

**Constraints**: ningún token en el repositorio; Docker Hub opcional

**Scale/Scope**: 2 imágenes, 2 destinos, 1 digest por imagen

## Constitution Check

- **Sin secretos versionados**: solo variables de CI/CD enmascaradas. ✅
- **Reproducibilidad**: tag por SHA y digest como artefacto. ✅
- **Test-first**: pruebas estáticas antes del job. ✅
- **AGPL**: la imagen se publica con el aviso de licencia del repositorio. ✅

## Project Structure

```text
.gitlab-ci.yml                        # pasos de login, push y digest
tests/test_gitlab_ci.py               # pruebas de AC-01 a AC-03
specs/069-hu-068-registry/
├── spec.md
├── plan.md
└── tasks.md
```

## Design decisions

1. **`CI_JOB_TOKEN` para GitLab.** Es efímero y no requiere crear un usuario más; el
   registry del proyecto lo acepta por defecto.
2. **Docker Hub opcional.** Sin cuenta, el pipeline sigue en verde y el Droplet baja del
   registry de GitLab con un deploy token.
3. **Digest como artefacto.** Permite auditar qué se desplegó y volver a un tag
   conocido.
4. **Nada de `docker login` con contraseñas literales.** Siempre por `--password-stdin`
   y con la salida silenciada.

## Risks

| Riesgo | Mitigación |
|---|---|
| Token del job filtrado | Es efímero y no se imprime |
| Docker Hub sin credenciales | Rama `else` explícita; el job queda en verde |
| Tag mutable `latest` | Se despliega por SHA; `latest` es solo comodidad |
| Registry lleno | Se conservan solo las últimas imágenes; limpieza documentada |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_gitlab_ci.py` (`CI_JOB_TOKEN`, `CI_REGISTRY_USER`, sin contraseñas literales) |
| AC-02 | `tests/test_gitlab_ci.py` (variables `DOCKERHUB_*` y rama sin credenciales) |
| AC-03 | `tests/test_gitlab_ci.py` (artefactos `api-digest.txt` y `web-digest.txt`) |
