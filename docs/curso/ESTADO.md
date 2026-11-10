# Estado operativo — GPCICD PPE Detection

> **Qué es:** dónde quedó el proyecto, no qué se planeó.
> **Cómo se actualiza:** `make estado-write` regenera el bloque de abajo y, al cerrar
> cada sesión, se añade una entrada a la bitácora.
> **Fuente de verdad:** issues, tablero, `specs/` y `CONSTITUTION.md`. Este archivo no
> puede contradecirlos.
> **Caduca:** si el bloque tiene más de 3 días o no coincide con `git log`, regenéralo
> antes de actuar.

<!-- estado:inicio -->
**Generado:** 2026-11-10 02:35 UTC

**Rama:** `feature/004-hu-003-visualizacion` · limpia · +1/-0 vs `origin/develop`
**develop:** b9d3af6 (2026-11-09)

**Últimos commits:**
- `f2e1d13 feat(viz): dibujar detecciones y guardar imagenes anotadas`
- `b9d3af6 Merge pull request #32 from GuillermoZ-Code/fix/estado-parser-y-gh`
- `8f7f958 docs(estado): registrar la correccion y regenerar el bloque`
- `685de75 fix(estado): corregir el parser de SP y evitar escrituras sin gh`
- `f975019 Merge pull request #31 from GuillermoZ-Code/chore/contexto-agentes`

**Pull requests abiertas (0):**
- ninguna

**Issues abiertas: 13 · 18 SP**
- M3-S1 (7 SP): #3 #4 #5 #6 #7
- M3-S2 (8 SP): #8 #9 #10 #11 #12 #13
- M4-S3 (3 SP): #14 #15

**En revisión:** ninguna
**Siguiente por orden:** #3 HU-003 — Visualizar las detecciones sobre la imagen
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

### 2026-11-10 · Guillermo (OpenCode)

- **Hecho:** HU-003 implementada: `draw_detections`, etiquetas en español, escalado
  proporcional, flag `--annotated` y 13 pruebas nuevas (95 passed + 1 skipped).
- **En vuelo:** `feature/004-hu-003-visualizacion`, pendiente de PR.
- **Siguiente:** PR de HU-003 y, tras el merge, HU-004 o HU-007.
