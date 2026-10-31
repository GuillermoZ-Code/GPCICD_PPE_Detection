<div align="center">

# GPCICD PPE Detection

**Detección de Equipos de Protección Personal (EPP) mediante visión por computador.**
Proyecto del curso GPCICD M2-M4.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
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

Este repositorio aloja el proyecto integrador del curso **GPCICD M2-M4**: un sistema de
visión por computador que detecta **Equipos de Protección Personal (EPP)** —por ejemplo,
casco, chaleco, guantes o gafas— en imágenes y video, y reporta su presencia o ausencia de
forma evaluable.

El proyecto se construye con un enfoque de ingeniería reproducible: entorno gestionado con
`uv`, calidad automatizada (Ruff, `ty`, `pytest`, pre-commit) y CI en GitHub Actions. La
funcionalidad de detección se implementará de forma incremental durante los módulos del
curso.

> 📘 La verdad técnica central —propósito, stack, decisiones, convenciones y flujo— vive en
> [`CONSTITUTION.md`](./CONSTITUTION.md). Es de lectura obligatoria antes de contribuir.

## 📑 Tabla de contenidos

- [Descripción general](#-descripción-general)
- [Estado del proyecto](#-estado-del-proyecto)
- [Stack tecnológico](#-stack-tecnológico)
- [Primeros pasos](#-primeros-pasos)
- [Calidad y automatización](#-calidad-y-automatización)
- [Estructura del repositorio](#-estructura-del-repositorio)
- [Roadmap](#-roadmap)
- [Flujo de trabajo y contribución](#-flujo-de-trabajo-y-contribución)
- [Licencia](#-licencia)

## 🚧 Estado del proyecto

| Área | Estado |
|------|:------:|
| Estructura del repositorio y entorno (`uv`) | ✅ |
| Constitución técnica y gobernanza | ✅ |
| CI configurada en GitHub Actions | ✅ |
| Requisitos y dataset del curso | ⏳ |
| Pipeline de detección de EPP | ⏳ |
| Pruebas de dominio | ⏳ |

> **Hoy el repositorio es un esqueleto de ingeniería.** Todavía no contiene un modelo
> entrenado ni un pipeline de inferencia; esos son los siguientes hitos del roadmap.

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
| **CI/CD** | [GitHub Actions](.github/workflows/ci.yml) |
| **Visión por computador** | `EN EVALUACIÓN` — candidato: PyTorch + Ultralytics YOLO |

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
```

> ⚠️ **Regla del proyecto:** toda gestión de dependencias y entornos pasa por `uv`.
> Está **prohibido** `pip` y `requirements.txt`.

## ✅ Calidad y automatización

| Herramienta | Rol |
|-------------|-----|
| [`uv`](https://docs.astral.sh/uv/) | Entornos, dependencias y lockfile determinista. |
| [Ruff](https://docs.astral.sh/ruff/) | Lint y formato. |
| [`ty`](https://github.com/astral-sh/ty) | Verificación estática de tipos. |
| [pre-commit](https://pre-commit.com) | Hooks antes de cada commit. |
| [pytest](https://docs.pytest.org/) | Pruebas unitarias. |

| Comando | Descripción |
|---------|-------------|
| `make help` | Lista los objetivos disponibles. |
| `make dev` | `uv sync` + instala los hooks de pre-commit. |
| `make check` | Verificación completa (lint + formato + tipos + pruebas). |
| `make lint` / `make format` | Ruff. |
| `make test` | `pytest`. |
| `make build` | Construye el paquete (sdist + wheel). |

## 📂 Estructura del repositorio

```text
GPCICD_PPE_Detection/
├── src/ppe_detection/       # código del paquete (src-layout)
├── tests/                   # pruebas
├── docs/                    # documentación
├── CONSTITUTION.md          # verdad central del proyecto
├── README.md                # este archivo
├── CONTRIBUTING.md          # guía de contribución
├── Makefile                 # automatización de tareas
├── pyproject.toml           # metadatos y dependencias (uv)
└── uv.lock                  # lockfile determinista
```

## 🗺️ Roadmap

- [ ] Definir requisitos y dataset (M2).
- [ ] Elegir el modelo/framework de detección.
- [ ] Implementar el pipeline de datos y el baseline.
- [ ] Implementar inferencia y evaluación.
- [ ] Ampliar la suite de pruebas (datos, post-procesamiento, inferencia).
- [ ] Verificar la CI en GitHub y proteger `main`.

El detalle vive en [`CONSTITUTION.md` §11](./CONSTITUTION.md#11-notas-y-tareas-pendientes).

## 🤝 Flujo de trabajo y contribución

> 📘 La guía completa está en [`CONTRIBUTING.md`](./CONTRIBUTING.md). Resumen:

1. Crea una rama: `git checkout -b feat/nombre-corto`.
2. Desarrolla y verifica: `make check`.
3. Commitea con [Conventional Commits](https://www.conventionalcommits.org/): `git commit -m "feat: ..."`.
4. Abre un Pull Request con la plantilla oficial.
5. Mantén `CONSTITUTION.md` actualizado ante cambios arquitectónicos o tecnológicos.

## 📄 Licencia

Distribuido bajo la [Licencia MIT](./LICENSE).

---

<div align="center">
<sub>Hecho con ❤️ por GuillermoZ</sub>
</div>
