# Capacidad y velocidad real — M4-S3

> **Periodo:** 19/11/2026 → 28/11/2026 (**10 días**) · **Equipo:** 4 integrantes
> **HU:** HU-109 (#165) · **Spec:** `specs/110-hu-109-capacidad/`
> **Datos:** GitHub Issues + [`backlog.md`](../backlog.md) al **27/11/2026 22:30
> (UTC-5)**. Fechas de cierre en UTC.

## 1. Capacidad del sprint

| Concepto | Valor |
|---|---:|
| Personas | 4 |
| Días del sprint | 10 |
| Capacidad bruta | **40 persona-día** |
| SP planificados | **200** |
| SP por persona-día planificados | **5,0** |
| SP entregados al corte | **184** |
| SP por persona-día reales | **4,6** |
| Avance sobre el plan | **92 %** |

## 2. Plan frente a entregado por integrante

| Integrante | Plan (SP) | Entregado (SP) | Desviación | SP/día |
|---|---:|---:|---:|---:|
| Guillermo Zabala | 50 | 45 | -10,0 % | 4,5 |
| Eliana Cardona | 50 | 47 | -6,0 % | 4,7 |
| Hernán Estrada | 50 | 50 | 0,0 % | 5,0 |
| Jesús Riveros | 50 | 42 | -16,0 % | 4,2 |
| **Total** | **200** | **184** | **-8,0 %** | **4,6** |

- **Cálculo:** `deviation(planned, delivered)` y `capacity(delivered, people, days)`
  viven en [`sprint.py`](../../../src/ppe_detection/tools/sprint.py).
- **HU cerradas:** 93 de 100; **7 abiertas** con **16 SP** (#111, #114, #136, #144,
  #165, #166 y #167).

## 3. Desviación frente al plan 1:1

El curso estima **1 SP ≈ 1 día**. Con ese criterio, 4 personas en 10 días rinden
**40 SP**, no 200: el plan del M4 equivale a **5 veces** la capacidad 1:1 (5 SP por
persona-día).

| Escenario | SP esperados | SP reales | Lectura |
|---|---:|---:|---|
| 1:1 estricto (1 SP = 1 persona-día) | 40 | 184 | El plan no usó 1:1 |
| Plan del M4 (50 SP por persona) | 200 | 184 | 92 % de cumplimiento |

**Conclusión para calibrar Fibonacci:** la estimación del M4 es consistente a nivel de
equipo (184/200), pero **no** con la regla 1:1 del curso. Para el siguiente sprint se
debe elegir una de dos:

1. **Mantener 5 SP/persona-día** y documentarlo como supuesto del equipo (lo que ocurrió
   aquí, con agentes en paralelo).
2. **Aplicar 1:1** y reducir el alcance a ~40 SP por sprint de 10 días con 4 personas.

## 4. Riesgos y límites

| Riesgo | Impacto | Mitigación |
|---|---|---|
| 16 SP abiertos | Cerrar en 92 % | Priorizar #111 y #114 (Eliana) y #136/#144 (Guillermo) |
| #166 (5 SP) depende del Droplet | La capacidad real cae a 179 SP si no se hace | Declararlo en la sustentación |
| Medición en UTC | Un cierre del 28/11 es la noche del 27/11 local | Se advierte en el informe |
| Datos de una sola foto | No captura trabajo en curso | Recalcular al cierre con `make pruebas` |

## 5. Verificación

```bash
uv run pytest -q tests/test_capacidad.py
make check
```
