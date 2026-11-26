# Implementation Plan: HU-085 — ADR de GitLab CI/CD, espejo y Droplet

**Branch**: `feature/086-hu-085-adr-gitlab-droplet` | **Date**: 2026-11-25 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/086-hu-085-adr-gitlab-droplet/spec.md`

## Summary

Escribir los ADR 0007 (GitLab CI con espejo de *push* desde GitHub) y 0008 (Droplet con
Docker Compose y Caddy), enlazarlos desde `CONSTITUTION.md` y desde el índice de ADR, y
proteger la coherencia con pruebas estáticas.

## Technical Context

**Language/Version**: Markdown (ADR en español)

**Primary Dependencies**: N/A

**Storage**: N/A

**Testing**: pytest estático sobre los ADR, la constitución y el índice

**Target Platform**: documentación del repositorio

**Project Type**: gobierno técnico

**Performance Goals**: N/A

**Constraints**: no reescribir ADR existentes; numeración append-only; sin contradicciones

**Scale/Scope**: 2 ADR nuevos, 2 archivos actualizados y 5 pruebas

## Constitution Check

- **Constitución como fuente**: los ADR la enlazan y no la contradicen. ✅
- **Test-first**: cada AC tiene prueba estática. ✅
- **Sin secretos ni datos**: solo documentación. ✅
- **Propiedad**: `docs/adr/` y `CONSTITUTION.md` son de Guillermo. ✅
- **Una HU por PR**. ✅

## Project Structure

```text
docs/adr/0007-gitlab-ci-espejo.md     # nuevo
docs/adr/0008-droplet-caddy.md        # nuevo
docs/adr/README.md                    # índice actualizado
CONSTITUTION.md                       # §7 enlaces y §11 historial
tests/test_adr_m4.py                  # 5 pruebas estáticas
specs/086-hu-085-adr-gitlab-droplet/
```

## Design decisions

1. **Dos ADR, no uno.** Pipeline y despliegue se deciden por separado y pueden cambiar
   por motivos distintos; mezclarlos impediría sustituir uno sin reescribir el otro.
2. **Se usan los números 0007 y 0008.** Estaban libres y la HU los fija; se advierte en el
   ADR para que nadie interprete que hubo reordenamiento.
3. **Las alternativas se registran con motivo.** «Descartado» sin porqué no es un ADR.
4. **CONSTITUTION enlaza en §7 y §11.** §7 da el rumbo de arquitectura; §11 deja el
   histórico con fecha y motivo.

## Risks

| Riesgo | Mitigación |
|---|---|
| El ADR 0008 describe algo aún no desplegado | Se declara como decisión objetivo y el estado real se documenta en HU-055/015 |
| Contradicción con ADR 0003 (AGPL) | Se enlaza y se repite la obligación de ofrecer el código en el servicio |
| Enlaces internos rotos | Prueba que verifica las rutas de los ADR y del índice |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_adr_m4.py` (existencia y decisión de cada ADR) |
| AC-02 | `tests/test_adr_m4.py` (alternativas descartadas) |
| AC-03 | `tests/test_adr_m4.py` (enlaces en `CONSTITUTION.md` y en el índice) |
