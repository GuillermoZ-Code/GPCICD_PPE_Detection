# Feature Specification: HU-072 — SPA con API relativa detrás del proxy

**Feature Branch**: `feature/073-hu-072-spa-api-relativa`

**Created**: 2026-11-25

**Status**: En implementación

**Input**: Issue #128 — «HU-072 — SPA con API relativa detrás del proxy». Asignada a
Guillermo (`GuillermoZ-Code`), épica `ep-11`, P0, ola 1, 2 SP, 8 pruebas objetivo. Sin
dependencias.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - La SPA llama a `/api` en el mismo dominio (Priority: P0)

Como usuario del sistema desplegado, quiero que la interfaz hable con la API usando una
ruta relativa del mismo dominio, para no depender de una URL horneada en el bundle ni de
CORS, y para que el despliegue funcione detrás de cualquier host o proxy.

**Why this priority**: el Dockerfile hornea `VITE_API_URL=http://localhost:8000`
(`Dockerfile:20`), así que la SPA publicada llama al equipo del visitante. Es un fallo
que rompe la demo del M4 y la prueba funcional del sistema desplegado (HU-015).

**Independent Test**: construir la SPA sin `VITE_API_URL` y comprobar que el cliente HTTP
resuelve `POST /api/predict` contra el origen actual; los tests de `config.ts` y
`client.ts` cubren ambos casos sin backend.

**Acceptance Scenarios** (AC de la issue #128):

1. **AC-01**: **Dado** `VITE_API_URL` vacío o sin definir, **Cuando** la SPA construye su
   cliente, **Entonces** usa la ruta relativa `/api`.
2. **AC-02**: **Dado** el servidor de desarrollo de Vite, **Cuando** la SPA llama a
   `/api/predict`, **Entonces** el proxy reenvía la petición a la API local
   (`http://localhost:8000/predict`) y el flujo sigue funcionando.
3. **AC-03**: **Dada** la configuración de la API, **Cuando** se ejecutan las pruebas,
   **Entonces** existen casos para la ruta relativa por omisión y para una URL absoluta
   explícita.

### Edge Cases

- `VITE_API_URL` con solo espacios o saltos de línea: se trata como vacío → `/api`.
- URL absoluta con barras finales (`http://api.local///`): se normaliza a una sola base
  sin barras finales.
- URL absoluta explícita en desarrollo (`http://127.0.0.1:8000`): se respeta tal cual y
  no pasa por el proxy.
- La SPA servida por nginx en `compose.yml`: `/api/*` debe llegar al servicio `api`; el
  prefijo `/api` no forma parte de la ruta del backend (`/predict`, `/health`).
- Sin API levantada: la petición falla en el proxy y la interfaz muestra el estado de
  error; el tratamiento de reintentos es de HU-081, no de esta HU.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La resolución de la base de la API MUST devolver `/api` cuando el valor
  recibido esté vacío, sea `undefined` o contenga solo espacios.
- **FR-002**: La resolución MUST conservar una URL absoluta explícita y quitarle las
  barras finales sobrantes.
- **FR-003**: El cliente de inferencia MUST usar la base resuelta y publicar en
  `{base}/predict`, de modo que la ruta efectiva por omisión sea `/api/predict`.
- **FR-004**: El servidor de desarrollo de Vite MUST exponer un proxy de `/api` hacia la
  API local, eliminando el prefijo antes de reenviar.
- **FR-005**: La imagen `web` (nginx) MUST reenviar `/api/*` al servicio `api` de
  `compose.yml` y mantener la SPA como fallback del resto de rutas.
- **FR-006**: El build de la SPA MUST NOT hornear `http://localhost:8000`; el valor
  por omisión pasa a ser la ruta relativa.

### Key Entities

- **Base de la API**: cadena que antecede a `/predict`; puede ser relativa (`/api`) o
  absoluta (`http://host:puerto`). Se resuelve al construir el cliente, no en tiempo de
  render.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: `npm run build` sin `VITE_API_URL` produce un bundle que llama a
  `/api/predict` (sin `localhost` embebido).
- **SC-002**: Al menos 8 pruebas (Vitest + pytest) cubren los AC-01, AC-02 y AC-03.
- **SC-003**: `make frontend-check` y `make check` quedan en verde.

## Assumptions

- La API expone `POST /predict` en la raíz (`http://api:8000/predict`), de modo que el
  proxy solo reescribe el prefijo `/api`.
- En `compose.yml` el servicio de la API se llama `api` y nginx lo resuelve por DNS
  interno de la red de Compose.
- El despliegue público (Caddy o Droplet) servirá la SPA y la API bajo el mismo origen;
  si no, el operador define `VITE_API_URL` en el build, que sigue siendo compatible.
- El cliente simulado (`MockDetectorClient`) se conserva para pruebas e inyección, pero
  ya no es el comportamiento por omisión de `createClient()`.
