# Feature Specification: HU-053 — MaaS: segunda URL pública del modelo

**Feature Branch**: `feature/054-hu-053-hf-spaces`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #109 — «MaaS: segunda URL pública del modelo (Cloud Run o HF
Spaces)». Asignada a Eliana (`ElianaCardona`), épica `ep-10`, SP 5, P1, Ola 3,
16 pruebas objetivo. Depende de HU-026 (descarga y verificación del modelo),
cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Alternativa pública reproducible (Priority: P1)

Como usuario externo, quiero una segunda URL pública del modelo, para tener
alternativa gratuita si el Droplet falla.

**Why this priority**: un único punto de exposición convierte cualquier incidente
del Droplet en pérdida total del servicio MaaS.

**Independent Test**: `uv run pytest -v tests/test_segunda_url_publica.py` lee los
artefactos de `deploy/maas-alt/` y `docs/maas/segunda-url.md`; no requiere red,
cuentas externas ni secretos.

**Acceptance Scenarios** (AC de la issue #109):

1. **AC-01**: **Dado** un proveedor alternativo, **Cuando** se revisa la decisión,
   **Entonces** el destino elegido está justificado frente a Cloud Run.
2. **AC-02**: **Dado** un visitante del Space, **Cuando** abre su README, **Entonces**
   ve la atribución CC-BY del dataset y el enlace al código AGPL.
3. **AC-03**: **Dado** un operador, **Cuando** sigue el runbook, **Entonces** puede
   reconstruir y publicar la imagen sin secretos en el repo ni en la imagen.

### Edge Cases

- No se publica una URL inventada: se usa `<SPACE_URL>` hasta crear el Space.
- El artefacto del modelo no está en Git (HU-026); la imagen arranca sin pesos y
  el runbook explica cómo inyectarlos en tiempo de ejecución.
- Publicar requiere una cuenta de Hugging Face con Spaces Docker disponible; si
  no hay credenciales, el bloqueo se registra en la issue y no se simula éxito.
- La atribución CC-BY no relicencia el código AGPL-3.0-only.
- La clave de API (HU-051) y el rate limit (HU-054) se documentan como variables
  de entorno del Space, nunca como valores en el Dockerfile.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `docs/maas/segunda-url.md` MUST justificar HF Spaces Docker frente
  a Cloud Run y documentar límites, secretos y modelo fuera de la imagen.
- **FR-002**: `deploy/maas-alt/README.md` MUST ser la tarjeta visible del Space
  con atribución CC-BY y enlace AGPL.
- **FR-003**: `deploy/maas-alt/Dockerfile` MUST construir con `uv sync --frozen`,
  exponer 7860 y no contener secretos ni pesos.
- **FR-004**: `deploy/maas-alt/.dockerignore` MUST excluir entornos, pesos, datos
  y secretos del contexto de construcción.
- **FR-005**: las 16 pruebas MUST ser estructurales, AAA y referenciar los AC.

### Key Entities

- **Space**: repositorio de Hugging Face que ejecuta el contenedor en 7860.
- **Tarjeta**: `README.md` del Space, renderizada públicamente.
- **Runbook**: `docs/maas/segunda-url.md`, con build, arranque y publicación.

## Acceptance → prueba

| AC | Evidencia prevista en `tests/test_segunda_url_publica.py` |
|----|-----------------------------------------------------------|
| AC-01 | `test_decision_hf_spaces_justificada_ac_01`, `test_space_card_identifica_destino_ac_01`, `test_dockerfile_expone_puerto_spaces_ac_01`, `test_sin_dominio_inventado_ac_01`, `test_documento_registra_limitaciones_ac_01`, `test_secretos_como_variables_de_entorno_ac_01` |
| AC-02 | `test_card_atribuye_dataset_cc_by_ac_02`, `test_card_enlaza_codigo_agpl_ac_02`, `test_doc_explica_atribucion_visible_ac_02`, `test_licencias_no_se_relicencian_ac_02` |
| AC-03 | `test_dockerfile_congela_lock_ac_03`, `test_dockerfile_no_copia_secretos_ac_03`, `test_dockerignore_excluye_pesos_y_entorno_ac_03`, `test_runbook_incluye_build_y_arranque_ac_03`, `test_modelo_fuera_de_la_imagen_ac_03`, `test_pasos_publicacion_reproducibles_ac_03` |

## Success Criteria *(mandatory)*

- **SC-001**: las 16 pruebas nuevas pasan y la suite completa sigue verde.
- **SC-002**: `check_specs` y `ownership` pasan sin bloqueos.
- **SC-003**: el bloqueo de credenciales HF queda registrado en la issue #109.

## Out of Scope

- Crear el Space remoto ni publicar credenciales: no hay cuenta autorizada en
  esta sesión y el bloqueo se documenta.
- Cambiar el Dockerfile principal, el compose ni los workflows de GitHub.
- Implementar HU-051 (clave), HU-054 (rate limit) ni HU-060 (metadatos AGPL).

## Assumptions

- El contexto de construcción del Space es la raíz del repositorio.
- Hugging Face renderiza `README.md` como página pública del Space.
- Los pesos se inyectan en ejecución desde una fuente verificada por SHA-256 (HU-026).
