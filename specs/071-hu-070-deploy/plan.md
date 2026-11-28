# Implementation Plan: HU-070 — Job `deploy` por SSH con rollback

**Branch**: `feature/071-hu-070-deploy` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/071-hu-070-deploy/spec.md`

## Summary

Publicar sin verificar es la forma más rápida de tumbar la demo. El rollback convierte un despliegue fallido en un incidente de un minuto.

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
deploy/deploy.sh        # nuevo: pull, up, espera y rollback
deploy/droplet/provision.sh  # nuevo: usuario, UFW y fail2ban
.gitlab-ci.yml         # job `deploy`
tests/test_deploy.py
specs/071-hu-070-deploy/
```

## Design decisions

1. **Script en el repositorio, ejecutado en el servidor.** El rollback queda versionado y probado, no escondido en un YAML.
2. **Tag anterior en un archivo.** `.last_tag` sobrevive al contenedor y no necesita estado externo.
3. **Salto automático sin servidor.** Un pipeline rojo por falta de Droplet no informa nada; el job se omite y la deuda queda en el registro de riesgos.

## Risks

| Riesgo | Mitigación |
|---|---|
| El servidor no responde | `ConnectTimeout` de 10 s y el job falla con el código |
| Rollback también falla | `deploy.sh` deja los logs y sale con error explícito |
| Llave expuesta | Variable tipo File, `chmod 600` y sin `echo` |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_deploy.py` (SSH, compose pull/up y `.env`) |
| AC-02 | `tests/test_deploy.py` (rollback y smoke) |
| AC-03 | `tests/test_deploy.py` (`resource_group` y salto sin host) |
