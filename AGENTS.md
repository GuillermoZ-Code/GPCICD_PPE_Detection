# AGENTS — GPCICD PPE Detection

> Contexto del proyecto para asistentes LLM (OpenCode, Copilot CLI, Claude Code, etc.).
> **Lee [`CONSTITUTION.md`](./CONSTITUTION.md) antes de operar.** Si hay conflicto,
> manda la constitución y se actualiza en el mismo commit.

## Proyecto

Detección de las seis categorías de EPP del dataset
[`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection)
con visión por computador. Curso **GPCICD M2-M4**. Licencia **AGPL-3.0-only**.

## Equipo y roles

| Integrante | GitHub | Rol |
|------------|--------|-----|
| Eliana Cardona | `ElianaCardona` | Documento maestro, Caps. 1–2, alcance, integración del PDF |
| Hernán Estrada | `HestradaUAO` | Modelo, Model Card, datos, licencia, hardware, métricas, sesgos, Cap. 4 y CRISP-DM |
| Guillermo Zabala | `GuillermoZ-Code` | Entorno, arquitectura y repositorio, evidencias y **Code Reviewer** |
| Jesús Riveros | `jesusriverosUAO` | Planificación, Gantt, CPM, HU, AC, estimación, Cap. 3 y 5, tablero Kanban |

> Los responsables de las HU se definen al iniciar el M3. No hay tabla de asignación
> de HU en el repo.

## Flujo de trabajo

- Ramas de Spec Kit: `feature/{number}-{slug}` con el ID en el slug
  (`feature/001-hu-001-carga-imagen`).
- Toda rama nace de `develop` y vuelve por PR. `develop → main` solo en entrega.
- Commits: [Conventional Commits](https://www.conventionalcommits.org/), imperativo,
  ≤72 caracteres, scope cuando aporte.
- PR con plantilla UAO, `Closes #N`, spec enlazada, assignee = autor, reviewers =
  otros integrantes, mínimo **1 aprobación**. El autor nunca se autoaprueba.
  Code Reviewer: Guillermo; si él es autor, revisa otro.
- Merge: squash por defecto en PR simples; merge commit cuando hay commits atómicos
  que conservar; **release `develop → main` siempre merge commit**.
- **No hay push directo a `main` ni a `develop`.** La protección es una regla escrita,
  no configuración de GitHub.

```bash
git checkout develop && git pull
git checkout -b feature/002-hu-002-detector-yolo
make check
git add -A
git commit -m "feat(detector): ..."
git push -u origin feature/002-hu-002-detector-yolo
```

## Spec Kit (SDD obligatorio)

```text
issue → /speckit.specify → /speckit.clarify → /speckit.plan
      → /speckit.tasks → /speckit.analyze → /speckit.implement
      → make check → PR a develop
```

- Una spec por HU en `specs/<NNN>-hu-xxx-slug/`.
- Los AC de la issue van a `spec.md`; issue y spec se enlazan.
- `CONSTITUTION.md` es la fuente; `.specify/memory/constitution.md` es un derivado
  con los principios no negociables y se sincroniza en el mismo commit.
- Spec Kit **v1.2.5** está inicializado en `.specify/`; los comandos viven en
  `.opencode/commands/` y `branch_template` es `feature/{number}-{slug}`.
- Hoy solo existe la spec de la TA de contract-first como ejemplo; no se implementa.

## Comandos

```bash
make help       # objetivos disponibles
make dev        # uv sync + hooks
make check      # lint + formato + tipos + pruebas
make lint       # Ruff
make format     # Ruff format
make test       # pytest
make arch       # regenera el diagrama Archify (si está instalado)
```

> ⚠️ Toda dependencia entra con `uv add` / `uv add --dev`. Prohibido `pip` y
> `requirements.txt`.

## Skills y MCP del equipo

| Herramienta | Tipo | Qué hace | Cuándo usarla |
|-------------|------|----------|----------------|
| `jan-project-standard` | Skill | Estándar de repositorio, constitución, uv, Ruff, CI y gobernanza | Crear o estandarizar el repo |
| Spec Kit | CLI/SDD | Especificaciones ejecutables y flujo por HU | Diseñar e implementar cada HU |
| `archify` | Skill | Diagramas interactivos de arquitectura | Actualizar `docs/architecture/` |
| `find-skills` | Skill | Descubrir skills instalables | Buscar una capacidad nueva |
| **GitHub MCP** | MCP | Issues, PRs, labels, milestones, revisiones | Operar el repositorio con la cuenta UAO `GuillermoZ-Code` |
| **context7** | MCP | Documentación vigente de librerías | FastAPI, gRPC, MLflow, Ultralytics, Spec Kit |
| **fetch** | MCP | Descargar documentación o datasets | Verificar fuentes externas |
| **Engram** | MCP | Memoria local de cada agente | **Fase 3**; no reemplaza CONSTITUTION ni ADR |
| **GGA** | CLI | Revisión de código con IA | **Fase 3**; no bloquea a quien no lo tenga |

> Engram y GGA se habilitan **después de la entrega del M2**, en un PR aparte.

## Dominio y límites

- 6 clases: Helmet, Vest, Gloves, Goggles, Mask, Safety Shoe.
- 16.014 objetos anotados; el número de imágenes no está publicado.
- Dataset CC-BY-4.0; la tarjeta no declara fuente original ni consentimiento.
- **No hay clase `person` ni `no-EPP`**: se reporta qué EPP aparecen, no cumplimiento.
- Detector YOLO nivel 3 (nano/small), CPU, <100 ms objetivo; sin LLM en inferencia.
- **Entrenamiento:** CPU local no es viable; Colab/Kaggle solo como cómputo GPU,
  ejecutando un script versionado con `uv`, sin `.ipynb`.
- **Test-first:** cada AC tiene una prueba pytest antes de la implementación; sin
  umbral de cobertura hasta HU-012.
- Pesos y dataset fuera de Git; artefacto con SHA256 y versión.
- Toda inferencia registra semilla, versión del modelo, tamaño de imagen y umbrales.

## Sincronía documental

El PDF de cada módulo se redacta fuera del repo. `docs/curso/backlog.md` es el espejo
de las issues y la fuente del Capítulo 5; debe coincidir 1:1 con issues, tablero y
`specs/`. Si hay diferencia, **avisa al usuario antes de continuar**.

## Reglas para agentes

- No hacer commits, push, PRs ni cambios en GitHub sin pedido explícito.
- Mostrar el diff o el plan antes de publicar.
- No cambiar títulos, AC ni SP de las issues sin aprobación de Jesús.
- No crear tableros, issues ni releases por iniciativa propia.
- No versionar secretos, datos, pesos, `.venv` ni archivos pesados.
