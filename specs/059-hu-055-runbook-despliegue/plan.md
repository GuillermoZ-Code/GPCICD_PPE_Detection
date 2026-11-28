# Plan — HU-055 Runbook de despliegue y rollback

**Branch**: `docs/059-hu-055-runbook` · **Issue**: #111 · **Spec**: `spec.md`

## Enfoque

El runbook existe en `docs/operacion/despliegue.md` y cubre la operación real del
Droplet. Falta la **spec** y la **prueba estructural** que exige la compuerta de
trazabilidad; no se reescribe el procedimiento.

## Componentes

| Pieza | Cambio |
|---|---|
| `specs/059-hu-055-runbook-despliegue/` | Spec, plan y tareas |
| `tests/test_runbook_despliegue.py` | 10 pruebas estructurales del runbook |

## Decisiones

- **No tocar el procedimiento**: el documento ya se usó para desplegar; cambiarlo sin
  necesidad añade riesgo.
- **Prueba estructural**: valida secciones, comandos, rollback y ausencia de secretos.
- **Rollback probado**: se referencia `tests/test_deploy.py`, que ya verifica
  `.deployed_env` y la restauración del tag anterior.

## Riesgos

- **Documento y script divergen**: la prueba exige `deploy.sh` y `.deployed_env` en el
  runbook; si el script cambia, falla.
- **Dominio/IP cambian**: la prueba solo exige que el dominio documentado sea el actual.

## Verificación

```bash
uv run pytest -q tests/test_runbook_despliegue.py
make check
```
