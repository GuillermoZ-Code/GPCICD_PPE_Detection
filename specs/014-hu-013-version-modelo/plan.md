# Implementation Plan: HU-013 — Versión verificable del modelo

**Branch**: `feature/014-hu-013-version-modelo` | **Date**: 2026-11-12 |
**Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/014-hu-013-version-modelo/spec.md` e issue #13.

## Summary

Ampliar la identidad del modelo que ya exponen REST y gRPC: además de
`model_version`, devolver SHA256, ruta del artefacto y una referencia verificable.
La identidad se calcula desde el entorno al crear la app/servidor, se puede inyectar en
pruebas y usa el mismo formato `sha256:<hash>` que MLflow.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: sin dependencias nuevas; `hashlib` de la biblioteca estándar

**Storage**: la ruta del artefacto (`PPE_MODEL_PATH`) y su SHA256; los pesos siguen
fuera de Git

**Testing**: pytest (AAA), `FakeDetector`, `tmp_path`; sin GPU, dataset ni red

**Target Platform**: CPU

**Project Type**: library + API REST + gRPC

**Performance Goals**: calcular el SHA256 una sola vez al crear la app/servidor; no por
petición

**Constraints**: no copiar pesos, no versionar artefactos, no cambiar el contrato de
detecciones

**Scale/Scope**: una identidad por app/servidor; dos versiones deben distinguirse

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] src-layout y pruebas en `tests/`.
- [x] Ruff, `ty`, pytest y `make check`.
- [x] Sin datos ni pesos en Git.
- [x] Contract-first: `ModelIdentity` se define antes de tocar REST/gRPC.
- [x] Sin LLM en inferencia.
- [x] Test-first: cada AC tiene una prueba que lo referencia.

## Project Structure

```text
src/ppe_detection/
├── detector_config.py       # ModelIdentity, sha256_file y default_model_identity
├── api/app.py               # PredictResponse + identidad inyectable
├── grpc/servicer.py         # identidad en la respuesta gRPC
├── grpc/server.py           # pasa la identidad al servicer
└── grpc/protos/ppe.proto    # campos nuevos + stubs regenerados

tests/
└── test_model_version.py    # 20 pruebas de AC-013.1/2/3

docs/architecture/contracts.md # contrato REST/gRPC y variable PPE_MODEL_SHA256
frontend/src/types.ts          # campos opcionales del contrato
```

## Phases

1. **Tests first**: identidad, SHA, REST, gRPC, distinción de versiones y enlace MLflow.
2. **Implementación**: `ModelIdentity`, `default_model_identity`, REST y gRPC.
3. **Contrato**: proto + `make protos`, OpenAPI, tipos del frontend.
4. **Documentación**: contracts, demo, PRUEBAS, backlog, M3 y README.
5. **Cierre**: `make check`, `uv build`, PR con `Closes #13`.

## Risks

- **Regenerar stubs**: `make protos` debe ejecutarse y versionar los archivos generados.
- **Compatibilidad**: los campos nuevos son aditivos; `model_version` se conserva.
- **Hashing al importar**: `create_app()` se ejecuta al importar el módulo; el cálculo
  es una sola vez y solo si el artefacto existe.
- **Env inválido**: `PPE_MODEL_SHA256` mal formado falla con un mensaje claro; no se
  ignora en silencio.
- **Artefacto ausente**: no se inventa un SHA; la referencia cae a la versión.
