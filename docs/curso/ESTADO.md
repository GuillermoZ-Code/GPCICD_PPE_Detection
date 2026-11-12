# Estado operativo — GPCICD PPE Detection

> **Qué es:** dónde quedó el proyecto, no qué se planeó.
> **Cómo se actualiza:** `make estado-write` regenera el bloque de abajo y, al cerrar
> cada sesión, se añade una entrada a la bitácora.
> **Fuente de verdad:** issues, tablero, `specs/` y `CONSTITUTION.md`. Este archivo no
> puede contradecirlos.
> **Caduca:** si el bloque tiene más de 3 días o no coincide con `git log`, regenéralo
> antes de actuar.

<!-- estado:inicio -->
**Generado:** 2026-11-12 18:32 UTC

**Rama:** `docs/estado-post-54` · 1 archivo(s) sin commit · +1/-0 vs `origin/develop`
**develop:** 6496621 (2026-11-12)

**Últimos commits:**
- `7d16381 docs(estado): cerrar HU-013 y actualizar el M3`
- `6496621 Merge pull request #54 from GuillermoZ-Code/feature/014-hu-013-version-modelo`
- `993805a docs(estado): registrar cierre de sesion`
- `0cae6f0 docs(hu-013): registrar la PR #54`
- `35ab8d1 feat(version): exponer version verificable del modelo (HU-013)`

**Pull requests abiertas (1):**
- #55 docs(estado): cerrar HU-013 y actualizar el M3 → `develop` · revisión: — · CI: ok

**Issues abiertas: 2 · 3 SP**
- M4-S3 (3 SP): #14 #15

**En revisión:** ninguna
**Siguiente por orden:** #14 HU-014 — Publicar versiones mediante un pipeline CI/CD con compuertas de calidad
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

### 2026-11-10 · Hernán (OpenCode) — HU-006

- **Hecho:** API FastAPI con `POST /predict`, validación de HU-005, detector
  inyectable, CORS y OpenAPI; 9 pruebas y spec 008.
- **En vuelo:** PR #42 (`feature/008-hu-006-api-rest`), pendiente de revisión.
- **Siguiente:** HU-012 o integración del frontend con la API real.

### 2026-11-10 · Eliana (OpenCode) — HU-010

- **Hecho:** HU-010 implementada con Spec Kit: contrato `ppe.v1` (`ppe.proto` +
  stubs regenerables con `make protos`), servidor y cliente de prueba que
  reutilizan `validate_image_bytes` (HU-005), el `Detector` del ADR 0005 y
  `build_inference_result` (HU-004); configuración compartida extraída a
  `detector_config` (también usa REST); 9 pruebas nuevas (135 passed + 1
  skipped) y demo e2e verificada con `FakeDetector`.
- **En vuelo:** PR #46 (`feature/009-hu-010-consumo-grpc`), revisión pendiente de
  Guillermo.
- **Siguiente:** revisión de Guillermo; tras el merge, HU-011 gana su
  dependencia gRPC.

### 2026-11-10 · Jesús (OpenCode) — HU-009

- **Hecho:** HU-009 implementada con Spec Kit: extra opcional `tracking` con MLflow
  3.18, módulo `tracking/` (payload, tracker, comparación y CLI), 11 pruebas y runbook
  `docs/operacion/mlflow.md`; `make check` 155 passed + 1 skipped y `uv build` en verde.
  Dos runs reales registrados y comparados en `sqlite:///mlflow.db`.
- **En vuelo:** PR #50 (`feature/011-hu-009-mlflow`), revisión pendiente de Guillermo.
- **Siguiente:** revisar y fusionar #50; después, HU-011 o el evaluador de HU-008.

### 2026-11-11 · Eliana (OpenCode) — HU-011

- **Hecho:** HU-011 implementada con Spec Kit: Dockerfile multi-stage (`runtime`
  Python 3.13-slim + uv con extras `inference`/`grpc` y torch CPU vía índice
  `pytorch-cpu` en Linux; `web` nginx con la SPA), `docker/entrypoint.sh`
  (`PPE_SERVICES`), `compose.yml` (api/grpc/frontend con modelo montado `:ro`),
  `.dockerignore`, `.gitattributes` y 9 pruebas (8 estáticas + smoke de Docker);
  build `--no-cache` verificado, inferencia REST y gRPC dentro del contenedor
  con `best.pt` (SHA256 `96ba99a7…`), mount `:ro` probado con `Read-only file
  system`, compose demo verificado (SPA :8080, REST :8000, gRPC :9000); runbook
  `docs/operacion/docker.md`, 152 passed + 2 skipped, ruff/ty/build/pre-commit
  en verde. Evidencia publicada en #11 (comentario).
- **En vuelo:** PR #52 (`feature/012-hu-011-docker-cpu`), revisión pendiente.
- **Siguiente:** revisión de la PR y cierre manual de #11 al fusionar; HU-014
  gana su dependencia Docker.

### 2026-11-12 · Guillermo (OpenCode) — cierre del M3-S2

- **Hecho:** cerradas #8–#12 (HU-008 a HU-012) al estar fusionadas; tablero con
  HU-001 a HU-012 en Done y #13 en Ready; specs renumeradas `009`–`013` sin
  duplicados; backlog, M3, README, constitución derivada y plantilla de PR
  sincronizados; conteo real **218** pruebas y plan de **212 nuevas** repartido por
  integrante en `docs/curso/PLAN-PRUEBAS.md`.
- **En vuelo:** PR #53 (`docs/cierre-m3-s2`), pendiente de revisión.
- **Siguiente:** fusionar #53; abrir HU-013 con Spec Kit (`specs/014-hu-013-version-modelo`),
  ejecutar el plan de pruebas y preparar el release `develop → main` con tag.

### 2026-11-12 · Jesús (OpenCode) — HU-013

- **Hecho:** HU-013 implementada: `ModelIdentity` (versión, SHA256, artefacto y
  referencia) en REST/gRPC, `PPE_MODEL_SHA256`, 20 pruebas, proto regenerado y contrato
  documentado; `make check` 197 passed + 2 skipped, `make frontend-check` 39 passed y
  `uv build` en verde. Se corrigió la bitácora de HU-009 y el conteo quedó en **238**.
- **En vuelo:** PR #54 (`feature/014-hu-013-version-modelo`), pendiente de revisión.
- **Siguiente:** revisar/fusionar #54; cerrar #13; completar las 192 pruebas restantes y
  preparar el release `develop → main` con tag `m3-entrega`.

### 2026-11-12 · Jesús (OpenCode) — cierre documental post-#54

- **Hecho:** PR #54 fusionada y #13 cerrada; M3 con **13/13 HUs**; README, M3, backlog,
  specs y estado sincronizados; conteo **238/400** y plan de **192 pruebas**.
- **En vuelo:** PR #55 (`docs/estado-post-54`), pendiente de revisión.
- **Siguiente:** abrir ramas `test/*` y ejecutar las 192 pruebas restantes; release M3.
