# Herramientas del agente para GitLab (HU-073)

> **Qué es:** el CLI `glab` y el MCP oficial de GitLab configurados para operar el
> proyecto `educacional-group/GPCICD_PPE_Detection` desde OpenCode y la terminal, sin
> tokens en el repositorio.

## 1. `glab` (CLI)

```bash
glab --version          # 1.131.0 o superior
glab auth status        # debe mostrar gitlab.com y el usuario autenticado
glab api user           # confirma la identidad
```

- La autenticación se guarda en el **keyring** del sistema (`glab auth login`), fuera del
  repositorio.
- Operaciones típicas: `glab ci lint`, `glab ci view`, `glab pipeline status`,
  `glab api projects/89281003/...`, `glab release`.
- Si el clon actual no tiene remoto de GitLab, se ejecuta desde un clon del proyecto de
  GitLab o se pasa `--repo educacional-group/GPCICD_PPE_Detection`.

## 2. MCP de GitLab

```jsonc
// opencode.json (este repositorio)
"gitlab": {
  "type": "remote",
  "url": "https://gitlab.com/api/v4/mcp",
  "enabled": true
}
```

- El servidor se llama **`gitlab`** en la configuración. La issue #129 lo menciona como
  `gitlab-mcp`; es el mismo servidor: el prefijo de las herramientas es `gitlab.*`.
- La conexión es **OAuth** contra `https://gitlab.com/api/v4/mcp`; no se guardan tokens en
  el repositorio ni en `opencode.json`.
- La misma entrada puede vivir en la configuración global (`~/.config/opencode/opencode.json`);
  si está en ambos sitios, la del repositorio la hace explícita para todo el equipo.

### Verificación

```bash
opencode mcp list        # debe listar `gitlab` como connected
```

En una sesión de agente, una llamada de lectura (por ejemplo, la versión del servidor)
confirma que el MCP responde.

## 3. Reglas

- **Nunca** se versionan tokens, `glpat-`, `PRIVATE-TOKEN` con valor ni credenciales de
  GitLab.
- El único token de escritura es el *project access token* del espejo (HU-065), que vive
  en `secrets.GITLAB_TOKEN` de GitHub.
- Las operaciones de escritura en GitLab (MRs, pipelines, releases) las hace el Code
  Reviewer y quedan trazadas en la issue o PR de GitHub.

## 4. Diagnóstico

| Síntoma | Causa probable | Acción |
|---------|----------------|--------|
| `glab auth status` sin sesión | Keyring vacío o token expirado | `glab auth login` |
| `401 Unauthorized` en `glab api` | Token sin scope o caducado | Reautenticar con `glab auth login` |
| El MCP no aparece en `opencode mcp list` | Entrada ausente o `enabled: false` | Revisar `opencode.json` y reiniciar la sesión |
| `opencode mcp list` muestra `gitlab` y no `gitlab-mcp` | Nombre canónico del servidor | Es lo esperado; usar el prefijo `gitlab.*` |
