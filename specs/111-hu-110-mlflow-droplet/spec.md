# Feature Specification: HU-110 — MLflow en el Droplet (decisión de alcance)

**Feature Branch**: No aplica (HU cerrada por alcance)

**Created**: 2026-11-28

**Status**: Cerrada por alcance

**Input**: Issue #166 — «HU-110 — MLflow accesible en el Droplet con autenticación».
Asignada a Jesús (`jesusriverosUAO`), épica `ep-14`, P2 · ola 3, 5 SP, 16 pruebas
objetivo. Depende de HU-071.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decidir si MLflow se publica (Priority: P2)

Como equipo, queremos decidir si MLflow se expone en el Droplet o se mantiene local,
para no añadir superficie, credenciales y carga a la entrega sin un requisito de la
rúbrica.

**Acceptance Scenarios**:

1. **AC-01**: **Dado** el despliegue, **Cuando** se revisa `compose.prod.yml` y el
   `Caddyfile`, **Entonces** MLflow **no** aparece como servicio ni como ruta pública;
   se usa en local con el extra `tracking` (HU-009).
2. **AC-02**: **Dado** el repositorio, **Cuando** se revisan los archivos de despliegue,
   **Entonces** no hay credenciales nuevas ni un backend persistente para MLflow.
3. **AC-03**: **Dada** la decisión, **Cuando** se ejecutan las pruebas, **Entonces** una
   prueba estructural verifica la ausencia de MLflow en producción y la documentación
   del alcance en `docs/operacion/mlflow.md`.

### Edge Cases

- MLflow local sigue disponible para evaluación y comparación de runs; no se elimina.
- Si en el futuro se requiere MLflow público, se abre una HU nueva con autenticación,
  almacenamiento persistente y presupuesto de CPU/RAM.
- El Droplet de 1 vCPU no debe cargar un servicio adicional durante la sustentación.

## Requirements *(mandatory)*

- **FR-001**: `compose.prod.yml` MUST NOT declarar un servicio `mlflow`.
- **FR-002**: `docker/Caddyfile` MUST NOT publicar una ruta `/mlflow`.
- **FR-003**: `docs/operacion/mlflow.md` MUST documentar que MLflow es local (HU-009).
- **FR-004**: La decisión MUST quedar registrada en esta spec y en el cierre de #166.
- **FR-005**: Al menos una prueba pytest MUST referenciar HU-110 y verificar la decisión.

## Acceptance → Test

| AC | Evidencia prevista |
|----|--------------------|
| AC-01 MLflow no se publica | `tests/test_mlflow_droplet_scope.py::test_ac01_mlflow_is_not_a_production_service` |
| AC-02 Sin credenciales nuevas | `tests/test_mlflow_droplet_scope.py::test_ac02_no_new_deployment_secrets` |
| AC-03 Decisión documentada | `tests/test_mlflow_droplet_scope.py::test_ac03_scope_is_documented` |

## Success Criteria

- **SC-001**: `trazabilidad --check` acepta HU-110 con spec y pruebas.
- **SC-002**: `make check` en verde.
- **SC-003**: No se añade ningún servicio ni credencial al despliegue.

## Test Mapping

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_mlflow_droplet_scope.py::test_ac01_mlflow_is_not_a_production_service` |
| AC-02 | `tests/test_mlflow_droplet_scope.py::test_ac02_no_new_deployment_secrets` |
| AC-03 | `tests/test_mlflow_droplet_scope.py::test_ac03_scope_is_documented` |
