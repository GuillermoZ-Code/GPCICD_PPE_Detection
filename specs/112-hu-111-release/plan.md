# Plan — HU-111 Release v1.0.0

**Branch**: `docs/112-hu-111-release` · **Issue**: #167 · **Spec**: `spec.md`

## Enfoque

El tag y la release ya existen; falta el **checklist verificable** en `docs/entrega/`.
El documento registra los hechos del release y declara lo que no se cumplió (suite
< 1.200 al cortar el tag), sin afirmar lo contrario.

## Componentes

| Pieza | Cambio |
|---|---|
| `RELEASE-V1.0.0.md` | Checklist, tag/commit, imagen, modelo, health, licencia, rollback |
| `tests/test_release_v1.py` | 10 pruebas del contenido y de los hechos |

## Decisiones

- **Declarar el pending de pruebas**: el tag se cortó con ~1.064; el documento lo dice y
  apunta a `v1.0.1` si `main` cambia.
- **Sin credenciales**: la imagen se documenta por su nombre de pipeline
  (`$CI_REGISTRY_IMAGE/api:<sha>`), no se consulta el registry.
- **Verificación real**: `/health` se consultó el 27/11 y devolvió `yolo26n-clean`.

## Riesgos

- **Tag anterior a #268–#273**: el release no incluye el frente de pruebas; se mitiga con
  `v1.0.1`.
- **Droplet caído**: la prueba del documento no depende de la red.

## Verificación

```bash
uv run pytest -q tests/test_release_v1.py
make check
curl -s https://143.198.10.157.sslip.io/health
```
