# Plan de implementación — HU-052 (spec 053)

**Rama**: `feature/053-hu-052-openapi-publica` · **Issue**: #108 · **Spec**: `spec.md`

## Enfoque

Enriquecer el documento OpenAPI generado por FastAPI con metadatos declarativos
(resumen, descripción, respuestas y ejemplos) y publicar una guía de consumidor
en `docs/maas/README.md`. No se cambia la lógica de inferencia ni el contrato de
`PredictResponse`.

## Estructura

- `src/ppe_detection/api/app.py`: metadatos de `/predict`, `/health` y del
  parámetro `conf`; descripción global de la app.
- `tests/test_openapi_publica.py`: 8 pruebas (AC-01 ×4, AC-02 ×2, AC-03 ×2).
- `docs/maas/README.md`: guía pública con URL configurable, curl, Python y límites.
- `specs/053-hu-052-openapi-publica/`: spec, plan y tareas.

## Decisiones

1. La URL pública se documenta como `PPE_MAAS_URL` / `<URL_PUBLICA>` porque
   HU-053 (segunda URL pública) sigue abierta; no se inventa un dominio.
2. Los ejemplos de OpenAPI son estáticos y no dependen del modelo cargado.
3. Los códigos de error documentados son los que ya devuelve el código: 400
   (imagen inválida) y 503 (modelo no cargado). 401 queda para HU-051.
4. La guía cita los límites reales del código: JPEG/PNG, 10 MB y conf 0.01–0.99.
5. Se usa `Form(..., description=..., examples=[0.25])` para documentar `conf`
   sin cambiar sus validaciones `ge`/`le`.

## Riesgos y mitigación

- **Contrato**: los metadatos son aditivos; las pruebas existentes de
  `PredictResponse.required` y de los límites de `conf` deben seguir pasando.
- **Propiedad**: `src/ppe_detection/api/` y `docs/maas/` son de Eliana;
  `specs/` es de Jesús (aviso); las pruebas son libres.
- **Documentación honesta**: se marcan como pendientes las HU no implementadas
  en lugar de prometer funcionalidad inexistente.
