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

- `VITE_API_URL` define la base de la API REST (HU-006). Si está vacía, la aplicación
  usa un **cliente simulado** determinista y funciona sin backend.

```bash
# Con API real
VITE_API_URL=http://localhost:8000 npm run dev

# Sin API (cliente simulado)
npm run dev
```

El cliente HTTP hace `POST {VITE_API_URL}/predict` con `multipart/form-data` y el campo
`file`. El contrato definitivo se ajusta cuando cierre HU-006.

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
- Sin backend, GPU ni red: el cliente simulado devuelve detecciones fijas.
- `src/setupTests.ts` sustituye `URL.createObjectURL` y `canvas.getContext` porque jsdom
  no los implementa.

## Licencia

AGPL-3.0-only. El pie de la aplicación enlaza el código fuente y atribuye el dataset
CC-BY-4.0.
