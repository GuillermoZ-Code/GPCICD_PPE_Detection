# Implementation Plan: HU-110 — MLflow en el Droplet (decisión de alcance)

**Branch**: No aplica | **Date**: 2026-11-28 | **Spec**: [spec.md](./spec.md)

## Summary

No se implementa un MLflow público en el Droplet. MLflow se mantiene como extra local
(`tracking`, HU-009) para evaluación y comparación de runs. La decisión se documenta y
se protege con pruebas estructurales que verifican que `compose.prod.yml` y el
`Caddyfile` no publican el servicio.

## Technical Context

**Language/Version**: Python 3.13 (pytest)

**Testing**: pytest estático sobre `compose.prod.yml`, `docker/Caddyfile` y documentación

**Constraints**: sin servicios nuevos, sin credenciales nuevas, sin carga adicional en
el Droplet de 1 vCPU

## Constitution Check

- **Test-first**: la prueba estructural se añade con la decisión. ✅
- **Sin secretos**: no se añaden credenciales. ✅
- **Sin cambios de despliegue**: el servicio vivo no se toca. ✅
- **Trazabilidad**: la spec y la prueba permiten cerrar #166. ✅

## Decision

- **MLflow local**: se conserva `docs/operacion/mlflow.md` y el extra `tracking`.
- **Sin ruta pública**: no hay `/mlflow` en Caddy ni servicio en compose.
- **Reapertura**: si se necesita, se abre una HU nueva con autenticación y persistencia.

## Verification

- `uv run pytest -q tests/test_mlflow_droplet_scope.py`
- `uv run python -m ppe_detection.tools.trazabilidad --check`
- `make check`
