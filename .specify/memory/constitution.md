# Constitución derivada — GPCICD PPE Detection

> **DERIVADO, NO FUENTE DE VERDAD.** La fuente única es
> [`../../CONSTITUTION.md`](../../CONSTITUTION.md). Este archivo resume los principios
> no negociables para Spec Kit y se sincroniza **en el mismo commit** que la
> constitución. Si hay conflicto, manda `CONSTITUTION.md`.

**Versión:** 1.2 · **Fecha:** 2026-11-28 · **Proyecto:** GPCICD PPE Detection
**Licencia:** AGPL-3.0-only

## Principios no negociables

### I. `uv` es el único gestor

- Toda dependencia y entorno pasa por `uv`.
- Prohibido `pip` y `requirements.txt`.
- `uv.lock` se versiona; `pyproject.toml` es la fuente de dependencias.

### II. src-layout y contratos explícitos

- Código importable en `src/ppe_detection/`.
- Pruebas en `tests/` con patrón **AAA**.
- Contrato de inferencia: `ImageData → Detector.detect() → list[Detection]`.
- `Detection` usa `bbox` `xyxy` y `confidence` en `[0, 1]`.

### III. Calidad automatizada

- Ruff (lint + formato), `ty`, pytest y pre-commit.
- `make check` debe estar en verde antes de una PR.
- CI en `develop` y `main`; no se fusiona con la CI en rojo.
- Prohibido `--no-verify` sin causa documentada.

### IV. Datos y pesos fuera de Git

- Dataset, videos y pesos no se versionan.
- El artefacto se identifica por versión y SHA256.
- La inferencia registra semilla, versión del modelo, tamaño de imagen y umbrales.

### V. Contract-first

- Antes del detector real se define el contrato y un `FakeDetector`.
- API, UI y gRPC avanzan en paralelo con el modelo.
- El detector real debe cumplir el mismo contrato.

### VI. Uso responsable

- Seis clases en el orden del `data.yaml`: `Gloves, Vest, goggles, helmet, mask,
  safety_shoe`. La interfaz puede capitalizarlas o traducirlas para mostrarlas.
- No hay clase `person` ni `no-EPP`: se reporta EPP detectado, no cumplimiento.
- El sistema es asistivo, no certifica seguridad.
- Dataset CC-BY-4.0 con fuente original no declarada; documentar la limitación.

### VII. AGPL-3.0-only

- El proyecto se distribuye bajo AGPL-3.0-only.
- El uso como servicio en red obliga a ofrecer el código fuente de la versión modificada.
- Las dependencias conservan sus licencias.

### VIII. Gitflow y revisión

- `feature/*` → `develop`; `develop → main` solo en entrega de módulo.
- Ramas de Spec Kit: `feature/{number}-{slug}` con el ID en el slug
  (`feature/001-hu-001-carga-imagen`).
- PR con plantilla UAO, mínimo 1 aprobación, autor nunca se autoaprueba.
- Release `develop → main` siempre con merge commit.

### IX. Test-first y trazabilidad AC → prueba

- Cada AC de una spec tiene al menos una prueba pytest que lo referencia (`AC-xx` en
  el nombre o docstring).
- Las pruebas se escriben antes de la implementación; deben fallar primero.
- Excepciones: SPI y specs de documentación.
- `/speckit.analyze` marca como error un AC sin prueba.
- **Sin umbral de cobertura:** el M3 exigió **≥ 400 pruebas unitarias** y el M4 exige
  **≥ 1.200** (mínimo, no techo); el plan vive en `docs/curso/PLAN-PRUEBAS.md`.

### X. Cómputo GPU

- El entrenamiento no se ejecuta en CPU local.
- Colab/Kaggle solo como cómputo GPU, ejecutando un script versionado del repo con
  `uv`.
- No se versionan `.ipynb` ni se usa la UI de notebooks como fuente de verdad.

## Stack, roadmap y riesgos del M4

### Stack y despliegue

- **Modelo productivo:** YOLO26n fine-tuneado + exportación **ONNX 640** (ADR 0009);
  YOLO11s queda como rollback.
- **Servicio:** FastAPI REST, gRPC, SPA React 19 + Vite y MLflow.
- **CI/CD:** GitHub Actions (fuente de verdad) + **GitLab CI** por espejo de *push* y
  despliegue en el **Droplet** con **Caddy** y HTTPS automático (ADR 0007 y 0008).
- **Seguridad:** basic auth en Caddy (`PPE_AUTH_HASH`), `/health*` abierto, gitleaks y
  variables enmascaradas (ADR 0013).
- **Pruebas:** el M4 exige **≥ 1.200** pruebas unitarias; no hay umbral de cobertura.

### Roadmap

- **M4:** 19/11/2026 → 28/11/2026; **100 HU y 200 SP** (50 SP por integrante).
- **Rúbrica:** 40 % pipeline de GitLab, 30 % Droplet con Caddy y HTTPS, 15 % secretos,
  15 % despliegue en vivo.
- **Cierre:** release `develop → main` con merge commit, tag `v1.0.0` y despliegue por
  el pipeline de GitLab.

### Decisiones y riesgos

- Decisiones: ADR 0007 (espejo GitLab), ADR 0008 (Droplet + Caddy), ADR 0009 (YOLO26n +
  ONNX), ADR 0012 (CODEOWNERS y checks) y ADR 0013 (basic auth y `sslip.io`).
- Riesgos: AGPL en el servicio público, Droplet como punto único, repo privado frente a
  AGPL y artefacto del modelo fuera de Git con SHA256.

## Sincronización

Cualquier cambio en `CONSTITUTION.md` que afecte estos principios se replica aquí en
el mismo commit. Si hay diferencia, el agente **avisa antes de continuar**.
