# Implementation Plan: HU-044 — Configuración por entorno validada al arrancar

**Branch**: `feature/045-hu-044-config-entorno` | **Date**: 2026-11-24

**Spec**: [spec.md](spec.md)

**Input**: Issue #100 y `specs/045-hu-044-config-entorno/spec.md`.

## Summary

Crear `src/ppe_detection/api/settings.py` con configuración tipada y validación
temprana; `.env.example` documentará las 16 variables `PPE_*` existentes más
`PPE_API_KEY` (reservada para HU-051). `create_app` validará al construirse y el módulo
`settings` ofrecerá un entrypoint CLI que devuelve 1 sin imprimir secretos.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: biblioteca estándar (`re`, `os`, `sys`, `urllib.parse`); sin
dependencias nuevas

**Storage**: solo lectura del entorno y de `.env.example`

**Testing**: pytest, `monkeypatch`, `subprocess` con `-m ppe_detection.api.settings`

**Target Platform**: CPU, Windows/Linux

**Project Type**: módulo de configuración dentro de la API

**Constraints**: no tocar `detector_config.py`, `.github/`, `uv.lock`, `PRUEBAS.md` ni
`tests/conftest.py`; test-first.

## Design

1. `Settings` (dataclass frozen) con valores por omisión idénticos a los actuales.
2. `validate_environment(env)` devuelve `list[str]`; cada mensaje nombra la variable,
   el motivo y, salvo secretos, el valor recibido.
3. `load_settings(env=None)` lanza `SettingsError` con los mensajes unidos.
4. `create_app()` llama a `load_settings()` antes de registrar endpoints.
5. `main()` en `settings.py` imprime `Configuración inválida: …` en stderr y devuelve 1;
   `python -m ppe_detection.api.settings` usa `SystemExit(main())`.
6. `.env.example` es un listado comentado con valores seguros (sin claves reales).

## Test-first plan

- Crear `tests/test_api_settings.py` con 8 pruebas AC-01/02/03.
- Ejecutar solo ese archivo y confirmar fallos antes de crear `settings.py`.
- Implementar y repetir suite completa.

## Validation

- `uv run pytest -v tests/test_api_settings.py`
- `uv run ruff check .` · `uv run ruff format --check .` · `uv run ty check`
- `uv run pytest -v`
- validación aislada de la spec con `check_specs._validate_spec`
- `uv run python -m ppe_detection.tools.ownership --base origin/develop`

## Risks

- `create_app()` se ejecuta al importar `ppe_detection.api`; si el entorno de un test
  ajeno tiene un valor inválido, fallará temprano. Por eso se validan solo variables
  conocidas y se permiten valores vacíos en opcionales.
- El CLI debe usar `stderr` y no `traceback` para que el mensaje sea claro.
