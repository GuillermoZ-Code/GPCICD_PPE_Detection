# Implementation Plan: HU-025 — Manifiesto canónico del modelo

**Branch**: `feature/026-hu-025-models-lock` | **Date**: 2026-11-21

**Spec**: [spec.md](spec.md)

**Input**: Issue #81 y `specs/026-hu-025-models-lock/spec.md`.

## Summary

Añadir `models.lock` como manifiesto TOML del artefacto y un cargador en
`detector_config.py`. La identidad que ya consumen REST, gRPC y `/health` usará el
manifiesto cuando no haya overrides explícitos en el entorno, de modo que la versión,
el SHA256 y la referencia `sha256:<hash>` sean las mismas en `/health` y MLflow.

No se descarga ni se copia el modelo. HU-026 se encargará de la descarga y la
verificación del archivo.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: `tomllib` (biblioteca estándar); sin dependencias nuevas

**Storage**: `models.lock` versionado; pesos fuera de Git

**Testing**: pytest con AAA, `tmp_path` y `monkeypatch`; sin red, GPU ni dataset

**Target Platform**: CPU

**Project Type**: biblioteca + API REST + gRPC + tracking

**Constraints**: no copiar pesos; no cambiar el contrato de detecciones; no tocar
`Dockerfile` ni `compose.yml` en esta HU

**Scale/Scope**: un manifiesto por despliegue; una identidad por app/servidor

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Test-first: cada AC tiene una prueba con `AC-0N` en el nombre o docstring.
- [x] Contract-first: se conserva `ImageData → list[Detection]`.
- [x] Sin LLM en inferencia.

## Project Structure

```text
models.lock                         # manifiesto canónico (nuevo)
src/ppe_detection/
└── detector_config.py              # ModelManifest, cargador y precedencia
tests/
├── test_model_manifest.py          # pruebas nuevas de AC-01/02/03
└── test_model_version.py           # aislamiento del manifiesto en pruebas previas
specs/026-hu-025-models-lock/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Formato de `models.lock`

```toml
name = "ppe-detection"
version = "yolo11s-clean"
sha256 = "E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959"
url = "file:///models/best.pt"
```

- `name`, `version`, `sha256` y `url` son obligatorios y no vacíos.
- El SHA256 se normaliza a mayúsculas.
- La URL puede ser local o remota; esta HU no la descarga.

### Precedencia de identidad

1. `PPE_MODEL_SHA256` explícito (se valida).
2. SHA calculado del archivo si `PPE_MODEL_PATH` existe.
3. SHA del manifiesto.
4. Sin SHA.

Para la versión:

1. `PPE_MODEL_VERSION` explícito.
2. `version` del manifiesto.
3. Nombre del archivo de `PPE_MODEL_PATH`.
4. `unknown`.

Para el artefacto:

1. `PPE_MODEL_PATH` explícito.
2. `url` del manifiesto.
3. `None`.

### API del módulo

- `ModelManifest`: dataclass inmutable con `name`, `version`, `sha256`, `url`.
- `ModelManifestError`: error de configuración del manifiesto.
- `load_model_manifest(path=None)`: carga y valida; `path` explícito debe existir.
- `DEFAULT_MANIFEST_PATH`: `models.lock` en la raíz del repositorio.
- `PPE_MODEL_MANIFEST`: ruta alternativa; si se define y no existe, falla.
- `default_model_identity()` y `default_model_version()`: integran el manifiesto sin
  romper los overrides actuales.

## Phases

1. **Tests first**: manifiesto válido, campos faltantes, SHA inválido, TOML inválido,
   ruta explícita ausente, precedencia, `/health` y MLflow.
2. **Implementación**: `ModelManifest`, cargador y precedencia en
   `detector_config.py`; `models.lock`.
3. **Compatibilidad**: aislar el manifiesto en las pruebas existentes que asumen que
   no hay ninguno.
4. **Cierre**: `make ownership-check`, `make check`, actualizar `PRUEBAS.md` (lo hace
   el dueño del conteo) y abrir PR con la plantilla UAO.

## Risks

- **Manifiesto en el contenedor**: el `Dockerfile` no copia `models.lock`; la
  integración con Docker se coordina en HU-024/HU-026 o se monta el archivo. Esta HU
  no modifica el Dockerfile.
- **Specs/ es de Jesús**: crear la spec genera un aviso de propiedad, no un bloqueo;
  el PR necesita su revisión.
- **SHA real**: el manifiesto usa el SHA del `best.pt` local de yolo11s; si el
  artefacto cambia, se actualiza el manifiesto en el mismo PR.
- **Compatibilidad**: los tests existentes que asumen “sin manifiesto” deben aislar
  `DEFAULT_MANIFEST_PATH` con `tmp_path`; no se cambia el comportamiento de los
  overrides.
