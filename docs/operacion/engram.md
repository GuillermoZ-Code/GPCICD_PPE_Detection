# Engram — memoria persistente de los agentes

> **Qué es:** servidor MCP que guarda decisiones, hallazgos y resúmenes de sesión en una
> base local, para que cada agente recupere contexto entre sesiones y entre
> compactaciones.
>
> **Qué no es:** no sustituye a [`CONSTITUTION.md`](../../CONSTITUTION.md), a los ADR, a
> `docs/curso/ESTADO.md` ni a las issues. Si una memoria contradice al repositorio, manda
> el repositorio.

## 1. Instalación y registro

Engram se instala una vez por equipo. El repositorio ya lo declara en
[`opencode.json`](../../opencode.json) como servidor MCP local:

```json
"mcp": {
  "engram": {
    "type": "local",
    "command": ["engram", "mcp", "--tools=agent"],
    "enabled": true
  }
}
```

El comando usa `engram` desde el `PATH`; no se versionan rutas absolutas de una máquina.

```bash
# Registrar el MCP en la configuración de OpenCode (una vez por equipo)
engram setup opencode
```

## 2. Verificación

```bash
# El servidor debe aparecer conectado
opencode mcp list
```

En la sesión del agente, `mem_current_project` debe devolver el proyecto
`gpcicd_ppe_detection`.

## 3. Uso

| Herramienta | Cuándo |
|---|---|
| `mem_save` | Tras una decisión, un bug resuelto, un hallazgo o una convención |
| `mem_search` | Al empezar algo que puede haberse hecho antes |
| `mem_context` | Al inicio de sesión o después de una compactación |
| `mem_session_summary` | Al cerrar una sesión de trabajo |

Formato recomendado de una memoria:

```text
**What**: una frase con lo hecho.
**Why**: qué lo motivó.
**Where**: archivos o rutas afectadas.
**Learned**: gotchas, casos borde, lo que sorprendió.
```

## 4. Dónde vive la base

La base local está en `~/.engram/engram.db` (con sus archivos `-wal` y `-shm`), **fuera de Git**. `.gitignore` excluye `*.db` y `*.sqlite`, así que nunca aparece en `git status`.

## 5. Deshabilitar en un equipo sin Engram

Si un integrante no tiene Engram instalado, el MCP se puede apagar sin tocar el resto de
la configuración:

```json
"mcp": {
  "engram": {
    "enabled": false
  }
}
```

OpenCode arranca igual; solo se pierden las herramientas de memoria.

## 6. Privacidad

- No guardes credenciales, tokens, rutas personales ni datos de personas.
- No pegues imágenes ni pesos; la memoria es texto.
- Las memorias son locales al equipo: no se sincronizan entre máquinas.

## 7. Evidencia (sesión del 23/11/2026)

- **Guardado:** `mem_save` de la decisión «Ola 2 del M4 en marcha» (observación #44).
- **Recuperación:** `mem_search` con la consulta «OLA 1 M4» devolvió las observaciones
  #44 y #43 con su fecha, tipo y proyecto.
- **Proyecto detectado:** `gpcicd_ppe_detection`, a partir del remoto de Git.

## 8. Relación con el protocolo de cierre

`mem_session_summary` complementa —no reemplaza— el cierre documental de
[`AGENTS.md`](../../AGENTS.md) §0.2: `make estado-write` lo corre una sola persona en la
sesión de cierre y la bitácora se actualiza con **hecho**, **en vuelo** y **siguiente**.
