# Implementation Plan: HU-107 — Definición de Ready y Done del M4

**Branch**: `feature/108-hu-107-dor-dod` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #163 y `specs/108-hu-107-dor-dod/spec.md`.

## Summary

Añadir a `CONTRIBUTING.md` una sección de criterios de entrada (DoR) y salida (DoD) con
al menos cinco puntos cada una, enlazada desde la tabla de contenidos. Un archivo de
pruebas nuevo valida que las dos listas existen, que cubren los cinco puntos de cada AC y
que cada criterio es una casilla marcable.

## Technical Context

**Language/Version**: Markdown + Python 3.13 para las pruebas

**Primary Dependencies**: solo la biblioteca estándar (`pathlib`, `re`); sin
dependencias nuevas

**Storage**: `CONTRIBUTING.md` versionado

**Testing**: pytest con AAA; lectura de archivos con `Path`; sin red

**Target Platform**: repositorio (documentación de proceso)

**Project Type**: gobierno del repositorio

**Constraints**: una HU por PR; no tocar `docs/curso/ESTADO.md`, `backlog.md` ni
`PRUEBAS.md`; no reescribir el resto de `CONTRIBUTING.md`

**Scale/Scope**: una sección y una entrada en la tabla de contenidos

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Cada AC tiene una prueba que lo referencia (documentación: pruebas estructurales).
- [x] Sin cambios en el contrato `ImageData → list[Detection]`.
- [x] `CONTRIBUTING.md` no tiene dueño en `propiedad.toml`: archivo libre.
- [x] Documentación en español, identificadores de código en inglés.

## Project Structure

```text
CONTRIBUTING.md                 # sección nueva + entrada en la tabla de contenidos
tests/test_dor_dod.py           # nuevo: valida DoR, DoD y sus casillas
specs/108-hu-107-dor-dod/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Sección nueva de `CONTRIBUTING.md`

```markdown
## 🚦 Criterios de entrada y salida (DoR / DoD)

### Definition of Ready (DoR)
- [ ] Spec creada con `/speckit.specify` en `specs/NNN-hu-xxx-slug/`.
- [ ] Criterios de aceptación (AC) escritos y numerados en la issue y en la spec.
- [ ] Story Points estimados con la serie Fibonacci, con dueño asignado.
- [ ] Dependencias identificadas (`—` si no tiene).
- [ ] Rama `feature/NNN-hu-xxx-slug` creada desde `develop`.
- [ ] `make ownership-check` sin bloqueos.

### Definition of Done (DoD)
- [ ] Cada AC tiene al menos una prueba que lo referencia (`AC-0N` en el nombre o docstring).
- [ ] `make check` en verde y CI en verde.
- [ ] PR con una aprobación de otro integrante (el autor nunca se autoaprueba).
- [ ] Issue cerrada a mano y HU movida a Done en el tablero.
- [ ] Conteo de pruebas actualizado en `docs/curso/PRUEBAS.md` por su dueño.
```

Los ítems coinciden con los de la plantilla de HU-091 (#147) en redacción, pero esta HU
no lee ese archivo: la plantilla sigue en revisión y acoplar la prueba a una rama sin
fusionar dejaría la suite en rojo. La comprobación automática entre guía y formulario
queda como HU posterior.

### Pruebas

`tests/test_dor_dod.py`:

1. `test_dor_lists_entry_criteria` → AC-01: la sección DoR menciona spec, AC, SP,
   dueño y dependencias, con al menos cinco casillas.
2. `test_dod_lists_exit_criteria` → AC-02: la sección DoD menciona pruebas, `make
   check`, aprobación, issue y conteo, con al menos cinco casillas.
3. `test_contributing_has_dor_dod_sections` → AC-03: encabezados y enlace en la tabla
   de contenidos.
4. `test_dor_and_dod_items_are_checkboxes` → AC-03: cada criterio es una casilla
   marcable.

### Alternativas descartadas

- **Poner la DoR/DoD solo en el README**: se descartó porque `CONTRIBUTING.md` es el
  documento de proceso que ya lee quien va a abrir una PR.
- **Duplicar la lista sin prueba**: se descartó; las pruebas verdes exigen los cinco
  puntos de cada lado y que todo sea casilla.
- **Acoplar la prueba a `.github/ISSUE_TEMPLATE/hu.yml`**: se descartó porque ese archivo
  llega con HU-091 (#147), que aún está en revisión.

## Phases

1. **Tests first**: escribir las cuatro pruebas y confirmar que fallan porque la sección
   no existe.
2. **Implementación**: añadir la sección y la entrada en la tabla de contenidos.
3. **Cierre**: `make ownership-check`, `make check`, PR con la plantilla UAO y
   `Closes #163`.

## Risks

- **Duplicación con la plantilla**: guía y formulario comparten redacción; si uno cambia,
  el otro puede quedar atrás. La comprobación cruzada se hará cuando #147 esté fusionada.
- **`CONTRIBUTING.md` desactualizado en otros temas** (menciona `specs/001–005`, M3 y
  `make estado-write` al cierre): no se corrige en esta HU para no mezclar propósitos;
  se reporta como observación en la issue.
