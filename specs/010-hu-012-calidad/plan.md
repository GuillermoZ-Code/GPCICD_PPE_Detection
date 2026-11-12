# Implementation Plan: HU-012 — Verificaciones automatizadas de calidad

**Branch**: `feature/010-hu-012-calidad` | **Date**: 2026-11-10 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/010-hu-012-calidad/spec.md` e issue #12.

## Summary

Agregar un comando de calidad que ejecute Ruff, formato, tipos y pytest, imprima un
informe legible y devuelva un código de salida útil para CI o para el equipo. La lógica
es inyectable para probar el caso de regresión sin ejecutar la suite real en bucle.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: herramientas de desarrollo ya existentes (`ruff`, `ty`,
`pytest`); sin dependencias nuevas.

**Storage**: n/a.

**Testing**: pytest con un runner falso; una prueba de integración ejecuta Ruff sobre
un archivo temporal con un import sin usar.

**Target Platform**: CPU

**Project Type**: tooling

**Performance Goals**: el comando orquesta verificaciones; el costo es el de las
herramientas que ejecuta.

**Constraints**: sin GPU, sin dataset; salida UTF-8; no duplicar el job de CI.

**Scale/Scope**: 1 módulo `tools/calidad.py` (~100 líneas), 1 archivo de pruebas
(~6 pruebas), un target de Makefile y documentación.

## Constitution Check

- [x] `uv` como único gestor; no hay dependencias nuevas.
- [x] src-layout y pruebas en `tests/` con patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Sin LLM.
- [x] Test-first.
- [x] Uso responsable: no aplica a inferencia.

## Design

```text
src/ppe_detection/tools/calidad.py
├── Check        # nombre + comando
├── Result       # check, returncode, output, passed
├── DEFAULT_CHECKS
├── run_check(check, cwd) -> Result
├── run_all(checks, runner) -> list[Result]
├── render_report(results) -> str
└── main(argv) -> int
```

- Comandos por defecto: `ruff check .`, `ruff format --check .`, `ty check`,
  `pytest -q`.
- `subprocess.run(..., encoding="utf-8", errors="replace")`.
- `main` imprime el informe y devuelve 0/1.
- `make calidad` ejecuta `uv run python -m ppe_detection.tools.calidad`.

## Risks

- **Recursión:** las pruebas del comando usan un runner falso; no invocan pytest real
  desde pytest.
- **Herramienta ausente:** se reporta como fallo, no como éxito.
- **Windows:** la decodificación UTF-8 evita el fallo de `cp1252` visto en `estado.py`.

## Verification

- `uv run pytest tests/test_calidad.py`
- `uv run python -m ppe_detection.tools.calidad`
- `make check`
- `uv build`
