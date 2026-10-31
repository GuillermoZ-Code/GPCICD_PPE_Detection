# 🤝 Guía de contribución

¡Gracias por contribuir a **GPCICD PPE Detection**! La verdad técnica central vive
en [`CONSTITUTION.md`](./CONSTITUTION.md). Léela antes de tu primera contribución.

## 📑 Tabla de contenidos

- [Equipo y roles](#-equipo-y-roles)
- [Requisitos previos](#-requisitos-previos)
- [Preparar tu equipo (Windows)](#-preparar-tu-equipo-windows)
- [Sin make](#-sin-make)
- [Gitflow](#-gitflow)
- [Commits](#-commits)
- [Pull Requests](#-pull-requests)
- [Spec Kit por HU](#-spec-kit-por-hu)
- [Estándares de código](#-estándares-de-código)
- [Sincronía documental](#-sincronía-documental)
- [Licencia](#-licencia)

---

## 👥 Equipo y roles

| Integrante | GitHub | Rol |
|------------|--------|-----|
| Eliana Cardona | [@ElianaCardona](https://github.com/ElianaCardona) | Documento maestro, Caps. 1–2, alcance, integración del PDF |
| Hernán Estrada | [@HestradaUAO](https://github.com/HestradaUAO) | Modelo, Model Card, datos, licencia, hardware, métricas, sesgos, Cap. 4 y CRISP-DM |
| Guillermo Zabala | [@GuillermoZ-Code](https://github.com/GuillermoZ-Code) | Entorno, arquitectura y repositorio, evidencias y **Code Reviewer** |
| Jesús Riveros | [@jesusriverosUAO](https://github.com/jesusriverosUAO) | Planificación, Gantt, CPM, HU, AC, estimación, Cap. 3 y 5, tablero Kanban |

Los responsables de las HU se definen en equipo al iniciar el M3; no hay una tabla de
asignación en el repositorio.

## ✅ Requisitos previos

| Herramienta | Versión | Notas |
|-------------|---------|-------|
| [Python](https://www.python.org/downloads/) | 3.13+ | Fijada en `.python-version` |
| [`uv`](https://docs.astral.sh/uv/) | Última estable | Entornos y dependencias |
| [Git](https://git-scm.com/) | Última estable | Control de versiones |
| [Git Bash](https://gitforwindows.org/) | — | Necesario para `make` en Windows |
| [GNU Make](https://www.gnu.org/software/make/) | 4.x | Opcional si usas la tabla “sin make” |
| [Node.js LTS](https://nodejs.org/) | 20+ | Necesario para Archify |
| [Spec Kit](https://github.com/github/spec-kit) | v1.2.5 | Flujo SDD; ya está inicializado en `.specify/` |
| [GitHub CLI](https://cli.github.com/) | Opcional | Issues y PRs |

> ⚠️ Está **prohibido** usar `pip` o `requirements.txt`.

## 🪟 Preparar tu equipo (Windows)

> Comandos verificados con `winget search` y la documentación vigente de uv, OpenCode
> y Spec Kit (31/10/2026). Ejecuta en PowerShell **como usuario normal**; algunos
> instaladores piden confirmación.

### 1. Git for Windows (incluye Git Bash)

```powershell
winget install --id Git.Git -e --source winget
git --version
Test-Path "C:\Program Files\Git\bin\bash.exe"
```

Git Bash es el shell que usa el `Makefile` en Windows.

### 2. uv

```powershell
winget install --id=astral-sh.uv -e
uv --version
```

Alternativa oficial si no usas winget:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. GNU Make

```powershell
winget install --id ezwinports.make -e
make --version
```

Si no puedes instalar `make`, usa la tabla [“Sin make”](#-sin-make) más abajo.

### 4. Node.js LTS (para Archify)

```powershell
winget install --id OpenJS.NodeJS.LTS -e
node --version
```

### 5. Spec Kit (solo si no está instalado)

```powershell
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.5
specify --version
```

> El repositorio ya trae `.specify/` y `.opencode/commands/`. **No ejecutes
> `specify init` de nuevo** salvo que se acuerde en el equipo.

### 6. Skills del equipo en OpenCode

OpenCode descubre skills en `~/.agents/skills` y `~/.config/opencode/skills`.

```powershell
# Archify (diagramas)
npx skills add tt-a1i/archify -g

# jan-project-standard: verifica que exista
Test-Path "$HOME\.agents\skills\jan-project-standard\SKILL.md"

# Si el docente lo entrega como carpeta:
Copy-Item -Recurse "C:\ruta\al\paquete\jan-project-standard" "$HOME\.agents\skills\jan-project-standard"
```

Si `jan-project-standard` está en un repositorio, instálalo con
`npx skills add <repo> -g`. OpenCode descubre `~/.agents/skills` y
`~/.config/opencode/skills`. Reinicia OpenCode y verifica que aparezcan `archify` y
`jan-project-standard`.

### 7. Clonar y verificar

```powershell
git clone https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection.git
cd GPCICD_PPE_Detection
uv sync
uv run pre-commit install
make check
```

**Verificación final:** `make check` debe terminar en verde (Ruff, formato, `ty` y
pytest).

### 🚫 Sin make

Si no puedes instalar GNU Make, ejecuta los equivalentes en Git Bash:

| Target | Comando equivalente |
|--------|---------------------|
| `make install` | `uv sync` |
| `make dev` | `uv sync && uv run pre-commit install` |
| `make pre-commit` | `uv run pre-commit run --all-files` |
| `make lint` | `uv run ruff check .` |
| `make format` | `uv run ruff format .` |
| `make format-check` | `uv run ruff format --check .` |
| `make typecheck` | `uv run ty check` |
| `make test` | `uv run pytest` |
| `make check` | `uv run ruff check . && uv run ruff format --check . && uv run ty check && uv run pytest` |
| `make build` | `uv build` |
| `make arch` | `node "$HOME/.agents/skills/archify/bin/archify.mjs" finalize architecture docs/architecture/arquitectura.json docs/architecture/arquitectura.html --quality showcase` |
| `make clean` | `rm -rf .pytest_cache .ruff_cache .mypy_cache dist build htmlcov .coverage && find . -type d -name __pycache__ -prune -exec rm -rf {} +` |
| `make help` | No tiene equivalente directo; usa esta tabla. |

> Los comandos con `&&` funcionan en Git Bash. En PowerShell ejecútalos por separado
> y revisa `$LASTEXITCODE` después de cada uno.

## 🌿 Gitflow

- `main`: solo entregas de módulo. **Nunca** se hace push directo.
- `develop`: integración diaria. **Nunca** se hace push directo.
- Ramas de trabajo: `feature/...`, `fix/...`, `docs/...`, `refactor/...`, `test/...`,
  `chore/...`.
- Ramas de Spec Kit: `feature/{number}-{slug}` con el ID en el slug
  (`feature/001-hu-001-carga-imagen`, `feature/002-ta-11-contract-first`).
- Toda rama nace de `develop` y vuelve a `develop` por Pull Request.
- `develop → main` solo en la entrega del módulo, con merge commit.

```bash
git checkout develop
git pull
git checkout -b feature/002-hu-002-detector-yolo
# trabajar...
git add -A
git commit -m "feat(detector): ..."
git push -u origin feature/002-hu-002-detector-yolo
```

## 📝 Commits

Se usa [Conventional Commits](https://www.conventionalcommits.org/):

```text
<tipo>(<ámbito opcional>): <descripción breve en imperativo>
```

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Documentación |
| `refactor` | Refactorización sin cambio de comportamiento |
| `style` | Formato o linting |
| `test` | Pruebas |
| `chore` | Mantenimiento, CI, dependencias |

- Mensajes en imperativo, ≤72 caracteres, un propósito por commit.
- Referencia la issue cuando aporte: `feat(api): agregar /predict (refs #6)`.
- El commit final de una HU usa `Closes #N`.

## 🔀 Pull Requests

- La PR va **siempre a `develop`** (salvo el release `develop → main`).
- Usa la plantilla [`.github/PULL_REQUEST_TEMPLATE.md`](./.github/PULL_REQUEST_TEMPLATE.md).
- **Assignee:** quien hizo el trabajo.
- **Reviewers:** otros integrantes; el autor **nunca** se aprueba a sí mismo.
- **Mínimo 1 aprobación** de otro integrante.
- **Code Reviewer designado:** Guillermo; si él es autor, revisa otro integrante.
- La PR enlaza su issue (`Closes #N`) y su spec (`specs/...`).
- La CI debe estar en verde y `make check` debe pasar antes de pedir revisión.
- No se fusiona con cambios de otros sin resolver; no se fuerza push a `main`.

### Estrategia de merge

| Caso | Método |
|------|--------|
| PR a `develop` de un solo propósito | **Squash and merge** (por defecto) |
| PR a `develop` con commits atómicos que vale la pena conservar | **Create a merge commit** |
| Release `develop → main` | **Create a merge commit** (nunca squash) |

> La protección de `main` y `develop` es una **regla escrita** de este documento y de
> `CONSTITUTION.md`; no se configura protección técnica en GitHub por decisión del
> equipo.

## 🧩 Spec Kit por HU

El desarrollo sigue **Spec-Driven Development** con
[GitHub Spec Kit](https://github.com/github/spec-kit):

```text
issue → /speckit.specify → /speckit.clarify → /speckit.plan
      → /speckit.tasks → /speckit.analyze → /speckit.implement
      → make check → PR a develop
```

- Una spec por HU: `specs/<NNN>-hu-xxx-slug/spec.md`, `plan.md`, `tasks.md`.
- Los AC de la issue se copian a `spec.md`; issue y spec se enlazan.
- `CONSTITUTION.md` es la fuente; `.specify/memory/constitution.md` es un derivado
  con los principios no negociables y se sincroniza en el mismo commit.
- Spec Kit **v1.2.5** está inicializado en `.specify/`; los comandos viven en
  `.opencode/commands/` y la rama se crea con `branch_template:
  "feature/{number}-{slug}"`.
- Hoy solo existe la spec de la TA de contract-first como ejemplo; no se implementa.

## 🧹 Estándares de código

- PEP 8 / PEP 257, Ruff (`line-length = 100`, comillas dobles).
- Tipado en funciones y firmas públicas; `ty` en CI.
- Docstrings en módulos, clases y funciones públicas.
- Pruebas pytest con patrón **AAA**.
- Sin `print()` de depuración, código muerto ni `TODO` sin issue.
- Sin secretos, rutas personales, datasets ni pesos en Git.
- Las pruebas unitarias no dependen de GPU, dataset completo ni red.

## 🔄 Sincronía documental

El PDF de cada módulo se redacta **fuera del repositorio** (responsable: Eliana).
[`docs/curso/backlog.md`](./docs/curso/backlog.md) es el espejo de las issues y la
fuente para el Capítulo 5. Debe coincidir 1:1 con las issues, el tablero y `specs/`.

Si alguien cambia título, AC o SP en uno de esos lugares, actualiza los demás en el
mismo cambio. Ante una diferencia, **avisa al equipo antes de continuar**.

## 📄 Licencia

El proyecto se distribuye bajo **AGPL-3.0-only**. Al contribuir, aceptas que tus
aportes se licencien bajo los mismos términos. Ver [`LICENSE`](./LICENSE).
