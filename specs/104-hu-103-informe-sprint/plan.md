# Plan — HU-103 Informe de sprint

**Branch**: `docs/104-hu-103-informe-sprint` · **Issue**: #159 · **Spec**: `spec.md`

## Enfoque

Separar el **cálculo** (módulo puro y testeable) del **informe** (documento con la foto
del sprint). El cálculo vive en `src/ppe_detection/tools/sprint.py`; el informe en
`docs/curso/M4/SPRINT.md`.

## Componentes

| Pieza | Cambio |
|---|---|
| `sprint.py` | `burndown()`, `velocity_by_person()`, `deviation()` y `SprintError` |
| `SPRINT.md` | Resumen, burndown diario, velocidad por integrante, HU abiertas |
| `tests/test_sprint.py` | 9 pruebas con datos simulados y aritmética del documento |

## Decisiones

- **Serie por día con cierres**: no se rellenan días vacíos; el documento sí los muestra
  para que la línea sea legible.
- **Sin acceso a la API en las pruebas**: el cálculo recibe la lista de cierres.
- **Fechas UTC**: GitHub devuelve `closedAt` en UTC; se advierte para no confundir el
  cierre del 28/11 con la noche del 27/11 en Colombia.

## Riesgos

- **Foto que envejece**: el documento es un corte; las pruebas validan su coherencia
  interna, no el estado vivo.
- **SP del backlog desactualizado**: la prueba de totales (100 HU/200 SP) lo detecta.

## Verificación

```bash
uv run pytest -q tests/test_sprint.py
make check
```
