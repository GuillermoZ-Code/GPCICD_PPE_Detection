# Implementation Plan: HU-093 — Matriz de trazabilidad HU → issue → spec → PR → pruebas

**Branch**: `feature/094-hu-093-matriz-trazabilidad` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #149 y `specs/094-hu-093-matriz-trazabilidad/spec.md`.

## Summary

Crear `src/ppe_detection/tools/trazabilidad.py`: lee las issues y PRs con `gh`, indexa
`specs/` y busca referencias `HU-NNN` en `tests/` y en los `*.test.tsx` del frontend.
Genera `docs/curso/TRAZABILIDAD.md` con una fila por HU y una compuerta `--check` que
falla si una HU cerrada no tiene spec o pruebas. Un workflow de CI ejecuta la compuerta.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: biblioteca estándar (`subprocess`, `json`, `re`, `pathlib`) y
`gh`; sin dependencias nuevas

**Storage**: `docs/curso/TRAZABILIDAD.md` (generado)

**Testing**: pytest con datos simulados; sin `gh` ni red

**Target Platform**: CPU, Windows/Linux; CI en Ubuntu

**Project Type**: herramienta de repositorio dentro del paquete

**Constraints**: no editar issues ni PR; no tocar `uv.lock`

**Scale/Scope**: 113 HU, un comando y un workflow

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Cada AC tiene una prueba que lo referencia.
- [x] Sin cambios en el contrato `ImageData → list[Detection]`.
- [x] `src/ppe_detection/tools/` y `tests/test_tools*.py` son del autor;
      `.github/` y `Makefile` generan aviso de propiedad.
- [x] Documentación en español, identificadores en inglés.

## Project Structure

```text
src/ppe_detection/tools/trazabilidad.py   # nuevo: matriz y compuerta
tests/test_tools_trazabilidad.py          # nuevo: parsers y check con datos simulados
.github/workflows/trazabilidad.yml        # nuevo: job de compuerta
Makefile                                  # + trazabilidad y trazabilidad-check
docs/curso/TRAZABILIDAD.md                # generado
specs/094-hu-093-matriz-trazabilidad/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Funciones puras (probadas sin red)

- `specs_by_hu(root) -> dict[str, str]`: carpetas `specs/NNN-hu-NNN-slug`.
- `tests_by_hu(root) -> dict[str, set[str]]`: apariciones de `HU-NNN` en `tests/*.py`
  y `frontend/src/**/*.test.tsx`.
- `spec_tests(root, specs) -> dict[str, set[str]]`: archivos citados en la tabla de
  aceptación de cada `spec.md` (`tests/test_*.py` y `src/...test.tsx`).
- `prs_by_hu(prs) -> dict[str, set[int]]`: `Closes #N`, `HU-NNN` en el título o
  `hu-nnn` en la rama.
- `build_rows(...) -> list[TraceRow]`: combina todo y marca faltantes.
- `check(rows, exemptions) -> list[str]`: HU cerradas incompletas, sin exenciones.
- `render(rows) -> str`: tabla Markdown con totales.

### Datos de GitHub

- `load_issues()`: `gh issue list --state all --limit 400`.
- `load_prs()`: `gh pr list --state merged --limit 400`.

### Compuerta

```bash
uv run python -m ppe_detection.tools.trazabilidad --check
```

Sale con 1 y lista las HU cerradas sin spec o sin pruebas. Las exenciones
(`EXEMPTIONS`) declaran el motivo: HU-016 (spike), HU-018 (GPU), HU-019 (informe),
HU-023 (ADR) y HU-089 (issues en GitHub).

### Alternativas descartadas

- **Construir la matriz a mano**: 113 filas se desactualizan en un día.
- **Usar la API GraphQL con `gh api`**: más código para el mismo resultado; `gh issue
  list` ya da número, título y estado.
- **Contar pruebas por AC (`AC-0N`)**: los AC son locales a cada HU y no identifican la
  HU; se usa `HU-NNN` y la cita de la spec.

## Phases

1. **Tests first**: parsers, filas y compuerta con datos simulados.
2. **Implementación**: módulo, objetivos del Makefile y workflow.
3. **Generación**: `make trazabilidad-write` y revisar el diff.
4. **Cierre**: `make trazabilidad-check`, `make check`, PR y `Closes #149`.

## Risks

- **Exenciones**: una HU nueva sin pruebas debe justificarse o el check falla; es el
  comportamiento buscado.
- **Referencias**: una prueba que no menciona su HU se marca como faltante; se corrige
  añadiendo la mención en el docstring del archivo.
- **CI con `gh`**: el workflow usa `GITHUB_TOKEN`; el repositorio es privado y el token
  tiene lectura de issues y PRs.
