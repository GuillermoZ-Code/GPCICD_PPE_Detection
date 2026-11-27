# Feature Specification: HU-086 — Diagrama de arquitectura de despliegue

**Feature Branch**: `feature/087-hu-086-diagrama-despliegue`

**Created**: 2026-11-27

**Status**: En revisión (PR #262, sin fusionar ni autoaprobar)

**Input**: Issue #142 — «HU-086 — Diagrama de arquitectura de despliegue». Asignada a
Eliana (`ElianaCardona`), épica `ep-15`, P1 · ola 3, 1 SP, 4 pruebas objetivo. Depende de
HU-070 (#126, *Done*).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Entender el flujo completo de entrega (Priority: P1)

Como evaluador, quiero ver en el diagrama el flujo GitHub → GitLab → Registry →
Droplet → usuario, para entender cómo llega una cambio al sitio publicado sin depender
de memorizar los scripts de despliegue.

**Why this priority**: el M4 evalúa 40 % pipeline y 30 % despliegue; el diagrama es la
entrada visual a esa evidencia y la puente con el runbook de HU-055.

**Independent Test**: `docs/architecture/arquitectura.json` contiene los componentes
`github`, `gitlab`, `registry`, `droplet` y `user`, y sus conexiones forman la cadena
de entrega; el HTML generado refleja esos mismos nodos.

**Acceptance Scenarios** (AC de la issue #142):

1. **AC-01**: **Dado** el diagrama, **Cuando** se abre `arquitectura.html`, **Entonces**
   muestra el flujo GitHub → GitLab → Registry → Droplet → usuario con Caddy delante de
   la API y la SPA.
2. **AC-02**: **Dado** el despliegue, **Cuando** se consulta el diagrama, **Entonces**
   incluye los secretos (`SSH_KEY`, `DOCKERHUB_TOKEN`, `PPE_AUTH_HASH`), los puertos
   (80/443 públicos, 8000 REST, 9000 gRPC interno, 80 interno de la SPA) y los
   healthchecks (`/health`, `/health/ready`).
3. **AC-03**: **Dada** la fuente del diagrama, **Cuando** se valida, **Entonces**
   `docs/architecture/arquitectura.json` es JSON válido, está versionado y declara
   `output` apuntando al HTML regenerado.

### Edge Cases

- El diagrama es **objetivo**: si el despliegue real cambia, se actualiza el JSON y se
  regenera el HTML en la misma PR; no se edita el HTML a mano.
- Los secretos se nombran, nunca se incluyen valores; el hash de basic auth se muestra
  como referencia a variable de entorno.
- gRPC queda en red interna: el diagrama no debe sugerir exposición pública del 9000.
- `docs/architecture/` es propiedad de Guillermo: la PR pide su revisión, pero no se
  modifican `deploy/*` ni scripts de plataforma.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST existir un componente `github`, `gitlab`, `registry`, `droplet`,
  `caddy`, `web` y `grpc` en `arquitectura.json`.
- **FR-002**: Las conexiones MUST incluir `github → gitlab`, `gitlab → registry`,
  `registry → droplet`, `droplet → caddy`, `caddy → web` y `caddy → api`.
- **FR-003**: El JSON MUST documentar secretos, puertos y healthchecks en tarjetas o
  componentes, sin valores sensibles.
- **FR-004**: `meta.output` MUST ser `docs/architecture/arquitectura.html` y el HTML
  MUST regenerarse desde el JSON con Archify (`--quality showcase`).
- **FR-005**: `docs/architecture/README.md` MUST conservar la instrucción de no editar
  el HTML a mano y enlazar la fuente versionada.
- **FR-006**: Al menos 4 pruebas pytest MUST referenciar AC-01, AC-02 y AC-03.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un lector sin contexto reconoce la cadena de entrega en menos de un minuto.
- **SC-002**: 4 pruebas estáticas cubren los tres AC.
- **SC-003**: `uv`-check local en verde; CI remoto se reporta solo con evidencia.

## Assumptions

- HU-070 dejó el job `deploy` por SSH con rollback operativo; la HU documenta, no
  reimplementa.
- El runbook `docs/operacion/despliegue.md` contiene los nombres reales de variables,
  puertos y healthchecks; el diagrama debe ser coherente con él.
- Archify se ejecuta desde una copia temporal del skill oficial para no instalar
  herramientas globales ni tocar `package-lock.json`.
