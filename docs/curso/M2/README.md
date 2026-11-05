# M2 — Checklist de evidencias del repositorio

> Entrega: **sábado 31/10/2026, 23:59**. Peso: **35 %**.
> El documento PDF se redacta fuera del repositorio (responsable: Eliana).
> Este checklist cubre **solo lo que vive en el repo**.

## 1. Estado de la entrega

| Evidencia | Estado | Dónde se verifica |
|-----------|:------:|-------------------|
| GitHub Projects compartido | ✅ | <https://github.com/users/GuillermoZ-Code/projects/1> — Project de la cuenta personal, público; usar la URL directa (no aparece en la pestaña *Projects* del repo) |
| Tablero sincronizado con las 15 HU | ✅ | 15 items · Estimate 22 (reestimado el 04/11/2026) · columnas Backlog / Ready / In progress / In review / Done |
| Fibonacci 1:1 coherente (1 SP ≈ 1 día) | ✅ | `docs/curso/backlog.md` (§ Responsables y reestimación) |
| Labels ML / Backend / Frontend / Testing | ✅ | GitHub Labels + `.github/labels.yml` |
| Labels de épica y prioridad | ✅ | `ep-01`…`ep-05`, `must-have`, `should-have` |
| Milestones por sprint | ✅ | `M3-S1`, `M3-S2`, `M4-S3` |
| src-layout + `pyproject.toml` | ✅ | `src/ppe_detection/`, `pyproject.toml` |
| `uv` funcionando | ✅ | `uv sync`, `uv.lock` |
| pytest, Ruff y `ty` en verde | ✅ | `make check` |
| Licencia AGPL-3.0 | ✅ | `LICENSE` canónico, `NOTICE`, `pyproject.toml`, badge del README |
| Plantilla UAO de PR | ✅ | `.github/PULL_REQUEST_TEMPLATE.md` |
| Gitflow `develop` / `main` | ✅ | `CONSTITUTION.md`, `CONTRIBUTING.md` |
| CI en `develop` y `main` | ✅ | `.github/workflows/ci.yml` |
| Dependabot mensual a `develop` | ✅ | `.github/dependabot.yml` |
| Spec Kit inicializado | ✅ v1.2.5 | `.specify/`, `.opencode/commands/` |
| Spec de contract-first | ✅ Borrador | `specs/001-ta-contract-first/` |
| Arquitectura interactiva | ✅ | `docs/architecture/arquitectura.html` |
| ADR 0001–0005 | ✅ | `docs/adr/` |
| Backlog espejo de las issues | ✅ | `docs/curso/backlog.md` |
| `make check` + `uv build` | ✅ | Salida en la descripción del PR |
| Release `develop → main` + tag `m2-entrega` | ✅ | `main`, tag `m2-entrega` |

## 2. Evidencias que se pegan en el PR

```bash
make check
uv build
```

- Salida de `pytest` (1 prueba smoke como mínimo).
- Salida de Ruff y `ty`.
- Salida de `uv build` (sdist + wheel).
- Enlace al tablero y a las issues por label/milestone.

## 3. Fuera del repositorio

- Documento maestro PDF (Eliana).
- Capítulos 1–2 y alcance (Eliana).
- Capítulo 4, Model Card, datos, licencia, hardware, métricas y sesgos (Hernán).
- Capítulos 3 y 5, Gantt, CPM, HU, AC, estimación y tablero (Jesús).
- Evidencias de comprobaciones y arquitectura (Guillermo).

## 4. Criterio de cierre del M2

- [x] El repo compila e instala con `uv sync`.
- [x] `make check` y `uv build` en verde.
- [x] Issues con labels, milestone y dependencias (15 HU; 7 en `M3-S1`, 6 en
      `M3-S2`, 2 en `M4-S3`; cada una con su línea “Depende de”).
- [ ] PR de alineación revisado y fusionado a `develop`.
      *Fusionado (PR #20), pero **sin aprobación registrada**: 0 revisiones.*
- [x] Release `develop → main` con merge commit y tag `m2-entrega`.
- [x] Documento PDF integrado por Eliana con la misma información del backlog
      *(entregado por la plataforma de la UAO)*.

## 5. Pendientes declarados al cierre

> Se declaran aquí para que la entrega no afirme como cumplido algo que no lo está.

| Pendiente | Dueño | Tipo | No bloquea porque |
|-----------|-------|------|-------------------|
| Fibonacci 1:1 y SP de HU-002 | Jesús | Decisión | `docs/curso/backlog.md` ya lo documenta como propuesta |
| Issues TA-04, TA-11, SPI-01, TA-02, TA-09, SPI-02, TA-10, TA-EDA | Jesús | Alcance M3 | Son alcance del M3, no criterio de cierre del M2 |
| AC de AGPL para HU-007 y HU-015 | Jesús + Eliana | Decisión | Propuesta, sin modificar las issues |
| Aprobación de la PR #20 | Revisor | Proceso | Se registra como incumplimiento, no se corrige a posteriori |
