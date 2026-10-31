# CONSTITUTION — GPCICD PPE Detection

> **Verdad central del proyecto.** Este documento define el propósito, el stack, la
> estructura, las convenciones y el flujo de trabajo de `GPCICD PPE Detection`. Si algo
> aquí contradice al código, el código manda **y este archivo se actualiza**.

> ⚠️ **Directiva de mantenimiento:** cada vez que se realicen cambios significativos
> (nuevas funcionalidades, cambios arquitectónicos, adición de clases/módulos o ajustes
> de tecnologías), **se debe actualizar este archivo en el mismo commit** para mantener
> la verdad central del proyecto bien documentada.

---

## 0. Identidad del proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | GPCICD PPE Detection |
| **Descripción** | Detección de Equipos de Protección Personal (EPP) mediante visión por computador. Proyecto del curso GPCICD M2-M4. |
| **Repositorio** | https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection |
| **Autoría** | GuillermoZ — Guillermo.zabala@uao.edu.co |
| **Licencia** | MIT |
| **Rama principal** | `main` |
| **Estado** | En construcción 🚧 — fase de definición |

## 1. Propósito y no-propósito

### Propósito

Desarrollar, con prácticas de ingeniería reproducibles y CI/CD, un sistema de visión por
computador capaz de **detectar Equipos de Protección Personal (EPP)** en imágenes y video,
y de reportar su presencia o ausencia de forma evaluable. Es el proyecto integrador del
curso **GPCICD M2-M4**.

### No-propósito

No es un producto certificado de seguridad industrial ni sustituye la inspección humana,
la normativa vigente o el criterio de un profesional de seguridad y salud en el trabajo.
Tampoco incluye —por ahora— hardware, gestión de cámaras, despliegue en producción ni
entrenamiento a gran escala.

## 2. Alcance

### Dentro del alcance

- Ingesta y preparación de imágenes/video y sus anotaciones.
- Entrenamiento o ajuste de un detector de EPP (modelo **por definir**).
- Inferencia sobre imágenes/video con umbrales configurables.
- Evaluación cuantitativa del detector (mAP, precisión, recall, F1) y generación de reportes.
- Pruebas automatizadas y pipeline de integración continua.

### Fuera del alcance (por ahora)

- Procesamiento en tiempo real sobre dispositivos edge o en producción.
- Infraestructura de cámaras, alarmas o integración con sistemas de planta.
- Certificación de cumplimiento normativo en seguridad industrial.
- Entrenamiento multi-GPU o sobre datasets de escala industrial.
- Aplicación web o interfaz gráfica de usuario.

## 3. Stack técnico

