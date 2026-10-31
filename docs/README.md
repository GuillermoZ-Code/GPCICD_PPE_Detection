# Documentación

| Carpeta / archivo | Contenido |
|-------------------|-----------|
| `adr/` | Architecture Decision Records (0001–0005). |
| `architecture/` | Diagrama Archify: `arquitectura.json` (fuente) y `arquitectura.html` (artefacto). |
| `curso/` | Contexto del curso, checklists M2–M4 y `backlog.md` espejo de las issues. |
| `spikes/` | Investigaciones técnicas acotadas (se crean con SPI-01/SPI-02). |
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
