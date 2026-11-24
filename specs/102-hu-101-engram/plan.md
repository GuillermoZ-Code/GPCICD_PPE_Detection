# Implementation Plan: HU-101 — Engram: memoria persistente para los agentes

**Branch**: `feature/102-hu-101-engram` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #157 y `specs/102-hu-101-engram/spec.md`.

## Summary

Registrar Engram como servidor MCP en `opencode.json` con un comando portable y documentar
en `docs/operacion/engram.md` la instalación, el uso (`mem_save` → `mem_search`), la
ubicación de la base y cómo deshabilitarlo. Las pruebas validan la configuración y el
runbook sin ejecutar Engram.

## Technical Context

**Language/Version**: JSON + Markdown + Python 3.13 para las pruebas

**Primary Dependencies**: ninguna nueva; Engram es una herramienta externa

**Storage**: `~/.engram/engram.db` (fuera del repositorio)

**Testing**: pytest; lectura de `opencode.json`, del runbook y de `.gitignore`

**Target Platform**: OpenCode en Windows/Linux/macOS

**Project Type**: configuración de agentes y documentación operativa

**Constraints**: no versionar la base; no usar rutas absolutas de una máquina

**Scale/Scope**: una entrada MCP y un runbook

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Cada AC tiene una prueba que lo referencia.
- [x] Sin cambios en el contrato `ImageData → list[Detection]`.
- [x] `opencode.json` (Guillermo) y `docs/operacion/` (Eliana) generan aviso, no bloqueo.
- [x] Documentación en español.

## Project Structure

```text
opencode.json                  # + mcp.engram
docs/operacion/engram.md       # nuevo: runbook
tests/test_engram_config.py    # nuevo: configuración y runbook
specs/102-hu-101-engram/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### `opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["..."],
  "mcp": {
    "engram": {
      "type": "local",
      "command": ["engram", "mcp", "--tools=agent"],
      "enabled": true
    }
  }
}
```

- `command` usa `engram` desde el PATH; cada equipo lo instala.
- Para desactivarlo: `"enabled": false` o quitar el bloque.

### Runbook

1. **Instalar**: `engram setup opencode` (o el binario del equipo) y verificar con
   `opencode mcp list`.
2. **Usar**: `mem_save` al cerrar una decisión; `mem_search`/`mem_context` para recuperar.
3. **Base**: `~/.engram/engram.db`; no se versiona.
4. **Deshabilitar**: `"enabled": false`; OpenCode sigue funcionando.
5. **Evidencia**: ejemplo real de `mem_save` y `mem_search` de esta sesión.

### Pruebas

`tests/test_engram_config.py`:

1. `test_opencode_json_is_valid_json` → AC-01.
2. `test_opencode_declares_engram_mcp` → AC-01.
3. `test_opencode_engram_is_enabled` → AC-01.
4. `test_runbook_documents_installation` → AC-01.
5. `test_runbook_documents_how_to_disable` → AC-01.
6. `test_runbook_documents_save_and_search` → AC-02.
7. `test_runbook_documents_local_database` → AC-03.
8. `test_gitignore_covers_engram_database` → AC-03.

### Alternativas descartadas

- **Ruta absoluta al binario**: rompe en los otros equipos; se usa el PATH.
- **Versionar la base**: contiene memorias y crece; queda fuera de Git.
- **Registrar solo en la configuración global**: no viaja con el repositorio y cada
  integrante tendría que repetirlo.

## Phases

1. **Tests first**: configuración, runbook y `.gitignore`.
2. **Implementación**: `opencode.json` y el runbook.
3. **Cierre**: `make check`, `make ownership-check`, PR y `Closes #157`.

## Risks

- **Equipo sin Engram**: el MCP falla al arrancar; el runbook explica cómo desactivarlo.
- **Propiedad**: los dos archivos son de otros dueños; la PR necesita su revisión.
- **Privacidad**: las memorias no deben incluir credenciales; se advierte en el runbook.
