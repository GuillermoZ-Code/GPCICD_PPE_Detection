# Specs — Spec-Driven Development

Este directorio contiene una spec por HU, creada con
[GitHub Spec Kit](https://github.com/github/spec-kit).

## Estado

- **Spec Kit v1.2.5** inicializado en `.specify/` con integración `opencode` y scripts
  `sh`.
- **Comandos:** `.opencode/commands/speckit.*.md`.
- **Rama:** `branch_template: "feature/{number}-{slug}"`; el slug incluye el ID
  (`feature/001-hu-001-carga-imagen`, `feature/002-ta-11-contract-first`).
- **Spec de ejemplo:** `001-ta-contract-first/` (borrador, sin implementar).

## Flujo por HU

```text
issue → /speckit.specify → /speckit.clarify → /speckit.plan
      → /speckit.tasks → /speckit.analyze → /speckit.implement
      → make check → PR a develop
```

## Convención

- Carpeta: `specs/<NNN>-hu-xxx-slug/` o `specs/<NNN>-ta-xx-slug/`.
- Archivos: `spec.md`, `plan.md`, `tasks.md`.
- Los AC de la issue se copian a `spec.md`; issue y spec se enlazan.
- `CONSTITUTION.md` es la fuente; `.specify/memory/constitution.md` es un derivado con
  los principios no negociables y se sincroniza en el mismo commit.

## Specs existentes

| Spec | Estado |
|------|--------|
| `001-ta-contract-first` | Borrador para validación de Jesús; sin implementar |
