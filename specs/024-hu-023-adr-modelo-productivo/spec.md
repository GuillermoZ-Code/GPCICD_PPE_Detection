# Feature Specification: HU-023 — ADR del modelo productivo

**Feature Branch**: `feature/024-hu-023-adr-modelo-productivo`

**Created**: 2026-11-23

**Status**: En implementación

**Input**: Issue #79 — «ADR: selección del modelo productivo». Asignada a Hernán
(`HestradaUAO`), épica `ep-09`, P0, Ola 3, 1 SP. Depende de HU-019, ya cerrada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Justificar el modelo desplegable (Priority: P0)

Como equipo, quiero una decisión documentada sobre qué modelo se despliega, para
justificar el cambio —o la permanencia— de YOLO26 en la sustentación.

**Why this priority**: HU-019 y HU-020 ya produjeron evidencia de calidad y latencia.
Sin un ADR, `models.lock`, la Model Card y el despliegue no tienen una decisión
trazable.

**Independent Test**: leer el ADR y comprobar que cita las métricas, la latencia, los
SHA256, el plan de rollback y la decisión sobre YOLO26n/s.

**Acceptance Scenarios** (AC de la issue #79):

1. **AC-01**: **Dado** el ADR 0009, **Cuando** se revisa, **Entonces** contiene
   criterios de mAP50-95, recall por clase, latencia y tamaño.
2. **AC-02**: **Dado** el ADR, **Cuando** se revisa, **Entonces** enlaza HU-019,
   HU-020 y el plan de rollback.
3. **AC-03**: **Dada** la decisión, **Cuando** se cierra la HU, **Entonces** la Model
   Card y `CONSTITUTION.md` reflejan el modelo seleccionado.

### Edge Cases

- YOLO26n es mejor en test completo, pero peor en el eval de 492; se explican ambas.
- YOLO26n ONNX cumple <100 ms; PyTorch no.
- YOLO26s no está fine-tuneado y es más lento; se descarta para producción.
- El despliegue actual sigue con YOLO11s hasta que se actualice el artefacto.
- Un rollback debe ser posible por tag/SHA256.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Crear `docs/adr/0009-modelo-productivo.md`.
- **FR-002**: Citar mAP50-95, recall por clase, latencia y tamaño.
- **FR-003**: Citar HU-019, HU-020 y SPI-03.
- **FR-004**: Definir YOLO26n como modelo seleccionado y YOLO11s como rollback.
- **FR-005**: Documentar el rollout: actualizar `models.lock`, artefacto y verificación
  SHA256.
- **FR-006**: Actualizar la Model Card al modelo seleccionado.
- **FR-007**: Actualizar `CONSTITUTION.md` y el índice de ADR.
- **FR-008**: No versionar pesos.

## Acceptance → Evidence

| AC | Evidencia |
|----|-----------|
| AC-01 Criterios | ADR §3–§5 |
| AC-02 Evidencia y rollback | ADR §6–§8 |
| AC-03 Model Card y CONSTITUTION | `docs/model-card.md`, `CONSTITUTION.md`, `docs/adr/README.md` |

## Success Criteria *(mandatory)*

- **SC-001**: La decisión es inequívoca: YOLO26n + ONNX.
- **SC-002**: El rollback a YOLO11s está documentado.
- **SC-003**: La Model Card no afirma que YOLO26n ya está desplegado.
- **SC-004**: No se versionan pesos.

## Out of Scope

- Ejecutar el despliegue o cambiar el contenedor.
- Actualizar `models.lock` en esta HU; se hace en el rollout.
- Entrenar YOLO26s.
- Cambiar la API, gRPC o la SPA.

## Assumptions

- YOLO26n es la mejor opción medida en test completo y latencia ONNX.
- El despliegue actual sigue siendo YOLO11s hasta el rollout.
- El ADR es append-only; no se reescriben los ADR 0001–0008.
