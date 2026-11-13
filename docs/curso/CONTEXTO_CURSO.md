# Contexto del curso — GPCICD M2–M4

> Documento de contexto para el equipo y para los agentes. La verdad técnica del
> repositorio vive en [`CONSTITUTION.md`](../../CONSTITUTION.md).

## 1. Curso y alcance

| Campo | Valor |
|-------|-------|
| **Curso** | GPCICD — Módulos 2 a 4 |
| **Docente** | Por confirmar con el grupo *(dato pendiente)* |
| **Proyecto** | Sistema de detección de Equipos de Protección Personal (EPP) mediante IA |
| **Grupo** | Grupo 4 |
| **Repositorio** | https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection |
| **Dataset** | [`51ddhesh/PPE_Detection`](https://huggingface.co/datasets/51ddhesh/PPE_Detection) |
| **Metodología** | Scrum + Kanban + CRISP-DM + Spec-Driven Development |
| **Licencia** | AGPL-3.0-only |

## 2. Equipo y roles

| Integrante | GitHub | Rol |
|------------|--------|-----|
| Eliana Vanessa Cardona Burbano | `ElianaCardona` | Documento maestro, Capítulos 1–2, alcance e integración del PDF |
| Hernán Darío Estrada Satizábal | `HestradaUAO` | Modelo, Model Card, datos, licencia, hardware, métricas, sesgos, Capítulo 4 y CRISP-DM |
| Guillermo Alexander Zabala Fernández | `GuillermoZ-Code` | Entorno, arquitectura y repositorio, evidencias y Code Reviewer |
| Wilson Jesús Riveros Gómez | `jesusriverosUAO` | Planificación, Gantt, CPM, HU, AC, estimación, Capítulos 3 y 5, tablero Kanban |

## 3. Cronograma y ponderaciones

| Módulo | Fechas | Peso | Entregable principal |
|--------|--------|-----:|----------------------|
| **M1** | Cerrado | **25 %** | Primera entrega del proyecto |
| **M2** | Hasta **31/10/2026, 23:59** | **35 %** | Documento maestro + repositorio alineado (código, arquitectura, evidencias) |
| **M3** | **31/10 → 14/11/2026** | **25 %** | Implementación local: FastAPI, gRPC, SPA React, MLflow, Docker CPU |
| **M4** | **19/11 → 28/11/2026** | **15 %** | MLOps, despliegue, CI/CD y credenciales |

### Hitos y clases

- **M2:** entrega hoy **sábado 31/10/2026 a las 23:59**.
- **M3:** clase **05/11 FastAPI/REST**; clase **07/11 MLflow + Streamlit**;
  sustentación **sábado 14/11/2026**.
- **M4:** inicio **19/11**; MLOps/despliegue, CI/CD y credenciales; sustentación
  **sábado 28/11/2026**.

## 4. Reglas transversales

1. **Gitflow:** `feature/*` → `develop`; `develop → main` solo en entrega de módulo.
2. **PR obligatoria** con plantilla UAO, mínimo 1 aprobación y CI verde.
3. **Sin push directo** a `main` ni a `develop`. La protección es una regla escrita;
   no se configura protección técnica en GitHub.
4. **Commits:** Conventional Commits, imperativo, ≤72 caracteres.
5. **Dependencias:** solo `uv`; prohibido `pip` y `requirements.txt`.
6. **Calidad:** Ruff, `ty`, pytest, pre-commit y `make check`.
7. **Spec Kit:** una spec por HU y flujo specify → clarify → plan → tasks → analyze →
   implement.
8. **Datos y pesos:** fuera de Git; se documenta origen, licencia y SHA256.
9. **Sin secretos** en el repositorio ni en los logs.
10. **Sincronía documental:** el PDF se redacta fuera del repo; `backlog.md` debe
    coincidir 1:1 con issues, tablero y specs. Si hay diferencia, se avisa antes de
    continuar.
11. **Pruebas:** la entrega exige **≥ 400 pruebas unitarias**. El conteo y el reparto
    por integrante viven en [`PRUEBAS.md`](PRUEBAS.md) y
    [`PLAN-PRUEBAS.md`](PLAN-PRUEBAS.md).

## 5. Glosario

| Término | Significado |
|---------|-------------|
| **SP** | Story Point; estimación relativa. Criterio del curso: 1 SP ≈ 1 día. |
| **AC** | Acceptance Criteria; criterios de aceptación verificables. |
| **DoD** | Definition of Done; condiciones para cerrar una historia. |
| **WIP** | Work In Progress; límite de trabajo simultáneo por integrante (WIP 1). |
| **CPM** | Critical Path Method; ruta crítica del cronograma. |
| **CRISP-DM** | Metodología de minería de datos: negocio, datos, preparación, modelado, evaluación, despliegue. |
| **EPP** | Equipo de Protección Personal (Helmet, Vest, Gloves, Goggles, Mask, Safety Shoe). |
| **mAP** | Mean Average Precision; métrica de detección de objetos. |
| **NMS** | Non-Maximum Suppression; filtrado de cajas solapadas. |
| **YOLO** | Familia de detectores de objetos en tiempo real (Ultralytics). |
| **AGPL** | GNU Affero General Public License v3; copyleft con obligación de compartir fuente en uso de red. |
| **Droplet** | Servidor virtual del curso para el despliegue. |
| **MLflow** | Plataforma de experiment tracking y registro de modelos. |
| **gRPC** | Framework RPC sobre Protocol Buffers. |
| **FastAPI** | Framework HTTP para la API REST. |
| **React + Vite** | Framework de interfaz web (SPA) del proyecto; sustituye a Streamlit (ADR 0006). |
| **Model Card** | Documento de propósito, datos, métricas, limitaciones y licencias del modelo. |
| **Spec Kit** | Herramienta de Spec-Driven Development de GitHub. |

## 6. Enlaces

- [Constitución](../../CONSTITUTION.md)
- [Backlog](backlog.md)
- [Inventario de pruebas](PRUEBAS.md)
- [Checklist M2](M2/README.md)
- [M3](M3/README.md)
- [M4](M4/README.md)
- [ADRs](../adr/)
- [Arquitectura](../architecture/arquitectura.html)
