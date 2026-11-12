# Specs — Spec-Driven Development

Este directorio contiene una spec por HU, creada con
[GitHub Spec Kit](https://github.com/github/spec-kit).

## Estado

- **Spec Kit v1.2.5** inicializado en `.specify/` con integración `opencode` y scripts
  `sh`.
- **Comandos:** `.opencode/commands/speckit.*.md`.
- **Rama:** `branch_template: "feature/{number}-{slug}"`; el slug incluye el ID
  (`feature/002-hu-001-carga-imagen`, `feature/003-hu-002-deteccion`).
- **Estado:** todas las specs de HU-001 a HU-012 están fusionadas en `develop`.
  HU-013 es la única HU del M3-S2 sin spec; su carpeta será `014-hu-013-...`.
- **Pruebas:** la entrega exige **≥ 400 pruebas unitarias**; el reparto y los casos
  concretos viven en [`docs/curso/PLAN-PRUEBAS.md`](../docs/curso/PLAN-PRUEBAS.md).

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
- **Sin umbral de cobertura** por ahora; el requisito de la entrega es **≥ 400 pruebas
  unitarias**, no un porcentaje de cobertura.
- `CONSTITUTION.md` es la fuente; `.specify/memory/constitution.md` es un derivado con
  los principios no negociables y se sincroniza en el mismo commit.

## Specs existentes

| Spec | Estado |
|------|--------|
| `001-ta-contract-first` | Absorbida en P4; contrato implementado con HU-001 (PR #28) |
| `002-hu-001-carga-imagen` | Fusionada (PR #28) |
| `003-hu-002-deteccion` | Fusionada (PR #30) |
| `004-hu-003-visualizacion` | Fusionada (PR #33) |
| `005-hu-007-interfaz` | Fusionada (PR #35) |
| `006-hu-004-informe-sin-detecciones` | Fusionada (PR #34) |
| `007-hu-005-validacion-imagenes` | Fusionada (PR #39) |
| `008-hu-006-api-rest` | Fusionada (PR #42) |
| `009-hu-008-evaluacion` | Fusionada (PR #51); informe en `docs/evaluation/HU-008.md` |
| `010-hu-010-consumo-grpc` | Fusionada (PR #46) |
| `011-hu-012-calidad` | Fusionada (PR #49) |
| `012-hu-009-mlflow` | Fusionada (PR #50) |
| `013-hu-011-docker-cpu` | Fusionada (PR #52) |
| `014-hu-013-version-modelo` | En revisión (PR #54) |

> La numeración es secuencial por orden de creación, no por número de HU: `006`
> corresponde a HU-004 porque su spec se creó después de `005`. Desde el 12/11/2026
> la secuencia no tiene duplicados: `009`–`013` cubren HU-008, HU-010, HU-012, HU-009
> y HU-011, en ese orden de creación.
