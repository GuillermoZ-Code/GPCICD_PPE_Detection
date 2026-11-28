# Implementation Plan: HU-069 — Aprovisionar el Droplet

**Branch**: `docs/070-hu-069-spec` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: Issue #125 y `specs/070-hu-069-droplet/spec.md`.

## Summary

Documentar la spec faltante de HU-069 y dejar trazabilidad entre los AC, el script
`deploy/droplet/provision.sh` y las pruebas existentes en `tests/test_deploy.py`.
No se cambia el comportamiento del aprovisionamiento.

## Technical Context

**Language/Version**: shell POSIX (`/bin/sh`), Ubuntu 24.04 LTS

**Primary Dependencies**: OpenSSH, UFW, fail2ban, Docker Engine y el plugin compose

**Testing**: pytest estático sobre el script; sin servidor, red ni credenciales

**Target Platform**: Droplet del curso

**Project Type**: infraestructura de despliegue

**Constraints**: sin secretos en el repositorio; sin puertos adicionales

**Scale/Scope**: 1 servidor, 1 usuario de despliegue, 3 puertos

## Constitution Check

- [x] Sin secretos versionados: la llave pública llega por `DEPLOY_PUBKEY`.
- [x] Sin pesos ni datos en Git.
- [x] Test-first: las pruebas de HU-069 ya existen y referencian cada AC.
- [x] Sin GPU ni red en la suite.
- [x] La spec se limita a documentar y trazar; no reescribe el script.
- [x] `make check` y `make specs-check` se ejecutan antes de la PR.

## Project Structure

```text
deploy/droplet/provision.sh       # existente; no se modifica
tests/test_deploy.py              # pruebas existentes de HU-069
docs/operacion/fallos.md          # diagnóstico del despliegue
specs/070-hu-069-droplet/
├── spec.md
├── plan.md
└── tasks.md
```

## Design decisions

1. **Reconstruir solo la spec.** El script está probado y fusionado; el hueco es
   documental y de trazabilidad. Reescribir el script añadiría riesgo sin beneficio.
2. **Mantener las pruebas existentes.** Seis pruebas cubren los tres AC; la issue
   fijó 12 como objetivo, pero la compuerta exige al menos una por AC.
3. **Documentar la deuda.** La spec declara que la documentación operativa vive en
   `docs/operacion/fallos.md` y que `docs/operacion/droplet.md` no se versionó.

## Risks

| Riesgo | Mitigación |
|--------|------------|
| Duplicar la spec de otra HU | Se usa el número 070 que la issue ya declaraba |
| Cambiar el script sin querer | La PR solo agrega archivos bajo `specs/` |
| Confundir 6 pruebas con las 12 objetivo | Se declara la diferencia en la spec |
| Aprobar sin revisar el script | El revisor comprueba las referencias `tests/test_deploy.py` |

## Testing strategy

```bash
uv run pytest tests/test_deploy.py -q
make specs-check
make trazabilidad-check
make check
uv build
```

## Phases

1. **Spec:** AC, escenarios, requisitos y tabla AC → prueba.
2. **Plan:** contexto, decisiones y riesgos.
3. **Tasks:** estado real de la implementación y cierre.
4. **Verificación:** compuertas locales y PR separada de HU-037.
