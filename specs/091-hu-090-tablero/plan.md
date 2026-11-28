# Plan — HU-090 Tablero del M4

**Branch**: `docs/091-hu-090-tablero` · **Issue**: #146 · **Spec**: `spec.md`

## Enfoque

El entregable es el **GitHub Project #1**, no código de producción. El trabajo tiene dos
partes:

1. **Configuración del tablero** (hecha con la API GraphQL):
   - `Estimate` (número) con el SP de cada HU.
   - `Size` (XS–XL) derivado del SP.
   - `Priority` (P0–P2) desde el backlog y los labels `must-have`/`should-have`.
   - `Ola` (1–3) y `Épica` (`ep-05`…`ep-15`) desde el backlog.
   - Vistas `Por integrante`, `Por ola` y `Por épica` con `createProjectV2View`.
2. **Verificación reproducible** (sin red): `tests/test_board_m4.py` valida el backlog
   que alimenta el tablero — 100 HU del M4, 50 SP por integrante, estimaciones
   Fibonacci, olas, épicas y prioridades.

## Componentes

| Pieza | Cambio |
|---|---|
| Project #1 | Campos completos en los 113 items + 3 vistas |
| `docs/curso/M4/TABLERO.md` | Guía de campos, vistas y burndown manual |
| `tests/test_board_m4.py` | 12 pruebas de los datos y de la guía |

## Decisiones

- **Size = f(SP)**: 1→XS, 2→S, 3→M, 5→L, 8→XL. Evita dos fuentes de verdad.
- **Burndown**: GitHub Projects solo ofrece TABLE, BOARD y ROADMAP; el burndown real se
  arma en *Insights* (Burn up) y se documenta como paso manual. No hay mutación para
  crear gráficos.
- **Sin tool nuevo en `src/`**: el llenado se hizo una vez con GraphQL; la prueba valida
  el origen (backlog), no la API.

## Riesgos

- **Reagrupación de vistas**: la API no expone el agrupamiento; se ajusta en la UI.
- **Drift del tablero**: si el backlog cambia, la prueba de sumas avisa.

## Verificación

```bash
uv run pytest -q tests/test_board_m4.py
make check
```
