# ADR 0002 — Dataset `51ddhesh/PPE_Detection`

- **Fecha:** 2026-10-31
- **Estado:** Aceptada con riesgos documentados
- **Decisores:** Grupo 4

## Contexto

El backlog oficial referencia el dataset
[`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection)
para las seis clases de EPP. Se verificó su contenido y sus metadatos.

## Decisión

Usar `51ddhesh/PPE_Detection` como dataset de entrenamiento y evaluación.

### Hechos verificados

- **6 clases:** Helmet, Vest, Gloves, Goggles, Mask, Safety Shoe.
- **16.014 objetos anotados**; el número de imágenes no está publicado.
- Un solo archivo **`PPE.zip` de 668 MB**.
- Estructura **YOLO** (`train/valid/test`, `data.yaml`).
- Licencia declarada: **CC-BY-4.0** (requiere atribución).
- La tarjeta **no declara la fuente original** y conserva el placeholder
  `<your-username>/ppe-detection`.
- No menciona consentimiento de rostros ni tratamiento de datos personales.
- **No existe clase `person` ni `no-EPP`**.

## Alternativas consideradas

- **COCO/OpenImages con subconjunto EPP:** más volumen, pero etiquetas heterogéneas y
  mayor esfuerzo de curaduría.
- **Dataset propio:** control total, pero sin tiempo ni capacidad de anotación en el
  plazo del curso.

## Consecuencias

- El sistema reporta **qué EPP aparecen**, no si un trabajador cumple o incumple.
- La ausencia de detecciones **no** prueba ausencia real de EPP.
- Se debe atribuir CC-BY-4.0 y documentar la procedencia desconocida.
- El dataset y los pesos se mantienen fuera de Git; se documenta su SHA256.
- La partición de evaluación se protege y se documenta en HU-008.
- La Model Card (Hernán) debe declarar estas limitaciones y sesgos.

> **Insumo para el Cap. 1/4 (responsable: Hernán); el repo registra la decisión técnica.**

## Referencias

- `CONSTITUTION.md` §7.
- `docs/curso/backlog.md` (HU-002, HU-008).
- Tarjeta del dataset en Hugging Face.
