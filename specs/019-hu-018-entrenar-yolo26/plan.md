# Implementation Plan: HU-018 — Entrenar YOLO26n y YOLO26s

**Branch**: `feature/019-hu-018-entrenar-yolo26` | **Date**: 2026-11-21

**Spec**: [spec.md](spec.md)

**Input**: Issue #74 y `specs/019-hu-018-entrenar-yolo26/spec.md`.

## Summary

Registrar el entrenamiento de YOLO26n ya ejecutado en Colab y dejar preparada la
decisión sobre YOLO26s. El entregable es documental: manifiesto, métricas, curvas y
SHA256; los pesos viven fuera de Git.

## Technical Context

**Entorno de entrenamiento**: Colab pago, Python 3.13.16, Ultralytics 8.4.216,
torch 2.15.0, GPU.

**Datos**: `data_colab.yaml` y `data_eval_colab.yaml`; 7.658 train, 2.188 valid,
1.095 test.

**Configuración**: `yolo26n.pt`, 100 épocas, `imgsz=640`, `batch=-1`, `seed=42`,
`device=0`, backup cada 5 épocas.

**Evidencia**: `run_manifest.json`, `eval/summary.json`, `eval/summary.md`, curvas,
`results.csv` y ZIP original.

**Constraints**: pesos fuera de Git; no se cambia el modelo productivo; no se
modifica `train.py` en esta HU.

## Constitution Check

- [x] `uv` y script versionado; no se usan notebooks.
- [x] Pesos fuera de Git.
- [x] Se registran semilla, `imgsz`, dataset y versión.
- [x] La evidencia permite reproducir el run.
- [x] No se cambia el contrato de detecciones.

## Project Structure

```text
docs/evaluation/yolo26-training.md          # informe de entrenamiento
specs/019-hu-018-entrenar-yolo26/
├── spec.md
├── plan.md
└── tasks.md
```

## Estado de los runs

| Run | Estado | Evidencia |
|---|---|---|
| YOLO26n | Completado | `dist/analisis/yolo26n/` |
| YOLO26s | Pendiente de decisión | Latencia del spike: p50 514 ms |

## Decisión sobre YOLO26s

No se ejecutó todavía. El spike mostró que `s` es ~3,2× más lento que `n` y no es
viable para CPU. Se entrenará solo si:

1. El equipo exige el AC de dos modelos, o
2. `n` no alcanza el rendimiento esperado en una clase crítica.

## Phases

1. **Evidencia**: verificar manifiesto, SHA256, curvas y métricas de `n`.
2. **Informe**: escribir `docs/evaluation/yolo26-training.md`.
3. **Decisión**: documentar por qué `s` sigue pendiente y qué condición lo activa.
4. **Cierre**: cuando #173 esté fusionada, abrir PR con `Closes #74`; si `s` no se
   entrena, solicitar a Jesús el ajuste del AC o dejar la issue parcial.

## Risks

- **AC-01 incompleto**: solo `n` está entrenado; la issue no se puede cerrar como
  completa sin decisión de Jesús sobre `s`.
- **Evidencia cruda inconsistente**: `args.yaml` y `results.csv` no coinciden con el
  manifiesto; se conservan en `raw/` y se advierte en el informe.
- **safety_shoe**: recall 0; el promedio no debe ocultar la debilidad.
- **Specs/ es de Jesús**: la spec genera aviso de propiedad.
