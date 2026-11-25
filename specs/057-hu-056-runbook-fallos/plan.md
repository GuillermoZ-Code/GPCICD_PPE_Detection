# Plan: HU-056 — Runbook de diagnóstico de fallos

**Input**: `specs/057-hu-056-runbook-fallos/spec.md` e issue #112.

## Enfoque

Documento único, escaneable en menos de dos minutos, con tres bloques:

1. **Árbol de decisión:** seis etapas ordenadas por frecuencia de fallo
   (pipeline → registry → SSH → contenedor → proxy → modelo). Cada etapa responde
   «qué veo», «qué corro» y «qué hago».
2. **Recetario de comandos:** `glab` para pipelines y logs, `docker logs` /
   `docker inspect` para contenedores, `curl` para proxy y salud del API. Cada
   comando lleva la interpretación esperada y una acción siguiente.
3. **Tres fallos simulados:** identificadores F1–F3 con síntoma, verificación,
   acción correctiva y resultado esperado. El registro separa la validación
   estática del documento del ensayo cronometrado del equipo.

## Archivos

- `docs/operacion/fallos.md` — nuevo runbook (entrega de la HU).
- `tests/test_docs_runbook_fallos.py` — nuevo; pruebas de contenido, sin red.
- `specs/057-hu-056-runbook-fallos/` — spec, plan y tareas.

## Decisiones

- No inventar evidencia de un ensayo grupal: el documento declara qué se verificó
  estáticamente y deja campos explícitos para la ejecución del equipo.
- No usar IPs ni nombres de droplet concretos: se emplean variables de entorno y
  marcadores `<...>` para que el runbook sirva en cualquier entorno.
- Los comandos de recuperación que reinician servicios se marcan con advertencia.

## Riesgos

- Que el runbook quede demasiado largo: se limita a tablas y listas cortas.
- Que las pruebas sean frágiles por cambios de redacción: se comprueban tokens
  estables (nombres de etapas, comandos y encabezados de las tablas).
