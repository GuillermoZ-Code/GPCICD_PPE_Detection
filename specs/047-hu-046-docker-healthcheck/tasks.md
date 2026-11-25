# Tasks: HU-046 — HEALTHCHECK en la imagen y en compose

**Input**: Design documents from `specs/047-hu-046-docker-healthcheck/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/047-hu-046-docker-healthcheck` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #102.

## Phase 2: Pruebas (test-first)

- [x] T003 [AC-01] `tests/test_docker_healthcheck.py`: `HEALTHCHECK` en el Dockerfile.
- [x] T004 [AC-01] `tests/test_docker_healthcheck.py`: `/health/ready` con REST.
- [x] T005 [AC-01] `tests/test_docker_healthcheck.py`: puerto 9000 con gRPC.
- [x] T006 [AC-03] `tests/test_docker_healthcheck.py`: copia, permisos y shebang.
- [x] T007 [AC-02] `tests/test_docker_healthcheck.py`: compose y `docker inspect`.

## Phase 3: Implementación

- [x] T008 `docker/healthcheck.sh` con los dos modos.
- [x] T009 `Dockerfile`: `COPY`, `chmod` y `HEALTHCHECK`.
- [x] T010 `compose.yml`: healthcheck heredado por `api` y `grpc`.
- [x] T011 `docs/operacion/docker.md`: sección de healthcheck.

## Phase 4: Cierre

- [x] T012 `make check` en verde.
- [x] T013 Rama preparada y pusheada sin PR (modo preparación).
