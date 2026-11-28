# Implementation Plan: HU-043 — Escaneo de secretos con gitleaks

**Branch**: `feature/044-hu-043-gitleaks` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

## Summary

Añadir una compuerta de secretos con gitleaks: configuración en la raíz, job en la CI
de GitHub que escanea el histórico y objetivo `make secrets` para repetirlo en local.

## Technical Context

**Language/Version**: TOML (configuración), YAML (workflow), GNU Make

**Primary Dependencies**: `gitleaks/gitleaks-action@v2`, binario `gitleaks` (local)

**Testing**: pytest estático sobre la configuración, el workflow y la superficie

**Target Platform**: GitHub Actions y máquina del integrante

**Constraints**: sin licencia (repo de cuenta personal); sin secretos reales

**Scale/Scope**: 1 configuración, 1 job, 1 objetivo

## Constitution Check

- **Sin secretos en el repositorio**: esto lo verifica. ✅
- **Test-first**: 8 pruebas antes del job. ✅
- **Sin dependencias de Python nuevas**: no toca `pyproject.toml`. ✅
- **Una HU por PR**: solo el escaneo. ✅

## Project Structure

```text
.gitleaks.toml                     # nuevo: reglas y exclusiones
.github/workflows/ci.yml           # job `secrets`
Makefile                           # objetivo `secrets`
tests/test_gitleaks.py             # 8 pruebas
specs/044-hu-043-gitleaks/
```

## Design decisions

1. **Acción oficial en CI.** Mantiene el escaneo actualizado y no obliga a compilar el
   binario en cada ejecución.
2. **Histórico completo.** Un token borrado en un commit posterior sigue en el
   historial; `fetch-depth: 0` lo detecta.
3. **Exclusiones explícitas.** `docs/` y `tests/` contienen ejemplos y fixtures; se
   excluyen con motivo escrito, no por comodidad.
4. **`make secrets` para local.** Mismo comando que la CI, sin esperar al pipeline.

## Risks

| Riesgo | Mitigación |
|---|---|
| Falso positivo por un ejemplo de documentación | Lista de exclusión con motivo |
| La acción pide licencia | El repo es de cuenta personal: no aplica |
| Escaneo lento del histórico | Solo corre en CI, con cache de checkout |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_gitleaks.py` (configuración y exclusiones) |
| AC-02 | `tests/test_gitleaks.py` (job, permisos y `fetch-depth`) |
| AC-03 | `tests/test_gitleaks.py` (`make secrets` y ausencia de tokens) |
