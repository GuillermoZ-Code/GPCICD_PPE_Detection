# Estado operativo — GPCICD PPE Detection

> **Qué es:** dónde quedó el proyecto, no qué se planeó.
> **Cómo se actualiza:** `make estado-write` regenera el bloque de abajo y, al cerrar
> cada sesión, se añade una entrada a la bitácora.
> **Fuente de verdad:** issues, tablero, `specs/` y `CONSTITUTION.md`. Este archivo no
> puede contradecirlos.
> **Caduca:** si el bloque tiene más de 3 días o no coincide con `git log`, regenéralo
> antes de actuar.

<!-- estado:inicio -->
**Generado:** 2026-11-10 03:11 UTC

**Rama:** `feature/005-hu-007-interfaz` · 5 archivo(s) sin commit · +4/-0 vs `origin/develop`
**develop:** c7ae721 (2026-11-09)

**Últimos commits:**
- `8d3f09d docs(estado): registrar el avance de HU-007`
- `a403a52 docs(proceso): cerrar la issue al fusionar en develop`
- `3edd27f docs(web): registrar el stack React en la constitucion y el ADR 0006`
- `b74f0b8 feat(web): interfaz React con cliente de inferencia y pruebas`
- `c7ae721 Merge pull request #33 from GuillermoZ-Code/feature/004-hu-003-visualizacion`

**Pull requests abiertas (2):**
- #35 feat(web): interfaz React con cliente de inferencia y pruebas → `develop` · revisión: — · CI: ok
- #34 feat(results): contrato y mensaje de resultado vacío de EPP (HU-004) → `develop` · revisión: — · CI: —

**Issues abiertas: 12 · 17 SP**
- M3-S1 (6 SP): #4 #5 #6 #7
- M3-S2 (8 SP): #8 #9 #10 #11 #12 #13
- M4-S3 (3 SP): #14 #15

**En revisión:** #7 (PR #35), #4 (PR #34)
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
