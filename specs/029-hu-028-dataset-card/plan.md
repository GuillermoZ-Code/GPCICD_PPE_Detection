# Implementation Plan: HU-028 — Dataset Card y atribución CC-BY-4.0

**Branch**: `feature/029-hu-028-dataset-card` | **Date**: 2026-11-26

**Spec**: [spec.md](spec.md)

**Input**: Issue #84 y `specs/029-hu-028-dataset-card/spec.md`.

## Summary

Crear `docs/dataset/README.md` como Dataset Card del corpus PPE Detection. La ficha
resume origen, licencia, clases, particiones, limpieza, riesgos y un bloque de
atribución reutilizable. Se apoya en el EDA y el ADR 0002 ya existentes; no descarga
ni redistribuye datos.

## Technical Context

**Language/Version**: Python 3.13 para las pruebas de documentación

**Primary Dependencies**: pytest y stdlib; sin dependencias nuevas

**Storage**: Markdown versionado; sin datos ni imágenes

**Testing**: pytest AAA; lectura del Markdown y aserciones de contenido

**Target Platform**: CPU / CI

**Project Type**: documentación de datos

**Constraints**: no publicar imágenes, no inventar procedencia, no cambiar el dataset

**Scale/Scope**: una ficha, cuatro pruebas, seis clases, tres particiones

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Pruebas en `tests/` y patrón AAA.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin GPU, dataset completo ni red en las pruebas.
- [x] La ficha declara licencia y límites.
- [x] No se versionan datos ni imágenes.
- [x] No se cambia el contrato de detección.

## Project Structure

```text
docs/dataset/
├── EDA.md                 # evidencia existente
└── README.md              # Dataset Card (nuevo)
tests/
└── test_dataset_card.py
specs/029-hu-028-dataset-card/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Contenido

La ficha se divide en:

1. Identidad y licencia, incluido SHA-256 del ZIP.
2. Clases y orden canónico.
3. Particiones originales y limpias.
4. Limpieza: duplicados, conflictos, líneas inválidas, vacías y fuga.
5. Atribución reutilizable con URL y licencia.
6. Limitaciones: fuente, consentimiento, ausencia de `person`/`no-EPP`, desbalance.
7. Evidencia enlazada.

### Pruebas

Se lee el Markdown y se verifica que los datos clave estén presentes, que los riesgos
no se omitan y que el bloque de atribución sea copiable. No se prueba el dataset
físico ni se descargan imágenes.

### Decisiones

- No se afirma que la fuente original sea conocida.
- Se documentan las dos variantes de split con una imagen de diferencia.
- La atribución incluye las modificaciones del proyecto.
- La ficha enlaza al EDA, al ADR 0002 y a la Model Card.

## Phases

1. **Documento:** escribir la Dataset Card.
2. **Pruebas:** cuatro casos de contenido y atribución.
3. **Verificación:** `make specs-check`, `make check`, `uv build`.
4. **Cierre:** PR con `Closes #84`.

## Risks

| Riesgo | Mitigación |
|---|---|
| Inventar procedencia | Se declara la ausencia de fuente original |
| Ocultar riesgo de consentimiento | Sección explícita de limitaciones |
| Números inconsistentes | Se enlazan EDA y ADR y se documentan las variantes |
| Publicar imágenes | La ficha solo contiene texto y conteos |
| Atribución difícil de reutilizar | Bloque copiable con URL y licencia |

## Verification

```bash
uv run pytest tests/test_dataset_card.py -q
make specs-check
make check
uv build
```
