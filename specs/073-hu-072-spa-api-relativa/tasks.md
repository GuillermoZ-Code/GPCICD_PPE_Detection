# Tasks: HU-072 — SPA con API relativa detrás del proxy

**Input**: Design documents from `specs/073-hu-072-spa-api-relativa/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/073-hu-072-spa-api-relativa` desde `develop`.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #128.

## Phase 2: Pruebas (test-first)

- [x] T003 [AC-01] `frontend/src/api/config.test.ts`: vacío, `undefined` y solo espacios
      devuelven `/api`.
- [x] T004 [AC-03] `frontend/src/api/config.test.ts`: URL absoluta se conserva y se le
      quitan las barras finales; `VITE_API_URL` vacía resuelve `/api`.
- [x] T005 [AC-01] `frontend/src/api/client.test.ts`: `createClient('')` y
      `createClient()` sin entorno construyen el cliente HTTP con base `/api`.
- [x] T006 [AC-01] `frontend/src/api/client.test.ts`: el cliente con base `/api` publica
      en `/api/predict`.
- [x] T007 [AC-02] `tests/test_frontend_config.py`: `vite.config.ts` declara el proxy
      `/api` hacia la API local con reescritura del prefijo.
- [x] T008 [AC-02] `tests/test_docker_assets.py`: `nginx.conf` reenvía `/api/` a
      `api:8000` y conserva el fallback de la SPA.
- [x] T009 [AC-01] `tests/test_docker_assets.py`: el Dockerfile ya no hornea
      `localhost:8000` y el stage `web` sigue sirviendo la SPA.

## Phase 3: Implementación

- [x] T010 `frontend/src/api/config.ts`: `DEFAULT_API_BASE` y `resolveApiBaseUrl`.
- [x] T011 `frontend/src/api/client.ts`: `createClient` usa `resolveApiBaseUrl`; el mock
      queda para inyección.
- [x] T012 `frontend/vite.config.ts`: `server.proxy['/api']` con `rewrite` y
      `VITE_API_PROXY` opcional.
- [x] T013 `Dockerfile`: retirar `ARG`/`ENV VITE_API_URL`.
- [x] T014 `compose.yml`: retirar el build arg `VITE_API_URL`.
- [x] T015 `docker/nginx.conf`: `location /api/` con `proxy_pass http://api:8000/`.

## Phase 4: Documentación y cierre

- [x] T016 `frontend/README.md`, `README.md`, `docs/operacion/demo-local.md` y
      `docs/operacion/docker.md`: describir `/api`, el proxy y el mock como inyección.
- [x] T017 `make frontend-check` y `make check` en verde.
- [x] T018 PR con plantilla UAO, `Closes #128`, revisor de otro integrante y
      `make ownership-check` sin bloqueos.
