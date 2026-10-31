# ADR 0004 — Gitflow, Spec Kit y estrategia de merge

- **Fecha:** 2026-10-31
- **Estado:** Aceptada
- **Decisores:** Grupo 4

## Contexto

El equipo necesita integrar trabajo de cuatro integrantes, mantener `main` estable
para las entregas y trazabilidad entre issues, specs y PRs. El curso exige PRs
revisadas y CI verde.

## Decisión

### Gitflow

- `main`: solo entregas de módulo.
- `develop`: integración diaria.
- Ramas de trabajo: `feature/*`, `fix/*`, `docs/*`, `refactor/*`, `test/*`, `chore/*`.
- Ramas de Spec Kit: `feature/{number}-{slug}` con el ID en el slug
  (`feature/001-hu-001-carga-imagen`).
- Toda rama vuelve a `develop` por PR; `develop → main` solo en entrega.

### Revisión

- Plantilla UAO obligatoria.
- Assignee = autor; reviewers = otros integrantes.
- Mínimo 1 aprobación; el autor nunca se autoaprueba.
- Code Reviewer designado: Guillermo; si él es autor, revisa otro integrante.
- CI verde y `make check` antes de fusionar.

### Merge

| Caso | Método |
|------|--------|
| PR a `develop` de un solo propósito | Squash |
| PR a `develop` con commits atómicos que conservar | Create a merge commit |
| Release `develop → main` | **Siempre merge commit**, nunca squash |

### Spec Kit

Flujo obligatorio por HU:

```text
issue → /speckit.specify → /speckit.clarify → /speckit.plan
      → /speckit.tasks → /speckit.analyze → /speckit.implement
      → make check → PR
```

- Una spec por HU en `specs/<NNN>-hu-xxx-slug/`.
- Los AC de la issue se copian a `spec.md`.
- `CONSTITUTION.md` es la fuente; `.specify/memory/constitution.md` es un derivado.
- Spec Kit v1.2.5 inicializado en `.specify/`; `branch_template` es
  `feature/{number}-{slug}` y los comandos viven en `.opencode/commands/`.

### Protección de ramas

La protección es una **regla escrita**. No se configura protección técnica en GitHub
por decisión del equipo.

## Alternativas consideradas

- **Trunk-based con `main` única:** más simple, pero sin integración estable para
  cuatro personas y entregas por módulo.
- **Gitflow completo con `release/*` y `hotfix/*`:** más ceremonial del necesario para
  el curso.
- **Squash siempre:** historial plano, pero pierde commits atómicos valiosos y hace
  divergir los releases.

## Consecuencias

- Los releases conservan historia; las PR simples no generan ruido.
- No hay push directo a `main` ni a `develop`.
- La trazabilidad issue → spec → PR → release queda documentada.

## Referencias

- `CONSTITUTION.md` §9 y §10.
- `CONTRIBUTING.md`.
- `.github/PULL_REQUEST_TEMPLATE.md`.