| Categoría | Tecnología |
|-----------|------------|
| **Lenguaje** | Python 3.13+ |
| **Gestor de paquetes y entorno** | [`uv`](https://docs.astral.sh/uv/) |
| **Build backend** | `uv_build` (src-layout) |
| **Paquete Python** | `ppe_detection` (distribución: `gpcicd-ppe-detection`) |
| **Tipado estático** | [`ty`](https://github.com/astral-sh/ty) |
| **Testing** | [`pytest`](https://docs.pytest.org/) |
| **Linting / Formato** | [Ruff](https://docs.astral.sh/ruff/) |
| **Pre-commit** | [pre-commit](https://pre-commit.com) |
| **CI/CD** | [GitHub Actions](.github/workflows/ci.yml) |
| **Dependencias automáticas** | [Dependabot](.github/dependabot.yml) |
| **Visión por computador** | `EN EVALUACIÓN` — candidato: PyTorch + Ultralytics YOLO |
| **Datos y anotaciones** | `PENDIENTE` — formato por definir (YOLO/COCO) |
| **Experiment tracking** | `PENDIENTE` — no se adopta ninguna herramienta todavía |

> ⚠️ **Regla dura:** toda gestión de dependencias y entornos pasa por `uv`. Está
> **prohibido** `pip` y `requirements.txt`.

## 4. Estructura del repositorio

```text
GPCICD_PPE_Detection/
├── src/ppe_detection/       # código del paquete (src-layout)
├── tests/                   # pruebas (pytest)
├── docs/                    # documentación, ADRs e investigación
├── .github/                 # gobernanza (PR/issue templates, CI, Dependabot, labels)
├── .opencode/rules/         # reglas para agentes (tgrep)
├── AGENTS.md                # contexto para agentes LLM
├── CONSTITUTION.md          # este archivo — verdad central
├── README.md                # puerta de entrada pública
├── CONTRIBUTING.md          # guía de contribución
├── CODE_OF_CONDUCT.md       # código de conducta
├── Makefile                 # automatización de tareas
├── pyproject.toml           # metadatos y dependencias (uv)
├── uv.lock                  # lockfile determinista (versionado)
├── .python-version          # versión de Python fijada
└── .pre-commit-config.yaml  # hooks de calidad
```

## 5. Convenciones de código

- **Estilo:** [PEP 8](https://peps.python.org/pep-0008/) y [PEP 257](https://peps.python.org/pep-0257/),
  impuesto por **Ruff** (`line-length = 100`, comillas dobles).
- **Tipado:** anotaciones en funciones y firmas públicas.
- **Nomenclatura:** `snake_case` (funciones/variables), `PascalCase` (clases),
  `UPPER_CASE` (constantes).
- **Docstrings:** en módulos, clases y funciones públicas.
- **Pruebas:** `pytest` con el patrón **AAA** (*Arrange · Act · Assert*).
- **Idioma:** UI, comentarios, documentación y commits en español; identificadores de
  código en inglés.
- **Reglas propias del dominio:**
  - Las rutas de datos, anotaciones y pesos se reciben por **configuración o CLI**; no se
    codifican de forma fija en el código.
  - Los datasets, videos y pesos de modelos **no se versionan** (ver `.gitignore`); se
    documenta cómo obtenerlos o generarlos.
  - Toda inferencia debe ser reproducible: registrar **semilla**, versión del modelo,
    tamaño de imagen y umbrales utilizados.
  - Las métricas se calculan con **código versionado**, nunca a mano ni en celdas de
    notebook sin control de versiones.
  - Las imágenes con personas solo se usan con permiso y no deben contener datos
    personales innecesarios.

## 6. Arquitectura y dominio

Flujo objetivo del sistema (**todavía no implementado**):

```text
imagen/video → preprocesamiento → detector de EPP → post-procesamiento (NMS/umbrales)
             → detecciones + reporte (visual y/o tabular)
```

Hechos no negociables:

- El sistema es **asistivo**: señala posibles ausencias de EPP, no certifica seguridad.
- Un falso negativo (no detectar un EPP presente) y un falso positivo tienen costos
  distintos; la elección de umbrales debe justificarse y documentarse.
- El detector y el formato de anotación se eligen **antes** de implementar el pipeline;
  hasta entonces permanecen como `EN EVALUACIÓN` en §3.

## 7. Calidad y automatización

| Herramienta | Rol | Comando |
|-------------|-----|---------|
| `uv` | Entornos y dependencias | `uv sync` |
| Ruff | Lint + formato | `make lint` / `make format` |
| `ty` | Verificación de tipos | `make typecheck` |
| `pytest` | Pruebas | `make test` |
| `pre-commit` | Hooks antes de cada commit | `make pre-commit` |
| GitHub Actions | CI (pre-commit + tipos + pruebas) | `.github/workflows/ci.yml` |

- Ningún commit se salta los hooks (`--no-verify` está prohibido salvo causa justificada y documentada).
- La **CI debe estar en verde** antes de fusionar un Pull Request.
- Toda dependencia nueva entra con `uv add` / `uv add --dev` (nunca editando `uv.lock` a mano).
- En Windows, `make` usa **Git Bash** (ver la detección de `SHELL` en el `Makefile`); en
  Linux/CI usa `/bin/bash`.

## 8. Repositorio y Git

- **Remoto (HTTPS):** `https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection.git`
- **Remoto (SSH):** `git@github.com:GuillermoZ-Code/GPCICD_PPE_Detection.git`
- **Rama principal:** `main`
- **Estrategia de ramas:** `feat/...`, `fix/...`, `docs/...`, `refactor/...`, `test/...`,
  `chore/...`; integración vía Pull Request.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) —
  `feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `test:`, `chore:`.
- **Identidad git:** se configura localmente en cada máquina; **no se versiona** (ver §12).

## 9. Flujo diario (commit + push)

```bash
# 1. Ver cambios
git status

# 2. Verificación completa (lint + formato + tipos + pruebas)
make check

# 3. Agregar y commitear (los hooks se ejecutan solos)
git add -A
git commit -m "tipo: mensaje descriptivo"

# 4. Subir a GitHub
git push
```

## 10. Historial de decisiones técnicas

| Fecha | Decisión | Motivo |
|-------|----------|--------|
| 2026-10-31 | Adoptar `uv` como gestor único de entornos y dependencias | Reproducibilidad; prohibido `pip`/`requirements.txt` |
| 2026-10-31 | Fijar Python 3.13 | Compatibilidad con el ecosistema de visión/ML; `uv` gestiona la versión |
| 2026-10-31 | Usar src-layout con paquete `ppe_detection` y `uv_build` | Separar código importable de scripts; distribución instalable |
| 2026-10-31 | Adoptar Ruff (lint + formato) y pre-commit | Calidad automatizada antes de cada commit |
| 2026-10-31 | Adoptar Conventional Commits | Historial legible y automatizable |
| 2026-10-31 | Adoptar licencia MIT y `CONSTITUTION.md` como fuente única de verdad | Claridad legal y operativa |
| 2026-10-31 | `Makefile` multiplataforma (Git Bash en Windows) | Mantener `make` como interfaz también en el entorno local |
| 2026-10-31 | No fijar aún el framework de detección | Evitar dependencias pesadas y decisiones prematuras antes de definir dataset y requisitos |

## 11. Notas y tareas pendientes

- [ ] Definir requisitos funcionales del proyecto (M2) y las clases de EPP a detectar.
- [ ] Seleccionar y documentar el dataset, su licencia y el formato de anotación.
- [ ] Elegir el modelo/framework de detección y su versión.
- [ ] Implementar el pipeline de carga y preprocesamiento de datos.
- [ ] Entrenar un baseline y registrar métricas reproducibles.
- [ ] Implementar la inferencia por CLI sobre imágenes y video.
- [ ] Añadir pruebas de datos, post-procesamiento y una prueba de humo de inferencia.
- [ ] Adaptar la CI para pruebas sin GPU (mocks o datos sintéticos).
- [ ] Configurar el remoto, proteger `main` y verificar la CI en GitHub.
- [ ] (Opcional) Generar el diagrama de arquitectura con Archify.

**Siguiente paso inmediato:** definir los requisitos y el dataset del módulo M2.

## 12. Configuración local (no versionar)

> Configuración específica de la máquina. **NO incluir en commits.**

- La identidad Git (`user.name`, `user.email`) y las llaves SSH se configuran **fuera del
  repositorio**, en la configuración local de Git.
- No se versionan `.env`, `.venv/`, datasets, videos, pesos de modelos ni credenciales.
- Si el proyecto necesita variables de entorno, se documentarán en un `.env.example` sin
  valores reales.
