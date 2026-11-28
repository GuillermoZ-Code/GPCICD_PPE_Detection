# Plan — HU-109 Capacidad y velocidad real

**Branch**: `docs/110-hu-109-capacidad` · **Issue**: #165 · **Spec**: `spec.md`

## Enfoque

Añadir `capacity()` al módulo puro `sprint.py` y documentar la comparación entre el plan
del M4 y lo entregado, con la regla 1:1 del curso como referencia.

## Componentes

| Pieza | Cambio |
|---|---|
| `sprint.py` | `capacity()`: SP por persona-día |
| `CAPACIDAD.md` | Capacidad, tabla por integrante, desviación y lectura |
| `tests/test_capacidad.py` | 8 pruebas del cálculo y de la tabla |

## Decisiones

- **Capacidad bruta**: 4 personas × 10 días = 40 persona-día; no se descuentan
  festivos.
- **Plan 1:1**: se muestra el contraste (40 SP vs 200 SP) en lugar de ocultarlo.
- **Desviación con signo**: negativa cuando falta, positiva cuando se supera.

## Riesgos

- **Foto que envejece**: 16 SP abiertos al corte; al cerrar #111/#114/#136/#144 el
  entregado sube a 200.
- **Datos en UTC**: se advierte en el documento.

## Verificación

```bash
uv run pytest -q tests/test_capacidad.py
make check
```
