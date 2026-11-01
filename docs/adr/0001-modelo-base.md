# ADR 0001 — Modelo base: detector especializado nivel 3

- **Fecha:** 2026-10-31
- **Estado:** Aceptada
- **Decisores:** Grupo 4

## Contexto

El sistema debe detectar seis categorías de EPP en imágenes, con inferencia local en
CPU y un objetivo de latencia menor a 100 ms. El dataset es pequeño frente a los
corpus de los modelos de frontera y las clases son fijas.

## Decisión

Usar un **detector de objetos especializado de nivel 3**, candidato **Ultralytics YOLO
en variante nano o small**, con fine-tuning sobre el dataset y exportación del
artefacto fuera de Git. La variante exacta, la versión de Ultralytics y la
compatibilidad con Python 3.13 + PyTorch CPU se confirman en **SPI-01**.

No se usa un LLM/VLM en el camino de inferencia.

### Jerarquía de tres niveles

| Nivel | Enfoque | Descartado porque |
|-------|---------|-------------------|
| 1 — Frontera | LLM/VLM general | Latencia y costo altos; no requiere razonamiento abierto. |
| 2 — Gama media | Detector mediano | Más latencia en CPU; sobredimensionado para 6 clases. |
| 3 — Especializado | YOLO nano/small | **Elegido:** local, CPU, <100 ms objetivo, AGPL compatible. |

## Alternativas consideradas

- **LLM/VLM de frontera:** buena generalización, pero latencia, costo y falta de
  determinismo; innecesario para detección acotada.
- **Detector mediano (YOLO medium/large):** mayor precisión potencial, pero no cumple
  el objetivo de latencia en CPU.
- **Modelo clásico (HOG/SVM):** menor costo, pero rendimiento insuficiente en escenas
  industriales.

## Consecuencias

- El artefacto debe versionarse y verificarse por SHA256; no se versiona en Git.
- La inferencia registra versión, semilla, tamaño de imagen y umbrales.
- La evaluación reporta mAP, precision, recall y F1 por clase.
- Si SPI-01 no confirma compatibilidad con Python 3.13 + torch CPU, se ajusta la
  variante o la versión de Python con un nuevo ADR.

> **Insumo para el Cap. 1/4 (responsable: Hernán); el repo registra la decisión técnica.**

## Referencias

- `CONSTITUTION.md` §4 y §7.
- `docs/curso/backlog.md` (HU-002, SPI-01).
- Ultralytics YOLO — licencia AGPL-3.0.
