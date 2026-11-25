# Implementation Plan: HU-074 — Instalar skills de GitLab y frontend-design

**Branch**: `feature/075-hu-074-skills-repo` | **Date**: 2026-11-25 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/075-hu-074-skills-repo/spec.md`

## Summary

Versionar en `.agents/skills/` la skill oficial de `glab` y la skill `frontend-design`,
con su licencia y un README de procedencia; documentarlas en la tabla de `AGENTS.md` y
proteger la estructura con pruebas estáticas que garanticen que un agente las descubre.

## Technical Context

**Language/Version**: Markdown con frontmatter YAML (Agent Skills specification)

**Primary Dependencies**: `glab` 1.131.0 (`glab skills install`), `npx skills` (origen de
`frontend-design`), `anthropics/skills`

**Storage**: archivos versionados en `.agents/skills/`

**Testing**: pytest estático (sin red, sin agentes)

**Target Platform**: cualquier agente compatible (OpenCode, Claude Code, Codex, GitLab
Duo)

**Project Type**: contexto y herramientas para agentes

**Performance Goals**: N/A

**Constraints**: sin binarios pesados en Git; licencias incluidas; una sola fuente por
skill

**Scale/Scope**: 2 skills versionadas (~35 KB), 4 archivos nuevos y `AGENTS.md`

## Constitution Check

- **Sin binarios pesados**: solo Markdown y licencias; `archify` (17 MB) queda fuera. ✅
- **Licencias**: `frontend-design` con Apache-2.0; `glab` bajo la licencia del CLI. ✅
- **Test-first**: cada AC tiene prueba estática. ✅
- **Propiedad**: `AGENTS.md` es de Guillermo; `tests/` no tiene dueño asignado. ✅
- **Una HU por PR**: solo skills, README y pruebas. ✅

## Project Structure

```text
.agents/skills/
├── README.md                     # origen, licencia y actualización
├── glab/SKILL.md                 # skill oficial del CLI (glab skills install)
└── frontend-design/
    ├── SKILL.md
    └── LICENSE.txt               # Apache-2.0
AGENTS.md                         # tabla de skills actualizada
tests/test_skills_repo.py         # 6 pruebas estáticas
specs/075-hu-074-skills-repo/
```

## Design decisions

1. **Solo se versionan las skills que pide el AC.** `archify`, `jan-project-standard` y
   `find-skills` siguen en `~/.agents/skills/`; la primera pesa ~17 MB y su ruta ya está
   parametrizada en el `Makefile` (`ARCHIFY_BIN`).
2. **`glab` se instala con su propio CLI en alcance de proyecto.** `glab skills install`
   escribe en `.agents/skills/` del repositorio; es el mecanismo oficial y no requiere
   copiar a mano.
3. **`frontend-design` se copia del usuario y se documenta `npx`.** La copia evita red y
   hace la instalación determinista; el README deja el comando canónico para actualizar.
4. **La licencia viaja con la skill.** Sin `LICENSE.txt` no se versiona.
5. **El descubrimiento se prueba en el contrato, no en el agente.** Las pruebas verifican
   `name` + `description` en el frontmatter, que es lo que cualquier agente lee.

## Risks

| Riesgo | Mitigación |
|---|---|
| `glab skills install` cambia (experimental) | El README fija el comando y las pruebas fallan con contexto si desaparece |
| El repo crece con skills pesadas | Regla explícita + prueba que verifica que `archify` no está versionada |
| Deriva entre la copia del repo y la del usuario | El README indica el comando de actualización y la licencia |
| Skill sin licencia | Requisito FR-002 y prueba sobre `LICENSE.txt` |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_skills_repo.py` (`glab`, `frontend-design` y su licencia) |
| AC-02 | `tests/test_skills_repo.py` (tabla de `AGENTS.md` y remisión a `.agents/skills/`) |
| AC-03 | `tests/test_skills_repo.py` (`name` + `description`, README y skills de usuario fuera) |
