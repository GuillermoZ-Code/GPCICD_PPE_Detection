# ADR 0011 — Memoria de agentes con Engram

- **Fecha:** 2026-11-24
- **Estado:** Aceptada
- **Decisores:** Grupo 4
- **Relacionada:** [HU-101](../curso/backlog.md) (registro del MCP) y
  [HU-102](../curso/backlog.md) (este protocolo)

## Contexto

El M3 se cerró con la observación de que cada agente empezaba sin contexto y que las
decisiones se repetían entre sesiones. Engram ya está registrado como servidor MCP en
[`opencode.json`](../opencode.json) y su base vive fuera de Git (`~/.engram/engram.db`).

Falta la regla de uso: qué se guarda, qué no, y cómo se comparte. Sin ella, la memoria
puede contradecir a [`CONSTITUTION.md`](../CONSTITUTION.md) o acumular datos personales.

## Decisión

**Usar Engram como memoria local de los agentes, subordinada al repositorio.**

1. **Jerarquía:** si una memoria contradice `CONSTITUTION.md`, los ADR, `AGENTS.md`,
   `docs/curso/ESTADO.md` o una issue, **manda el repositorio** y la memoria se corrige.
2. **Qué se guarda:**
   - decisiones y su motivo;
   - bugs y su causa raíz;
   - hallazgos no obvios del código o del entorno;
   - convenciones y patrones del equipo;
   - resumen de sesión con hecho / en vuelo / siguiente.
3. **Qué no se guarda:**
   - credenciales, tokens, claves ni cadenas de conexión;
   - datos personales de terceros, imágenes o rostros;
   - contenido de datasets, pesos o binarios;
   - transcripciones completas de conversaciones.
4. **Sincronización:** la memoria es **local a cada equipo**. No se sincroniza entre
   máquinas ni se comparte por Git. Lo que debe viajar va al repositorio (ADR, docs,
   issues).
5. **Exportación:** cada integrante puede exportar su base para respaldo o para migrar de
   equipo; el archivo exportado queda fuera de Git y no se adjunta a las PR.
6. **Cierre:** `mem_session_summary` complementa el protocolo de `AGENTS.md` §0.2; la
   bitácora de `ESTADO.md` la actualiza una sola persona en la sesión de cierre.

## Alternativas consideradas

- **Sincronizar la memoria en Git:** expone datos locales, crece sin control y genera
  conflictos entre agentes.
- **Un servidor central de memoria:** requiere infraestructura y credenciales que el
  curso no provee; además, mezcla contexto de cuatro máquinas.
- **No usar memoria:** vuelve el problema del M3 (contexto perdido).

## Consecuencias

- Cada agente gana continuidad sin tocar el repositorio.
- La fuente de verdad sigue siendo el repositorio; la memoria es apoyo.
- El runbook [`docs/operacion/engram.md`](../operacion/engram.md) explica instalación,
  uso y deshabilitación.
- Si un equipo no tiene Engram, el MCP se desactiva con `"enabled": false` y el resto del
  flujo no cambia.

## Referencias

- [`CONSTITUTION.md`](../CONSTITUTION.md) §13.
- [`AGENTS.md`](../AGENTS.md) §0 y tabla de herramientas.
- [`docs/operacion/engram.md`](../operacion/engram.md).
- HU-101 (#157) y HU-102 (#158).
