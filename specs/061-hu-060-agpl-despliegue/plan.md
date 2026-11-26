# Plan de implementación — HU-060 (spec 061)

**Rama**: `feature/061-hu-060-agpl-despliegue` · **Issue**: #116 · **Spec**: `spec.md`

## Enfoque

Ampliar `GET /health` con dos campos que identifican el código servido:
`source_url` y `commit`. Los valores vienen de variables de entorno con
valores por omisión explícitos y se resuelven al crear la aplicación, de modo
que la respuesta sea estable durante el ciclo de vida del proceso.

## Estructura

- `src/ppe_detection/api/app.py`: nuevos campos en `HealthResponse` y values en
  `health()`; sin tocar `/live` ni `/ready`.
- `tests/test_agpl_despliegue.py`: 4 pruebas (AC-01 ×2, AC-02, AC-03).
- `docs/operacion/licencias-despliegue.md`: variables y atribución CC-BY.
- `specs/061-hu-060-agpl-despliegue/`: spec, plan y tareas.

## Decisiones

1. `PPE_SOURCE_URL` por omisión apunta al repositorio público AGPL del proyecto.
2. `PPE_DEPLOY_COMMIT` es opcional: vacío o ausente se publica como `null`.
3. No se modifica `Settings`: estas dos variables son metadatos de despliegue,
   no parámetros de inferencia, y así se evita romper constructores existentes.
4. La atribución CC-BY se verifica sobre el pie de `App.tsx` (ya implementado);
   no se duplica enlace en el backend.
5. El OpenAPI se genera de `HealthResponse`, por lo que los campos nuevos quedan
   documentados automáticamente.

## Riesgos y mitigación

- **Contrato**: agregar campos es aditivo; las pruebas de `/health` existentes
  comprueban claves concretas, no igualdad de diccionario.
- **Propiedad**: `src/ppe_detection/api/` y `docs/operacion/` son de Eliana;
  `specs/` es de Jesús (aviso); las pruebas son libres.
- **Privacidad**: no se publican rutas locales ni secretos; solo URL pública y
  SHA del commit.
