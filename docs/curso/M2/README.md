# M2 — Checklist de evidencias del repositorio

> Entrega: **sábado 31/10/2026, 23:59**. Peso: **35 %**.
> El documento PDF se redacta fuera del repositorio (responsable: Eliana).
> Este checklist cubre **solo lo que vive en el repo**.

## 1. Estado de la entrega

| Evidencia | Estado | Dónde se verifica |
|-----------|:------:|-------------------|
| GitHub Projects compartido | ⏳ Jesús | Pendiente de confirmar si ya existe |
| Tablero sincronizado con las 15 HU | ⏳ Jesús | Columnas To Do / In Progress / Review-PR / Done |
| Fibonacci 1:1 coherente (1 SP ≈ 1 día) | ⏳ Jesús | `docs/curso/backlog.md` (§ pendiente de validación) |
| Labels ML / Backend / Frontend / Testing | ✅ | GitHub Labels + `.github/labels.yml` |
| Labels de épica y prioridad | ✅ | `ep-01`…`ep-05`, `must-have`, `should-have` |
| Milestones por sprint | ✅ | `M3-S1`, `M3-S2`, `M4-S3` |
| src-layout + `pyproject.toml` | ✅ | `src/ppe_detection/`, `pyproject.toml` |
| `uv` funcionando | ✅ | `uv sync`, `uv.lock` |
| pytest, Ruff y `ty` en verde | ✅ | `make check` |
| Licencia AGPL-3.0 | ✅ | `LICENSE`, `pyproject.toml`, badge del README |
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

- [ ] El repo compila e instala con `uv sync`.
- [ ] `make check` y `uv build` en verde.
- [ ] Issues con labels, milestone y dependencias.
- [ ] PR de alineación revisado y fusionado a `develop`.
- [ ] Release `develop → main` con merge commit y tag `m2-entrega`.
- [ ] Documento PDF integrado por Eliana con la misma información del backlog.
