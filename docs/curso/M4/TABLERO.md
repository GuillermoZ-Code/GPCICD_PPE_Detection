# Tablero del M4 — GitHub Project #1

> **URL:** <https://github.com/users/GuillermoZ-Code/projects/1>
> **Dueño:** Jesús (`jesusriverosUAO`) · **HU:** HU-090 (#146) · **Spec:** `specs/091-hu-090-tablero/`

El tablero reúne las **113 HU** del proyecto (13 del M3 y 100 del M4) y es la evidencia
operativa del sprint. La fuente de verdad de los valores es
[`backlog.md`](../backlog.md); los items se rellenaron una vez con la API GraphQL.

## 1. Campos

| Campo | Tipo | Regla |
|---|---|---|
| `Estimate` | Número | Story Points: 1, 2, 3, 5 u 8 |
| `Size` | Selección | Derivado del SP (tabla de abajo) |
| `Priority` | Selección | `P0`, `P1` o `P2` |
| `Ola` | Selección | 1, 2 o 3 |
| `Épica` | Selección | `ep-05` a `ep-15` |

### SP → Size

| **SP** | **Size** |
|---|---|
| 1 | XS |
| 2 | S |
| 3 | M |
| 5 | L |
| 8 | XL |

Las HU del M3 no llevan `Ola` ni `Épica`; se excluyen de la suma del M4.

## 2. Vistas

| Vista | Layout | Uso |
|---|---|---|
| **Por integrante** | Tabla | Agrupar por *Assignees* y sumar `Estimate` (50 SP por persona) |
| **Por ola** | Board | Agrupar por `Ola`: ola 1, ola 2 y ola 3 |
| **Por épica** | Board | Agrupar por `Épica`: `ep-05` a `ep-15` |
| Backlog | Board | Agrupar por `Status` (Backlog → Done) |
| Priority board | Board | Agrupar por `Priority` |
| Team items | Tabla | Vista de trabajo diario |
| Roadmap | Roadmap | Fechas de inicio y objetivo |
| My items | Tabla | Filtro por la persona que consulta |

La API crea la vista, pero **no expone el agrupamiento**: en la UI se elige
*Group by* → `Assignees`, `Ola` o `Épica` respectivamente, y se guarda.

## 3. Burndown

GitHub Projects **no tiene un layout de burndown**: solo `TABLE`, `BOARD` y `ROADMAP`,
y los gráficos viven en *Insights* sin mutación pública. El paso manual es:

1. Abrir el proyecto → pestaña **Insights** → **New chart**.
2. Elegir **Burn up** (el más cercano al burndown) y el milestone `M4-S3`.
3. Guardar el gráfico como «Burndown M4» y capturarlo para el informe de sprint
   (HU-103).

## 4. Verificación

```bash
uv run pytest -q tests/test_board_m4.py   # datos del backlog y esta guía
```

La prueba no consulta GitHub: valida que el origen del tablero (100 HU, 50 SP por
integrante, Fibonacci, olas, épicas y prioridades) siga cuadrando.
