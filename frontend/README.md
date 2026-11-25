# Frontend — GPCICD PPE Detection

Interfaz web de HU-007: **React 19 + Vite 8 + TypeScript 6**.

## Requisitos

- Node.js 24 LTS
- npm 11

## Instalación

```bash
cd frontend
npm ci
```

## Scripts

| Comando | Qué hace |
|---|---|
| `npm run dev` | Servidor de desarrollo en <http://localhost:5173> |
| `npm run build` | Comprueba tipos y genera `dist/` estático |
| `npm run preview` | Sirve el build de producción |
| `npm run lint` | ESLint sobre todo el proyecto |
| `npm run test` | Vitest en modo CI |
| `npm run test:watch` | Vitest en modo interactivo |

## API

- Sin `VITE_API_URL`, la SPA llama a la ruta relativa `/api` (HU-072). En desarrollo, el
  proxy de Vite reenvía `/api/*` a `http://localhost:8000/*` (sin el prefijo).
- `VITE_API_PROXY` cambia el destino del proxy si la API escucha en otro host o puerto.
- Una `VITE_API_URL` absoluta se sigue respetando, por si la API vive en otro origen.
- Copia `.env.example` a `.env.local` o exporta la variable.

```bash
# Desarrollo con la API local (proxy /api → http://localhost:8000)
npm run dev

# API en otro host, sin pasar por el proxy
VITE_API_URL=http://127.0.0.1:8000 npm run dev
```

El cliente HTTP hace `POST {base}/predict` con `multipart/form-data` y el campo
`file`; la base es `/api` por omisión. El contrato está cerrado desde HU-006 y la
respuesta incluye `model_version` y `elapsed_ms`.

La receta completa —descarga de pesos, variables de la API, CORS y verificación— está en
[`docs/operacion/demo-local.md`](../docs/operacion/demo-local.md).

## Estructura

```text
src/
├── api/client.ts        # DetectorClient, HTTP y simulado
├── components/          # UploadPanel, AnnotatedCanvas, DetectionTable, StatusBanner
├── App.tsx              # estados idle / loading / ready / error
├── labels.ts            # nombres legibles y colores por clase
├── validate.ts          # tipo MIME y tamaño máximo
└── types.ts             # espejo del contrato TA-11
```

## Pruebas

- Vitest + Testing Library + jsdom.
- Sin backend, GPU ni red: las pruebas inyectan el cliente simulado y obtienen
  detecciones fijas.
- `src/setupTests.ts` sustituye `URL.createObjectURL` y `canvas.getContext` porque jsdom
  no los implementa.

## Licencia

AGPL-3.0-only. El pie de la aplicación enlaza el código fuente y atribuye el dataset
CC-BY-4.0.
