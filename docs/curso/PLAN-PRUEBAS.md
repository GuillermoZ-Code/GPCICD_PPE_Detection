# Plan de pruebas — llegar a 1.200 en la entrega del M4

> **Requisito del curso:** **mínimo 1.200 pruebas unitarias** para el M4 (indicación del
> docente). No es un techo.
>
> **Para qué sirve este archivo:** cada integrante (y el agente que lo asiste) lee su
> fila, aporta las pruebas de sus HU y demuestra el avance con el contador del
> repositorio. No se reparte por «escribir muchas pruebas», sino por **AC y FR sin
> cubrir**.

## 1. Punto de partida y objetivo

| Campo | Valor |
|---|---|
| **Punto de partida** | **533** (457 pytest + 76 Vitest) |
| **Objetivo** | **1.200** |
| **Brecha** | **667** |
| **Fecha de medición** | 2026-11-23 |
| **Medición actual (2026-11-27)** | **1.168** (1.067 pytest + 101 Vitest) |
| **Brecha actual** | **32** |
| **Comando** | `make pruebas-write` |

El punto de partida es el conteo real del repositorio, no una cifra congelada: lo
produce `make pruebas` (HU-094) y queda escrito en
[`PRUEBAS.md`](PRUEBAS.md), que es generado y no se edita a mano.

## 2. Reparto por integrante

| Integrante | Plan M4 | HU cerradas | Restante planificado | Ajuste de cierre | Total a aportar |
|---|---:|---:|---:|---:|---:|
| Guillermo Zabala | 192 | 0 | 192 | 0 | 192 |
| Hernán Estrada | 192 | 80 | 112 | 0 | 112 |
| Eliana Cardona | 192 | 0 | 192 | 0 | 192 |
| Jesús Riveros | 192 | 24 | 168 | +3 | 171 |
| **Total** | **768** | **104** | **664** | **+3** | **667** |

- **HU cerradas (104 pruebas planificadas):** HU-016, HU-017, HU-019, HU-020, HU-021,
  HU-023, HU-025, HU-026, HU-033, HU-091, HU-094, HU-095, HU-105 y HU-107.
- **Ajuste de cierre (+3, HU-113):** algunas HU entregaron más pruebas de las
  planificadas y otras menos; con el ajuste, `533 + 667 = 1.200`.
- El reparto por persona es la suma de las pruebas objetivo de sus HU abiertas en
  [`M4/ASIGNACION.md`](M4/ASIGNACION.md).

## 3. Cómo se cuenta

```bash
make pruebas        # imprime el resumen
make pruebas-write  # regenera docs/curso/PRUEBAS.md
```

- **pytest:** `uv run pytest --collect-only` (casos recolectados, sin ejecutar la suite).
- **Vitest:** `npx vitest list --json` desde `frontend/`.
- El informe incluye el desglose por archivo con su dueño y los totales por integrante.

## 4. Reglas del reparto

1. Cada HU aporta las pruebas de su tabla de `ASIGNACION.md`, con `AC-0N` en el nombre o
   docstring.
2. Test-first: la prueba se escribe antes de la implementación y debe fallar primero.
3. Una prueba unitaria no depende de GPU, dataset completo ni red.
4. Si una HU entrega menos pruebas de las planificadas, el faltante se compensa en la
   siguiente HU del mismo integrante.
5. El conteo se actualiza con `make pruebas-write` al cerrar cada ola; el cambio de
   baseline se registra en el historial.
6. Las HU de documentación aportan pruebas estructurales; no se descuentan del reparto.

## 5. Historial de correcciones

| Fecha | Baseline | Problema | Corrección |
|---|---:|---|---|
| 13/11/2026 | 375 pytest + 76 Vitest = 451 | primer inventario del M3 | — |
| 21/11/2026 | 451 congelado | se planificaron 749 nuevas sin contar lo ya fusionado del M4 | el plan nace desactualizado |
| 23/11/2026 | 451 vs. 529 reales | convivían 375, 425, 451 y 515 en distintos documentos | se adopta el conteo real con `make pruebas` (HU-094) |
| 23/11/2026 | **533** | baseline tras HU-094 y esta HU | plan de **667** pruebas nuevas |

## 6. Verificación

```bash
uv run pytest tests/test_plan_pruebas.py
make check
make ownership-check
```

- Las pruebas del plan comprueban la aritmética, el reparto por integrante, el comando y
  el historial.
- `make ownership-check` no debe reportar bloqueos.

## 7. Instrucción para los agentes

- Lee tu fila y tus HU abiertas en `M4/ASIGNACION.md`; no inventes pruebas fuera de tus
  AC.
- Si un caso no se puede reproducir en CPU, sustitúyelo por uno equivalente con
  `FakeDetector` o datos sintéticos y anótalo en la PR.
- No edites `PRUEBAS.md` a mano: ejecuta `make pruebas-write`.
- Si detectas una cifra contradictoria, avisa antes de continuar.
