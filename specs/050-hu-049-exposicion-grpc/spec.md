# Feature Specification: HU-049 - Decisión y configuración de exposición de gRPC

**Feature Branch**: `feature/050-hu-049-exposicion-grpc`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #105 — «HU-049 - Decisión y configuración de exposición de gRPC». Asignada a Eliana (`ElianaCardona`), épica `ep-07`, P1 · ola 3, 1 SP, 4 pruebas objetivo. Depende de HU-041 (#97, *Done*).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Decidir la exposición del servicio (Priority: P1)

Como arquitecto, quiero decidir si gRPC se expone por TLS o queda interno, para no abrir puertos innecesarios en el Droplet.

**Why this priority**: el sitio público solo necesita REST y la SPA; publicar gRPC ampliaría la superficie de ataque y exigiría gestionar h2c/TLS sin un consumidor externo identificado.

**Independent Test**: `uv run pytest -q tests/test_adr_exposicion_grpc.py` verifica que el ADR 0010 registre la decisión, riesgos y alternativas, que `compose.prod.yml` no publique el puerto 9000 y que UFW solo permita 22/80/443.

**Acceptance Scenarios** (AC de la issue #105):

1. **AC-01**: **Dado** el ADR 0010, **Cuando** se lee, **Entonces** registra la decisión con riesgos y la alternativa de exponer gRPC mediante Caddy con h2c y TLS.
2. **AC-02**: **Dado** el despliegue, **Cuando** se revisa la configuración, **Entonces** el puerto 9000 no se publica: gRPC queda en red interna y Caddy no define ruta `/grpc`.
3. **AC-03**: **Dado** el aprovisionamiento, **Cuando** se revisa UFW, **Entonces** solo abren 22, 80 y 443, coherentes con la decisión.

### Edge Cases

- El ADR 0008 mencionó `/grpc` como ruta provisional; el ADR 0010 lo sustituye sin reescribir el histórico.
- `expose` de Docker Compose no publica el puerto en el host; `ports` sí lo haría y está prohibido para 9000.
- La alternativa h2c + TLS se documenta, no se implementa: no hay cliente externo que la necesite.
- Los secretos y el hash de basic auth no se copian al ADR.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST existir `docs/adr/0010-exposicion-grpc.md` con estado Aceptada y evidencia de HU-049 (#105).
- **FR-002**: El ADR MUST registrar decisión, riesgos/consecuencias y al menos la alternativa h2c + TLS (con mTLS como refuerzo).
- **FR-003**: `compose.prod.yml` MUST mantener `9000` solo en `expose` del servicio `grpc` y MUST NO contener un mapeo `9000:9000`.
- **FR-004**: `docker/Caddyfile` MUST NO contener `h2c`, la ruta `/grpc` ni el puerto 9000.
- **FR-005**: `deploy/droplet/provision.sh` MUST mantener UFW en `deny incoming` con solo 22/80/443 y sin regla para 9000.
- **FR-006**: MUST existir al menos 4 pruebas pytest que referencien AC-01, AC-02 y AC-03.
- **FR-007**: NO se MUST modificar código de aplicación ni archivos de despliegue; la HU solo decide y documenta.

### Key Entities

- **ADR 0010**: registro inmutable de la decisión de exposición de gRPC.
- **Superficie pública**: pares `ports` de Compose, rutas de Caddy y reglas UFW.

## Success Criteria *(mandatory)*

- **SC-001**: Las 4 pruebas nuevas pasan, junto con la suite completa.
- **SC-002**: Ruff, formato, `ty`, specs y propiedad sin hallazgos.
- **SC-003**: PR abierta a `develop` con revisor de otro integrante y sin fusión automática.

## Out of Scope

- Publicar gRPC en un subdominio con h2c y TLS.
- Cambiar `compose.prod.yml`, `docker/Caddyfile` ni `deploy/droplet/provision.sh`.
- Modificar el contrato gRPC o el cliente de verificación remota (HU-050).

## Assumptions

- HU-041 (#97) dejó Caddy con HTTPS automático y basic auth; no se reabre esa decisión.
- El smoke remoto usa REST; gRPC se verifica desde la red interna del Droplet.
- ADR 0008 conserva su valor histórico; la decisión vigente es la del ADR 0010.
