# Plan: HU-010 — Consumir inferencias mediante gRPC

**Branch**: `feature/009-hu-010-consumo-grpc` · **Issue**: #10 · **Spec**: [spec.md](spec.md)

## 1. Decisión de diseño

### 1.1 Contrato Protocol Buffers (`ppe.proto`)

Un servicio unary único que espeja el esquema HTTP de HU-006
(`PredictResponse` en `src/ppe_detection/api/app.py`):

```text
package ppe.v1;
service PpeDetection { rpc Detect(PredictRequest) returns (PredictResponse); }
message BoundingBox { double x1; double y1; double x2; double y2; }        // xyxy px
message Detection { class_id, class_name, confidence, bbox, image_width, image_height }
message PredictRequest { bytes image; string source; }                      // JPEG/PNG ≤10 MB
message PredictResponse { repeated Detection detections; image_width; image_height;
                         model_version; elapsed_ms; message }
```

- `message` replica el contrato de resultado de HU-004 (`build_inference_result`)
  y es la única adición semántica respecto al esquema REST.
- Convenciones idénticas al contrato HTTP y a ADR 0005: `bbox` `xyxy` en píxeles
  de la imagen **original**, `confidence` en `[0, 1]`, `class_name` canónico del
  `data.yaml` (`Gloves, Vest, goggles, helmet, mask, safety_shoe`).

### 1.2 Un solo componente central (AC-010.2)

La construcción del detector desde variables de entorno se extrae a
`src/ppe_detection/detector_config.py` y la usan REST y gRPC:

```text
ppe_detection.detector_config   build_detector() · default_model_version()
        │                              (DetectorNotConfiguredError)
        ├── api/app.py      HTTPException 503            (HU-006, sin cambio de conducta)
        └── grpc/servicer.py StatusCode.UNAVAILABLE      (HU-010)
```

El adaptador gRPC no conoce `YoloDetector`; solo ve `Detector.detect()`,
`validate_image_bytes` y `build_inference_result`. Ni entrena ni duplica.

### 1.3 Mapa de errores (REST → gRPC)

| Situación | REST (HU-006) | gRPC (HU-010) |
|---|---|---|
| Vacío / corrupto / > 10 MB / formato no admitido | 400 + detalle | `INVALID_ARGUMENT` + detalle (`InvalidImageError`) |
| Sin `PPE_MODEL_PATH` ni detector inyectado | 503 + detalle | `UNAVAILABLE` + detalle (`DetectorNotConfiguredError`) |
| Fallo inesperado del detector | 500 implícito | `INTERNAL` + `type(e).__name__` |

Los estados se usan vía `context.abort(...)`, que no interrumpe el servidor.

### 1.4 Estructura de módulos

```text
src/ppe_detection/
├── detector_config.py            # compartido REST/gRPC (FR-005)
├── api/app.py                    # refactor mínimo: usa detector_config
└── grpc/
    ├── __init__.py
    ├── __main__.py               # python -m ppe_detection.grpc (servidor)
    ├── client.py                 # cliente de prueba + python -m …grpc.client
    ├── gen.py                    # regeneración con grpcio-tools
    ├── server.py                 # create_server() para pruebas y arranque
    ├── servicer.py               # adaptador hacia el pipeline compartido
    └── protos/
        ├── ppe.proto             # fuente del contrato (duplicado deliberado)
        ├── ppe_pb2.py            # generado; versionado; excluido de Ruff/ty
        ├── ppe_pb2_grpc.py        # generado; versionado; excluido de Ruff/ty
        └── __init__.py
```

### 1.5 Dependencias y generación (uv, prohibido pip)

- Runtime: `grpcio`, `protobuf` (`uv add grpcio protobuf`).
- Dev: `grpcio-tools` (`uv add --dev grpcio-tools`).
- `make protos` ejecuta `uv run python -m ppe_detection.grpc.gen`; se usa la
  ruta `-I src` para que el módulo generado importe `ppe_detection.grpc.protos`
  de forma absoluta. Los `*_pb2*.py` se versionan para que CI y el paquete
  construido no dependan de `protoc`, y quedan fuera de Ruff y `ty`.

### 1.6 Estrategia de pruebas (test-first, AAA, sin GPU ni red externa)

- Servidor `grpc.server` (thread pool) en `127.0.0.1:0` (puerto efímero) con
  stub generado: cliente-servidor real sin hardware externo.
- CASO AC-010.1: `FakeDetector` con una `Detection` por cada clase del catálogo
  canónico; imagen válida 12×8; verificación de orden, campos y rangos.
- CASO AC-010.2: misma imagen y el **mismo** `FakeDetector` inyectado en
  `create_app()` (REST, `TestClient`) y en el servicer gRPC; comparación campo a
  campo (`elapsed_ms` se excluye, ambos ≥ 0); equivalencia también del estado
  vacío de HU-004 (`message` idéntico a `NO_DETECTIONS_MESSAGE`).
- CASO AC-010.3: bytes vacíos, corruptos y > `MAX_IMAGE_BYTES` →
  `INVALID_ARGUMENT`; sin modelo → `UNAVAILABLE`; después de cada fallo la
  siguiente solicitud válida o reiterada se atiende.
- El cliente de prueba se valida contra el servidor levantado
  (`ppe_detection.grpc.client.detect(...)`).

## 2. Alternativas consideradas

- **Segundo detector interno en gRPC** — descartado: viola AC-010.2 y duplica la
  carga del artefacto.
- **Empaquetar `*_pb2*.py` y no versionarlos** — descartado: exigiría `protoc` en
  CI y rompería la reproducibilidad del paquete; se regeneran con `make protos`.
- **`grpcio-tools` como dependencia de runtime** — descartado: la generación es
  de desarrollo; el runtime necesita solo `grpcio` + `protobuf`.
- **Refactor grande del pipeline REST** — descartado: solo se extrae
  `detector_config.py` con nombres y conducta equivalentes; el resto queda intacto.

## 3. Documentación entregable

- `README.md`: generación (`make protos`), arranque (`python -m
  ppe_detection.grpc`) y consumo (cliente CLI) del servicio.
- `docs/architecture/contracts.md`: sección gRPC (servicio, mensajes y mapa de
  errores).
- `specs/README.md`, `docs/curso/backlog.md`, `docs/curso/PRUEBAS.md`: enlaces e
  inventario.
