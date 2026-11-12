# Estado operativo — GPCICD PPE Detection

> **Qué es:** dónde quedó el proyecto, no qué se planeó.
> **Cómo se actualiza:** `make estado-write` regenera el bloque de abajo y, al cerrar
> cada sesión, se añade una entrada a la bitácora.
> **Fuente de verdad:** issues, tablero, `specs/` y `CONSTITUTION.md`. Este archivo no
> puede contradecirlos.
> **Caduca:** si el bloque tiene más de 3 días o no coincide con `git log`, regenéralo
> antes de actuar.

<!-- estado:inicio -->
**Generado:** 2026-11-12 02:35 UTC

**Rama:** `feature/012-hu-011-docker-cpu` · limpia · +7/-0 vs `origin/develop`
**develop:** 35b28d5 (2026-11-11)

**Últimos commits:**
- `6b8dd28 Merge remote-tracking branch 'origin/develop' into feature/012-hu-011-docker-cpu`
- `b98ce95 docs(estado): registrar cierre de sesion`
- `35b28d5 Merge pull request #50 from GuillermoZ-Code/feature/011-hu-009-mlflow`
- `67d939a Merge branch 'develop' into feature/011-hu-009-mlflow`
- `8e5febc Merge pull request #51 from GuillermoZ-Code/feature/009-hu-008-evaluador`

**Pull requests abiertas (2):**
- #52 feat(docker): ejecutar el sistema en un contenedor CPU (HU-011) → `develop` · revisión: — · CI: —
- #49 feat(calidad): informe automatizado de verificaciones (HU-012) → `develop` · revisión: aprobada · CI: ok

**Issues abiertas: 8 · 11 SP**
- M3-S2 (8 SP): #8 #9 #10 #11 #12 #13
- M4-S3 (3 SP): #14 #15

**En revisión:** #11 (PR #52), #12 (PR #49)
**Siguiente por orden:** #8 HU-008 — Evaluar el desempeño del modelo de detección
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

### 2026-11-10 · Hernán (OpenCode) — HU-012

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
