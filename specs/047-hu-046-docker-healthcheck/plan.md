# Implementation Plan: HU-046 — HEALTHCHECK en la imagen y en compose

**Branch**: `feature/047-hu-046-docker-healthcheck` | **Date**: 2026-11-25 | **Spec**:
[spec.md](./spec.md)

## Summary

Añadir `HEALTHCHECK` a la imagen `runtime` mediante `docker/healthcheck.sh`, que consulta
`/health/ready` en REST y el puerto 9000 en gRPC, y heredarlo en `compose.yml` para los
servicios `api` y `grpc`.

## Technical Context

**Language/Version**: Dockerfile, shell POSIX, Docker Compose

**Primary Dependencies**: `python:3.13-slim`, `/health/ready` de HU-045

**Storage**: N/A

**Testing**: pytest estático (Dockerfile, script, compose y runbook)

**Target Platform**: Docker CPU (Linux)

**Project Type**: infraestructura de despliegue

**Performance Goals**: el healthcheck no debe cargar el modelo ni bloquear el arranque

**Constraints**: un solo script para REST y gRPC; `start-period` por la carga de torch

**Scale/Scope**: Dockerfile, compose, script y runbook

## Constitution Check

- **Calidad**: pruebas estáticas y `make check`. ✅
- **Sin secretos**: el healthcheck no imprime credenciales. ✅
- **Propiedad**: `Dockerfile`, `docker/` y `compose.yml` son de Guillermo. ✅
- **Una HU por PR**. ✅

## Project Structure

```text
docker/healthcheck.sh              # nuevo
Dockerfile                         # COPY + HEALTHCHECK
compose.yml                        # healthcheck heredado por api y grpc
docs/operacion/docker.md           # sección de healthcheck
tests/test_docker_healthcheck.py   # 5 pruebas estáticas
specs/047-hu-046-docker-healthcheck/
```

## Design decisions

1. **Un script, dos modos.** `PPE_SERVICES` decide entre HTTP (`/health/ready`) y puerto
   9000; evita dos imágenes o dos healthchecks distintos.
2. **`start-period` de 40 s.** torch tarda en cargar; sin margen, Docker marcaría
   `unhealthy` durante el arranque normal.
3. **Heredado desde `x-backend`.** Un solo bloque en compose cubre `api` y `grpc`.
4. **Se usa `/health/ready`, no `/health`.** Distingue «proceso vivo» de «detector listo»,
   que es lo que interesa antes de mandar tráfico.

## Risks

| Riesgo | Mitigación |
|---|---|
| Falso `unhealthy` durante el arranque | `start-period: 40s` y `retries: 3` |
| gRPC sin HTTP | Chequeo por socket al 9000 |
| Healthcheck costoso | Solo una petición HTTP o un connect cada 30 s |
| `docker inspect` en el smoke | Documentado en el runbook |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_docker_healthcheck.py` (HEALTHCHECK, `/health/ready`, gRPC) |
| AC-02 | `tests/test_docker_healthcheck.py` (compose y `docker inspect` en el runbook) |
| AC-03 | `tests/test_docker_healthcheck.py` (copia, permisos y shebang) |
