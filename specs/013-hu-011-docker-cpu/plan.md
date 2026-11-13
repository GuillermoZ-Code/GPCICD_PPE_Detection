# Plan: HU-011 — Ejecutar el sistema en un contenedor Docker CPU

**Branch**: `feature/012-hu-011-docker-cpu` · **Issue**: #11 · **Spec**: [spec.md](spec.md)

## 1. Decisión de diseño

### 1.1 Dockerfile multi-stage con dos targets

```text
frontend-builder (node:24-alpine)          web (nginx:stable-alpine)
        │  npm ci + npm run build            ▲
        └── dist/ ───────────────────────────┘  COPY --from=frontend-builder
runtime (python:3.13-slim + uv)
        ├── uv sync --frozen --no-dev --extra inference --extra grpc
        └── ENTRYPOINT docker/entrypoint.sh  (REST :8000 · gRPC :9000)
```

- `runtime` es la imagen del sistema: REST y gRPC comparten la misma
  configuración (`detector_config.py`, HU-006/HU-010) y el mismo contenedor puede
  servir ambos con `PPE_SERVICES=rest,grpc`.
- `web` sirve el build estático de la SPA (HU-007) con nginx; la imagen del
  backend no necesita Node y la de la web no necesita Python.
- `VITE_API_URL` es build-arg (por omisión `http://localhost:8000`): la SPA lo
  hornea en el bundle, igual que el flujo documentado en
  `docs/operacion/demo-local.md`.

### 1.2 Dependencias: `uv.lock` como única fuente (AC-011.1)

- `uv sync --frozen --no-dev --extra inference --extra grpc` dentro de la imagen:
  sin dev (pytest/ruff/grpcio-tools) y con los dos extras de runtime.
- **Prohibido** `pip` y `requirements.txt` (CONSTITUTION §4/§8). No se usa
  `uv export` para burlar el lock: la resolución sale del `uv.lock`.
- `grpcio` pasa a dependencia de runtime (extra `grpc`): el servidor gRPC es
  parte del paquete desplegable (HU-010); `grpcio-tools` sigue siendo dev.

### 1.3 PyTorch CPU en Linux (frontera clave)

En PyPI, las ruedas de `torch` para Linux dependen de paquetes NVIDIA (CUDA):
una imagen construida con `uv sync` normal pesaría varios GB. Solución
documentada por uv («Using uv with PyTorch» → environment markers):

```toml
[[tool.uv.index]]
name = "pytorch-cpu"
url = "https://download.pytorch.org/whl/cpu"
explicit = true

[tool.uv.sources]
torch = [{ index = "pytorch-cpu", marker = "sys_platform == 'linux'" }]
torchvision = [{ index = "pytorch-cpu", marker = "sys_platform == 'linux'" }]
```

- Con `explicit = true` el índice solo aplica a torch/torchvision.
- El marcador `sys_platform == 'linux'` deja intacta la resolución de Windows y
  macOS (PyPI ya distribuye builds CPU); el `uv.lock` del equipo en Windows no
  cambia de versiones.
- `--frozen` garantiza que el contenedor instala exactamente el lock.

### 1.4 Bibliotecas del sistema (Debian 13 trixie)

`python:3.13-slim` es Debian trixie: el paquete glib es `libglib2.0-0t64` (la
transición t64 renombró `libglib2.0-0`; sin candidato en trixie). Se instalan,
con `--no-install-recommends`: `libgl1` y `libxcb1` (OpenCV headless 5.x),
`libglib2.0-0t64`, `libgomp1` y `libquadmath0` (torch CPU) y
`ca-certificates`. La lista completa la fija la prueba
`test_dockerfile_instala_librerias_del_sistema`.

### 1.5 Artefacto del modelo: montaje externo (AC-011.3)

- Nada de pesos en la imagen: `.dockerignore` excluye `*.pt`, `*.pth`, `*.onnx`,
  `*.zip`, `artifacts/`, `weights/`, `datasets/`, `data/`, `.env`, cachés,
  `node_modules`, `dist`, docs, specs y tests; el Dockerfile solo copia
  `pyproject.toml`, `uv.lock`, `README.md`, `LICENSE`, `src/`, `frontend/` (para
  el target web) y `docker/`.
