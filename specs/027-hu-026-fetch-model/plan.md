# Implementation Plan: HU-026 — Descarga y verificación del modelo

**Branch**: `feature/027-hu-026-fetch-model` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #82 y `specs/027-hu-026-fetch-model/spec.md`.

## Summary

Añadir `ppe_detection.detection.artifact`, un descargador con verificación SHA256 que
lee `models.lock`, escribe en un archivo temporal y solo reemplaza el destino cuando
el hash coincide. Expone una CLI `fetch`.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `urllib.request`, `hashlib`, `tomllib`; sin dependencias
nuevas

**Storage**: `models.lock` y archivo destino; pesos fuera de Git

**Testing**: pytest con `tmp_path`, `file://` y `urlopen` simulado; sin red

**Target Platform**: CPU / CI / contenedor

**Project Type**: biblioteca + CLI de despliegue

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Test-first: cada AC tiene una prueba que lo referencia.
- [x] No se cambia el contrato de detecciones.

## Project Structure

```text
src/ppe_detection/detection/
└── artifact.py                     # fetch, verificación y CLI
tests/
└── test_artifact_fetch.py          # 8 pruebas de AC-01/02/03
specs/027-hu-026-fetch-model/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### API

- `ArtifactError(RuntimeError)`.
- `fetch_artifact(manifest, destination, timeout=30.0) -> ArtifactFetchResult`.
- `main(argv=None) -> int` para la CLI.
- `DEFAULT_DESTINATION = Path("artifacts/models/best.pt")`.

### Flujo

1. Cargar el manifiesto (`load_model_manifest`).
2. Resolver URL (`file`, `http`, `https`).
3. Descargar a `<destination>.part`.
4. Calcular SHA256 y comparar con el manifiesto.
5. Si coincide, `Path.replace(destination)`.
6. Si falla, borrar `.part` y lanzar `ArtifactError`.

### CLI

```bash
python -m ppe_detection.detection.artifact fetch \
  --manifest models.lock \
  --output artifacts/models/best.pt
```

## Risks

- **file:// en Windows/Linux**: usar `url2pathname` para no hardcodear separadores.
- **URLs remotas**: timeout y limpieza del temporal.
- **Destino existente**: no reemplazar hasta verificar.
- **Specs/ es de Jesús**: la spec genera aviso de propiedad.
