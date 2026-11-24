# Implementation Plan: HU-091 — Plantilla de issue HU con AC y DoR/DoD

**Branch**: `feature/092-hu-091-plantilla-hu` | **Date**: 2026-11-23

**Spec**: [spec.md](spec.md)

**Input**: Issue #147 y `specs/092-hu-091-plantilla-hu/spec.md`.

## Summary

Crear `.github/ISSUE_TEMPLATE/hu.yml` como issue form de GitHub con los seis campos que
la issue exige (historia, criterios de aceptación, SP Fibonacci, dependencias, spec y
pruebas objetivo) y los dos checklists de DoR/DoD. La plantilla se valida con pruebas
que cargan el YAML y comprueban el contrato de los issue forms, sin añadir
dependencias.

No se tocan las 100 issues existentes, ni los labels, ni el tablero.

## Technical Context

**Language/Version**: YAML 1.2 (issue forms de GitHub) validado desde Python 3.13

**Primary Dependencies**: PyYAML 6.0.3, ya presente como dependencia transitiva de
`pre-commit` (grupo `dev`) y `mlflow` (extra `tracking`); no se añade nada

**Storage**: archivo versionado en `.github/ISSUE_TEMPLATE/`

**Testing**: pytest con AAA; `Path` y `yaml.safe_load`; sin red

**Target Platform**: GitHub.com (formulario de issues)

**Project Type**: gobierno del repositorio (documentación operativa)

**Constraints**: no editar `docs/curso/backlog.md` ni `docs/curso/PRUEBAS.md`; no
reordenar el `Makefile`; una HU por PR

**Scale/Scope**: una plantilla para todas las HU del M4 en adelante

## Constitution Check

- [x] `uv` como único gestor; no se agregan dependencias.
- [x] Sin datos, pesos ni secretos en Git.
- [x] Test-first: cada AC tiene una prueba con `AC-0N` en el nombre o docstring.
- [x] Sin cambios en el contrato `ImageData → list[Detection]` ni en la inferencia.
- [x] Rutas bajo el dueño declarado en `propiedad.toml`
      (`.github/ISSUE_TEMPLATE/` → `jesusriverosUAO`).
- [x] Documentación y pruebas en español, identificadores en inglés.

## Project Structure

```text
.github/ISSUE_TEMPLATE/
├── hu.yml                    # nuevo: issue form de HU
├── bug_report.yml            # sin cambios
├── feature_request.yml       # sin cambios
├── spike.yml                 # sin cambios
└── config.yml                # sin cambios
tests/
└── test_issue_template.py    # nuevo: valida YAML y contrato del formulario
specs/092-hu-091-plantilla-hu/
├── spec.md
├── plan.md
└── tasks.md
```

## Design

### Estructura de `hu.yml`

```yaml
name: "HU — Historia de usuario"
description: "Plantilla de HU con AC, SP Fibonacci, dependencias, spec y DoR/DoD."
title: "[HU] "
body:
  - type: markdown        # recordatorio de Spec Kit y del tablero
  - type: textarea        # id: historia
  - type: textarea        # id: criterios  (AC-01, AC-02, ...)
  - type: dropdown        # id: sp        (1, 2, 3, 5, 8, 13)
  - type: input           # id: dependencias ("—" si no tiene)
  - type: input           # id: spec
  - type: input           # id: pruebas
  - type: checkboxes      # id: dor
  - type: checkboxes      # id: dod
```

- `title` es un prefijo `[HU] `; el autor lo reemplaza por `HU-NNN — título`, que es la
  convención de las 100 issues ya creadas.
- Todos los campos llevan `validations.required: true`; el de dependencias acepta `—`.
- Los `checkboxes` usan `options[].required: true` para que el autor no pueda enviar el
  formulario sin marcar la DoR y la DoD.
- El desplegable de SP solo ofrece la serie Fibonacci; no hay entrada libre.

### Pruebas

`tests/test_issue_template.py` carga el archivo una vez y valida:

1. `test_hu_template_is_valid_yaml` → AC-03: `yaml.safe_load` no lanza y devuelve un
   mapping.
2. `test_hu_template_form_contract` → AC-03: `name`, `description` y `body` presentes;
   tipos admitidos; cada elemento con `id`.
3. `test_hu_template_has_unique_field_ids` → AC-03: ids únicos.
4. `test_hu_template_requests_required_fields` → AC-01: historia, criterios, sp,
   dependencias, spec y pruebas, todos obligatorios.
5. `test_hu_template_uses_fibonacci_story_points` → AC-01: opciones exactamente
   `["1", "2", "3", "5", "8", "13"]`.
6. `test_hu_template_has_dor_and_dod_checklists` → AC-02: `dor` y `dod` con sus ítems y
   `required: true`.

### Alternativas descartadas

- **Plantilla Markdown (`.md`)**: GitHub no valida campos ni obligatoriedad; el autor
  puede dejar la HU sin AC ni SP.
- **Validar el YAML con un parser propio**: se descartó por frágil; PyYAML ya está en
  el entorno y evita falsos positivos.
- **Añadir PyYAML como dependencia**: implicaría `pyproject.toml` y `uv.lock`, que son
  de otro dueño; no hace falta porque ya está instalada de forma transitiva.

## Phases

1. **Tests first**: escribir las seis pruebas y confirmar que fallan porque `hu.yml` no
   existe.
2. **Implementación**: crear `.github/ISSUE_TEMPLATE/hu.yml` hasta poner la suite en
   verde.
3. **Cierre**: `make ownership-check`, `make check`, PR con la plantilla UAO y
   `Closes #147`.

## Risks

- **PyYAML transitiva**: si `pre-commit` o `mlflow` dejan de traerla, la prueba falla de
  forma visible. Se pedirá declararla en un PR del dueño de `uv.lock` si el equipo lo
  considera necesario.
- **`title` prellenado**: GitHub lo usa tal cual; el prefijo `[HU] ` obliga a escribir el
  número. Se documenta en la descripción del formulario.
- **Duplicidad con las 100 issues**: la plantilla no regenera issues; solo aplica a las
  nuevas. HU-089 valida las existentes.
