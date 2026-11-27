---
description: "Task list for HU-049 - Decisión y configuración de exposición de gRPC"
---

# Tasks: HU-049 - Decisión y configuración de exposición de gRPC

**Input**: `specs/050-hu-049-exposicion-grpc/spec.md` y `plan.md`.

**Prerequisites**: issue #105, rama `feature/050-hu-049-exposicion-grpc`, tarjeta #105 en *In progress* (WIP 1 verificado).

**Tests**: obligatorias y **antes** de la implementación (test-first).

## Phase 1: Setup

- [x] T001 Revisar #105, #97 (HU-041, *Done*) y la propiedad de archivos.
- [x] T002 Crear spec, plan y tareas.
- [x] T003 Mover #105 a **In progress** en el tablero (WIP 1).
- [x] T004 Crear la rama desde `develop` actualizado.

## Phase 2: Tests first (deben fallar)

- [x] T005 [AC-01] `test_ac_01_decision_con_riesgos_y_alternativa`: ADR con decisión, riesgos y alternativa h2c/mTLS.
- [x] T006 [AC-02] `test_ac_02_puerto_9000_no_publicado`: Compose expone 9000 sin mapearlo al host.
- [x] T007 [AC-02] `test_ac_02_proxy_sin_ruta_grpc`: Caddyfile sin `/grpc`, `h2c` ni 9000.
- [x] T008 [AC-03] `test_ac_03_firewall_coherente`: UFW solo 22/80/443, sin 9000.

## Phase 3: Implementación (documentación)

- [ ] T009 Crear `docs/adr/0010-exposicion-grpc.md` con contexto, decisión, alternativas, consecuencias y referencias.
- [ ] T010 Añadir la entrada de ADR 0010 en `docs/adr/README.md`.

## Phase 4: Validación y entrega

- [ ] T011 Ejecutar pruebas dirigidas y completas; Ruff, formato, `ty`, specs y propiedad.
- [ ] T012 Commit convencional y push de la rama.
- [ ] T013 Abrir PR a `develop` con plantilla UAO, `Closes #105` y revisor Guillermo por propiedad de `docs/adr/`.
- [ ] T014 Mover #105 a *In review* y dejar la PR sin fusionar ni autoaprobar.
