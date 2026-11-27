# Feature Specification: HU-075 — GGA: revisión de código con IA en pre-commit

**Feature Branch**: `feature/076-hu-075-gga`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #131 — «HU-075 — GGA: revisión de código con IA en pre-commit».
Épica `ep-12`, P0, ola 2, 2 SP, 8 pruebas objetivo. Depende de —.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Revisión automática antes del commit (Priority: P0)

Como Code Reviewer, quiero una revisión automática con IA antes de cada commit, para
atender la observación del M3 sin reemplazar la revisión humana.

**Why this priority**: el equipo tiene cuatro agentes escribiendo en paralelo; una
revisión local ayuda a detectar violaciones de la constitución antes de abrir la PR.

**Independent Test**: el hook se ejecuta con GGA instalado y devuelve su veredicto; sin
GGA termina con 0 y no bloquea.

**Acceptance Scenarios** (AC de la issue #131):

1. **AC-01**: **Dado** el repositorio, **Cuando** se ejecuta GGA, **Entonces** usa
   `.gga` con reglas derivadas de `CONSTITUTION.md`.
2. **AC-02**: **Dado** un equipo sin GGA, **Cuando** se ejecuta pre-commit, **Entonces**
   el hook opcional no bloquea el commit.
3. **AC-03**: **Dada** una PR, **Cuando** se revisa con GGA, **Entonces** queda
   evidencia de la revisión real en la PR.

### Edge Cases

- GGA ausente del `PATH`: aviso y salida 0.
- GGA instalado pero OpenCode sin configurar: el hook propaga el error de GGA; es una
  decisión del equipo, no un fallo silencioso.
- Archivos generados o dependencias: excluidos en `.gga`.
- Diferencias grandes: usar `--pr-mode --diff-only`.
- Credenciales: nunca se versionan ni se copian a la evidencia.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `.gga` MUST declarar `PROVIDER="opencode"` y
  `RULES_FILE="CONSTITUTION.md"`.
- **FR-002**: `.gga` MUST excluir `.venv`, `node_modules`, `dist`, `build` y locks.
- **FR-003**: El hook de pre-commit MUST llamar a un wrapper, no a GGA directamente.
- **FR-004**: El wrapper MUST devolver 0 si `gga` no está en el `PATH`.
- **FR-005**: El wrapper MUST propagar el código de GGA si está instalado.
- **FR-006**: El runbook MUST explicar instalación, uso, evidencia y desactivación.
- **FR-007**: No se MUST versionar ningún token ni credencial.
- **FR-008**: Las pruebas MUST ser estáticas y no invocar al proveedor de IA.

### Key Entities

- **`.gga`**: configuración versionada sin secretos.
- **`gga_hook`**: wrapper opcional de `pre-commit`.
- **Runbook**: `docs/operacion/gga.md`.
- **Evidencia**: salida de una revisión real adjunta a la PR.

## Acceptance → Test

| AC | Evidencia |
|----|-----------|
| AC-01 Reglas y configuración | `tests/test_gga.py::test_gga_config_uses_opencode_and_the_constitution`, `tests/test_gga.py::test_gga_config_reviews_code_and_excludes_artifacts`, `tests/test_gga.py::test_gga_config_has_no_literal_tokens` |
| AC-02 Hook opcional | `tests/test_gga.py::test_precommit_declares_the_optional_hook`, `tests/test_gga.py::test_hook_is_not_blocking_when_gga_is_absent`, `tests/test_gga.py::test_hook_propagates_gga_exit_code_when_available`, `tests/test_gga.py::test_main_prints_a_skip_message_without_gga` |
| AC-03 Evidencia de revisión | `docs/operacion/gga.md` y la salida adjunta en la PR |

## Success Criteria *(mandatory)*

- **SC-001**: El equipo sin GGA puede commitear sin cambios.
- **SC-002**: El equipo con GGA recibe una revisión antes del commit.
- **SC-003**: La configuración no contiene credenciales.
- **SC-004**: `make check` y `uv build` quedan en verde.

## Out of Scope

- Sustituir la revisión humana o la CI.
- Entrenar un modelo propio de revisión.
- Versionar el binario de GGA.
- Bloquear commits de quien no tenga GGA instalado.

## Assumptions

- GGA se instala en el equipo de cada integrante.
- OpenCode ya está configurado como proveedor local.
- La revisión real se ejecuta sobre el diff de la PR.
- Las credenciales del proveedor viven fuera del repositorio.
