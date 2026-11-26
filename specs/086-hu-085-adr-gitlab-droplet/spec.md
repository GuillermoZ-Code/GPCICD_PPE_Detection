# Feature Specification: HU-085 — ADR de GitLab CI/CD, espejo y Droplet

**Feature Branch**: `feature/086-hu-085-adr-gitlab-droplet`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #141 — «HU-085 — ADR de GitLab CI/CD, espejo y Droplet». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-14`, P0, ola 2, 1 SP, 4 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Justificar la arquitectura de despliegue (Priority: P0)

Como equipo, quiero registrar por qué se usa GitLab CI con espejo desde GitHub y por qué
el despliegue va en un Droplet con Caddy, para que la defensa del M4 pueda explicar las
decisiones y las alternativas descartadas sin depender de la memoria de nadie.

**Why this priority**: la rúbrica del M4 pesa 40 % pipeline y 30 % despliegue. Sin ADR,
esas dos decisiones no tienen trazabilidad y cualquier cambio de rumbo queda sin registro.

**Independent Test**: existen `docs/adr/0007-gitlab-ci-espejo.md` y
`docs/adr/0008-droplet-caddy.md`, ambos enlazados desde `CONSTITUTION.md` y desde el
índice de ADR, con sus alternativas descartadas.

**Acceptance Scenarios** (AC de la issue #141):

1. **AC-01**: **Dado** el repositorio, **Cuando** se revisa `docs/adr/`, **Entonces**
   existen el ADR 0007 (GitLab CI + espejo) y el ADR 0008 (Droplet + Caddy).
2. **AC-02**: **Dados** ambos ADR, **Cuando** se leen sus alternativas, **Entonces**
   registran el descarte de GitLab Premium, Render y Hugging Face como despliegue
   principal.
3. **AC-03**: **Dada** la constitución, **Cuando** se consulta, **Entonces** enlaza los
   dos ADR.

### Edge Cases

- Numeración: 0007 y 0008 quedaron libres al escribirse 0009 y 0011; se usan por
  trazabilidad y se advierte en el propio ADR.
- Si el despliegue cambia (por ejemplo, otro proveedor), se crea un ADR nuevo; no se
  reescribe este.
- El ADR 0008 describe el objetivo; si el Droplet no se aprovisiona, el estado se
  declara en el ADR y en el informe, no se da por hecho.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST existir un ADR 0007 con contexto, decisión, alternativas y
  consecuencias del espejo GitHub → GitLab.
- **FR-002**: MUST existir un ADR 0008 con contexto, decisión, alternativas y
  consecuencias del despliegue en Droplet con Caddy.
- **FR-003**: Los ADR MUST registrar el descarte de GitLab Premium, Render y Hugging Face
  como opción principal.
- **FR-004**: `CONSTITUTION.md` MUST enlazar ambos ADR en la sección de arquitectura.
- **FR-005**: El índice `docs/adr/README.md` MUST listar ambos ADR.
- **FR-006**: Los ADR MUST NOT contradecir `CONSTITUTION.md` ni los ADR existentes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un lector sin contexto entiende por qué GitLab y por qué Droplet.
- **SC-002**: Al menos 4 pruebas estáticas cubren los tres AC.
- **SC-003**: `make check` en verde y CI de GitHub en verde.

## Assumptions

- El pipeline de GitLab se implementa en HU-066 y el despliegue en HU-069 a HU-071; este
  ADR decide el rumbo, no lo implementa.
- El Droplet lo provee el curso y el dominio se resuelve con Caddy.
- El ADR 0009 (modelo productivo) y el 0011 (memoria de agentes) ya ocuparon sus números.
