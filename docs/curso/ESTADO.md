# Estado operativo — GPCICD PPE Detection

> **Qué es:** dónde quedó el proyecto, no qué se planeó.
> **Cómo se actualiza:** `make estado-write` regenera el bloque de abajo y, al cerrar
> cada sesión, se añade una entrada a la bitácora.
> **Fuente de verdad:** issues, tablero, `specs/` y `CONSTITUTION.md`. Este archivo no
> puede contradecirlos.
> **Caduca:** si el bloque tiene más de 3 días o no coincide con `git log`, regenéralo
> antes de actuar.

<!-- estado:inicio -->
**Generado:** 2026-11-10 03:31 UTC

**Rama:** `docs/estado-post-merge` · 8 archivo(s) sin commit · +0/-0 vs `origin/develop`
**develop:** 976437d (2026-11-09)

**Últimos commits:**
- `976437d Merge pull request #35 from GuillermoZ-Code/feature/005-hu-007-interfaz`
- `cbb91e0 Merge branch 'develop' into feature/005-hu-007-interfaz`
- `c1fbcc4 Merge pull request #36 from GuillermoZ-Code/docs/estado-sesion`
- `ad9a801 feat(frontend): agregar make frontend-dev y frontend-preview`
- `8018055 docs(estado): regenerar bloque de estado`

**Pull requests abiertas (0):**
- ninguna

**Issues abiertas: 10 · 14 SP**
- M3-S1 (3 SP): #5 #6
- M3-S2 (8 SP): #8 #9 #10 #11 #12 #13
- M4-S3 (3 SP): #14 #15

**En revisión:** ninguna
**Siguiente por orden:** #5 HU-005 — Validar las imágenes recibidas
<!-- estado:fin -->

## Bitácora de sesiones

> Una entrada por sesión. Tres líneas: **hecho**, **en vuelo**, **siguiente**.
> No se borra: es el historial de dónde quedó cada quien.

### 2026-11-09 · Guillermo (OpenCode)

- **Hecho:** revisión de #28 y #30; 6 commits de corrección; ambas PRs fusionadas y
  issues #1 y #2 cerradas.
- **En vuelo:** ninguna PR de código abierta; queda este PR de contexto para agentes.
- **Siguiente:** abrir HU-003 (depende de #2, ya cerrada) con Spec Kit.

### 2026-11-10 · Guillermo (OpenCode)

- **Hecho:** corregido el parser de SP (HU-015 daba 3), bloqueada la escritura sin `gh`,
  arreglado el comando de la constitución y añadidas 4 pruebas.
- **En vuelo:** `fix/estado-parser-y-gh`, pendiente de PR.
- **Siguiente:** fusionar la corrección y abrir HU-003 con Spec Kit.

### 2026-11-10 · Guillermo (OpenCode) — HU-003

- **Hecho:** HU-003 implementada: `draw_detections`, etiquetas en español, escalado
  proporcional, flag `--annotated` y 13 pruebas nuevas (95 passed + 1 skipped).
- **En vuelo:** `feature/004-hu-003-visualizacion`, pendiente de PR.
- **Siguiente:** PR de HU-003 y, tras el merge, HU-004 o HU-007.

### 2026-11-10 · Guillermo (OpenCode)

- **Hecho:** HU-007 con SPA React + Vite + TypeScript: cliente HTTP y simulado, 19
  pruebas, job de CI y ADR 0006; cerrada la issue #3 al fusionar #33.
- **En vuelo:** `feature/005-hu-007-interfaz`, pendiente de PR; PR #34 (HU-004) abierta.
- **Siguiente:** PR de HU-007 y revisar #34 de Eliana.

### 2026-11-10 · Guillermo (OpenCode) — cierre post-merge

- **Hecho:** #34 y #35 fusionadas; issues #4 y #7 cerradas; spec de HU-004 renumerada a
  `006`; README, M3, specs y backlog sincronizados.
- **En vuelo:** ninguna PR; rama `docs/estado-post-merge` pendiente de revisión.
- **Siguiente:** HU-005 y HU-006 (Hernán); Guillermo pasa a HU-015 en el M4.

### 2026-11-10 · Hernán (OpenCode) — HU-005

- **Hecho:** validación de imágenes (JPEG/PNG, 10 MB, vacío/corrupto) con 7 pruebas;
  spec 007 y contrato actualizado.
- **En vuelo:** PR #39 (`feature/007-hu-005-validacion-imagenes`), pendiente de revisión.
- **Siguiente:** HU-006 (API REST) tras el merge.
