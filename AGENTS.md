# AGENTS — GPCICD PPE Detection

> Contexto del proyecto para asistentes LLM (OpenCode, Copilot CLI, Claude Code, etc.).
> **Lee [`CONSTITUTION.md`](./CONSTITUTION.md) antes de operar.** Si hay conflicto,
> manda la constitución y se actualiza en el mismo commit.

## 0. Estado actual y protocolo de sesión

> **Este bloque caduca.** Si tiene más de 3 días o no coincide con `git log`, ignóralo
> y reconstruye el estado con `make estado`.

Sprint activo: **M3-S2** (08/11 → 14/11/2026). Sustentación del M3: 14/11/2026.

<!-- estado:inicio -->
**Actualizado:** 2026-11-11 04:44 UTC
- **Rama:** `feature/009-hu-008-evaluador` · +3/-0 vs `origin/develop`
- **Issues abiertas:** 8 · 11 SP
- **En vuelo:** #51 feat(eval): implementar evaluador reproducible de HU-008 (PR, revisión: —); #50 feat(tracking): registrar y comparar experimentos en MLflow (HU-009) (PR, revisión: —); #49 feat(calidad): informe automatizado de verificaciones (HU-012) (PR, revisión: —)
- **Siguiente:** #10 HU-010 — Consumir inferencias mediante gRPC
<!-- estado:fin -->

- **Detalle:** [`docs/curso/ESTADO.md`](./docs/curso/ESTADO.md).

### 0.1 Protocolo de arranque (obligatorio para OpenCode y Codex)

1. Ejecuta `make estado`. Lee **git, PRs e issues**, no la memoria de este archivo.
2. Contrasta con `docs/curso/backlog.md` y `docs/curso/ESTADO.md`.
3. Si dos fuentes difieren, **avisa al usuario antes de continuar**.
4. Elige la tarea: la del §0 o la siguiente HU abierta del sprint activo.
5. Una HU sin `specs/<NNN>-.../spec.md` no se implementa: primero Spec Kit.

### 0.2 Protocolo de cierre (obligatorio)

1. `make estado-write` regenera `docs/curso/ESTADO.md` y el bloque del §0.
2. Si cambió el stack, una decisión o el estado del proyecto, actualiza también
   `CONSTITUTION.md`, `README.md` y el ADR correspondiente en el mismo PR.
3. Añade una entrada a la bitácora con: **hecho**, **en vuelo**, **siguiente**.
4. Commit: `docs(estado): registrar cierre de sesion`.
5. Si no puedes commitear, deja el archivo modificado y dilo explícitamente.

### 0.3 Precedencia de fuentes

| Nivel | Fuente | Qué manda |
|-------|--------|-----------|
| 1 | Código + `git` | El hecho: rama, commits, PRs, CI |
| 2 | Issues + tablero | Operación del sprint |
| 3 | `specs/<HU>` | Diseño de esa HU |
| 4 | `CONSTITUTION.md` | Reglas técnicas |
| 5 | `AGENTS.md` | Cómo trabajar; el §0 es el nivel más débil |
| 6 | `docs/curso/backlog.md` | Espejo; si difiere, gana la issue y se corrige el espejo |
| 7 | `docs/adr/` | Histórico; no se reescribe |

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

> Los responsables de las HU se definen al iniciar el M3; la tabla vigente está en
> [`docs/curso/backlog.md`](./docs/curso/backlog.md#responsables).

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
- Al fusionar en `develop`, **cierra la issue a mano**: `Closes #N` solo actúa de forma
  automática cuando la PR apunta a la rama por defecto (`main`).

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
- Specs `001`–`006` en `specs/`; las HU se implementan con el flujo anterior.

## Comandos

```bash
make help       # objetivos disponibles
make dev        # uv sync + hooks
make check      # lint + formato + tipos + pruebas
make lint       # Ruff
make format     # Ruff format
make test       # pytest
make frontend-check  # ESLint + Vitest + build del frontend
make frontend-dev    # levanta la interfaz en http://localhost:5173
make app             # levanta API + interfaz con el modelo local
make arch       # regenera el diagrama Archify (si está instalado)
```

> ⚠️ Toda dependencia de Python entra con `uv add` / `uv add --dev`. Prohibido `pip` y
> `requirements.txt`. El frontend usa `npm` con `package-lock.json` (ADR 0006).

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

- 6 clases en el orden del `data.yaml`: Gloves, Vest, goggles, helmet, mask, safety_shoe.
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
