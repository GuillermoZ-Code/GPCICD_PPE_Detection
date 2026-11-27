# Tasks: HU-069 — Aprovisionar el Droplet

**Input**: `specs/070-hu-069-droplet/spec.md` y `plan.md`.

**Prerequisites**: script `deploy/droplet/provision.sh` y pruebas de
`tests/test_deploy.py` ya fusionados.

## Phase 1: Reconstrucción documental

- [x] T001 Crear `specs/070-hu-069-droplet/spec.md` con los AC de #125.
- [x] T002 Crear `plan.md` con decisiones, riesgos y verificación.
- [x] T003 Crear `tasks.md` con el estado real de la HU.

## Phase 2: Trazabilidad

- [x] T004 Enlazar AC-01 con las pruebas de usuario y SSH.
- [x] T005 Enlazar AC-02 con las pruebas de UFW y fail2ban.
- [x] T006 Enlazar AC-03 con las pruebas de idempotencia y directorios.
- [x] T007 Declarar que `docs/operacion/droplet.md` no se versionó y que el
  diagnóstico vive en `docs/operacion/fallos.md`.

## Phase 3: Verificación

- [x] T008 Ejecutar `uv run pytest tests/test_deploy.py -q`.
- [x] T009 Ejecutar `make specs-check`.
- [x] T010 Ejecutar `make trazabilidad-check` con la spec presente.
- [x] T011 Ejecutar `make check` y `uv build`.
- [ ] T012 Abrir PR separada con `Refs #125`, sin mezclarla con HU-037.

## Notes

- No se modifica `deploy/droplet/provision.sh` ni las pruebas.
- La spec es histórica: #125 ya está cerrada; se agrega para que la compuerta
  `Matriz` no quede roja por un artefacto faltante.
- La spec declara 6 pruebas existentes; la issue fijó 12 como objetivo, pero no se
  inventan pruebas ni se reabre la issue en esta PR.
