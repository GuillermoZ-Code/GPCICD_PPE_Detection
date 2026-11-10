# CONSTITUTION — GPCICD PPE Detection

> **Verdad central del proyecto.** Este documento define el propósito, el equipo, el
> stack, la arquitectura, las convenciones y el flujo de trabajo de
> `GPCICD PPE Detection`. Si algo aquí contradice al código, el código manda **y este
> archivo se actualiza en el mismo commit**.

> ⚠️ **Directiva de mantenimiento:** cada cambio significativo (funcionalidad,
> arquitectura, tecnología, proceso o rol) se refleja aquí en el mismo commit.

---

## 0. Identidad del proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | GPCICD PPE Detection |
| **Descripción** | Detección de Equipos de Protección Personal (EPP) mediante visión por computador. Proyecto del curso GPCICD M2-M4. |
| **Repositorio** | https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection |
| **Licencia** | **AGPL-3.0-only** |
| **Rama principal** | `main` |
| **Rama de integración** | `develop` |
| **Módulo activo** | M2 (alineación) → M3 (implementación) |
| **Estado** | En construcción 🚧 |

## 1. Equipo y roles

| Integrante | GitHub | Rol en el proyecto |
|------------|--------|--------------------|
| **Eliana Vanessa Cardona Burbano** | [@ElianaCardona](https://github.com/ElianaCardona) | Documento maestro, Capítulos 1–2, alcance e integración del PDF. |
| **Hernán Darío Estrada Satizábal** | [@HestradaUAO](https://github.com/HestradaUAO) | Modelo, Model Card, datos, licencia, hardware, métricas, sesgos, Capítulo 4 y CRISP-DM. |
| **Guillermo Alexander Zabala Fernández** | [@GuillermoZ-Code](https://github.com/GuillermoZ-Code) | Entorno, arquitectura y repositorio (`src/`, `pyproject.toml`, `uv`, Ruff, pytest, pre-commit, build, CI, Spec Kit), evidencias de comprobaciones y **Code Reviewer**. |
| **Wilson Jesús Riveros Gómez** | [@jesusriverosUAO](https://github.com/jesusriverosUAO) | Planificación, Gantt, CPM, HU, AC, estimación (Capítulos 3 y 5) y tablero Kanban. |

> Los responsables de las HU se definen en equipo al iniciar el M3. La tabla vigente
> vive en [`docs/curso/backlog.md`](./docs/curso/backlog.md#responsables); el tablero y
> las issues son la fuente operativa.

## 2. Propósito y no-propósito

### Propósito

Desarrollar un sistema de visión por computador que **detecte las seis categorías de
EPP** del dataset seleccionado en imágenes estáticas y reporte su presencia con
coordenadas y confianza, con un pipeline reproducible, pruebas automatizadas y
despliegue en CPU. Es el proyecto integrador del curso **GPCICD M2-M4**.

### No-propósito

- No certifica cumplimiento de normas de seguridad ni sustituye la inspección humana.
- No determina si un trabajador “cumple” o “incumple”: el dataset **no tiene clase
  `person` ni clase `no-EPP`**.
- No incorpora un LLM en el camino de inferencia.
- No incluye captura por cámara, RTSP, alertas, hardware ni operación 24/7.

## 3. Alcance

### Dentro del alcance

- Carga y validación de imágenes JPEG/PNG.
- Preprocesamiento con contrato numérico documentado (resize/letterbox, normalización).
- Detección con un detector especializado de nivel 3 (YOLO nano/small, por confirmar
  variante exacta en SPI-01), ajustado con el dataset.
- Postprocesamiento con NMS y umbrales configurables.
- Visualización de detecciones y respuesta vacía cuando no hay EPP.
- API REST con FastAPI, servicio gRPC y interfaz Streamlit.
- Evaluación con mAP@0.5, mAP@0.5:0.95, precision, recall y F1 por clase.
- Registro de experimentos en MLflow.
- Docker CPU, CI/CD en GitHub Actions y despliegue en Droplet.
- Pruebas deterministas sin GPU y verificación de calidad con Ruff, `ty` y `make check`.

### Fuera del alcance (por ahora)

- Detección de personas, cascos mal puestos o EPP “incorrecto”.
- Alertas, monitoreo continuo, cámaras IP/RTSP o integración con plantas.
- Entrenamiento multi-GPU o modelos de frontera (LLM/VLM).
- Aplicación móvil, autenticación multiusuario o SLA de producción.
- Certificación normativa o uso como dispositivo de seguridad.

## 4. Stack técnico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.13+ |
| **Gestor de paquetes y entorno** | [`uv`](https://docs.astral.sh/uv/) |
| **Build backend** | `uv_build` (src-layout) |
| **Paquete Python** | `ppe_detection` (distribución `gpcicd-ppe-detection`) |
| **Tipado estático** | [`ty`](https://github.com/astral-sh/ty) |
| **Testing** | [`pytest`](https://docs.pytest.org/) |
| **Linting / Formato** | [Ruff](https://docs.astral.sh/ruff/) |
| **Pre-commit** | [pre-commit](https://pre-commit.com) |
| **API REST** | FastAPI + Pydantic |
| **RPC** | gRPC + Protocol Buffers |
| **Interfaz** | Streamlit |
| **Visión por computador** | Ultralytics YOLO (nano/small) + PyTorch CPU |
| **Procesamiento de imagen** | OpenCV + NumPy |
| **Experiment tracking** | MLflow (local) |
| **Contenedor** | Docker CPU (sin CUDA) |
| **CI/CD** | GitHub Actions + Droplet |
| **Spec-Driven Development** | [GitHub Spec Kit](https://github.com/github/spec-kit) |
| **Diagramas** | [Archify](https://github.com/tt-a1i/archify) |
| **Dataset** | [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection) (CC-BY-4.0) |
| **Licencia** | AGPL-3.0-only |

> ⚠️ **Regla dura:** toda gestión de dependencias pasa por `uv`. Está **prohibido**
> `pip` y `requirements.txt`.

> La variante exacta de YOLO y la compatibilidad con Python 3.13 + torch CPU se
> confirman en **SPI-01**; hasta entonces no se fija una versión.

## 5. Estructura del repositorio

```text
GPCICD_PPE_Detection/
├── src/ppe_detection/       # paquete (src-layout)
│   ├── contracts.py         # contrato ImageData / Detection / Detector (previsto)
│   ├── io/                  # carga y validación (previsto)
│   ├── preprocessing/       # contrato numérico (previsto)
│   ├── detection/           # carga del modelo e inferencia (previsto)
│   ├── postprocessing/      # NMS y umbrales (previsto)
│   ├── api/                 # FastAPI (previsto)
│   ├── grpc/                # gRPC (previsto)
│   ├── ui/                  # Streamlit (previsto)
│   ├── evaluation/          # métricas y MLflow (previsto)
│   └── training/            # fine-tuning YOLO (script de Colab)
├── tests/                   # pytest, patrón AAA
├── docs/
│   ├── adr/                 # ADR 0001–0005
│   ├── architecture/        # diagrama Archify (JSON + HTML)
│   ├── curso/               # contexto, backlog y checklists por módulo
│   ├── dataset/             # EDA y auditoría del dataset
│   └── spikes/              # SPI-01 y SPI-02
├── specs/                   # specs de Spec Kit
├── .specify/                # Spec Kit v1.2.5 (integrado; no editar a mano)
├── .github/                 # PR/issue templates, CI, labels, Dependabot
├── AGENTS.md                # contexto para agentes
├── CONSTITUTION.md          # este archivo
├── README.md
├── CONTRIBUTING.md
├── Makefile
├── pyproject.toml
├── uv.lock
└── LICENSE                  # AGPL-3.0
```

Las carpetas marcadas como “previsto” se crean en la HU o TA correspondiente; no se
crean vacías por adelantado.

## 6. Convenciones de código

- **Estilo:** PEP 8 y PEP 257, impuesto por Ruff (`line-length = 100`, comillas dobles).
- **Tipado:** anotaciones en funciones y firmas públicas.
- **Nomenclatura:** `snake_case`, `PascalCase` (clases), `UPPER_CASE` (constantes).
- **Docstrings:** en módulos, clases y funciones públicas.
- **Pruebas:** pytest con patrón **AAA** (*Arrange · Act · Assert*).
- **Test-first:** cada AC de una spec tiene al menos una prueba pytest que lo
  referencia (`AC-xx` en el nombre o docstring). Las pruebas se escriben antes de la
  implementación y deben fallar primero. Excepciones: SPI y specs de documentación.
  `/speckit.analyze` marca como error un AC sin prueba.
- **Cómputo GPU:** el entrenamiento no se ejecuta en CPU local. Se permite
  **Colab/Kaggle solo como cómputo GPU**, ejecutando un script versionado del repo con
  `uv`; no se versionan `.ipynb` ni se usa la UI de notebooks como fuente de verdad.
- **Idioma:** documentación, comentarios y commits en español; identificadores de
  código en inglés.
- **Contratos:** `Detection` usa `bbox` en formato `xyxy`, `confidence` en `[0, 1]` y
  `class_name` limitado a las seis clases del dataset. Los nombres canónicos y su orden
  son los del `data.yaml`: `Gloves, Vest, goggles, helmet, mask, safety_shoe`; la
  interfaz puede capitalizarlos o traducirlos para mostrarlos.
- **Rutas:** datos, artefactos y configuración se reciben por CLI o configuración; no
  se codifican rutas absolutas.
- **Datos y pesos:** nunca se versionan. Se documenta su origen, licencia y SHA256.
- **Reproducibilidad:** semilla, versión del modelo, tamaño de imagen y umbrales se
  registran en cada experimento o inferencia.
- **Métricas:** se calculan con código versionado; no se reportan valores manuales.
- **Uso responsable:** el sistema reporta EPP detectado, no cumplimiento normativo.
- **Privacidad:** imágenes con personas solo con permiso; no se publican datos
  personales innecesarios.

## 7. Arquitectura y dominio

Flujo objetivo:

```text
Imagen → validación → preprocesamiento → detector YOLO → postprocesamiento (NMS/umbrales)
       → API REST / gRPC → Streamlit
                                     ↘ MLflow (experimentos y métricas)
Todo en Docker CPU; CI/CD → Droplet
```

- Diagrama interactivo: [`docs/architecture/arquitectura.html`](docs/architecture/arquitectura.html)
- Fuente versionada: [`docs/architecture/arquitectura.json`](docs/architecture/arquitectura.json)

### Contract-first

Antes de implementar el detector real se define el contrato:

```text
ImageData → Detector.detect() → list[Detection]
```

Con un `FakeDetector` determinista, las HU de API (HU-006), interfaz (HU-007) y gRPC
(HU-010) avanzan en paralelo con la HU del modelo (HU-002), reduciendo la ruta crítica.

### Jerarquía de modelo (3 niveles)

| Nivel | Enfoque | Por qué no se elige |
|-------|---------|---------------------|
| 1 — Frontera | LLM/VLM general | Latencia y costo altos; no requiere razonamiento abierto. |
| 2 — Gama media | Detector mediano | Más latencia en CPU; sobredimensionado para 6 clases. |
| 3 — Especializado | YOLO nano/small | **Elegido:** local, CPU, <100 ms objetivo, AGPL compatible. |

No hay LLM en inferencia: la tarea es detección de objetos acotada, con clases fijas,
requisito de CPU y necesidad de reproducibilidad.

### Dataset: hechos y límites

- 6 clases en el orden del `data.yaml`: **Gloves, Vest, goggles, helmet, mask, safety_shoe**
  (la interfaz puede mostrarlas capitalizadas o traducidas).
- **16.014 objetos anotados**; el número de imágenes no está publicado.
- Un solo `PPE.zip` de **668 MB**; estructura YOLO (`train/valid/test`, `data.yaml`).
- Licencia declarada: **CC-BY-4.0** (requiere atribución).
- La tarjeta **no declara la fuente original**, conserva el placeholder
  `<your-username>/ppe-detection` y no menciona consentimiento de rostros.
- **No hay clase `person` ni `no-EPP`**.

Consecuencia: el sistema reporta **qué EPP aparecen**, no qué trabajador incumple. Los
falsos positivos/negativos y la ausencia de detecciones no son prueba de incumplimiento.

## 8. Calidad y automatización

| Herramienta | Rol | Comando |
|-------------|-----|---------|
| `uv` | Entornos y dependencias | `uv sync` |
| Ruff | Lint + formato | `make lint` / `make format` |
| `ty` | Verificación de tipos | `make typecheck` |
| `pytest` | Pruebas | `make test` |
| `pre-commit` | Hooks antes de cada commit | `make pre-commit` |
| GitHub Actions | CI en `develop` y `main` | `.github/workflows/ci.yml` |
| `uv build` | Construcción del paquete | `uv build` |

- `make check` debe estar en verde antes de abrir una PR.
- La CI debe estar en verde antes de fusionar.
- No se usa `--no-verify` salvo causa documentada.
- Las pruebas unitarias no dependen de GPU, dataset completo ni red.
- **Sin umbral de cobertura por ahora:** se decide en HU-012 con evidencia.
- Toda dependencia nueva entra con `uv add` / `uv add --dev`.

## 9. Repositorio y Git

- **Remoto HTTPS:** `https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection.git`
- **Remoto SSH:** `git@github.com:GuillermoZ-Code/GPCICD_PPE_Detection.git`
- **Ramas:** `main` (entregas), `develop` (integración), `feature/*`, `fix/*`,
  `docs/*`, `refactor/*`, `test/*`, `chore/*`.
- **Ramas de Spec Kit:** `feature/{number}-{slug}`; el slug incluye el ID
  (`hu-001-...`, `ta-11-...`). Ejemplo: `feature/001-hu-001-carga-imagen` desde
  `develop`.
- **Commits:** Conventional Commits, imperativo, ≤72 caracteres, con scope cuando
  aporte (`feat(api): ...`, `fix(detector): ...`).
- **PR:** siempre a `develop`; `develop → main` solo en la entrega del módulo.
- **Plantilla:** `.github/PULL_REQUEST_TEMPLATE.md` (UAO).
- **Assignee:** quien hizo el trabajo.
- **Reviewers:** otros integrantes; el autor **nunca** se aprueba a sí mismo;
  mínimo **1 aprobación**.
- **Code Reviewer designado:** Guillermo. Si él es autor, revisa otro integrante.
- **Merge:**
  - PR a `develop`: **Squash** por defecto para PR de un solo propósito; **Create a
    merge commit** cuando trae commits atómicos que vale la pena conservar.
  - Release `develop → main`: **siempre merge commit**, nunca squash.
  - Nunca push directo a `main` ni a `develop`.
- **Protección de ramas:** es una **regla escrita** de este documento y de
  `CONTRIBUTING.md`; no se configura protección técnica en GitHub (decisión del
  equipo).
- **Dependabot:** target `develop`, ejecución mensual, actualizaciones agrupadas por
  ecosistema y labels `chore` + `infra`.

## 10. Spec-Driven Development (Spec Kit)

Spec Kit es el flujo **obligatorio** para las HU:

```text
issue → /speckit.specify → /speckit.clarify → /speckit.plan
      → /speckit.tasks → /speckit.analyze → /speckit.implement
      → make check → PR a develop con plantilla UAO
```

- Una spec por HU: `specs/<NNN>-hu-xxx-slug/spec.md`, `plan.md`, `tasks.md`.
- Los AC de la issue se copian a `spec.md`; issue y spec se enlazan mutuamente.
- `CONSTITUTION.md` es la fuente de verdad. `.specify/memory/constitution.md` es un
  **derivado** con los principios no negociables (uv, src-layout, AAA, Ruff, sin pesos
  ni datos versionados, reproducibilidad, contract-first, AGPL) y un encabezado que lo
  indique; se sincroniza en el mismo commit.
- Spec Kit **v1.2.5** está inicializado en `.specify/` (integración `opencode`,
  scripts `sh` y comandos `speckit.git.*`). Los comandos viven en
  `.opencode/commands/`.
- La rama se crea con `branch_template: "feature/{number}-{slug}"`; el slug incluye
  el ID (`hu-001-...`, `ta-11-...`).
- **Test-first:** los AC se convierten en pruebas antes de la implementación;
  `/speckit.analyze` marca error si un AC no tiene prueba. Excepciones: SPI y specs de
  documentación.
- **Sin umbral de cobertura** por ahora; se decide en HU-012.
- Hoy se deja **solo** la spec de la TA de contract-first como ejemplo, sin
  implementar.

## 11. Historial de decisiones técnicas

| Fecha | Decisión | Motivo |
|-------|----------|--------|
| 2026-10-31 | Adoptar `uv` como gestor único | Reproducibilidad; prohibido `pip`/`requirements.txt` |
| 2026-10-31 | Fijar Python 3.13 | Compatibilidad con el ecosistema de visión/ML |
| 2026-10-31 | src-layout con paquete `ppe_detection` | Separar código importable de scripts |
| 2026-10-31 | Ruff + pre-commit | Calidad automatizada antes de cada commit |
| 2026-10-31 | Conventional Commits | Historial legible y automatizable |
| 2026-10-31 | Gitflow `develop`/`main` | Integración continua y releases por módulo |
| 2026-10-31 | Licencia **AGPL-3.0-only** | Ultralytics YOLO es AGPL y el sistema se expone como servicio en red |
| 2026-10-31 | Dataset `51ddhesh/PPE_Detection` | 6 clases EPP, formato YOLO, CC-BY-4.0 |
| 2026-10-31 | Detector especializado nivel 3 (YOLO nano/small) | <100 ms en CPU; sin LLM en inferencia |
| 2026-10-31 | Dependabot mensual y agrupado en `develop` | Menos ruido y control de actualizaciones |
| 2026-10-31 | Contract-first con `FakeDetector` | Desbloquea API/UI/gRPC en paralelo con el modelo |
| 2026-10-31 | Spec Kit como flujo obligatorio | Especificaciones ejecutables y trazabilidad |
| 2026-10-31 | Merge commit para releases; squash por defecto en PR simples | Conservar historial en releases sin ruido diario |
| 2026-10-31 | Protección de ramas como regla escrita, no configuración de GitHub | Decisión del equipo |
| 2026-10-31 | Roles por módulo (Eliana, Hernán, Guillermo, Jesús) | Responsabilidades claras para el M2–M4 |
| 2026-10-31 | Test-first con trazabilidad AC → prueba | Evitar AC sin verificación y regresiones |
| 2026-10-31 | Colab/Kaggle solo como cómputo GPU, sin `.ipynb` | CPU local no es viable para entrenar |
| 2026-10-31 | Sin umbral de cobertura hasta HU-012 | El equipo decide con evidencia |
| 2026-11-04 | Reestimar el backlog de 67 a 22 SP (HU-001 a HU-015) | Alinear con el documento del M2; las TA/SPI se absorben en la preparación P1–P4 |
| 2026-11-04 | HU-002 pasa temporalmente de Jesús a Hernán | Jesús no disponible; HU-002 tiene holgura cero y bloquea la ruta crítica |

## 12. Roadmap M3–M4

### M3 — 31/10/2026 a 14/11/2026

- Clases: **05/11 FastAPI/REST**, **07/11 MLflow + Streamlit**.
- Sustentación: **sábado 14/11/2026**.
- **M3-S1 (31/10–07/11): HU-001 a HU-007 — 11 SP.**
- **M3-S2 (08/11–14/11): HU-008 a HU-013 — 8 SP.**

### M4 — 19/11/2026 a 28/11/2026

- MLOps/despliegue, CI/CD y credenciales.
- Sustentación: **sábado 28/11/2026**.
- **M4-S3 (15/11–28/11): HU-014 y HU-015 — 3 SP.**

**Total backlog oficial:** 22 SP (reestimación del 04/11/2026 sobre la planificación del
documento del M2, aprobada por Jesús). Las actividades de preparación del M3 (P1–P4)
suman 12 SP y no son issues, por lo que no entran en el total del tablero. Las TA/SPI
propuestas (25 SP) están **pendientes de validación por Jesús** y no se suman. Ver
`docs/curso/backlog.md`.

### Riesgos y decisiones pendientes

| Riesgo / decisión | Responsable sugerido por rol | Acción / fecha |
|-------------------|------------------------------|----------------|
| **Entrenamiento en CPU no es viable** | Hernán (modelo) | Colab/Kaggle **solo como cómputo GPU**, ejecutando un script versionado del repo con `uv`, sin `.ipynb`. Documentar la excepción en la Model Card antes de HU-002. |
| **Python 3.13 + Ultralytics/torch CPU** | Guillermo (entorno/arquitectura) | Validar en **SPI-01, días 1–2 del M3**. Plan B: fijar **3.12** en `.python-version` y `pyproject.toml`. |
| **EDA y descarga del dataset** | Jesús (planificación/backlog) valida; Hernán ejecuta | TA propuesta **“EDA del dataset”**: conteo de imágenes por split, objetos por clase, desbalance, imágenes sin etiquetas y cajas inválidas; descarga reproducible del ZIP con SHA256 y ruta configurable. Pendiente de validación de Jesús. |
| **AGPL en el despliegue (M4)** | Guillermo (repo) + Eliana (documento) | La interfaz y la API deben enlazar el código fuente; el dataset CC-BY exige atribución visible. AC propuesto en HU-007 y HU-015, pendiente de validación de Jesús. |
| **Droplet (M4)** | Guillermo (infra) + Jesús (planificación) | Definir dueño de la cuenta, costo y administración de los secrets de GitHub Actions **antes del 19/11**. |
| **Repo privado vs. AGPL** | Guillermo + Eliana | Si el servicio se publica, el repo debe ser público o el código debe ofrecerse a los usuarios. Decidir antes del M4. |

## 13. Configuración local y sincronía documental

- No se versionan `.env`, `.venv/`, datasets, videos, pesos, credenciales ni llaves.
- La identidad Git y las llaves SSH se configuran fuera del repositorio.
- El **PDF de cada módulo se redacta fuera del repo** (responsable: Eliana).
- `docs/curso/backlog.md` es el espejo de las issues y la fuente para el Capítulo 5.
  Debe coincidir 1:1 con las issues, el tablero y `specs/`. Si alguien cambia título,
  AC o SP en uno, actualiza los demás en el mismo cambio.
- `docs/curso/ESTADO.md` registra el estado operativo (rama, PRs, issues y bitácora de
  sesiones). Se regenera con `make estado-write` y **no** sustituye a issues,
  tablero, backlog ni specs.
- Ante una diferencia entre PDF, backlog, issues o specs, **el agente avisa al usuario
  antes de continuar**.
- Engram y GGA se habilitan en la **Fase 3**; no reemplazan este documento ni los ADR.
