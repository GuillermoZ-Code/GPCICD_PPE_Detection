# Cumplimiento de la rúbrica — M4

> **Generado:** 2026-11-28 04:26 UTC · `make rubrica-write`
> **Ítems:** 14 · cumplidos: 14 · pendientes: 0
> **Fecha de corte:** 27/11/2026

| ID | Área | Criterio | Evidencia | Responsable | Estado |
|---|---|---|---|---|---|
| R-01 | Pipeline | CI/CD con compuertas de calidad | `.github/workflows/ci.yml` | Guillermo | ✔ |
| R-02 | Contenedor | Imagen Docker CPU reproducible | `Dockerfile` | Eliana | ✔ |
| R-03 | Modelo | Artefacto versionado por SHA256 | `models.lock` | Hernán | ✔ |
| R-04 | Modelo | Informe de evaluación comparativa | `docs/evaluation/YOLO26.md` | Hernán | ✔ |
| R-05 | Modelo | ADR del modelo productivo | `docs/adr/0009-modelo-productivo.md` | Hernán | ✔ |
| R-06 | Trazabilidad | Matriz HU → issue → spec → PR → pruebas | `docs/curso/TRAZABILIDAD.md` | Jesús | ✔ |
| R-07 | Pruebas | Inventario generado de pruebas | `docs/curso/PRUEBAS.md` | Jesús | ✔ |
| R-08 | Backlog | Espejo 1:1 de las issues | `docs/curso/backlog.md` | Jesús | ✔ |
| R-09 | API | Healthcheck y contrato REST | `src/ppe_detection/api/app.py` | Eliana | ✔ |
| R-10 | Interfaz | SPA React operativa | `frontend/src/App.tsx` | Guillermo | ✔ |
| R-11 | Operación | Runbook de Docker | `docs/operacion/docker.md` | Eliana | ✔ |
| R-12 | Documentación | Mapa de documentación y glosario | `docs/README.md` | Jesús | ✔ |
| R-13 | Riesgos | Registro de riesgos del cierre | `docs/curso/M4/RIESGOS.md` | Jesús | ✔ |
| R-14 | Equipo | Retrospectiva y acciones | `docs/curso/M4/RETRO.md` | Jesús | ✔ |

## Criterio

- ✔: la evidencia existe en el repositorio.
- ✘: falta o está pendiente; la HU responsable la completa antes del 27/11/2026.
- El informe se regenera con `make rubrica-write`; no se edita a mano.
