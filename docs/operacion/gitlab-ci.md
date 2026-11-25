# Pipeline de GitLab CI/CD (HU-066)

> **Qué es:** [`.gitlab-ci.yml`](../../.gitlab-ci.yml) replica en GitLab las compuertas de
> la CI de GitHub: Ruff, `ty`, pytest, frontend y build del paquete.
> **Cómo llega:** GitHub es la fuente de verdad; el workflow
> [`mirror-gitlab.yml`](../../.github/workflows/mirror-gitlab.yml) empuja `develop` y
> `main` a GitLab (ADR 0007).

## 1. Etapas

| Etapa | Job | Qué hace | Cuándo |
|-------|-----|----------|--------|
| `quality` | `quality` | `uv sync --frozen`, Ruff, `ty`, pytest | MR y `develop`/`main` |
| `frontend` | `frontend` | `npm ci`, lint, Vitest y build | MR y `develop`/`main` |
| `build` | `build` | `uv build` y artefactos `dist/` | `main` o ejecución manual |
| `deploy` | `deploy` | Marcador manual de HU-070 | `main`, manual |

## 2. Cachés

- `uv`: clave por `uv.lock`, directorio `.uv-cache/`.
- `npm`: clave por `frontend/package-lock.json`, directorio `frontend/node_modules/`.

## 3. Reglas

- `workflow.rules` evita pipelines duplicados: uno por MR, uno por push a `develop` o
  `main`, y ejecución manual.
- `quality` y `frontend` corren en todas las pipelines.
- `build` y `deploy` solo en `main` (o manual); `deploy` es manual y lo sustituye HU-070.

## 4. Validar el archivo

```bash
glab ci lint --ref main          # valida la sintaxis contra el proyecto de GitLab
glab ci view                     # pipelines del proyecto
```

Si `glab` no está autenticado en el repositorio actual, se ejecuta desde un clon del
proyecto de GitLab o se usa `glab api projects/89281003/ci/lint`.

## 5. Diagnóstico

| Síntoma | Causa probable | Acción |
|---------|----------------|--------|
| `quality` falla en `uv sync --frozen` | `uv.lock` desactualizado | `uv lock` en local y commit |
| `frontend` falla en `npm ci` | `package-lock.json` desincronizado | `npm install` y commit |
| `build` no aparece en `develop` | Regla restrictiva a `main` | Es lo esperado; se ejecuta manual |
| `deploy` queda en manual | Marcador de HU-070 | Ejecutarlo a mano o esperar HU-070 |
