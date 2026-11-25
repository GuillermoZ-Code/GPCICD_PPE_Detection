# Feature Specification: HU-065 — Proyecto GitLab y espejo GitHub → GitLab

**Feature Branch**: `feature/066-hu-065-gitlab-espejo`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #121 — «HU-065 — Proyecto GitLab y espejo GitHub → GitLab». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-06`, P0, ola 3, 3 SP, 12 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cada push de GitHub llega a GitLab con el mismo SHA (Priority: P0)

Como equipo, quiero que cada push a `develop` o `main` en GitHub se replique en GitLab
con el mismo SHA, para ejecutar GitLab CI/CD sobre el commit exacto que revisó y aprobó
el equipo, sin depender de funciones Premium de espejo.

**Why this priority**: el 40 % de la rúbrica del M4 es el pipeline de GitLab. Sin espejo,
lo que corre en GitLab no es lo que está en GitHub, y el SHA del pipeline no se puede
trazar contra la PR ni contra la entrega.

**Independent Test**: se hace un push a `develop`, el workflow `Espejo GitLab` termina en
verde y el commit de la rama `develop` en GitLab tiene el mismo SHA que GitHub
(verificado con la API de GitLab dentro del propio workflow).

**Acceptance Scenarios** (AC de la issue #121):

1. **AC-01**: **Dado** un push a `develop` o `main` en GitHub, **Cuando** corre el
   workflow, **Entonces** hace `git push` a GitLab en la misma rama.
2. **AC-02**: **Dado** el workflow en verde, **Cuando** se consulta la rama en GitLab,
   **Entonces** el SHA del último commit coincide con `GITHUB_SHA`.
3. **AC-03**: **Dado** el token de GitLab, **Cuando** se configura el espejo, **Entonces**
   vive en un secret de GitHub (`GITLAB_TOKEN`), con permiso mínimo
   (`write_repository`) y nunca aparece en el repositorio ni en los logs.

### Edge Cases

- **Falta el secret**: el workflow falla de inmediato con un mensaje claro, sin intentar
  el push.
- **`main` protegida**: el push normal solo avanza si GitLab no divergió. Si alguien
  comitea directo en GitLab, el push falla y el workflow lo muestra; el repositorio
  fuente es GitHub.
- **Rama distinta de `develop`/`main`**: no se espeja; el workflow solo escucha esas dos.
- **Reejecución manual**: `workflow_dispatch` permite repetir el espejo sin un push.
- **Divergencia inicial de `main`**: GitLab tiene un commit que GitHub no (creado por
  web). Se alinea una sola vez; después el push normal se mantiene.
- **Token expirado o sin scope**: el push devuelve 401/403 y el workflow falla con el
  código, sin exponer el token.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El workflow MUST dispararse con `push` a `develop` y `main`, y admitir
  `workflow_dispatch`.
- **FR-002**: El checkout MUST ser completo (`fetch-depth: 0`) para no crear commits
  parciales ni ramas huérfanas.
- **FR-003**: El push MUST ir a
  `gitlab.com/educacional-group/GPCICD_PPE_Detection` en la rama de origen, sin prefijo
  de credenciales en la URL.
- **FR-004**: El token MUST leerse de `secrets.GITLAB_TOKEN` y enmascararse
  (`::add-mask::`) antes de cualquier uso.
- **FR-005**: El workflow MUST verificar con la API de GitLab que el último commit de la
  rama es `GITHUB_SHA`, y fallar si no coincide.
- **FR-006**: El workflow MUST declarar `permissions: contents: read` y no usar
  `--force` sobre ramas protegidas.
- **FR-007**: La operación MUST quedar documentada en un runbook con la creación del
  token, el secret, la verificación y el diagnóstico.

### Key Entities

- **Espejo**: replicación de una rama GitHub → GitLab con el mismo SHA; no es una copia
  de historial completo, sino de la rama empujada.
- **`GITLAB_TOKEN`**: project access token con scope `write_repository` y rol suficiente
  para empujar a `main` protegida; vive solo en GitHub Secrets.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un push a `develop` deja GitLab `develop` con el mismo SHA en menos de
  2 minutos.
- **SC-002**: 12 pruebas estáticas cubren el workflow, el uso del secret y la
  documentación, sin red ni GitLab.
- **SC-003**: `make check` en verde y CI de GitHub en verde.

## Assumptions

- El proyecto GitLab ya existe (`educacional-group/GPCICD_PPE_Detection`, id 89281003) y
  el repositorio GitHub es público, así que el push no necesita credenciales de lectura.
- GitHub es la fuente de verdad; GitLab solo recibe y ejecuta.
- El espejo de tipo *pull* que tenía GitLab está deshabilitado: competiría con el push y
  reescribiría ramas.
