# Espejo GitHub → GitLab (HU-065)

> **Qué es:** el workflow [`mirror-gitlab.yml`](../../.github/workflows/mirror-gitlab.yml)
> replica `develop` y `main` de GitHub en el proyecto GitLab
> `educacional-group/GPCICD_PPE_Detection` (id `89281003`) con el mismo SHA.
> **Por qué:** el 40 % de la rúbrica del M4 es el pipeline de GitLab, y debe ejecutar
> exactamente el commit que revisó y aprobó el equipo.

## 1. Regla de oro

**GitHub es la fuente de verdad.** No se comitea directo en GitLab: el espejo empuja en
una sola dirección y, si GitLab tiene un commit que GitHub no, el push falla y el
workflow lo muestra. El espejo de tipo *pull* que traía el proyecto (importación desde
GitHub) está **deshabilitado**, porque compite con este push y reescribe ramas.

## 2. Token: project access token con permiso mínimo

1. En GitLab: **Settings → Access tokens** del proyecto (o *Group → Access tokens*).
2. Crear un **project access token**:
   - Nombre: `github-mirror`
   - Rol: **Maintainer** (necesario para empujar a `main`, que está protegida)
   - Scopes: **`write_repository`** (nada más)
   - Caducidad: la mínima que permita la entrega; se rota al vencer.
3. Guardar el valor **una sola vez**: no se puede volver a ver.

El token no se versiona ni se pega en issues, PRs o logs.

## 3. Secret en GitHub

```bash
gh secret set GITLAB_TOKEN --repo GuillermoZ-Code/GPCICD_PPE_Detection
# pega el token cuando lo pida
gh secret list --repo GuillermoZ-Code/GPCICD_PPE_Detection
```

El workflow lo lee de `secrets.GITLAB_TOKEN`, lo enmascara con `::add-mask::` y lo pasa
a `git` con un `credential.helper`, nunca en la URL del remoto.

## 4. Flujo

```text
push a develop|main en GitHub
  → actions/checkout (fetch-depth: 0)
  → git push https://gitlab.com/educacional-group/GPCICD_PPE_Detection.git HEAD:<rama>
  → GET /projects/:id/repository/commits?ref_name=<rama>
  → compara con GITHUB_SHA y falla si no coincide
```

## 5. Verificación

```bash
# Último run del espejo
gh run list --workflow "Espejo GitLab" --limit 5

# SHA en GitLab (debe ser el mismo de GitHub)
glab api "projects/89281003/repository/commits?ref_name=develop&per_page=1"

# SHA en GitHub
git rev-parse origin/develop
```

Un run en verde implica que ambos SHA coinciden: el propio workflow lo comprueba y falla
si difieren.

## 6. Alineación inicial de `main` (una sola vez)

El proyecto GitLab tiene un commit `7a9b206b` («Update .gitlab-ci.yml file») creado por
web que GitHub no tiene; por eso `main` divergió y `import_status` quedó en `failed`.
GitHub es la fuente de verdad, así que se alinea una vez:

```bash
# Con el remoto gitlab configurado y credenciales de Maintainer
git push --force-with-lease gitlab origin/main:main
```

Después de esa alineación, el workflow empuja sin `--force` y solo avanza.

## 7. Diagnóstico

| Síntoma | Causa probable | Acción |
|---|---|---|
| `Falta el secret GITLAB_TOKEN` | No existe el secret o está vacío | `gh secret set GITLAB_TOKEN` |
| `403 Forbidden` al empujar | Token sin `write_repository` o sin rol Maintainer | Crear otro project access token |
| `! [rejected] (non-fast-forward)` | GitLab divergió (commit directo allí) | Revisar qué commit es; alinear desde GitHub |
| El SHA no coincide | El push falló pero el paso de verificación corrió con caché | Reejecutar el workflow; revisar el log del push |
| `import_status: failed` con «Could not update main» | Espejo *pull* activo | Deshabilitarlo en **Settings → Repository → Mirroring repositories** |

## 8. Deshabilitar el espejo *pull*

En **Settings → Repository → Mirroring repositories** se elimina o deshabilita el espejo
de importación desde GitHub. Motivo: el proyecto usa un espejo de *push* desde GitHub
Actions; dos mecanismos en direcciones distintas reescriben ramas y rompen el SHA.
