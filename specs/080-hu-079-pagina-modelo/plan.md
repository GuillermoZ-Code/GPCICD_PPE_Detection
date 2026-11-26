# Plan de implementación — HU-079 (spec 080)

**Rama**: `feature/080-hu-079-pagina-modelo` · **Issue**: #135 · **Spec**: `spec.md`

## Enfoque

Un componente autocontenido `ModelInfo` consulta `/health/ready` usando la base
resuelta por `resolveApiBaseUrl()`. La SPA abre la vista desde un botón en la
barra superior. El componente no conoce el detector ni el cliente de inferencia:
solo consume un contrato HTTP ya publicado.

## Estructura

- `frontend/src/types.ts`: tipo espejo `ReadyResponse`.
- `frontend/src/components/ModelInfo.tsx`: estados `loading | ready | error` y
  enlaces de licencia/fuente.
- `frontend/src/components/ModelInfo.test.tsx`: 4 pruebas Vitest con `fetch`
  simulado.
- `frontend/src/App.tsx`: botón «Acerca del modelo» y render condicional.
- `docs/operacion/modelo.md`: guía de uso y nota del contrato.
- `specs/080-hu-079-pagina-modelo/`: spec, plan y tareas.

## Decisiones

1. `commit` no existe en `ReadyResponse`: se muestra `model_reference` con la
   etiqueta «Referencia (commit)» y `api_version`; la issue no se modifica.
2. Licencia y fuente son enlaces estáticos ya usados en el pie de la SPA.
3. `apiBaseUrl` es una prop opcional; por omisión usa `resolveApiBaseUrl()` para
   que las pruebas puedan inyectar una base sin depender de variables de entorno.
4. Cualquier respuesta `!ok` (incluido 503 `not_ready`) entra en estado de error;
   el botón «Reintentar» vuelve a lanzar la consulta.
5. El estado de error usa `StatusBanner tone="error"`, ya existente en la SPA.

## Riesgos y mitigación

- **Propiedad**: `frontend/` es de Guillermo (aviso, no bloqueo); `specs/` es de
  Jesús (aviso); `docs/operacion/` es de Eliana.
- **Contrato**: no se toca el backend; las pruebas simulan la respuesta exacta
  de `ReadyResponse`.
- **Carga diferida**: `ModelInfo` solo hace `fetch` al montarse, por lo que abrir
  la vista no dispara inferencia ni carga del modelo.
