# Implementation Plan: HU-094 — Conteo reproducible de pruebas

**Branch**: `feature/095-hu-094-conteo-pruebas` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #150 y `specs/095-hu-094-conteo-pruebas/spec.md`.

## Summary

Añadir `src/ppe_detection/tools/pruebas.py`, un contador que lanza
`pytest --collect-only` y `vitest list --json`, agrupa los casos por archivo, resuelve el
dueño con `propiedad.toml` y escribe `docs/curso/PRUEBAS.md`. Los parsers y el render son
funciones puras para probarlas con salidas simuladas. Se añade el objetivo
`make pruebas` al Makefile sin reordenar lo existente.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: biblioteca estándar (`subprocess`, `json`, `shutil`,
`pathlib`) y `tomllib`; sin dependencias nuevas

**Storage**: `docs/curso/PRUEBAS.md` regenerado; nada más se escribe

**Testing**: pytest con AAA y salidas simuladas; sin Node ni subprocesos en las pruebas

**Target Platform**: CPU, Windows/Linux

**Project Type**: herramienta de repositorio dentro del paquete

**Constraints**: no ejecutar la suite completa; no tocar `uv.lock`,
`frontend/package.json` ni las pruebas existentes

**Scale/Scope**: un comando, un archivo de salida y un objetivo de Makefile

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Cada AC tiene una prueba que lo referencia (`AC-0N` en el docstring).
- [x] Sin cambios en el contrato `ImageData → list[Detection]`.
- [x] `src/ppe_detection/tools/` y `docs/curso/PRUEBAS.md` pertenecen a
      `jesusriverosUAO`; el Makefile genera aviso y revisión, no bloqueo.
- [x] Documentación y pruebas en español, identificadores en inglés.

## Project Structure

```text
src/ppe_detection/tools/pruebas.py   # nuevo: contador y render
tests/test_tools_pruebas.py          # nuevo: parsers y render con salidas simuladas
Makefile                             # + objetivo pruebas (sin reordenar)
docs/curso/PRUEBAS.md                # regenerado por el comando
specs/095-hu-094-conteo-pruebas/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Flujo

```text
pytest --collect-only -q   ─┐
                            ├─> contar_por_archivo() ─> filas con dueño ─> Markdown
npx vitest list --json     ─┘                          (propiedad.toml)
```

### Funciones

- `count_pytest(output: str) -> dict[str, int]`: acepta `archivo.py: N` (doble quiet) y
  `archivo.py::test` (ids); ignora resúmenes y líneas vacías.
- `count_vitest(output: str) -> dict[str, int]`: parsea el JSON de `vitest list --json`
  y normaliza rutas absolutas a relativas al repositorio.
- `build_rows(pytest_counts, vitest_counts, manifest) -> list[ReportRow]`: ordena
  pytest antes que Vitest y resuelve el dueño con `ownership.owner_of`.
- `render_report(rows, generated_at) -> str`: resumen por suite, desglose por archivo y
  totales por integrante.
- `write_report(path, content)`: escribe UTF-8 con salto final.
- `collect_counts(root, skip_frontend) -> tuple[dict, dict]`: lanza los subprocesos y
  falla con un mensaje claro si falta Node.

### Salida

```markdown
## 1. Resumen

| Suite | Herramienta | Archivos | Pruebas | Comando |
|-------|-------------|---------:|--------:|---------|
| Backend | pytest | 35 | 447 | `make test` |
| Frontend | Vitest | 9 | 76 | `make frontend-test` |
| **Total** | | **44** | **523** | ... |

## 2. Desglose por archivo

| Archivo | Suite | Pruebas | Dueño |
|---|---:|---:|---|
...

## 3. Totales por integrante

| Integrante | pytest | Vitest | Total |
...
```

- El dueño se muestra con el nombre de `propiedad.toml`; si no hay patrón, «sin dueño».
- La fecha de generación se pasa como argumento para que la prueba sea determinista.

### CLI

```bash
uv run python -m ppe_detection.tools.pruebas            # imprime el resumen
uv run python -m ppe_detection.tools.pruebas --write    # regenera PRUEBAS.md
uv run python -m ppe_detection.tools.pruebas --skip-frontend
```

### Alternativas descartadas

- **Contar líneas de `pytest -q`**: obliga a ejecutar la suite; el AC pide casos
  recolectados.
- **Leer los archivos `.py` y contar `def test_`**: no cuenta parametrizaciones ni
  `@pytest.mark.parametrize`.
- **Escribir la tabla a mano otra vez**: es lo que produjo las cifras contradictorias.

## Phases

1. **Tests first**: parsers, render y escritura con salidas simuladas.
2. **Implementación**: módulo y objetivo `make pruebas`.
3. **Regeneración**: ejecutar `make pruebas-write` y revisar el diff de `PRUEBAS.md`.
4. **Cierre**: `make ownership-check`, `make check`, PR y `Closes #150`.

## Risks

- **Formato de pytest**: depende de `addopts = "-q"`; el parser acepta ids y doble quiet.
- **Vitest list**: si una versión futura cambia el JSON, la prueba con salida simulada lo
  detecta al actualizar el fixture.
- **Makefile ajeno**: el objetivo nuevo genera aviso de propiedad y revisión de Guillermo.
- **Conteo cambiante**: el informe lleva fecha y comando; no se compara contra números
  fijos.
