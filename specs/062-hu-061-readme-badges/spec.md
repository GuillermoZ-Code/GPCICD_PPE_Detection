# Feature Specification: HU-061 — README con badges y enlaces públicos del M4

**Feature Branch**: `feature/062-hu-061-readme-badges`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #117 — «README con badges y enlaces públicos del M4». Asignada a
Eliana (`ElianaCardona`), épica `ep-15`, SP 1, P0, Ola 3, 4 pruebas objetivo.
Depende de HU-065.

## Verificación de la dependencia (HU-065)

La dependencia está **satisfecha en código**: la PR #218 (`Closes #121`) está
fusionada (`merge_commit 35d8b97`) e incorpora
`.github/workflows/mirror-gitlab.yml`, `docs/operacion/gitlab-espejo.md`, su spec
y 12 pruebas. El workflow dispara en `push` a `develop`/`main`, empuja con el
mismo SHA a `gitlab.com/educacional-group/GPCICD_PPE_Detection` y compara el SHA
devuelto por la API contra `GITHUB_SHA`; el token `GITLAB_TOKEN` se enmascara y
el job declara `permissions: contents: read`. Las 21 tareas de la spec están
marcadas como completadas, incluidas las de configuración remota.

La issue #121 sigue **abierta** por el procedimiento del repositorio («al fusionar
en `develop`, cierra la issue a mano»); ese dato administrativo **no** bloquea
HU-061 porque los AC de HU-065 ya están implementados y verificados. No se cierra
la issue ajena desde esta HU: se registra la observación para sudueño.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Verificación del proyecto de un vistazo (Priority: P0)

Como evaluador, quiero ver en el README el estado de CI, pipeline, imagen y URL
pública, para verificar el proyecto de un vistazo.

**Why this priority**: el README es la primera fuente que abre un evaluador; los
enlaces y badges deben reflejar solo evidencia verificable.

**Independent Test**: `uv run pytest -v tests/test_readme_badges.py` analiza el
README como texto; no requiere red, modelo ni credenciales.

**Acceptance Scenarios** (AC de la issue #117):

1. **AC-01**: el README muestra badges de GitHub CI, pipeline de GitLab, licencia
   y Docker Hub.
2. **AC-02**: el README enlaza la URL HTTPS del repositorio, el Registry y
   `CONSTITUTION.md`.
3. **AC-03**: los enlaces internos del README resuelven a archivos presentes.

### Edge Cases

- HU-068 (#124, «Publicar imágenes en GitLab Registry y Docker Hub») sigue
  abierta y no hay namespace de Docker Hub versionado: el badge de Docker Hub
  debe ser honesto («pendiente») y enlazar la issue, no un dominio inventado.
- La URL pública MaaS depende de HU-053: se usa `<URL_PUBLICA>` como plantilla,
  igual que en `docs/maas/README.md`, sin inventar un dominio.
- Los badges de CI y GitLab usan rutas verificadas (`actions/workflows/ci.yml`,
  proyecto GitLab `educacional-group/GPCICD_PPE_Detection` de HU-065).
- La licencia del código es AGPL-3.0-only y el badge enlaza `./LICENSE`.
- No se versionan secretos ni variables de registro en el README.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `README.md` MUST contener cuatro badges: GitHub CI, pipeline de
  GitLab, licencia AGPL-3.0-only y Docker Hub (pendiente de HU-068).
- **FR-002**: `README.md` MUST enlazar el remoto HTTPS del repositorio, el
  Registry de GitLab, `CONSTITUTION.md` y el marcador `<URL_PUBLICA>`.
- **FR-003**: todo enlace relativo del README MUST resolver a un archivo que
  exista en el repositorio.
- **FR-004**: `tests/test_readme_badges.py` MUST tener 4 pruebas AAA que
  referencien AC-01 ×2, AC-02 ×1 y AC-03 ×1.

### Key Entities

- **Badge**: imagen Markdown con destino; el destino es evidencia verificable.
- **Enlace público**: URL HTTPS derivada de fuentes versionadas o plantilla
  explícitamente pendiente.
- **README**: `README.md` en la raíz, de propiedad de Eliana.

## Acceptance → prueba

| AC | Prueba en `tests/test_readme_badges.py` |
|----|------------------------------------------|
| AC-01 | `test_badges_de_ci_pipeline_licencia_y_docker_hub_ac_01`, `test_badge_docker_hub_no_inventa_namespace_ac_01` |
| AC-02 | `test_enlaces_https_registry_y_constitucion_ac_02` |
| AC-03 | `test_enlaces_internos_resuelven_y_toc_existe_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: las 4 pruebas pasan y han fallado antes del cambio.
- **SC-002**: `ruff format --check README.md`, `check_specs` y propiedad pasan.
- **SC-003**: la PR queda con checks remotos en verde sin autoaprobación.

## Out of Scope

- Cerrar la issue #121 de HU-065 (propiedad de Guillermo; solo se observa).
- Publicar imágenes en Docker Hub ni inventar un namespace (HU-068).
- Definir el dominio público definitivo (HU-053).
- Cambiar badges que ya funcionan sin relación con los AC.

## Assumptions

- El proyecto GitLab es `educacional-group/GPCICD_PPE_Detection` (id `89281003`),
  según el workflow fusionado en HU-065.
- El remoto HTTPS es
  `https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection.git` (CONSTITUTION).
- El README se renderiza en `develop` y en `main` sin procesamiento adicional.
