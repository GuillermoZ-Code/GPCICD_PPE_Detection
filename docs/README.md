# Documentación — mapa y glosario

> **Qué es:** índice de la documentación del repositorio, agrupado por tema, con un
> glosario de los términos que aparecen en el curso, el código y la operación.
> **Para quién:** integrantes nuevos, revisores y el evaluador de la sustentación.
> **Regla:** cada documento nuevo se añade a este mapa en su propio PR.

## Mapa por tema

| Tema | Documentos | Para qué |
|---|---|---|
| **Gobierno** | [Constitución](../CONSTITUTION.md) · [Agentes](../AGENTS.md) · [Contribución](../CONTRIBUTING.md) · [ADR](adr/) | Reglas, decisiones y flujo de trabajo |
| **Curso** | [Contexto](curso/CONTEXTO_CURSO.md) · [Backlog](curso/backlog.md) · [Estado](curso/ESTADO.md) · [Pruebas](curso/PRUEBAS.md) · [Plan de pruebas](curso/PLAN-PRUEBAS.md) · [Trazabilidad](curso/TRAZABILIDAD.md) · [M4](curso/M4/README.md) · [Asignación M4](curso/M4/ASIGNACION.md) | Planificación y evidencias del curso |
| **Operación** | [Demo local](operacion/demo-local.md) · [Docker](operacion/docker.md) · [MLflow](operacion/mlflow.md) | Cómo levantar y diagnosticar el sistema |
| **Datos y modelo** | [EDA del dataset](dataset/EDA.md) · [Evaluación](evaluation/) · [Model Card](model-card.md) | Qué datos se usaron y cómo rinde el modelo |
| **Arquitectura** | [Diagrama interactivo](architecture/) | Componentes y flujo del sistema |
| **Specs** | [Spec Kit](../specs/) | Una carpeta por HU con spec, plan y tareas |

## Glosario

| Término | Definición |
|---|---|
| **EPP** | Equipo de Protección Personal: las seis clases del dataset (Gloves, Vest, goggles, helmet, mask, safety_shoe). |
| **mAP** | *Mean Average Precision*; calidad de la detección. `mAP50` usa IoU 0,5 y `mAP50-95` promedia varios umbrales. |
| **NMS** | *Non-Maximum Suppression*; elimina cajas solapadas de la misma clase. |
| **ONNX** | Formato abierto de modelo; YOLO26n exportado a ONNX 640 cumple la latencia objetivo en CPU. |
| **YOLO26n** | Detector nano elegido como modelo productivo (ADR 0009); YOLO11s queda como rollback. |
| **AGPL** | GNU Affero GPL v3: obliga a ofrecer el código fuente a quien use el servicio en red. |
| **Droplet** | Servidor virtual del curso donde se despliega la aplicación. |
| **MLflow** | Registro de experimentos y Model Registry del proyecto. |
| **gRPC** | RPC sobre Protocol Buffers; segundo mecanismo de inferencia, junto a REST. |
| **FastAPI** | Framework HTTP de la API REST (`POST /predict`). |
| **SPA** | *Single Page Application*; la interfaz React + Vite + TypeScript. |
| **MaaS** | *Model as a Service*: exponer el modelo con API pública, clave opcional y documentación. |
| **SDD** | *Spec-Driven Development*: issue → spec → plan → tareas → implementación → PR. |
| **DinD** | *Docker-in-Docker*: el runner construye imágenes dentro del pipeline de GitLab. |
| **DoR / DoD** | *Definition of Ready* y *Definition of Done*: compuertas de entrada y salida de una HU. |
| **WIP 1** | Una sola HU en progreso por integrante; el assignee es el candado. |

## Cómo se mantiene

- Un documento nuevo se enlaza aquí en el mismo PR que lo crea.
- `uv run pytest tests/test_docs_readme.py` valida que los enlaces resuelven y que el
  glosario conserva los términos obligatorios.
- Si un documento cambia de ruta, se actualiza el mapa en el mismo cambio.
