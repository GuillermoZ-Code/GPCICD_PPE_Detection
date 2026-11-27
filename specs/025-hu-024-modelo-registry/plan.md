# Implementation Plan: HU-024 — Modelo en GitLab Generic Packages

**Branch**: `feature/025-hu-024-modelo-registry` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

## Summary

Publicar el artefacto de YOLO26n en el Generic Package Registry del proyecto, apuntar
`models.lock` a esa URL y hacer que el job `deploy` lo descargue y lo verifique antes de
montarlo `:ro`. El peso nunca viaja en Git ni dentro de la imagen.

## Technical Context

**Language/Version**: TOML (`models.lock`), shell POSIX, YAML de GitLab CI/CD

**Primary Dependencies**: GitLab Package Registry, `curl`, `sha256sum`

**Testing**: pytest estático sobre el manifiesto y el pipeline

**Target Platform**: gitlab.com + Droplet

**Project Type**: MLOps / empaquetado de artefactos

**Constraints**: sin pesos en Git; sin tokens en el repositorio

**Scale/Scope**: 1 artefacto (5,21 MB), 1 versión activa

## Constitution Check

- **Pesos fuera de Git**: se publican en el registry y se referencian por URL + SHA. ✅
- **Reproducibilidad**: versión y SHA256 fijos en `models.lock`. ✅
- **Test-first**: pruebas estáticas sobre el manifiesto. ✅
- **`uv` como único gestor**: la descarga usa `curl`, no `pip`. ✅

## Project Structure

```text
models.lock                      # url → paquete genérico del proyecto
deploy/model/publish.sh          # publica y verifica el artefacto
tests/test_models_lock.py        # nuevo: manifiesto y coherencia
specs/025-hu-024-modelo-registry/
```

## Design decisions

1. **Paquete genérico en vez de artefactos de CI.** Los artefactos caducan; el paquete
   queda versionado y se puede volver a descargar meses después.
2. **Publicación manual y versionada.** CI no puede producir los pesos; el script exige
   archivo y versión y verifica lo subido.
3. **SHA en el manifiesto.** Un tag se puede reemplazar; el SHA256 detecta cualquier
   cambio antes de arrancar la API.
4. **Montaje `:ro`.** El contenedor no puede modificar el artefacto y la imagen sigue
   siendo reutilizable entre versiones del modelo.

## Risks

| Riesgo | Mitigación |
|---|---|
| Paquete reemplazado por error | El SHA256 del manifiesto lo detecta |
| Token caducado | El script falla antes de subir; el job de deploy usa `CI_JOB_TOKEN` |
| Versión distinta a la del manifiesto | Prueba estática que compara versión y URL |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_models_lock.py` (URL de paquete genérico) |
| AC-02 | `tests/test_models_lock.py` (SHA256 y versión coherentes) |
| AC-03 | `tests/test_models_lock.py` + `tests/test_model_publish.py` (descarga verificada y montaje `:ro`) |
