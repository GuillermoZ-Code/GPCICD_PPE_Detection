# M4 — MLOps, despliegue y operación

> **Periodo:** 19/11/2026 → 28/11/2026. **Peso:** 15 %.
> **Cierre de issues:** 26/11/2026. **Sustentación:** sábado **28/11/2026**.
> **Contrato de trabajo:** [`ASIGNACION.md`](ASIGNACION.md). Si una tarea no está ahí,
> no es tuya.

## 1. Focos

- MLOps: versionado del modelo, artefactos y trazabilidad.
- Pipeline de GitLab con compuertas de calidad y publicación en el registry.
- Credenciales y secretos gestionados con variables protegidas.
- Despliegue en Droplet con Docker CPU, Caddy y HTTPS.
- Healthcheck, logs y prueba funcional del sistema desplegado.
- Informe de cumplimiento de la rúbrica y release v1.1.0.

## 2. Sprint M4-S3 — 100 HU y 200 SP

| Persona | GitHub | HU | SP | Pruebas | Foco |
|---|---|---:|---:|---:|---|
| Guillermo Zabala | `GuillermoZ-Code` | 24 | 50 | 192 | GitLab, despliegue, interfaz y gobierno técnico |
| Eliana Cardona | `ElianaCardona` | 26 | 50 | 192 | Servicio, MaaS, seguridad y operación |
| Hernán Estrada | `HestradaUAO` | 25 | 50 | 192 | Modelo, datos, evaluación y empaquetado |
| Jesús Riveros | `jesusriverosUAO` | 25 | 50 | 192 | Backlog, tablero, trazabilidad, MLflow y agentes |
| **Total** | | **100** | **200** | **768** | |

- **Tres olas:** empieza por la ola 1 y pasa a la siguiente solo cuando la anterior
  esté fusionada o en revisión. La ola 3 concentra el cierre de la ruta crítica
  (pipeline, Droplet y release).
- **Reglas:** 1 HU = 1 issue = 1 spec = 1 rama = 1 PR; WIP 1; el dueño de cada ruta
  está en [`propiedad.toml`](../propiedad.toml) y `make ownership-check` corre antes
  de cada push.
- **Dependencias entre personas:** solo cruzan de dueño las que lista
  [`ASIGNACION.md`](ASIGNACION.md#dependencias-entre-personas). Si tu HU espera algo
  de otra persona, adelanta la parte que no depende.

## 3. Épicas ep-05 a ep-15

| Épica | Qué cubre |
|---|---|
| `ep-05` | Despliegue y operación: pipeline CI/CD con compuertas (HU-014) y comprobación del sistema desplegado (HU-015). |
| `ep-06` | CI/CD y pipeline de GitLab: proyecto y espejo, `.gitlab-ci.yml`, `build_image`, registry, deploy y artefacto del modelo. |
| `ep-07` | Despliegue e infraestructura: Droplet, `compose.prod.yml`, Caddy, exposición de gRPC y optimización de la imagen. |
| `ep-08` | Seguridad y cumplimiento: variables enmascaradas, gitleaks, límites de entrada, CORS, AGPL y CC-BY, Trivy. |
| `ep-09` | Modelo y evaluación: YOLO26 en CPU, entrenamiento, benchmark de latencia, umbrales, robustez y análisis de errores. |
| `ep-10` | Servicio, API y MaaS: configuración por entorno, clave de API opcional, documentación pública, segunda URL y paridad REST/gRPC. |
| `ep-11` | Interfaz web (SPA): API relativa, rediseño visual, flujo de resultados, exportación CSV/JSON, accesibilidad e historial. |
| `ep-12` | Herramientas para agentes: MCP de GitLab, `glab`, skills de GitLab y `frontend-design`, GGA y Engram. |
| `ep-13` | Observabilidad y operación: liveness y readiness, `HEALTHCHECK`, logs JSON con `request_id`, verificación remota, carga y deriva. |
| `ep-14` | Gobierno técnico y trazabilidad: `models.lock`, CODEOWNERS, tablero, matriz HU → issue → spec → PR, MLflow y riesgos. |
| `ep-15` | Documentación y entrega: Model Card, Dataset Card, runbooks, README, release v1.1.0, retrospectiva e informe de rúbrica. |

## 4. Entregables del M4

- Pipeline de GitLab con compuertas: lint → test → build → deploy → verify.
- Imágenes publicadas en el registry de GitLab y en Docker Hub con tag por commit.
- Despliegue en Droplet con Docker Compose, Caddy y HTTPS automático.
- Smoke posterior al deploy, con rollback al tag anterior si falla.
- Modelo descargado por SHA256 desde GitLab Generic Packages y montado `:ro`.
- Secrets gestionados en variables protegidas y enmascaradas de GitLab CI/CD.
- Healthcheck, logs técnicos sin secretos y una inferencia real contra el sistema
  desplegado.
- Informe de cumplimiento de la rúbrica y release v1.1.0 `develop → main`.
- Documentación de operación y recuperación (runbooks de despliegue y diagnóstico).

## 5. Requisito de pruebas

- Mínimo **1.200 pruebas unitarias** para la entrega del M4 (indicación del docente;
  no es un techo).
- Punto de partida: **533** al 23/11/2026 (457 pytest + 76 Vitest).
- El reparto del M4 planifica **768** pruebas nuevas: 192 por integrante.
- El conteo se genera con `make pruebas-write` y vive en [`PRUEBAS.md`](../PRUEBAS.md);
  el plan y el reparto están en [`PLAN-PRUEBAS.md`](../PLAN-PRUEBAS.md).

## 6. Decisiones de planificación

- **21/11/2026:** 100 HU nuevas y 200 SP, 50 por integrante, en tres olas; la
  reasignación pasó todo lo de GitLab al Code Reviewer.
- **HU-014 y HU-015** quedan dentro de esas 100 HU; HU-014 actúa como paraguas y se
  cierra cuando estén fusionadas las HU-066 a HU-068 y la HU-070.
- Las decisiones técnicas del despliegue están en el [ADR 0007](../../adr/0007-gitlab-ci-espejo.md)
  (espejo de GitLab) y el [ADR 0008](../../adr/0008-droplet-caddy.md) (Droplet y
  Caddy).

## 7. Riesgos y decisiones pendientes

| Riesgo / decisión | Responsable sugerido por rol | Acción |
|-------------------|------------------------------|--------|
| **AGPL en el despliegue** | Guillermo (repo) + Eliana (documento) | La interfaz y la API deben enlazar el código fuente; el dataset CC-BY exige atribución visible. Lo cubre **HU-060**. |
| **Droplet** | Guillermo (infra) + Jesús (planificación) | Definir dueño de la cuenta y costo; el aprovisionamiento es **HU-069**, el compose de producción **HU-071** y los secretos de despliegue **HU-042**. |
| **Repo privado vs. AGPL** | Guillermo + Eliana | Si el servicio se publica, el repo debe ser público o el código debe ofrecerse a los usuarios (ADR 0003). |

La matriz completa, con probabilidad, impacto y mitigación, vive en
[`RIESGOS.md`](RIESGOS.md).

## 8. Referencias

- [ASIGNACION.md](ASIGNACION.md) — reparto de las 100 HU, olas y dependencias.
- [PLAN-M4-100-SPECS.md](PLAN-M4-100-SPECS.md) — plan de las 100 specs.
- [RIESGOS.md](RIESGOS.md) — matriz de riesgos del cierre y la sustentación.
- [PLAN-PRUEBAS.md](../PLAN-PRUEBAS.md) — reparto de pruebas hacia 1.200.
- [backlog.md](../backlog.md) — espejo de las issues.
