# ADR 0007 — GitLab CI/CD con espejo desde GitHub

- **Fecha:** 2026-11-25
- **Estado:** Aceptada
- **Decisores:** Grupo 4
- **Evidencia:** HU-065 (#121), `.github/workflows/mirror-gitlab.yml`,
  [`docs/operacion/gitlab-espejo.md`](../operacion/gitlab-espejo.md)
- **Relacionada:** ADR 0004 (Gitflow, Spec Kit y merge)

> Los números 0007 y 0008 quedaron libres cuando se escribieron los ADR 0009 y 0011.
> Se usan aquí por trazabilidad con HU-085; la numeración no se reordena.

## Contexto

La rúbrica del M4 exige un pipeline de GitLab con compuertas de calidad, build de imagen
y despliegue. El equipo trabaja en GitHub (issues, PRs, revisiones, MCP) y no quiere
duplicar la operación diaria en dos forjas.

GitLab ofrece espejo de repositorios, pero el espejo *pull* (GitLab importa desde GitHub)
y las reglas de espejo más cómodas viven en **GitLab Premium**. El plan gratuito permite
un proyecto privado con CI/CD, registry y packages.

## Decisión

**GitHub sigue siendo la fuente de verdad y GitLab ejecuta el pipeline**, alimentado por un
espejo de *push* desde GitHub Actions.

- `.github/workflows/mirror-gitlab.yml` empuja `develop` y `main` a
  `gitlab.com/educacional-group/GPCICD_PPE_Detection` en cada push.
- El workflow **verifica** con la API de GitLab que el último commit de la rama coincide
  con `GITHUB_SHA`; si no, falla.
- El token es un *project access token* con **solo** `write_repository`, guardado como
  `secrets.GITLAB_TOKEN`.
- El espejo *pull* del proyecto queda **deshabilitado**: dos mecanismos en direcciones
  opuestas reescriben ramas y rompen la trazabilidad del SHA.
- No se comitea directamente en GitLab; si alguien lo hace, el push falla y se alinea
  desde GitHub.

## Alternativas consideradas

### GitLab Premium con espejo *pull* nativo

- **A favor:** configuración en la UI y sin workflow propio.
- **En contra:** costo por usuario; el curso no lo provee y la cuenta es gratuita.
- **Decisión:** descartado.

### Sincronización manual (`git push gitlab`)

- **A favor:** cero infraestructura.
- **En contra:** depende de que alguien recuerde hacerlo; el pipeline puede correr sobre
  un commit viejo y la evidencia deja de ser confiable.
- **Decisión:** descartado.

### Migrar todo el desarrollo a GitLab

- **A favor:** una sola forja y espejo innecesario.
- **En contra:** pierde el flujo ya montado en GitHub (PRs, CODEOWNERS, MCP, tablero,
  Actions) a una semana de la entrega.
- **Decisión:** descartado para el M4.

### Webhook propio o *mirror* con servicio externo

- **A favor:** control total.
- **En contra:** un servicio más que operar y autenticar; el runner de GitHub ya existe.
- **Decisión:** descartado.

## Consecuencias

- El SHA del pipeline de GitLab es trazable contra la PR y el commit de GitHub (AC-02 de
  HU-065).
- El pipeline de GitLab no necesita credenciales de GitHub: el repositorio es público y
  el push lo hace Actions con un token de escritura mínimo.
- Si GitHub Actions falla, GitLab se queda atrás de forma visible; no hay silencio.
- El proyecto GitLab conserva `backup/gitlab-ci-web` con el commit que existía solo allí
  antes de alinear `main`.
- Rotar el token es una tarea de operación: expira el 31/12/2026 y se reemplaza en
  **Settings → Access tokens** + `gh secret set GITLAB_TOKEN`.

## Referencias

- HU-065 (#121) y su runbook [`docs/operacion/gitlab-espejo.md`](../operacion/gitlab-espejo.md).
- HU-066 (#122): `.gitlab-ci.yml` con stages, cachés y reglas.
- `CONSTITUTION.md` §7 y §11.
- ADR 0004 — Gitflow y estrategia de merge.
