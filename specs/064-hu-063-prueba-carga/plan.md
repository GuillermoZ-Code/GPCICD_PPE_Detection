# Implementation Plan: HU-063 — Prueba de carga ligera e informe de capacidad

**Branch**: `feature/064-hu-063-prueba-carga` | **Date**: 2026-11-27

**Spec**: [spec.md](./spec.md)

**Input**: Issue #119 y `specs/064-hu-063-prueba-carga/spec.md`.

## Summary

Versionar un instrumento de carga con concurrencia configurable sobre `httpx`, un
informe reproducible con p50/p95, errores y CPU/RAM, y una recomendación explícita de
tamaño de Droplet y workers. La medición versionada es una validación local del
instrumento; la medición real queda pendiente y se atribuye a Guillermo.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `httpx` (o `httpx2` como alias en entornos sin extras),
`psutil` con aproximación estándar de respaldo, `argparse`, `concurrent.futures`, `threading`

**Testing**: pytest con cliente, reloj y muestreo inyectables; sin red, GPU ni modelo

**Target Platform**: estación local y Droplet CPU

**Project Type**: herramienta de operación + documento

**Constraints**: sin dependencias nuevas, sin secretos versionados, sin afirmar medición
real del Droplet, WIP 1, una HU por PR

**Scale/Scope**: 1 script, 1 informe, 16 pruebas

## Constitution Check

- [x] No se agregan dependencias: `httpx`/`httpx2` y `psutil` ya están en `uv.lock`.
- [x] Las pruebas SON deterministas y no abren conexiones ni cargan pesos.
- [x] Ruff, formato, `ty`, pytest, specs y propiedad se mantienen en verde.
- [x] No se versionan credenciales ni rutas personales.
- [x] No se cambia el despliegue ni se debilitan pruebas existentes.
- [x] El informe distingue validación local de medición real.

## Project Structure

```text
src/ppe_detection/tools/load_test.py  # CLI y lógica de carga
tests/test_load_test.py               # 16 pruebas AC-01/AC-02/AC-03
docs/operacion/capacidad.md           # informe de la validación local
specs/064-hu-063-prueba-carga/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### CLI

`--url`, `--path`, `--requests`, `--concurrency`, `--timeout`, `--image`,
`--sample-interval`, `--auth-env`, `--label`, `--output`. La validación ocurre antes de
construir el cliente. `PPE_LOAD_AUTH` aporta `usuario:clave` sin exponerla en la línea de
comandos ni en el informe.

### Ejecución

`run_load` recibe un cliente inyectable, un reloj inyectable y un muestreador inyectable.
Un `ThreadPoolExecutor(max_workers=concurrency)` envía exactamente `requests` llamadas
`client.request(...)`. Un hilo muestrea CPU/RAM mientras corre el lote; se agrega una
muestra inicial para que el informe siempre tenga datos.

### Métricas

Percentil nearest-rank: `ceil(q·n)` sobre la lista ordenada. `throughput = total / elapsed`.
Los errores se normalizan como `HTTP <status>` o `<Tipo>: <mensaje>` y se agrupan.

### Informe y recomendación

`render_report` escribe configuración, resultados, errores, CPU/RAM, recomendación,
comandos de reproducción y pendiente real. `recommend` usa reglas deterministas:

| Condición | Droplet | Workers |
|---|---|---|
| Error > 5 % | `s-2vcpu-4gb` | 2, corregir errores antes de escalar |
| p95 ≤ 200 ms, ≥ 15 req/s, CPU < 70 % | `s-1vcpu-2gb` | 2 |
| p95 ≤ 500 ms, CPU < 85 % | `s-2vcpu-4gb` | 4 |
| En otro caso | `s-4vcpu-8gb` | 6, repetir medición |

## Phases

1. **Spec:** spec, plan, tasks y WIP en el tablero.
2. **Tests:** 16 pruebas test-first; ejecutar fase roja.
3. **Implementación:** `load_test.py` y generación del informe local.
4. **Verificación:** pytest, Ruff, formato, `ty`, specs, propiedad, PR y CI.

## Risks

| Riesgo | Mitigación |
|---|---|
| `httpx` ausente en CI | alias a `httpx2` y cliente inyectable en pruebas |
| `psutil` ausente | muestreo aproximado con librería estándar |
| Medición falsificada | el informe declara explícitamente que es local |
| Concurrencia no efectiva | el executor recibe `max_workers` y hay prueba dedicada |
| Secretos en el informe | credenciales solo por entorno y nunca se renderizan |

## Verification

```bash
uv run pytest tests/test_load_test.py -q
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run python -m ppe_detection.tools.check_specs --check
uv run python -m ppe_detection.tools.ownership --base origin/develop
```
