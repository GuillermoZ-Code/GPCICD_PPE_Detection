# Implementation Plan: HU-049 - Decisión y configuración de exposición de gRPC

**Branch**: `feature/050-hu-049-exposicion-grpc` | **Date**: 2026-11-27 | **Spec**: [spec.md](./spec.md)

**Input**: `specs/050-hu-049-exposicion-grpc/spec.md`

## Summary

Registrar en el ADR 0010 la decisión de mantener gRPC en red interna, con riesgos y la alternativa descartada de h2c + TLS, y proteger con cuatro pruebas estáticas que la configuración desplegada siga sin publicar el puerto 9000.

## Technical Context

**Language/Version**: Markdown + Python 3.13 para pruebas

**Primary Dependencies**: pytest; sin dependencias nuevas

**Storage**: `docs/adr/0010-exposicion-grpc.md` y su entrada en `docs/adr/README.md`

**Testing**: pytest estático sobre ADR, Compose, Caddyfile y script de aprovisionamiento

**Target Platform**: documentación del repositorio

**Project Type**: decisión de arquitectura (ADR)

**Performance Goals**: N/A

**Constraints**: no modificar `deploy/`, `docker/` ni `compose.prod.yml`; sin secretos; `docs/adr/` es propiedad de Guillermo (revisión obligatoria)

**Scale/Scope**: 1 ADR, 1 entrada de índice, 4 pruebas, 3 documentos de Spec Kit

## Constitution Check

- **Spec Kit antes de implementar**: spec/plan/tasks creados antes del ADR. ✅
- **Test-first**: 4 pruebas referencian AC-01/AC-02/AC-03. ✅
- **Sin secretos**: el ADR solo nombra variables. ✅
- **Propiedad**: `docs/adr/` genera aviso de CODEOWNERS; se pide revisión a Guillermo. ✅
- **Una HU por PR**. ✅

## Project Structure

```text
docs/adr/0010-exposicion-grpc.md       # decisión vigente
docs/adr/README.md                     # índice actualizado
tests/test_adr_exposicion_grpc.py      # 4 pruebas estáticas
specs/050-hu-049-exposicion-grpc/      # spec/plan/tasks
```

## Design decisions

1. **Interno por defecto.** No hay consumidor externo de gRPC: el cliente de verificación se ejecuta dentro de la red del Droplet y la API pública es REST detrás de Caddy.
2. **Alternativa documentada, no implementada.** h2c + TLS (y opcionalmente mTLS) queda registrada como alternativa con sus costes de certificados, configuración y superficie de ataque.
3. **El ADR manda sobre el histórico.** ADR 0008 mencionó `/grpc` de forma provisional; 0010 lo sustituye sin reescribirlo.
4. **Pruebas sobre la configuración real.** Se leen `compose.prod.yml`, `docker/Caddyfile` y `deploy/droplet/provision.sh` para detectar regressions que abran 9000.

## Risks

| Riesgo | Mitigación |
|---|---|
| Reabrir una decisión ya cerrada de HU-041 | El ADR solo cubre gRPC; Caddy y REST quedan intactos |
| Contradecir el ADR 0008 | 0010 declara explícitamente que sustituye la mención provisional a `/grpc` |
| Que un cambio futuro publique 9000 | Prueba estática que prohíbe `9000:9000` y reglas UFW para 9000 |
| CODEOWNERS pida revisión de Guillermo | Se añade como reviewer en la PR; no se fusiona sin aprobación |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_adr_exposicion_grpc.py::test_ac_01_decision_con_riesgos_y_alternativa` |
| AC-02 | `tests/test_adr_exposicion_grpc.py::test_ac_02_puerto_9000_no_publicado` |
| AC-02 | `tests/test_adr_exposicion_grpc.py::test_ac_02_proxy_sin_ruta_grpc` |
| AC-03 | `tests/test_adr_exposicion_grpc.py::test_ac_03_firewall_coherente` |
