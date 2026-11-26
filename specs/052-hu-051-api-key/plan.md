# Plan de implementación — HU-051 (spec 052)

**Rama**: `feature/052-hu-051-api-key` · **Issue**: #107 · **Spec**: `spec.md`

## Enfoque

Añadir un módulo de seguridad puro (`security.py`) que resuelve y compara claves,
y conectarlo a `create_app()` como dependencia exclusiva de `/predict`. El
comportamiento sin claves es idéntico al actual, por lo que las pruebas
existentes no se modifican.

## Estructura

- `src/ppe_detection/api/security.py`: `configured_keys()` e `is_authorized()`.
- `src/ppe_detection/api/app.py`: guarda `Depends` en `/predict` y código 401 en
  los metadatos de la ruta.
- `.env.example`: documentación de `PPE_API_KEYS` y `PPE_API_KEY` (compatibilidad).
- `tests/test_api_key.py`: 12 pruebas (AC-01 ×6, AC-02 ×3, AC-03 ×3).
- `specs/052-hu-051-api-key/`: spec, plan y tareas.

## Decisiones

1. `PPE_API_KEYS` (plural) es la variable principal; `PPE_API_KEY` se conserva
   como fallback para no romper HU-044.
2. Se comparan digests SHA-256 con `hmac.compare_digest` acumulando el resultado
   con `|=`, sin `any()` ni `break`, para no cortocircuitar y no filtrar qué clave
   coincidió.
3. La guarda se crea dentro de `create_app()` capturando las claves resueltas al
   arrancar: cambiar el entorno en caliente no altera una instancia ya creada.
4. Solo `/predict` lleva la dependencia; los healthchecks siguen públicos.
5. El error 401 usa `detail` genérico y `WWW-Authenticate: ApiKey`, sin eco de la
   clave recibida.

## Riesgos y mitigación

- **Compatibilidad:** sin variables, `configured_keys()` devuelve `()` y la guarda
  es transparente; las pruebas actuales de `/predict` deben seguir pasando.
- **Propiedad:** `src/ppe_detection/api/` y `.env.example` son de Eliana;
  `specs/` es de Jesús (aviso); las pruebas son libres.
- **Secretos:** las claves no se versionan, no se registran y no aparecen en
  mensajes de error; el middleware de logs no se toca.
