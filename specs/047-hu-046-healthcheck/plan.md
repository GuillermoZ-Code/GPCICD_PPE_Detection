# Implementation Plan: HU-046 — HEALTHCHECK en la imagen y en compose

**Branch**: `feature/047-hu-046-healthcheck` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/047-hu-046-healthcheck/spec.md`

## Summary

Sin HEALTHCHECK no hay forma de distinguir «arrancó» de «puede atender». El deploy con rollback depende de esa señal.

## Technical Context

**Language/Version**: Docker Compose, shell POSIX, YAML de GitLab CI/CD

**Primary Dependencies**: imágenes del registry del proyecto, Caddy 2, OpenSSH

**Testing**: pytest estático sobre los archivos de despliegue (sin servidor)

**Target Platform**: Droplet con Docker CPU

**Project Type**: infraestructura de despliegue

**Constraints**: sin secretos en el repositorio; sin puertos innecesarios abiertos

**Scale/Scope**: 4 servicios, 1 servidor

## Constitution Check

- **Sin secretos versionados**: llaves y tokens solo en variables de CI/CD. ✅
- **Pesos fuera de Git y fuera de la imagen**: montaje `:ro`. ✅
- **Test-first**: pruebas estáticas antes de los archivos. ✅
- **AGPL**: la interfaz publicada enlaza el código fuente. ✅
- **Una HU por PR**: el bloque de despliegue se revisa junto y se cierra por issue. ✅

## Project Structure

```text
docker/healthcheck.sh   # nuevo: comprobación REST o gRPC
Dockerfile              # HEALTHCHECK y copia del script
tests/test_healthcheck.py
specs/047-hu-046-healthcheck/
```

## Design decisions

1. **Script propio en vez de `curl`.** La imagen no trae curl y añadirlo engorda la superficie de ataque; `python` ya está.
2. **Un solo healthcheck para los dos modos.** `PPE_SERVICES` decide si comprueba HTTP (`rest`) o TCP (`grpc`); el compose no duplica lógica.
3. **`start-period` largo.** Importar torch tarda decenas de segundos; sin margen, el contenedor se marcaría enfermo antes de poder responder.

## Risks

| Riesgo | Mitigación |
|---|---|
| El contenedor gRPC se marca enfermo | El script detecta `PPE_SERVICES=grpc` y prueba TCP |
| El modelo tarda en cargar | `start-period` de 90 s y 3 reintentos |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_healthcheck.py` (el script consulta `/health/ready` en modo REST) |
| AC-02 | `tests/test_healthcheck.py` (modo gRPC comprueba el puerto 9000) |
| AC-03 | `tests/test_healthcheck.py` (el Dockerfile declara HEALTHCHECK y copia el script) |
