# Implementation Plan: HU-072 — SPA con API relativa detrás del proxy

**Branch**: `feature/073-hu-072-spa-api-relativa` | **Date**: 2026-11-25 | **Spec**:
[spec.md](./spec.md)

**Input**: Feature specification from `specs/073-hu-072-spa-api-relativa/spec.md`

## Summary

Sustituir la URL de la API horneada en el bundle por una resolución única que devuelve
`/api` cuando no hay configuración, y hacer que ese prefijo funcione en los dos entornos
reales: el servidor de desarrollo de Vite (proxy) y la SPA servida por nginx en
`compose.yml` (proxy inverso al servicio `api`). Se retira el `ARG VITE_API_URL` del
Dockerfile y el valor de `compose.yml`.

## Technical Context

**Language/Version**: TypeScript 6 (frontend), Python 3.13 (pruebas estáticas)

**Primary Dependencies**: React 19, Vite 8, Vitest 5, nginx 1.29 (imagen `nginx:alpine`)

**Storage**: N/A

**Testing**: Vitest + Testing Library (frontend) y pytest (pruebas estáticas de Docker y
nginx, sin Docker ni red)

**Target Platform**: navegador; contenedor `web` sobre Linux

**Project Type**: aplicación web (SPA + API REST)

**Performance Goals**: sin cambio; el proxy añade un salto local dentro del mismo host

**Constraints**: el bundle no puede contener `localhost`; una sola fuente de verdad para
la base de la API; sin dependencias nuevas

**Scale/Scope**: 1 módulo nuevo (`frontend/src/api/config.ts`), 2 archivos de
configuración (`vite.config.ts`, `docker/nginx.conf`) y 2 de build (`Dockerfile`,
`compose.yml`)

## Constitution Check

- **uv / npm**: sin dependencias nuevas; se respeta `package-lock.json`. ✅
- **Test-first**: cada AC tendrá prueba que lo referencia antes de la implementación. ✅
- **Calidad**: `make frontend-check` y `make check` en verde. ✅
- **Contract-first**: el contrato `DetectorClient` no cambia; solo cambia la resolución
  de la base. ✅
- **Sin secretos ni rutas absolutas horneadas**: se elimina `localhost:8000` del bundle. ✅
- **Propiedad**: `frontend/`, `Dockerfile`, `compose.yml` y `docker/` son de Guillermo;
  las pruebas `tests/test_docker*.py` no tienen dueño asignado. ✅

## Project Structure

### Documentation (this feature)

```text
specs/073-hu-072-spa-api-relativa/
├── spec.md
├── plan.md
└── tasks.md
```

### Source Code

```text
frontend/src/api/config.ts          # nuevo: resolveApiBaseUrl + DEFAULT_API_BASE
frontend/src/api/config.test.ts     # nuevo: AC-01 y AC-03
frontend/src/api/client.ts          # createClient usa la base resuelta
frontend/src/api/client.test.ts     # actualiza el caso por omisión a /api
frontend/vite.config.ts             # proxy /api → API local (AC-02)
frontend/README.md                  # cómo se resuelve la base
Dockerfile                          # sin ARG/ENV VITE_API_URL (AC-01)
compose.yml                         # sin build arg VITE_API_URL
docker/nginx.conf                   # location /api/ → api:8000 (AC-02)
tests/test_docker_assets.py         # pruebas estáticas de nginx y Dockerfile
tests/test_frontend_config.py       # prueba estática del proxy de Vite
README.md                           # sección del frontend: /api en vez de mock
docs/operacion/demo-local.md        # demo local con proxy y make app
docs/operacion/docker.md            # el proxy sustituye al build arg
```

## Design decisions

1. **Un módulo, una responsabilidad.** `frontend/src/config.ts` ya existe y contiene las
   preferencias de interfaz (tema, acento, densidad). La base de la API vive en
   `frontend/src/api/config.ts` para no mezclar preferencias con transporte. La issue
   menciona `frontend/src/config.ts`; se interpreta como «la configuración», no como el
   archivo concreto.
2. **El valor por omisión es `/api`.** Se aplica el AC-01 en `resolveApiBaseUrl`, con
   `trim()` y sin barras finales. `createClient()` deja de caer en el mock: el mock queda
   disponible para inyección en pruebas.
3. **El proxy reescribe el prefijo.** Vite (`rewrite`) y nginx (`proxy_pass` con barra
   final) eliminan `/api`, así que `POST /api/predict` llega como `POST /predict`.
4. **Sin dependencias nuevas.** El proxy de Vite usa `loadEnv(mode, '.', '')` de `vite`
   con `VITE_API_PROXY` opcional, sin `process` ni `@types/node`.
5. **Docker deja de hornear la URL.** Sin `ARG VITE_API_URL`, el bundle usa `/api`; el
   operador aún puede definir `VITE_API_URL` en el build si la API vive en otro origen.

## Risks

| Riesgo | Mitigación |
|---|---|
| `make frontend-dev` sin API muestra error en vez del mock | Documentado en `demo-local.md`: usar `make app` o definir `VITE_API_URL`; el estado de error lo trata HU-081 |
| El proxy de nginx depende del nombre `api` en Compose | Prueba estática del `location /api/` y `proxy_pass http://api:8000/`; el servicio ya se llama `api` |
| Usuarios con `VITE_API_URL` absoluta | Se sigue respetando y normalizando (FR-002) |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `frontend/src/api/config.test.ts` (vacío, espacios, `import.meta.env` vacío), `tests/test_docker_assets.py` (sin `localhost:8000` horneado) |
| AC-02 | `tests/test_frontend_config.py` (proxy de Vite + rewrite) y `tests/test_docker_assets.py` (nginx `/api/` → `api:8000`) |
| AC-03 | `frontend/src/api/config.test.ts` (URL absoluta, barras finales) y `frontend/src/api/client.test.ts` (`/api/predict`) |
