# Documentación

| Carpeta / archivo | Contenido |
|-------------------|-----------|
| `adr/` | Architecture Decision Records (0001–0005); índice en [`adr/README.md`](adr/README.md). |
| `architecture/` | Diagrama Archify: `arquitectura.json` (fuente) y `arquitectura.html` (artefacto). |
| `curso/` | Contexto del curso, checklists M2–M4 y `backlog.md` espejo de las issues. |
| `dataset/` | EDA del dataset: auditoría, duplicados, fuga y baseline ([EDA.md](dataset/EDA.md)). |
| `evaluation/` | Informes de evaluación del detector ([HU-008.md](evaluation/HU-008.md)). |
| `operacion/` | Runbooks locales: demo API + frontend y [MLflow](operacion/mlflow.md). |
| `spikes/` | Investigaciones técnicas acotadas: [SPI-01](spikes/SPI-01-compatibilidad-yolo.md) y [SPI-02](spikes/SPI-02-baseline-evaluacion.md). |
| `research/` | Notas de investigación y comparativas (si aplica). |

> El historial de decisiones resumido vive en
> [`../CONSTITUTION.md`](../CONSTITUTION.md); los ADR entran en detalle.

Reglas:

- Un documento, un tema.
- Fechas en ISO (`AAAA-MM-DD`).
- Enlaza cada documento desde la constitución o el README cuando sea relevante.
- No subas datos sensibles, personales ni pesos de modelos.
- El PDF de cada módulo se redacta fuera del repositorio; `curso/backlog.md` es la
  fuente para el Capítulo 5 y debe coincidir 1:1 con las issues.
- El HTML de arquitectura no se edita a mano: se regenera con `make arch`.
