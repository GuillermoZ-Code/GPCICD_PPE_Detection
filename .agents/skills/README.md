# Skills del repositorio (`.agents/skills/`)

> **Qué es:** skills versionadas con el proyecto, en el formato de la
> [Agent Skills specification](https://agentskills.io). Cualquier agente compatible
> (OpenCode, Claude Code, Codex, GitLab Duo) las descubre por su `SKILL.md` sin
> instalar nada aparte.

## Skills incluidas

| Skill | Origen | Cómo se actualiza | Licencia |
|-------|--------|-------------------|----------|
| `glab` | Skill oficial que trae el CLI de GitLab | `glab skills install --force` (instala en `.agents/skills/`) | MIT (la del CLI) |
| `frontend-design` | [`anthropics/skills`](https://github.com/anthropics/skills) | `npx skills add https://github.com/anthropics/skills --skill frontend-design` | Apache-2.0 (`LICENSE.txt`) |

## Skills de usuario (no versionadas)

Estas viven en `~/.agents/skills/` porque son herramientas personales o pesadas:

| Skill | Motivo |
|-------|--------|
| `archify` | ~17 MB con binarios y ejemplos; `make arch` la resuelve desde `$USERPROFILE` |
| `jan-project-standard` | Estándar personal de repositorio |
| `find-skills` | Descubrimiento de skills instalables |

## Cómo comprobar que un agente las ve

1. Cada skill tiene `SKILL.md` con frontmatter `name` y `description`; el agente las
   lista al iniciar la sesión.
2. `glab skills list` muestra las skills empaquetadas del CLI y su origen.
3. `uv run pytest tests/test_skills_repo.py` verifica que las skills versionadas y la
   tabla de `AGENTS.md` siguen sincronizadas.

## Reglas

- No se versionan skills con binarios, `node_modules` ni datos de ejemplo pesados.
- Toda skill nueva entra con su licencia y su origen documentados en esta tabla.
- Si una skill cambia de versión, se actualiza en el mismo commit que su uso.
