# Feature Specification: HU-083 — CI GitHub: build de Docker, smoke y Trivy

**Feature Branch**: `feature/084-hu-083-ci-docker-trivy`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #139 — «CI GitHub: build de Docker, smoke y escaneo Trivy».
Asignada a Eliana (`ElianaCardona`), épica `ep-08`, SP 2, P1, Ola 2, 8 pruebas
objetivo. Sin dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Seguridad visible antes de publicar (Priority: P1)

Como responsable de seguridad, quiero escanear la imagen en cada PR, para detectar
vulnerabilidades HIGH/CRITICAL antes de publicar.

**Why this priority**: el contenedor es la unidad que se despliega; un escaneo solo
al publicar llega tarde y no deja evidencia descargable para la revisión.

**Independent Test**: `uv run pytest -v tests/test_ci_docker_trivy.py` valida el job
del workflow y el runbook con lectura de archivos, sin Docker ni red.

**Acceptance Scenarios** (AC de la issue #139):

1. **AC-01**: **Dado** un PR, **Cuando** corre el job `Docker y Trivy`, **Entonces**
   construye el target `runtime` y ejecuta un smoke de la API sin montar pesos.
2. **AC-02**: **Dado** el escaneo, **Cuando** Trivy encuentra vulnerabilidades
   HIGH/CRITICAL, **Entonces** las reporta en SARIF sin romper la compuerta por
   hallazgos heredados.
3. **AC-03**: **Dado** el SARIF generado, **Cuando** termina el job, **Entonces** se
   publica como artefacto descargable con `if-no-files-found: error`.

### Edge Cases

- El smoke no debe arrancar el servidor ni cargar el modelo: usa `create_app()`.
- Trivy debe escanear exactamente la imagen construida en el mismo job.
- `exit-code: '0'` es report-only: no desactiva el check, que sigue fallando si el
  build, el smoke, el escaneo o la subida del artefacto fallan.
- La subida falla si no hay SARIF: se exige `if-no-files-found: error`.
- El job declara `actions: write` para poder publicar el artefacto.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `.github/workflows/ci.yml` MUST añadir un job `docker` llamado
  `Docker y Trivy`.
- **FR-002**: El job MUST construir `gpcicd-ppe-detection:ci` desde el target `runtime`
  y ejecutar un smoke sin `PPE_MODEL_PATH`.
- **FR-003**: El job MUST ejecutar `aquasecurity/trivy-action` sobre esa imagen con
  `severity: HIGH,CRITICAL`, `format: sarif` y `output: trivy-results.sarif`.
- **FR-004**: El job MUST publicar el SARIF con `actions/upload-artifact@v4`.
- **FR-005**: `docs/operacion/docker.md` MUST documentar el job y la descarga del
  reporte.
- **FR-006**: Las 8 pruebas MUST ser nuevas, AAA y referenciar los AC por nombre.

### Key Entities

- **Job `docker`**: secuencia build → smoke → Trivy → artefacto.
- **SARIF**: reporte de vulnerabilidades descargable por PR.
- **Smoke sin modelo**: verificación de importación y construcción de la API.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_ci_docker_trivy.py::test_job_construye_imagen_runtime_ac_01`, `::test_smoke_no_monta_modelo_ac_01`, `::test_smoke_construye_la_api_sin_pesos_ac_01` |
| AC-02 | `tests/test_ci_docker_trivy.py::test_trivy_escanea_la_imagen_del_job_ac_02`, `::test_trivy_reporta_high_y_critical_en_sarif_ac_02` |
| AC-03 | `tests/test_ci_docker_trivy.py::test_reporte_se_publica_como_artefacto_ac_03`, `::test_job_tiene_permisos_para_artefactos_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 8 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: `ruff`, formato, ty, check_specs y propiedad pasan sin bloqueos.
- **SC-003**: El job se ejecuta en la PR y el reporte queda descargable.

## Out of Scope

- Cambiar el Dockerfile (HU-084) ni el compose (HU-071).
- Publicar el SARIF en GitHub Code Scanning: se entrega como artefacto (AC-03).
- Instalar dependencias ni tocar `uv.lock`.
- Modificar los otros jobs del workflow.

## Assumptions

- La imagen `runtime` construye sin pesos y `create_app()` no carga el modelo.
- `aquasecurity/trivy-action@0.33.0` es la versión estable disponible en Actions.
- El token de Actions puede escribir artefactos con `actions: write`.
