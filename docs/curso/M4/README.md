# M4 — MLOps, despliegue y operación

> **Periodo:** 19/11/2026 → 28/11/2026. **Peso:** 15 %.
> **Sustentación:** sábado **28/11/2026**.

## 1. Focos

- MLOps: versionado del modelo, artefactos y trazabilidad.
- CI/CD con compuertas de calidad.
- Credenciales y secretos en GitHub Actions.
- Despliegue en Droplet con Docker CPU.
- Healthcheck, logs y prueba funcional del sistema desplegado.

## 2. Sprint M4-S3 — 15/11 a 28/11 (3 SP)

| HU | Título | SP | Responsable | Dependencias |
|----|--------|----|-------------|--------------|
| HU-014 | Pipeline CI/CD con compuertas de calidad | 2 | Eliana | HU-011, HU-012, TA-10 |
| HU-015 | Comprobar el sistema desplegado | 1 | Guillermo | HU-014 |

## 3. Entregables del M4

- Pipeline de publicación con compuertas (calidad → build → deploy → smoke).
- Versión desplegada asociada a un artefacto de modelo identificado.
- Credenciales gestionadas por el mecanismo seguro de GitHub Actions.
- Prueba de falla deliberada de compuerta.
- Healthcheck y logs técnicos sin secretos.
- Demostración de una inferencia real contra el sistema desplegado.
- Documentación de operación y recuperación.

## 4. Decisiones de planificación

**Resuelto el 04/11/2026:** TA-10 y el criterio de SP de TA/SPI se absorbieron en las
actividades de preparación P1–P4 (12 SP); no se crean como issues salvo decisión
expresa de Jesús.

Ver [`docs/curso/backlog.md`](../backlog.md).

## 5. Riesgos y decisiones pendientes

| Riesgo / decisión | Responsable sugerido por rol | Acción |
|-------------------|------------------------------|--------|
| **AGPL en el despliegue** | Guillermo (repo) + Eliana (documento) | La interfaz y la API deben enlazar el código fuente; el dataset CC-BY exige atribución visible. AC propuesto en HU-007 y HU-015, pendiente de validación de Jesús. |
| **Droplet** | Guillermo (infra) + Jesús (planificación) | Definir dueño de la cuenta, costo y administración de los secrets de GitHub Actions **antes del 19/11**. |
| **Repo privado vs. AGPL** | Guillermo + Eliana | Si el servicio se publica, el repo debe ser público o el código debe ofrecerse a los usuarios. Decidir antes del M4. |
