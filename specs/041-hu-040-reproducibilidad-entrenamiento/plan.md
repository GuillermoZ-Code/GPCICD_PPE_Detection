# Implementation Plan: HU-040 — Guía de reproducibilidad del entrenamiento

**Branch**: `feature/041-hu-040-reproducibilidad-entrenamiento` | **Date**: 2026-11-26

**Spec**: [spec.md](spec.md)

**Input**: Issue #96 y `specs/041-hu-040-reproducibilidad-entrenamiento/spec.md`.

## Summary

Crear `docs/evaluation/reproducibilidad.md` con los pasos, versiones, hardware,
semilla, tiempos y enlaces necesarios para repetir el fine-tuning de YOLO26n y
verificar su artefacto. La guía se apoya en la evidencia existente de HU-018, la Model
Card y MLflow; no reentrena ni descarga datos.

## Technical Context

**Language/Version**: Python 3.13 para las pruebas de documentación

**Primary Dependencies**: pytest y stdlib; sin dependencias nuevas

**Storage**: Markdown versionado; pesos/datasets fuera de Git

**Testing**: pytest AAA; lectura del Markdown y aserciones de estructura

**Target Platform**: CPU / CI para la guía; GPU externa para el entrenamiento real

**Project Type**: documentación de reproducibilidad

**Constraints**: no entrenar en CI; no publicar pesos, datasets ni notebooks

**Scale/Scope**: una guía, cuatro pruebas, un run de referencia, seis clases

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red en las pruebas.
- [x] La guía documenta semilla, versiones y hardware.
- [x] Pesos y datasets fuera de Git.
- [x] No se cambia el contrato de detección.

## Project Structure

```text
docs/evaluation/
├── reproducibilidad.md     # guía nueva
├── yolo26-training.md      # evidencia del run
├── mlflow-comparacion.md   # comparación de runs
└── YOLO26.md               # evaluación de referencia
tests/
└── test_reproducibilidad.py
specs/041-hu-040-reproducibilidad-entrenamiento/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Contenido

1. Alcance y fuentes.
2. Entorno: Colab GPU y CPU de evaluación.
3. Datos, YAML, SHA256 y particiones.
4. Comandos con `uv`, rutas externas y `--config`.
5. Tiempos: ~85 min de entrenamiento y latencia de servicio.
6. MLflow: tracking, runbook y comparación.
7. Paquete: `models.lock`, SHA256 y `artifact fetch`.
8. Verificación: evaluación reproducible y métricas.
9. Límites de la reproducción.

### Pruebas

Se leen las secciones y se comprueba que aparecen versiones, semilla, hardware,
tiempo, enlaces a MLflow/modelo y que no hay secretos. No se ejecuta entrenamiento.

### Decisiones

- Se usan rutas externas genéricas para no versionar rutas personales.
- No se inventan IDs de MLflow; se enlaza el runbook y la comparación.
- Se declara que Colab/Kaggle solo son cómputo GPU.
- Se diferencia entrenamiento GPU de evaluación/servicio CPU.

## Phases

1. **Documento:** escribir la guía con la evidencia de HU-018.
2. **Pruebas:** cuatro casos de estructura, datos y seguridad.
3. **Verificación:** `make specs-check`, `make check`, `uv build`.
4. **Cierre:** PR con `Closes #96`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Rutas personales | Se usan variables de entorno y rutas genéricas |
| IDs de MLflow inventados | Se enlaza el procedimiento y la comparación |
| Entorno GPU no reproducible | Se declara en límites |
| Datos fuera de Git | Se documentan SHA256 y origen |
| Guía desactualizada | Las pruebas fallan si faltan secciones clave |

## Verification

```bash
uv run pytest tests/test_reproducibilidad.py -q
make specs-check
make check
uv build
```
