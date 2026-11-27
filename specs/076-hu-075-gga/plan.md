# Implementation Plan: HU-075 — GGA en pre-commit

**Branch**: `feature/076-hu-075-gga` | **Date**: 2026-11-27

**Spec**: [spec.md](./spec.md)

**Input**: Issue #131 y `specs/076-hu-075-gga/spec.md`.

## Summary

Versionar `.gga`, un wrapper opcional y el runbook de GGA. El hook de pre-commit
invoca el wrapper; si GGA no está instalado, el commit sigue. Si está instalado,
GGA revisa los cambios con OpenCode y su veredicto se propaga.

## Technical Context

**Language/Version**: Python 3.13, shell, YAML de pre-commit

**Primary Dependencies**: GGA v2.10.1 (externo, no versionado), OpenCode

**Testing**: pytest estático sobre `.gga`, el hook y el runbook; sin IA ni red

**Target Platform**: estaciones de desarrollo y CI

**Project Type**: infraestructura de calidad

**Constraints**: sin credenciales; GGA no bloquea si falta; no reemplaza la revisión

**Scale/Scope**: 1 configuración, 1 wrapper, 1 hook, 8 pruebas

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias Python.
- [x] Las pruebas corren sin GGA, GPU, dataset ni red.
- [x] Ruff, `ty`, pytest y `make check` se mantienen.
- [x] Sin tokens ni rutas personales versionadas.
- [x] La revisión humana y la CI siguen siendo obligatorias.
- [x] El hook es opcional y no bloquea equipos sin GGA.
- [x] Las reglas se leen de `CONSTITUTION.md`, no se duplican.

## Project Structure

```text
.gga                              # configuración versionada, sin secretos
.pre-commit-config.yaml           # hook local `gga-optional`
src/ppe_detection/tools/gga_hook.py
tests/test_gga.py
docs/operacion/gga.md
specs/076-hu-075-gga/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Flujo

```text
git commit
  └─ pre-commit
       └─ gga_hook
            ├─ ¿gga en PATH? → no: aviso + exit 0
            └─ sí: gga run → exit code de GGA
```

### Configuración

`.gga` usa `PROVIDER="opencode"` y `RULES_FILE="CONSTITUTION.md"`. Se revisan
`src/*`, `tests/*`, `frontend/src/*` y `deploy/*`; se excluyen entornos,
dependencias, artefactos y locks.

### Evidencia real

Se ejecuta `gga run --ci` o `gga run --pr-mode --diff-only` sobre una PR y la salida se
adjunta como comentario. No se copian credenciales ni rutas de la máquina.

## Phases

1. **Tests:** configuración, hook, wrapper, runbook y ausencia de tokens.
2. **Implementación:** `.gga`, `gga_hook.py`, hook y runbook.
3. **Evidencia:** revisión real con GGA sobre el diff de la PR.
4. **Cierre:** `make specs-check`, `make check`, `uv build`, PR `Closes #131`.

## Risks

| Riesgo | Mitigación |
|---|---|
| GGA no instalado | Wrapper devuelve 0 y avisa |
| Proveedor sin configurar | El error se propaga; el equipo decide desactivar el hook |
| Costo o latencia | `--diff-only` y `TIMEOUT=300` |
| Credenciales en `.gga` | Prueba de tokens y configuración sin claves |
| Revisión que sustituya al humano | Runbook y AC lo prohíben explícitamente |

## Verification

```bash
uv run pytest tests/test_gga.py -q
make specs-check
make check
uv build
```
