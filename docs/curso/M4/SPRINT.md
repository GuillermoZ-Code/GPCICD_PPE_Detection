# Informe de sprint — M4-S3

> **Periodo:** 19/11/2026 → 28/11/2026 · **Dueño del backlog:** Jesús (`jesusriverosUAO`)
> **HU:** HU-103 (#159) · **Spec:** `specs/104-hu-103-informe-sprint/`
> **Datos:** exportados de GitHub Issues + [`backlog.md`](../backlog.md) el **27/11/2026
> 22:20 (UTC-5)**. Las fechas de la tabla están en **UTC**: las filas del 28/11
> corresponden a la noche del 27/11 en Colombia (UTC-5).

## 1. Resumen

| Métrica | Plan | Real | Avance |
|---|---:|---:|---:|
| HU del M4 | 100 | 91 cerradas | 91 % |
| SP del M4 | 200 | 180 cerrados | 90 % |
| HU abiertas | — | 9 | 20 SP |
| Pruebas unitarias | **≥ 1.200** | 1.148 | 95,7 % |
| Release v1.0.0 | `develop → main` + tag | merge en `main`; tag pendiente | — |

## 2. Burndown de SP

| Fecha | HU cerradas | SP cerrados | SP restantes |
|---|---:|---:|---:|
| 19/11 | 0 | 0 | 200 |
| 20/11 | 0 | 0 | 200 |
| 21/11 | 0 | 0 | 200 |
| 22/11 | 0 | 0 | 200 |
| 23/11 | 0 | 0 | 200 |
| 24/11 | 27 | 60 | 140 |
| 25/11 | 10 | 19 | 121 |
| 26/11 | 5 | 8 | 113 |
| 27/11 | 39 | 75 | 38 |
| 28/11 | 10 | 18 | 20 |

- **Velocidad media:** 180 SP / 9 días = **20 SP/día** de equipo.
- **Pico:** 75 SP el 27/11 (cierre de las olas 2 y 3).
- **Restante:** 20 SP en 9 HU (tabla de la sección 4).

## 3. Velocidad por integrante

| Integrante | Plan M4 | SP cerrados | HU cerradas |
|---|---:|---:|---:|
| Guillermo Zabala | 50 | 45 | — |
| Eliana Cardona | 50 | 47 | — |
| Hernán Estrada | 50 | 50 | — |
| Jesús Riveros | 50 | 38 | — |
| **Total** | **200** | **180** | **91** |

La suma planificada es 50 SP por integrante con el reparto de
[`ASIGNACION.md`](ASIGNACION.md). El detalle de la desviación y la capacidad está en
[`CAPACIDAD.md`](CAPACIDAD.md) (HU-109).

## 4. HU abiertas al corte

| HU | Issue | SP | Dueño |
|---|---|---:|---|
| HU-055 | #111 | 2 | Eliana |
| HU-058 | #114 | 1 | Eliana |
| HU-080 | #136 | 2 | Guillermo |
| HU-088 | #144 | 3 | Guillermo |
| HU-090 | #146 | 2 | Jesús |
| HU-103 | #159 | 2 | Jesús |
| HU-109 | #165 | 1 | Jesús |
| HU-110 | #166 | 5 | Jesús |
| HU-111 | #167 | 2 | Jesús |
| **Total** | | **20** | |

## 5. Cómo se generó

1. Exportar del tablero las 100 HU del milestone `M4-S3` con `state`, `closedAt`,
   `assignees` y el SP de `backlog.md`.
2. Agrupar los cierres por día UTC y aplicar
   [`burndown()`](../../../src/ppe_detection/tools/sprint.py), que resta los SP
   cerrados al total comprometido.
3. Calcular la velocidad con `velocity_by_person()` y la desviación con `deviation()`.
4. Las pruebas de `tests/test_sprint.py` reproducen el cálculo con datos simulados y
   comprueban la aritmética de esta tabla.

## 6. Riesgos del cierre

| Riesgo | Impacto | Mitigación |
|---|---|---|
| 20 SP abiertos | Release sin el 100 % de las HU | Cerrar las 9 HU el 28/11 antes de la sustentación |
| 1.148 pruebas (< 1.200) | Requisito del M4 incompleto | Objetivos de las 9 HU abiertas (+76) y margen del frente de cierre |
| Tag v1.0.0 pendiente | Entrega sin release formal | Crear el tag sobre el merge de `main` al cerrar las HU |
| #166 requiere el Droplet | 5 SP en riesgo | Ejecutarlo solo si hay acceso SSH; si no, declararlo |
