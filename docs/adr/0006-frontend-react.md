# ADR 0006 — Frontend web con React, Vite y TypeScript

- **Fecha:** 2026-11-09
- **Estado:** Aceptada
- **Decisores:** Grupo 4

## Contexto

`CONSTITUTION.md` definía Streamlit como interfaz y la issue #7 dejaba abierta la
elección entre Streamlit y Tkinter. Ninguna de las dos opciones da una experiencia
profesional: Streamlit impone su propio layout y mezcla la UI con Python; Tkinter es de
escritorio y no se despliega como servicio web.

El sistema ya expone (o expondrá) una API REST con FastAPI (HU-006) y un contrato de
datos estable (`ImageData → list[Detection]`, ADR 0005). Eso permite separar la interfaz
del runtime de Python.

## Decisión

Construir la interfaz como una **SPA con React 19, Vite 8 y TypeScript 6** en
`frontend/`, consumiendo la API por HTTP.

- **Pruebas:** Vitest 5 + Testing Library + jsdom.
- **Calidad:** ESLint 10 con typescript-eslint y modo estricto de TypeScript.
- **Entrega:** build estático (`dist/`) que puede servirse desde el propio FastAPI o
  desde cualquier servidor estático.
- **Sin backend para desarrollar:** si `VITE_API_URL` no está definida, la app usa un
  cliente simulado determinista.

Se retiran **Streamlit y Tkinter** del alcance.

## Alternativas consideradas

- **Streamlit:** rápido de escribir, pero sin control real del layout, difícil de probar
  como UI y acoplado a Python. No encaja con un frontend "profesional".
- **Tkinter:** escritorio, no web; no se puede desplegar en el Droplet como servicio.
- **Next.js:** SSR innecesario para una herramienta interna de una sola página; añade
  complejidad de servidor.
- **Vue/Svelte:** válidos, pero el equipo ya conoce React y el ecosistema de pruebas es
  el más maduro.

## Consecuencias

- El repositorio incorpora `package.json`, `package-lock.json` y un job de CI para
  Node 24. `node_modules/` y `dist/` no se versionan.
- La API de HU-006 se vuelve crítica: el frontend depende del contrato HTTP
  (`POST /predict`, multipart `file`).
- La licencia AGPL-3.0-only cubre también el código del frontend.
- El build estático se puede servir desde FastAPI o desde el contenedor de HU-011.
- La issue #7 menciona Streamlit/Tkinter; su texto debe actualizarse cuando Jesús lo
  apruebe. Mientras tanto, este ADR es la fuente de la decisión.
- `CONSTITUTION.md`, `README.md`, `docs/curso/` y la plantilla de PR se actualizan en el
  mismo commit.

## Referencias

- `CONSTITUTION.md` §4, §5, §7, §8 y §11.
- `docs/curso/backlog.md` (HU-007).
- ADR 0005 — contract-first.
- Issue #7.
