# Implementation Plan: HU-073 — MCP de GitLab y `glab` autenticado

**Branch**: `feature/074-hu-073-gitlab-mcp-glab` | **Date**: 2026-11-25 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/074-hu-073-gitlab-mcp-glab/spec.md`

## Summary

Declarar el MCP oficial de GitLab en `opencode.json` (remoto, OAuth, sin tokens) y
documentar en `docs/operacion/herramientas-agente.md` cómo verificar el MCP y el CLI
`glab`, incluido el nombre canónico del servidor y el diagnóstico básico.

## Technical Context

**Language/Version**: JSON + Markdown

**Primary Dependencies**: MCP remoto `https://gitlab.com/api/v4/mcp`, `glab` 1.131.0

**Storage**: N/A

**Testing**: pytest estático sobre el JSON y el runbook

**Target Platform**: OpenCode / terminal

**Project Type**: herramientas para agentes

**Performance Goals**: N/A

**Constraints**: sin tokens en el repositorio; OAuth o keyring del sistema

**Scale/Scope**: un archivo de configuración y un runbook

## Constitution Check

- **Sin secretos**: el MCP es remoto con OAuth; no hay tokens. ✅
- **Test-first**: cada AC tiene prueba estática. ✅
- **Propiedad**: `opencode.json` y `docs/operacion/` (aviso de Eliana). ✅
- **Una HU por PR**. ✅

## Project Structure

```text
opencode.json                              # entrada `gitlab` del MCP
docs/operacion/herramientas-agente.md      # nuevo: CLI, MCP, verificación y diagnóstico
tests/test_herramientas_agente.py          # 5 pruebas estáticas
specs/074-hu-073-gitlab-mcp-glab/
```

## Design decisions

1. **El MCP se declara en el repo.** La configuración global no viaja con el proyecto; la
   del repositorio hace explícita la capacidad para todo el equipo.
2. **Nombre `gitlab`, no `gitlab-mcp`.** Es el nombre canónico del servidor y el prefijo
   de las herramientas; el runbook explica la diferencia con el texto de la issue.
3. **OAuth, no token.** No se versiona ninguna credencial; el keyring de `glab` queda en el
   sistema operativo.
4. **El runbook es ejecutable.** Cada paso se puede copiar y pegar para verificar sin leer
   el código.

## Risks

| Riesgo | Mitigación |
|---|---|
| Duplicar el servidor entre config global y del repo | Misma URL y nombre; el repo la hace explícita |
| `opencode mcp list` no muestra el servidor | Runbook indica revisar `enabled` y reiniciar la sesión |
| Token del espejo filtrado | Ese token vive en GitHub Secrets; aquí no se usa |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_herramientas_agente.py` (MCP remoto habilitado y Engram intacto) |
| AC-02 | `tests/test_herramientas_agente.py` (comandos de verificación en el runbook) |
| AC-03 | `tests/test_herramientas_agente.py` (sin `glpat-`, `PRIVATE-TOKEN` ni `GITLAB_TOKEN`) |
