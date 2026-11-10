# Specs — Spec-Driven Development

Este directorio contiene una spec por HU, creada con
[GitHub Spec Kit](https://github.com/github/spec-kit).

## Estado

- **Spec Kit v1.2.5** inicializado en `.specify/` con integración `opencode` y scripts
  `sh`.
- **Comandos:** `.opencode/commands/speckit.*.md`.
- **Rama:** `branch_template: "feature/{number}-{slug}"`; el slug incluye el ID
  (`feature/002-hu-001-carga-imagen`, `feature/003-hu-002-deteccion`).
- **Specs en curso:** `004-hu-004-informe-sin-detecciones` (PR #34, rama
  `feature/004-hu-004-...`, revisor: Guillermo).

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
- **Test-first:** cada AC tiene al menos una prueba pytest que lo referencia; las
  pruebas se escriben antes de la implementación. Excepciones: SPI y specs de
  documentación. `/speckit.analyze` marca error si un AC no tiene prueba.
- **Sin umbral de cobertura** por ahora; se decide en HU-012.
- `CONSTITUTION.md` es la fuente; `.specify/memory/constitution.md` es un derivado con
  los principios no negociables y se sincroniza en el mismo commit.

## Specs existentes

| Spec | Estado |
|------|--------|
| `001-ta-contract-first` | Borrador; el contrato se implementó con la carga de HU-001 |
| `002-hu-001-carga-imagen` | Implementada en `feature/002-hu-001-carga-imagen` (PR #28) |
| `003-hu-002-deteccion` | Implementada en `feature/003-hu-002-deteccion` (PR #30) |
| `004-hu-003-visualizacion` | Implementada en `feature/004-hu-003-visualizacion` (PR #33) |
| `004-hu-004-informe-sin-detecciones` | En revisión (PR #34); numeración 004 compartida con HU-003 por creación en paralelo |
