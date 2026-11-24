# Implementation Plan: HU-105 — Milestones y labels de las nuevas épicas

**Branch**: `feature/106-hu-105-milestones-labels` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #161 y `specs/106-hu-105-milestones-labels/spec.md`.

## Summary

Completar `.github/labels.yml` con las diez épicas que faltan (`ep-06`…`ep-15`) y la
prioridad `could-have`, con color y descripción reales en lugar de las etiquetas grises
genéricas que GitHub tiene hoy. Cerrar los milestones `M3-S1` y `M3-S2`, que ya no
tienen issues abiertas. Un archivo de pruebas valida el catálogo y el formato.

## Technical Context

**Language/Version**: YAML + Python 3.13 para las pruebas

**Primary Dependencies**: PyYAML (transitiva de `pre-commit`); sin dependencias nuevas

**Storage**: `.github/labels.yml` versionado; GitHub como destino de la sincronización

**Testing**: pytest con AAA; `yaml.safe_load` y `re`; sin red

**Target Platform**: GitHub.com (labels y milestones)

**Project Type**: gobierno del repositorio

**Constraints**: no borrar etiquetas (`skip-delete: true`); no renombrar `ep-01`…`ep-05`;
no tocar issues ni el tablero

**Scale/Scope**: 11 etiquetas nuevas y 2 milestones cerrados

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Cada AC tiene una prueba o una verificación manual documentada.
- [x] Sin cambios en el contrato `ImageData → list[Detection]`.
- [x] `docs/curso/backlog.md` y `PRUEBAS.md` no se tocan.
- [x] `.github/labels.yml` no está en `[[locked]]`: se puede editar con revisión del
      dueño de `.github/`.

## Project Structure

```text
.github/labels.yml              # + ep-06 … ep-15 y could-have
tests/test_labels.py            # nuevo: catálogo y formato
specs/106-hu-105-milestones-labels/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Etiquetas nuevas

| Etiqueta | Color | Descripción |
|----------|-------|-------------|
| `ep-06` | `1d76db` | EP-06 — CI/CD y pipeline (GitLab) |
| `ep-07` | `0e8a16` | EP-07 — Despliegue e infraestructura |
| `ep-08` | `b60205` | EP-08 — Seguridad y cumplimiento |
| `ep-09` | `fbca04` | EP-09 — Modelo y evaluación |
| `ep-10` | `5319e7` | EP-10 — Servicio, API y MaaS |
| `ep-11` | `f9d0c4` | EP-11 — Interfaz web (SPA) |
| `ep-12` | `c2e0c6` | EP-12 — Herramientas para agentes |
| `ep-13` | `bfdadc` | EP-13 — Observabilidad y operación |
| `ep-14` | `c5def5` | EP-14 — Gobierno técnico y trazabilidad |
| `ep-15` | `fef2c0` | EP-15 — Documentación y entrega |
| `could-have` | `ededed` | Requisito opcional de la rúbrica |

- Los colores se eligen distintos entre épicas; se reutilizan los de `ep-01`…`ep-05`
  solo donde el matiz ya está asociado al área.
- `skip-delete: true` sigue vigente: la sincronización crea y actualiza, no borra.

### Pruebas

`tests/test_labels.py`:

1. `test_labels_is_a_list_of_mappings` → AC-02: el archivo es una lista de mappings.
2. `test_labels_have_unique_name_color_and_description` → AC-03: nombre único, color de
   seis hexadecimales y descripción no vacía.
3. `test_labels_cover_all_epics` → AC-01: `ep-01`…`ep-15` presentes.
4. `test_labels_cover_priorities` → AC-01: `must-have`, `should-have`, `could-have`.

### Cierre de milestones

```bash
gh api -X PATCH repos/GuillermoZ-Code/GPCICD_PPE_Detection/milestones/1 -f state=closed
gh api -X PATCH repos/GuillermoZ-Code/GPCICD_PPE_Detection/milestones/2 -f state=closed
```

Se hace después de confirmar que ambos tienen `open_issues: 0`.

### Alternativas descartadas

- **Crear las etiquetas solo por `gh label create`**: se descartó porque el workflow
  `Labels` las volvería a crear en el siguiente push; la fuente debe ser el archivo.
- **Borrar y recrear `ep-06`…`ep-15`**: se descartó porque las 100 issues ya las usan y
  se perdería la asociación.

## Phases

1. **Tests first**: escribir las cuatro pruebas y confirmar que fallan por el catálogo
   incompleto.
2. **Implementación**: completar `labels.yml`.
3. **GitHub**: cerrar `M3-S1` y `M3-S2`.
4. **Cierre**: `make ownership-check`, `make check`, PR y `Closes #161`.

## Risks

- **Dueño de `.github/`**: la edición de `labels.yml` genera aviso de propiedad y exige
  revisión de Guillermo; no bloquea.
- **Colores**: si dos épicas comparten color, no es un error de GitHub, pero la prueba no
  lo exige; se documenta la tabla para mantener el criterio.
- **Sincronización**: hasta que el PR se fusione, GitHub conserva las etiquetas grises;
  el cambio real en GitHub ocurre con el workflow tras el merge.
