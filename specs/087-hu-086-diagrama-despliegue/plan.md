# Implementation Plan: HU-086 — Diagrama de arquitectura de despliegue

**Branch**: `feature/087-hu-086-diagrama-despliegue` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: `specs/087-hu-086-diagrama-despliegue/spec.md`

## Summary

Actualizar la fuente `docs/architecture/arquitectura.json` para mostrar la cadena
GitHub → GitLab → Registry → Droplet → usuario, con Caddy, puertos, secretos y
healthchecks; regenerar el HTML con Archify y proteger los tres AC con cuatro pruebas
estáticas.

## Technical Context

**Language/Version**: JSON + Markdown; Python 3.13 para pruebas

**Primary Dependencies**: Archify skill oficial (CLI `archify.mjs`, copia temporal)

**Storage**: `docs/architecture/arquitectura.json` (fuente) y `arquitectura.html` (artefacto)

**Testing**: pytest estático sobre JSON, HTML y README

**Target Platform**: documentación del repositorio

**Project Type**: documentación de arquitectura

**Performance Goals**: N/A

**Constraints**: no editar el HTML a mano; no valores de secretos; no tocar `deploy/*`;
`docs/architecture/` es de Guillermo (revisión obligatoria)

**Scale/Scope**: 1 JSON actualizado, 1 HTML regenerado, 1 README ajustado, 4 pruebas

## Constitution Check

- **Spec Kit antes de implementar**: spec/plan/tasks creados antes del código. ✅
- **Test-first**: cuatro pruebas referencian AC-01/AC-02/AC-03. ✅
- **Sin secretos**: solo nombres de variables. ✅
- **Propiedad**: `docs/architecture/` y `specs/` generan aviso de CODEOWNERS; se pide
  revisión a Guillermo. No se tocan scripts. ✅
- **Una HU por PR**. ✅

## Project Structure

```text
docs/architecture/arquitectura.json      # fuente actualizada
docs/architecture/arquitectura.html      # regenerado con Archify
docs/architecture/README.md              # lectura del flujo de despliegue
tests/test_arquitectura_despliegue.py    # 4 pruebas estáticas
specs/087-hu-086-diagrama-despliegue/    # spec/plan/tasks
```

## Design decisions

1. **La fuente manda.** El HTML es un artefacto generado; todo cambio semántico va en
   el JSON y se regenera con `finalize architecture --quality showcase`.
2. **Cadena de entrega explícita.** Se separan GitHub, GitLab y Registry en lugar de
   un genérico «CI/CD», para que el evaluador vea el espejo y la publicación de imágenes.
3. **Secretos como nombres.** El diagrama lista `SSH_KEY`, `DOCKERHUB_TOKEN` y
   `PPE_AUTH_HASH` sin valores, igual que el runbook de HU-055.
4. **Puertos y healthchecks en tarjetas.** Evita saturar el grafo y mantiene legible el
   contrato: 80/443 públicos, 8000/9000 internos, `/health` y `/health/ready`.
5. **Sin cambios de plataforma.** `deploy/`, `.gitlab-ci.yml` y `compose.prod.yml`
   quedan intactos: esta HU solo documenta lo ya implementado.

## Risks

| Riesgo | Mitigación |
|---|---|
| El HTML se genera con una versión distinta de Archify | Usar el skill oficial descargado a temp y registrar el comando exacto |
| El diagrama contradiga el runbook | Las pruebas comparan nombres con `docs/operacion/despliegue.md` |
| CODEOWNERS pida revisión de Guillermo | Se añade como reviewer en la PR; no se fusiona sin aprobación |
| Secretos mal interpretados | Prueba que prohíbe valores y permite solo nombres de variables |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_arquitectura_despliegue.py::test_ac_01_cadena_de_despliegue` |
| AC-02 | `tests/test_arquitectura_despliegue.py::test_ac_02_secretos_puertos_y_healthchecks` |
| AC-03 | `tests/test_arquitectura_despliegue.py::test_ac_03_fuente_json_versionada` |
| AC-01/03 | `tests/test_arquitectura_despliegue.py::test_html_regenerado_contiene_cadena` |
