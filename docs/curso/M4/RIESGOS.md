# Registro de riesgos — M4

> **Qué es:** matriz de riesgos del cierre del M4 (26/11) y de la sustentación (28/11),
> con dueño, disparador y mitigación.
> **Cómo se usa:** cuando un disparador se cumple, el dueño ejecuta la mitigación y
> actualiza el estado. El registro se revisa al cierre.
> **Fuente:** [`M4/ASIGNACION.md`](ASIGNACION.md), ADR 0009 y el estado operativo.

## 1. Matriz

| ID | Riesgo | Categoría | Prob. | Impacto | Dueño | Disparador | Mitigación | Estado |
|---|---|---|---|---|---|---|---|---|
| R-01 | Droplet sin aprovisionar al 26/11 | infraestructura | Media | Alto | Guillermo | No hay Droplet el 24/11 | Demo local con `make app` y video; `compose.prod.yml` listo | Abierto |
| R-02 | Docker no corre en el equipo de demo | infraestructura | Media | Alto | Eliana | `docker info` falla el 25/11 | Demo con `make app` (API + SPA) sin contenedor | Abierto |
| R-03 | Cuota de GitHub Actions agotada | ci | Media | Medio | Guillermo | Jobs en cola o fallo por cuota | `make check` local como evidencia; reducir matriz de CI | Abierto |
| R-04 | Espejo GitHub → GitLab roto | ci | Alta | Medio | Guillermo | Pipeline de GitLab en rojo | Release desde GitHub; documentar el espejo como no bloqueante | Abierto |
| R-05 | `best.pt` de YOLO26n no publicado | modelo | Media | Alto | Hernán | SHA256 no coincide con `models.lock` | Rollback a YOLO11s según ADR 0009 | Abierto |
| R-06 | Latencia > 100 ms en el servidor | modelo | Media | Medio | Hernán | Smoke supera 100 ms p95 | ONNX 640 y, si falla, rollback a YOLO11s | Abierto |
| R-07 | Reclamo de atribución del dataset | modelo | Baja | Medio | Hernán | Falta visible CC-BY-4.0 | Atribución en README, SPA y Model Card | Abierto |
| R-08 | Indisponibilidad de un integrante | equipo | Media | Alto | Jesús | Sin respuesta en 24 h | WIP 1 y reparto de `ASIGNACION.md`; reasignar la HU | Abierto |
| R-09 | PR sin revisor asignado | equipo | Media | Medio | Jesús | PR con más de 24 h sin revisión | Workflow `Revisores` y aviso en el grupo | Abierto |
| R-10 | Secreto expuesto en el repositorio | equipo | Baja | Alto | Guillermo | `gitleaks` o revisión manual | Variables enmascaradas y rotación inmediata | Abierto |

## 2. Riesgos materializados

| ID | Fecha | Qué pasó | Evidencia | Acción |
|---|---|---|---|---|
| — | — | — | — | — |

## 3. Revisión

- **23/11/2026:** registro inicial.
- **Cierre del M4 (26/11):** se actualiza el estado y se añaden los materializados.
