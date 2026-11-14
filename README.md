<div align="center">

# GPCICD PPE Detection

**Detección de Equipos de Protección Personal (EPP) mediante visión por computador.**

API REST + gRPC · SPA React · YOLO en CPU · MLflow · Docker

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Python 3.13+](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![CI](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/actions/workflows/ci.yml/badge.svg)](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/actions/workflows/ci.yml)
[![Managed with uv](https://img.shields.io/badge/managed%20with-uv-de5fe9.svg)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=precommit&logoColor=white)](./.pre-commit-config.yaml)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-fe5196.svg)](https://conventionalcommits.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](./CONTRIBUTING.md)

</div>

---

## Descripción

Sistema de visión por computador que detecta **seis categorías de EPP** —`Gloves`,
`Vest`, `goggles`, `helmet`, `mask` y `safety_shoe`— en imágenes, y reporta su
ubicación (`bbox` xyxy) y confianza en `[0, 1]`. Es el proyecto integrador del curso
**GPCICD M2–M4**.

El repositorio se construye con un enfoque de ingeniería reproducible: `uv`, Ruff,
`ty`, pytest, pre-commit, CI en GitHub Actions, Spec Kit para el flujo por historia y
Docker CPU para la ejecución. La interfaz es una **SPA React desacoplada** que consume
la API por HTTP; el detector nunca vive dentro del cliente.

> 📘 La verdad técnica central —equipo, propósito, stack, decisiones y flujo— vive en
> [`CONSTITUTION.md`](./CONSTITUTION.md). Es de lectura obligatoria antes de contribuir.

**Enlaces rápidos:** [Tablero Kanban](https://github.com/users/GuillermoZ-Code/projects/1) ·
[Model Card](./docs/model-card.md) · [Especificaciones SDD](./specs/) ·
[Arquitectura interactiva](./docs/architecture/arquitectura.html) ·
[Backlog](./docs/curso/backlog.md) · [Estado operativo](./docs/curso/ESTADO.md)

## Estado del proyecto

| Área | Estado |
|------|:------:|
| Repositorio, gobernanza y entorno (`uv`) | ✅ |
| Gitflow `develop`/`main`, plantilla UAO y CI | ✅ |
| Contrato `ImageData → list[Detection]` y `FakeDetector` | ✅ |
| Detector YOLO11s ajustado (inferencia CPU) | ✅ |
| Validación, carga y visualización de imágenes | ✅ |
| API REST FastAPI (`/predict`, `/health`) | ✅ |
| Servicio gRPC | ✅ |
| SPA React + Vite + TypeScript | ✅ |
| MLflow: runs, comparación y Model Registry | ✅ |
| Docker CPU (REST + gRPC + SPA) | ✅ |
| Suite de pruebas (375 pytest + 76 Vitest) | ✅ |
| Módulo 3 (HU-001 a HU-013) | ✅ 13/13 |
| Módulo 4 (CI/CD y despliegue) | 🚧 19/11 → 28/11 |

## Inicio rápido

```bash
git clone https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection.git
cd GPCICD_PPE_Detection
uv sync

# El artefacto del modelo vive fuera de Git
export PPE_MODEL_PATH=artifacts/drive/yolo11s_clean/weights/best.pt

make app        # API en http://localhost:8000 y SPA en http://localhost:5173
```

| Servicio | URL | Comando |
|----------|-----|---------|
| API REST + Swagger | <http://localhost:8000/docs> | `uv run python -m ppe_detection.api` |
| SPA React | <http://localhost:5173> | `make frontend-dev` |
| gRPC | `127.0.0.1:9000` | `uv run python -m ppe_detection.grpc` |
| MLflow UI | <http://localhost:5000> | `make mlflow-ui` |

## Tabla de contenidos

- [Descripción](#descripción)
- [Estado del proyecto](#estado-del-proyecto)
- [Inicio rápido](#inicio-rápido)
- [Arquitectura](#arquitectura)
- [Stack tecnológico](#stack-tecnológico)
- [Instalación](#instalación)
- [Uso](#uso)
- [Modelo y métricas](#modelo-y-métricas)
- [Calidad y automatización](#calidad-y-automatización)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Flujo de trabajo y trazabilidad](#flujo-de-trabajo-y-trazabilidad)
- [Roadmap](#roadmap)
- [Datos, licencia y límites](#datos-licencia-y-límites)
- [Licencia del código](#licencia-del-código)
- [Equipo](#equipo)

## Arquitectura

```text
Navegador ──HTTP/JSON──► FastAPI ──► capa de servicio ──► detector YOLO ──► respuesta tipada
    ▲                        │                                   │
    └──── SPA React ◄────────┘                                   └──► MLflow (runs y métricas)
                    gRPC ──► servidor gRPC ──► mismo detector
Todo en Docker CPU; CI/CD en GitHub Actions → Droplet (M4)
```

El sistema respeta tres capas:

1. **Inferencia** (`detection/`, `preprocessing/`, `postprocessing/`): carga el modelo
   una sola vez, preprocesa, infiere y postprocesa. No conoce HTTP.
2. **Servicio** (`contracts.py`, `detector_config.py`, `evaluation/`, `visualization/`):
   valida reglas, decide umbrales y arma la respuesta.
3. **API / cliente** (`api/`, `grpc/`, `frontend/`): expone el contrato, valida
   payloads y traduce errores a HTTP o gRPC.

- [Diagrama interactivo (Archify)](./docs/architecture/arquitectura.html)
- [Fuente versionada](./docs/architecture/arquitectura.json)
- [Contratos y semántica](./docs/architecture/contracts.md)
- [ADRs](./docs/adr/)

El contrato `ImageData → Detector.detect() → list[Detection]` se define antes del
detector real, con un `FakeDetector` determinista, para que API, interfaz y gRPC
avancen en paralelo ([ADR 0005](./docs/adr/0005-contract-first.md)).

## Stack tecnológico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.13+ |
| **Gestor de paquetes** | [`uv`](https://docs.astral.sh/uv/) |
| **Build backend** | `uv_build` (src-layout) |
| **Tipado estático** | [`ty`](https://github.com/astral-sh/ty) |
| **Testing** | [`pytest`](https://docs.pytest.org/) + Vitest |
| **Linting / Formato** | [Ruff](https://docs.astral.sh/ruff/) + ESLint |
| **Pre-commit** | [pre-commit](https://pre-commit.com) |
| **API REST** | FastAPI + Pydantic |
| **RPC** | gRPC + Protocol Buffers |
| **Interfaz** | React 19 + Vite + TypeScript (`frontend/`) |
| **Visión** | Ultralytics YOLO11s + PyTorch CPU |
| **Experiment tracking** | MLflow 3 (runs + Model Registry) |
| **Contenedor** | Docker CPU multi-stage |
| **CI/CD** | GitHub Actions + Droplet (M4) |
| **Spec-Driven Development** | [GitHub Spec Kit](https://github.com/github/spec-kit) |
| **Dataset** | [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection) |
| **Licencia** | AGPL-3.0-only |

## Instalación

### Requisitos previos

- [Python 3.13+](https://www.python.org/downloads/)
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- [Git](https://git-scm.com/)
- Node.js 24 + npm (solo para la SPA)
- En Windows: [Git Bash](https://gitforwindows.org/) (lo usa el `Makefile`)

### Entorno

```bash
git clone https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection.git
cd GPCICD_PPE_Detection

uv sync                    # dependencias base
make dev                   # uv sync + hooks de pre-commit
npm ci --prefix frontend   # dependencias de la SPA
```

Los extras opcionales se activan con `uv sync --extra <nombre>`:

| Extra | Qué aporta |
|-------|------------|
| `inference` | Ultralytics + torch CPU (detector real) |
| `grpc` | gRPC y Protobuf |
| `tracking` | MLflow |

> ⚠️ **Regla del proyecto:** toda gestión de dependencias y entornos pasa por `uv`.
> Está **prohibido** `pip` y `requirements.txt`.

### Verificación

```bash
make check            # lint + formato + tipos + pytest
make frontend-check   # ESLint + Vitest + build
uv build              # sdist + wheel
```

## Uso

### API REST

```bash
export PPE_MODEL_PATH=artifacts/drive/yolo11s_clean/weights/best.pt
uv run --extra inference python -m ppe_detection.api
```

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/health` | Estado del componente e identidad del modelo cargado |
| `POST` | `/predict` | Inferencia sobre una imagen (`multipart/form-data`, JPEG/PNG ≤ 10 MB) |
| `GET` | `/docs` | Swagger / OpenAPI |

```bash
# Healthcheck: estado + contrato publicado
curl http://127.0.0.1:8000/health
# {"status":"ok","api_version":"0.1.0","model_loaded":true,
#  "model_version":"yolo11s-clean","model_reference":"sha256:E51EB0…"}

# Inferencia
curl -F "file=@foto.jpg" -F "conf=0.35" http://127.0.0.1:8000/predict
```

La respuesta de `/predict` incluye `detections`, dimensiones de la imagen,
`model_version`, `model_sha256`, `model_artifact`, `model_reference` y `elapsed_ms`.
Los errores de entrada se traducen a `400`; un modelo no configurado, a `503`.

### gRPC

```bash
uv run --extra grpc --extra inference python -m ppe_detection.grpc
uv run --extra grpc --extra inference python -m ppe_detection.grpc.client --image ruta/imagen.png
```

El contrato `ppe.v1` vive en `src/ppe_detection/grpc/ppe.proto` y los stubs se
regeneran con `make protos`. REST y gRPC comparten el mismo `Detector` y la misma
semántica de respuesta.

### Interfaz web

```bash
make frontend-dev     # http://localhost:5173
make frontend-build   # build estático en frontend/dist/
```

Flujo de la SPA: seleccionar imagen → estados `idle` / `loading` / `success` /
`error` → inferencia → cajas con clase y confianza → descarga de resultados. Si
`VITE_API_URL` no está definida, usa un cliente simulado determinista.

### MLflow

```bash
make mlflow-ui        # http://localhost:5000
```

El experimento `ppe-detection-inference` contiene tres sesiones comparables del
mismo modelo (baseline, umbral de confianza y resolución). El modelo está
registrado como `ppe-detection` con alias `production` y su identidad por SHA256.

```bash
# Medir y registrar una sesión
make mlflow-benchmark

# Registrar el modelo de un run
make mlflow-register RUN_ID=<run_id>
```

Detalle en [`docs/operacion/mlflow.md`](./docs/operacion/mlflow.md).

### Docker

```bash
make docker-build     # imagen backend CPU (uv.lock)
docker run -d --name ppe-system --rm \
  -p 8000:8000 -p 9000:9000 \
  -v "/ruta/modelos-epp:/models:ro" \
  -e PPE_MODEL_PATH=/models/best.pt \
  -e PPE_SERVICES=rest,grpc \
  gpcicd-ppe-detection:local
```

El contenedor expone REST (8000) y gRPC (9000) sin GPU; el artefacto se monta
**read-only**. La aplicación completa (REST + gRPC + SPA en nginx) se levanta con
`PPE_MODELS_DIR=/ruta/modelos-epp make docker-up`. Paso a paso en
[`docs/operacion/docker.md`](./docs/operacion/docker.md).

## Modelo y métricas

| Campo | Valor |
|---|---|
| Modelo | YOLO11s ajustado para 6 clases (`yolo11s_clean`) |
| Artefacto | `best.pt` (18,3 MB, fuera de Git) |
| SHA256 | `E51EB08078F8ABADA1D5F3D15BFB17D94E32DA0C70467D7C79E43C338D7A9959` |
| Dataset | `51ddhesh/PPE_Detection` (CC-BY-4.0), 10.941 imágenes limpias |

| Métrica (test limpio, 1.094 imágenes) | Valor |
|---|---:|
| Precisión | 0.800 |
| Recall | 0.767 |
| mAP@0.5 | 0.810 |
| mAP@0.5:0.95 | 0.516 |
| Latencia medida (CPU, 640 px) | 82 ms media · 90 ms p95 · 12 fps |
| Latencia medida (CPU, 416 px) | 41 ms media · 44 ms p95 · 24 fps |

La Model Card completa —modelo base, dataset, sesgos, limitaciones y licencia— está
en [`docs/model-card.md`](./docs/model-card.md); el informe de evaluación, en
[`docs/evaluation/HU-008.md`](./docs/evaluation/HU-008.md).

## Calidad y automatización

| Herramienta | Rol |
|-------------|-----|
| [`uv`](https://docs.astral.sh/uv/) | Entornos, dependencias y lockfile |
| [Ruff](https://docs.astral.sh/ruff/) | Lint y formato |
| [`ty`](https://github.com/astral-sh/ty) | Verificación estática de tipos |
| [pre-commit](https://pre-commit.com) | Hooks antes de cada commit |
| [pytest](https://docs.pytest.org/) | Pruebas unitarias (patrón AAA) |
| [Vitest](https://vitest.dev/) | Pruebas de la SPA |
| GitHub Actions | CI en `develop` y `main` |

| Comando | Descripción |
|---------|-------------|
| `make help` | Lista los objetivos disponibles |
| `make dev` | `uv sync` + hooks |
| `make check` | Lint + formato + tipos + pruebas |
| `make calidad` | Informe único de lint, formato, tipos y pruebas |
| `make lint` / `make format` | Ruff |
| `make test` | pytest |
| `make frontend-check` | ESLint + Vitest + build |
| `make mlflow-ui` | UI local de MLflow |
| `make arch` | Regenera el diagrama Archify |
| `make build` | `uv build` |
| `make docker-build` | Imagen backend CPU |
| `make docker-up` / `make docker-down` | Compose: API + gRPC + SPA |
| `make docker-smoke` | Inferencia REST + gRPC en el contenedor |

La suite suma **451 pruebas** (375 pytest + 76 Vitest) y no depende de GPU, del
dataset completo ni de red. El conteo y el reparto por integrante están en
[`docs/curso/PRUEBAS.md`](./docs/curso/PRUEBAS.md) y
[`docs/curso/PLAN-PRUEBAS.md`](./docs/curso/PLAN-PRUEBAS.md).

## Estructura del repositorio

```text
GPCICD_PPE_Detection/
├── src/ppe_detection/       # paquete (src-layout)
│   ├── api/                 # FastAPI: /predict y /health (HU-006)
│   ├── grpc/                # contrato ppe.v1, servidor y cliente (HU-010)
│   ├── detection/           # detector YOLO (HU-002)
│   ├── io/                  # carga y validación de imágenes (HU-001, HU-005)
│   ├── evaluation/          # métricas y evaluación (HU-008)
│   ├── tracking/            # MLflow: runs, benchmark y registry (HU-009)
│   ├── visualization/       # superposición de detecciones (HU-003)
│   ├── training/            # fine-tuning en GPU (script versionado)
│   └── tools/               # estado, calidad y launcher
├── frontend/                # SPA React + Vite + TypeScript
├── docker/                  # entrypoint y nginx del contenedor
├── Dockerfile               # imagen CPU multi-stage
├── compose.yml              # api + grpc + frontend
├── tests/                   # pytest (patrón AAA)
├── specs/                   # especificaciones SDD de Spec Kit
├── docs/
│   ├── adr/                 # ADR 0001–0006
│   ├── architecture/        # diagrama Archify y contratos
│   ├── curso/               # contexto, backlog y checklists M2–M4
│   ├── dataset/             # EDA y limpieza
│   ├── evaluation/          # informe de evaluación
│   ├── operacion/           # runbooks de demo, MLflow y Docker
│   └── model-card.md        # Model Card del modelo servido
├── .specify/                # Spec Kit v1.2.5
├── CONSTITUTION.md          # verdad central
├── AGENTS.md                # contexto para agentes
├── Makefile
├── pyproject.toml
├── uv.lock
└── LICENSE                  # AGPL-3.0
```

## Flujo de trabajo y trazabilidad

- **Tablero:** [GitHub Projects](https://github.com/users/GuillermoZ-Code/projects/1)
  con Backlog / Ready / In Progress / In Review / Done.
- **Especificaciones SDD:** una carpeta por historia en [`specs/`](./specs/) con
  `spec.md` (problema, requisitos y AC), `plan.md` (diseño) y `tasks.md` (tareas).
- **Gitflow:** `feature/*` → `develop`; `develop → main` solo en entregas de módulo.
- **Commits:** Conventional Commits, imperativo, ≤ 72 caracteres.
- **PR:** plantilla UAO, `Closes #N`, spec enlazada, assignee = autor, reviewers =
  otros integrantes, mínimo 1 aprobación. El autor nunca se autoaprueba.
- **Merge:** squash por defecto en PR simples; merge commit cuando hay commits
  atómicos que conservar; release `develop → main` siempre con merge commit.
- **Sin push directo** a `main` ni a `develop`.

Ver [`CONTRIBUTING.md`](./CONTRIBUTING.md) para el detalle.

## Roadmap

| Sprint | Fechas | HUs | SP | Estado |
|--------|--------|-----|----|--------|
| **M3-S1** | 31/10–07/11 | HU-001 a HU-007 | 11 | ✅ |
| **M3-S2** | 08/11–14/11 | HU-008 a HU-013 | 8 | ✅ |
| **M4-S3** | 15/11–28/11 | HU-014 y HU-015 | 3 | 🚧 |
| **Total** | | | **22** | |

Sustentaciones: **M3 14/11/2026** y **M4 28/11/2026**. El detalle vive en
[`docs/curso/backlog.md`](./docs/curso/backlog.md).

## Datos, licencia y límites

- Dataset: [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection),
  **CC-BY-4.0**, 6 clases, **16.011 objetos anotados verificados** (la tarjeta declara
  16.014), formato YOLO.
- La tarjeta **no declara la fuente original** ni el consentimiento de las personas;
  conserva el placeholder `<your-username>/ppe-detection`.
- **No hay clase `person` ni `no-EPP`**: el sistema reporta **qué EPP aparecen**, no
  si un trabajador cumple o incumple. Una detección ausente no prueba ausencia real.
- Los datasets y pesos **no se versionan**; el artefacto se identifica por versión y
  SHA256 y se sirve desde fuera del repositorio.
- El sistema es **asistivo**: no sustituye la inspección humana ni la normativa.

## Licencia del código

Distribuido bajo **GNU Affero General Public License v3.0 only**
([AGPL-3.0-only](./LICENSE)). El uso del sistema como servicio en red obliga a poner
a disposición el código fuente de la versión modificada. El modelo base Ultralytics
también es AGPL-3.0; el dataset es CC-BY-4.0 y exige atribución.

El aviso de copyright y las atribuciones de terceros están en [`NOTICE`](./NOTICE).

## Equipo

| Integrante | GitHub | Rol |
|------------|--------|-----|
| Eliana Cardona | [@ElianaCardona](https://github.com/ElianaCardona) | Documento maestro, Caps. 1–2, alcance, integración del PDF |
| Hernán Estrada | [@HestradaUAO](https://github.com/HestradaUAO) | Modelo, Model Card, datos, licencia, hardware, métricas y sesgos |
| Guillermo Zabala | [@GuillermoZ-Code](https://github.com/GuillermoZ-Code) | Entorno, arquitectura, repositorio, evidencias y **Code Reviewer** |
| Jesús Riveros | [@jesusriverosUAO](https://github.com/jesusriverosUAO) | Planificación, Gantt, CPM, HU, AC, estimación y tablero Kanban |

---

<div align="center">
<sub>Grupo 4 — GPCICD M2–M4 · Universidad Autónoma de Occidente</sub>
</div>
