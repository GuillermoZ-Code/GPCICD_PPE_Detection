<div align="center">

# GPCICD PPE Detection

**Detección de Equipos de Protección Personal (EPP) mediante visión por computador.**
Proyecto del curso GPCICD M2-M4.

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

## 📖 Descripción general

Sistema de visión por computador que detecta **seis categorías de EPP** —Helmet,
Vest, Gloves, Goggles, Mask y Safety Shoe— en imágenes estáticas, y reporta su
ubicación y confianza. Es el proyecto integrador del curso **GPCICD M2-M4**.

El repositorio se construye con un enfoque de ingeniería reproducible: `uv`, Ruff,
`ty`, pytest, pre-commit, CI en GitHub Actions, Spec Kit para el flujo por HU y
Docker CPU para la ejecución. La entrega del M2 consolida la alineación del
repositorio, el backlog y la arquitectura; la implementación del detector se
desarrolla en M3–M4.

> 📘 La verdad técnica central —equipo, propósito, stack, decisiones y flujo— vive en
> [`CONSTITUTION.md`](./CONSTITUTION.md). Es de lectura obligatoria antes de contribuir.

## 📑 Tabla de contenidos

- [Descripción general](#-descripción-general)
- [Estado del proyecto](#-estado-del-proyecto)
- [Equipo y roles](#-equipo-y-roles)
- [Stack tecnológico](#-stack-tecnológico)
- [Primeros pasos](#-primeros-pasos)
- [Arquitectura](#-arquitectura)
- [Calidad y automatización](#-calidad-y-automatización)
- [Estructura del repositorio](#-estructura-del-repositorio)
- [Flujo de trabajo](#-flujo-de-trabajo)
- [Roadmap](#-roadmap)
- [Datos, licencia y límites](#-datos-licencia-y-límites)
- [Licencia del código](#-licencia-del-código)

## 🚧 Estado del proyecto

| Área | Estado |
|------|:------:|
| Estructura del repositorio y entorno (`uv`) | ✅ |
| Constitución, roles y gobernanza | ✅ |
| Gitflow `develop`/`main` y plantilla UAO | ✅ |
| Dataset seleccionado y documentado | ✅ |
| Arquitectura objetivo (Archify) | ✅ |
| Spec Kit inicializado | ✅ v1.2.5 |
| Contrato de inferencia y carga de imágenes | ✅ HU-001 |
| Detector YOLO (inferencia CPU) | ✅ HU-002 |
| Visualización de detecciones | ✅ HU-003 |
| Resultado vacío de EPP | ✅ HU-004 |
| SPA React con Vite y TypeScript | ✅ HU-007 |
| API REST (FastAPI) | ✅ HU-006 |
| Servicio gRPC | ✅ HU-010 |
| MLflow (experimentos) | 🔍 HU-009 · PR #50 en revisión |
| Docker CPU y CI/CD | ⏳ M3–M4 |
| Sistema desplegado en Droplet | ⏳ M4 |

## 👥 Equipo y roles

| Integrante | GitHub | Rol |
|------------|--------|-----|
| Eliana Cardona | [@ElianaCardona](https://github.com/ElianaCardona) | Documento maestro, Caps. 1–2, alcance, integración del PDF |
| Hernán Estrada | [@HestradaUAO](https://github.com/HestradaUAO) | Modelo, Model Card, datos, licencia, hardware, métricas, sesgos, Cap. 4 y CRISP-DM |
| Guillermo Zabala | [@GuillermoZ-Code](https://github.com/GuillermoZ-Code) | Entorno, arquitectura y repositorio, evidencias y **Code Reviewer** |
| Jesús Riveros | [@jesusriverosUAO](https://github.com/jesusriverosUAO) | Planificación, Gantt, CPM, HU, AC, estimación, Cap. 3 y 5, tablero Kanban |

> Los responsables de las HU se definen al iniciar el M3; la tabla vigente está en
> [`docs/curso/backlog.md`](./docs/curso/backlog.md#responsables).

## 🛠️ Stack tecnológico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.13+ |
| **Gestor de paquetes** | [`uv`](https://docs.astral.sh/uv/) |
| **Build backend** | `uv_build` (src-layout) |
| **Tipado estático** | [`ty`](https://github.com/astral-sh/ty) |
| **Testing** | [`pytest`](https://docs.pytest.org/) |
| **Linting / Formato** | [Ruff](https://docs.astral.sh/ruff/) |
| **Pre-commit** | [pre-commit](https://pre-commit.com) |
| **API REST** | FastAPI + Pydantic |
| **RPC** | gRPC + Protocol Buffers |
| **Interfaz** | React 19 + Vite + TypeScript (`frontend/`) |
| **Visión** | Ultralytics YOLO (nano/small) + PyTorch CPU |
| **Experiment tracking** | MLflow |
| **Contenedor** | Docker CPU |
| **CI/CD** | GitHub Actions + Droplet |
| **Spec-Driven Development** | [GitHub Spec Kit](https://github.com/github/spec-kit) |
| **Dataset** | [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection) |
| **Licencia** | AGPL-3.0-only |

## 🚀 Primeros pasos

### Requisitos previos

- [Python 3.13+](https://www.python.org/downloads/)
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- [Git](https://git-scm.com/)
- En Windows: [Git Bash](https://gitforwindows.org/) (lo usa el `Makefile`)

### Instalación

```bash
git clone https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection.git
cd GPCICD_PPE_Detection

uv sync
uv run pre-commit install   # equivalente a: make dev
```

### Verificación

```bash
make check   # lint + formato + tipos + pruebas
uv build     # construye sdist + wheel
```

> ⚠️ **Regla del proyecto:** toda gestión de dependencias y entornos pasa por `uv`.
> Está **prohibido** `pip` y `requirements.txt`.

### Iniciar servicios

```bash
# API REST (HU-006) — http://localhost:8000/docs
uv run python -m ppe_detection.api

# Servicio gRPC (HU-010) — 127.0.0.1:9000
uv run python -m ppe_detection.grpc

# Cliente de prueba del servicio gRPC
uv run python -m ppe_detection.grpc.client --image ruta/imagen.png
```

El servidor gRPC y su cliente usan `PPE_GRPC_HOST` / `PPE_GRPC_PORT` (y
`PPE_GRPC_TARGET` en el cliente); el detector se configura con las mismas
variables que la API REST (`PPE_MODEL_PATH`, `PPE_MODEL_VERSION`, `PPE_CONF`,
`PPE_IOU`, `PPE_IMGSZ`, `PPE_DEVICE`). Los mensajes Protocol Buffers se
regeneran con `make protos`. El detalle del contrato está en
[`docs/architecture/contracts.md`](./docs/architecture/contracts.md).

## 🗺️ Arquitectura

```text
Imagen → validación → preprocesamiento → detector YOLO → postprocesamiento (NMS/umbrales)
       → API REST / gRPC → SPA React
                                     ↘ MLflow (experimentos y métricas)
Todo en Docker CPU; CI/CD → Droplet
```

- [Diagrama interactivo](docs/architecture/arquitectura.html)
- [Fuente versionada](docs/architecture/arquitectura.json)
- [ADRs](docs/adr/)
- [Constitución](CONSTITUTION.md)

El contrato `ImageData → list[Detection]` se define antes del detector real, con un
`FakeDetector` determinista, para que API, interfaz y gRPC avancen en paralelo.

## ✅ Calidad y automatización

| Herramienta | Rol |
|-------------|-----|
| [`uv`](https://docs.astral.sh/uv/) | Entornos, dependencias y lockfile |
| [Ruff](https://docs.astral.sh/ruff/) | Lint y formato |
| [`ty`](https://github.com/astral-sh/ty) | Verificación estática de tipos |
| [pre-commit](https://pre-commit.com) | Hooks antes de cada commit |
| [pytest](https://docs.pytest.org/) | Pruebas unitarias (AAA) |
| GitHub Actions | CI en `develop` y `main` |

| Comando | Descripción |
|---------|-------------|
| `make help` | Lista los objetivos |
| `make dev` | `uv sync` + hooks |
| `make check` | Lint + formato + tipos + pruebas |
| `make lint` / `make format` | Ruff |
| `make test` | pytest |
| `make mlflow-ui` | UI local de MLflow (`http://localhost:5000`) |
| `make arch` | Regenera el diagrama Archify (si está instalado) |
| `make build` | `uv build` |

## 📂 Estructura del repositorio

```text
GPCICD_PPE_Detection/
├── src/ppe_detection/       # paquete (src-layout)
│   └── tracking/            # MLflow: registro y comparación (HU-009)
├── tests/                   # pytest
├── docs/
│   ├── adr/                 # ADR 0001–0006
│   ├── architecture/        # diagrama Archify
│   ├── curso/               # contexto, backlog y checklists M2–M4
│   └── operacion/           # runbooks locales (demo y MLflow)
├── specs/                   # specs de Spec Kit
├── .specify/                # Spec Kit v1.2.5 (integrado)
├── CONSTITUTION.md          # verdad central
├── README.md                # este archivo
├── CONTRIBUTING.md          # guía de contribución
├── AGENTS.md                # contexto para agentes
├── Makefile
├── pyproject.toml
├── uv.lock
└── LICENSE                  # AGPL-3.0
```

## 🔄 Flujo de trabajo

- **Gitflow:** `feature/*` → `develop`; `develop → main` solo en entregas de módulo.
- **Commits:** Conventional Commits, imperativo, ≤72 caracteres.
- **PR:** plantilla UAO, `Closes #N`, spec enlazada, assignee = autor, reviewers =
  otros integrantes, mínimo 1 aprobación. El autor nunca se autoaprueba.
- **Merge:** squash por defecto en PR simples; merge commit cuando hay commits
  atómicos que conservar; release `develop → main` siempre con merge commit.
- **Spec Kit:** issue → specify → clarify → plan → tasks → analyze → implement →
  `make check` → PR.
- **Sin push directo** a `main` ni a `develop`.

Ver [`CONTRIBUTING.md`](./CONTRIBUTING.md) para el detalle.

## 🗓️ Roadmap

| Sprint | Fechas | HUs | SP |
|--------|--------|-----|----|
| **M3-S1** | 31/10–07/11 | HU-001 a HU-007 | 11 |
| **M3-S2** | 08/11–14/11 | HU-008 a HU-013 | 8 |
| **M4-S3** | 15/11–28/11 | HU-014 y HU-015 | 3 |
| **Total** | | | **22** |

Sustentaciones: **M3 14/11/2026** y **M4 28/11/2026**. El detalle vive en
[`docs/curso/backlog.md`](docs/curso/backlog.md).

## 📊 Datos, licencia y límites

- Dataset: [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection),
  **CC-BY-4.0**, 6 clases, **16.014 objetos anotados**, formato YOLO.
- El número de imágenes no está publicado; la tarjeta no declara la fuente original,
  conserva el placeholder `<your-username>/ppe-detection` y no menciona consentimiento.
- **No hay clase `person` ni `no-EPP`**: el sistema reporta qué EPP aparecen, no si un
  trabajador cumple o incumple.
- Los datasets y pesos **no se versionan**; el artefacto se identifica por versión y
  SHA256.
- El sistema es **asistivo** y no sustituye la inspección humana ni la normativa.

## 📄 Licencia del código

Distribuido bajo **GNU Affero General Public License v3.0 only**
([AGPL-3.0-only](./LICENSE)). El uso del sistema como servicio en red obliga a poner
a disposición el código fuente de la versión modificada.

El aviso de copyright y las atribuciones de terceros están en [`NOTICE`](./NOTICE).

---

<div align="center">
<sub>Hecho con ❤️ por el Grupo 4 — GPCICD M2-M4</sub>
</div>
