# Feature Specification: HU-084 — Optimizar la imagen Docker

**Feature Branch**: `feature/085-hu-084-optimizar-imagen`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #140 — «Optimizar la imagen Docker». Asignada a Eliana
(`ElianaCardona`), épica `ep-07`, SP 1, P2, Ola 2, 4 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Imagen menor y sin root (Priority: P2)

Como operador, quiero una imagen más pequeña y con usuario no root, para acelerar
el deploy y reducir superficie.

**Why this priority**: el contenedor se publica y se despliega en cada entrega;
cada megabyte descargado y cada privilegio de root aumentan el costo y la
superficie de ataque.

**Independent Test**: `uv run pytest -v tests/test_optimizacion_imagen.py` lee el
`Dockerfile` y el runbook; no requiere Docker ni red.

**Acceptance Scenarios** (AC de la issue #140):

1. **AC-01**: **Dado** el `Dockerfile`, **Cuando** se construye el target `runtime`,
   **Entonces** el proceso final corre como usuario no root y las capas están
   ordenadas (manifiestos → dependencias → código).
2. **AC-02**: **Dado** el tamaño de la imagen actual, **Cuando** se aplica la
   optimización, **Entonces** el runbook documenta el tamaño antes y después con
   el comando de medición.
3. **AC-03**: **Dado** el `Dockerfile` versionado, **Cuando** corre la prueba
   estática, **Entonces** verifica la directiva `USER` sin arrancar contenedores.

### Edge Cases

- El usuario creado debe tener UID > 0 y no puede haber un `USER root` posterior.
- El entorno virtual se construye en una etapa con uv y se copia al runtime final;
  el binario de uv y la caché no deben quedar en la imagen publicada.
- Las librerías del sistema se instalan en el runtime final y se limpia la lista
  de apt en la misma capa.
- El smoke de HU-083 (`create_app()`) debe seguir funcionando sin modelo.
- El target `web` y el builder de la SPA no cambian.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El target `runtime` MUST terminar con `USER appuser` (UID > 0).
- **FR-002**: `runtime-deps` MUST construir `.venv` con `uv sync --frozen` y
  `runtime` MUST copiarla; el runtime NO MUST contener `/usr/local/bin/uv`.
- **FR-003**: La caché de uv MUST desactivarse (`UV_NO_CACHE=1`) y la lista de
  apt MUST borrarse en la misma capa de instalación.
- **FR-004**: `docs/operacion/docker.md` MUST documentar tamaño antes/después en MB
  y el comando reproducible de medición.
- **FR-005**: Las 4 pruebas MUST ser nuevas, AAA y referenciar AC-01/AC-02/AC-03.

### Key Entities

- **runtime-deps**: etapa temporaria que resuelve y instala dependencias.
- **runtime**: etapa final con librerías del sistema, `.venv`, entrypoint y usuario.
- **Runbook**: registro del tamaño medido antes y después.

## Acceptance → prueba

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 | `tests/test_optimizacion_imagen.py::test_runtime_usa_usuario_no_root_ac_01`, `::test_capas_ordenadas_sin_uv_en_runtime_ac_01` |
| AC-02 | `tests/test_optimizacion_imagen.py::test_runbook_documenta_tamano_antes_despues_ac_02` |
| AC-03 | `tests/test_optimizacion_imagen.py::test_directiva_user_se_verifica_estaticamente_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: Las 4 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: `ruff`, formato, ty, check_specs y propiedad pasan sin bloqueos.
- **SC-003**: El target `runtime` sigue satisfaciendo las pruebas existentes de HU-011.

## Out of Scope

- Cambiar el compose, el entrypoint, nginx ni el builder de la SPA.
- Modificar `pyproject.toml`, `uv.lock` ni dependencias.
- Cambiar el job de CI de HU-083.

## Assumptions

- El entorno virtual construido sobre `python:3.13-slim` es portable a la misma
  imagen base en la etapa final.
- Se pueden medir ambos tamaños en un runner con Docker antes de documentarlos.