- Arranque: `-v <dir de modelos>:/models:ro` + `PPE_MODEL_PATH=/models/best.pt`.
- El artefacto verificado para la evidencia es
  `C:\Users\dasan\Downloads\modelos-epp\best.pt`
  (SHA256 `96ba99a7fd04566c95c1dac1e188f197efe50b2f170e4b5c76ac81ac0448c828`,
  igual al `EXPECTED_SHA256.txt` del artefacto). La ruta vive fuera del repo y
  solo aparece en la ejecución local (`PPE_DOCKER_MODEL`), nunca en el código.

### 1.6 Estrategia de pruebas (test-first, AAA)

- Estáticas (corren en CI, sin Docker): el Dockerfile usa `uv sync --frozen` y
  no `pip`; instala las libglib/libgomp; no copia pesos; `.dockerignore` y
  `.gitignore` bloquean pesos/datos/secretos; compose monta `:ro`; el entrypoint
  tiene finales de línea Unix (CRLF rompe la imagen); el runbook documenta
  build/config/arranque/inferencia.
- Contenedor (`@pytest.mark.docker`, opt-in con `PPE_DOCKER_SMOKE=1`): arranque
  real con imagen preconstruida + modelo montado, espera de carga (primera
  petición lenta), REST `POST /predict` y gRPC `Detect` verificados contra el
  contrato (campos, catálogo canónico, confianza en [0,1], `bbox` xyxy,
  `model_version="best"`), todo con el servicio **dentro del contenedor**.
- `markers = ["docker: …"]` se registra en `pyproject.toml`; la suite completa
  no depende de Docker (la prueba se salta sin Docker/imagen/artefacto).

### 1.7 Estructura de archivos nuevos

```text
Dockerfile                     # multi-stage: frontend-builder / runtime / web
docker/
├── entrypoint.sh              # PPE_SERVICES: rest | grpc | rest,grpc
└── nginx.conf                 # SPA estática + try_files
compose.yml                    # api + grpc + frontend, modelos :ro
.dockerignore                  # bloquea pesos, datos, secretos y cachés
docs/operacion/docker.md       # runbook HU-011
tests/test_docker.py           # AC-011.1–AC-011.4
```

## 2. Alternativas consideradas

- **`uv pip` + `--torch-backend=cpu` dentro de la imagen** — descartado:
  `--torch-backend` solo existe en la interfaz `uv pip` y obligaría a generar un
  requirements temporal; el marcador en `tool.uv.sources` mantiene `uv sync
  --frozen` (AC-011.1 literal) y el lock como fuente única.
- **Forzar pytorch-cpu en todas las plataformas** — descartado por ahora:
  cambiaría la resolución de Windows de todo el equipo a `+cpu` justo antes de
  la sustentación del M3; el marcador por plataforma es el cambio mínimo.
  Revisar en M4 si se unifica (posible issue de limpieza).
- **Imagen única «todo incluido» (backend + SPA + nginx)** — descartada:
  mezcla responsabilidades, duplica runtime y complica el healthcheck de HU-015;
  compose separa `api`, `grpc` y `frontend` con la misma imagen backend.
- **Copiar pesos en la imagen** — prohibido (CONSTITUTION §6/§13 y DoD-G): el
  montaje read-only cumple AC-011.3 y mantiene la imagen portable.
- **ESLint/Vitest del frontend dentro de la imagen** — no: la imagen ejecuta el
  build de producción; las verificaciones del frontend ya viven en
  `make frontend-check` y CI.

## 3. Documentación entregable

- `docs/operacion/docker.md`: runbook completo (build, SHA256, arranque single
  container y compose, inferencia REST/gRPC/SPA, montaje ro, troubleshooting).
- `README.md`: sección Docker en «Iniciar servicios», fila de estado HU-011 y
  estructura del repositorio (`Dockerfile`, `docker/`, `compose.yml`).
- `CONSTITUTION.md`: árbol §5, fila en §8 y decisión en §11 (mismo commit).
- `docs/curso/backlog.md` y `docs/curso/M3/README.md`: spec y PR de HU-011.
- `docs/curso/PRUEBAS.md`: inventario actualizado con `tests/test_docker.py`.
- `specs/README.md` y `AGENTS.md` (comandos docker): enlaces de estado.
