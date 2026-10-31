# ADR 0003 — Licencia AGPL-3.0-only

- **Fecha:** 2026-10-31
- **Estado:** Aceptada
- **Decisores:** Grupo 4

## Contexto

El detector candidato es **Ultralytics YOLO**, distribuido bajo **AGPL-3.0**. El
sistema se expone como servicio en red (API REST, gRPC y Streamlit). La licencia MIT
original del repositorio no es compatible con esa obligación.

## Decisión

Licenciar el proyecto bajo **GNU Affero General Public License v3.0 only
(AGPL-3.0-only)**.

Actualizar:

- `LICENSE` con el texto completo de AGPL-3.0.
- `pyproject.toml`: `license = "AGPL-3.0-only"`.
- Badge del README y referencias en `CONSTITUTION.md` y `CONTRIBUTING.md`.

## Alternativas consideradas

- **MIT:** simple, pero incompatible con la obligación de red de Ultralytics YOLO.
- **Apache-2.0:** permisiva, pero tampoco resuelve la obligación AGPL del detector.
- **No exponer el servicio en red:** reduciría la obligación, pero el M3/M4 exige
  FastAPI, gRPC, Streamlit y despliegue; no es viable.

## Consecuencias

- Si el sistema se usa como servicio en red, debe ofrecerse el código fuente de la
  versión modificada a los usuarios.
- Las dependencias conservan sus propias licencias; se documentan en la Model Card.
- El aviso de copyright y la licencia se mantienen en el repositorio.
- Cualquier cambio de licencia requiere un nuevo ADR y aprobación del equipo.

## Referencias

- `LICENSE`.
- `CONSTITUTION.md` §0 y §11.
- Ultralytics YOLO — AGPL-3.0.
