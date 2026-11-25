# Plan: HU-062 — Paridad REST/gRPC con el modelo productivo

**Input**: `specs/063-hu-062-paridad-rest-grpc/spec.md` e issue #118.

## Enfoque

1. **Arreglo de tests**: crear `tests/test_paridad_protocolos.py` con helpers para
   generar PNG/JPEG deterministas, `FakeDetector` compartido, `ModelIdentity` fija,
   `TestClient` REST y servidor gRPC en puerto efímero.
2. **AC-01**: comparar detecciones, orden, bbox xyxy, dimensiones e identidad de modelo
   para el mismo contenido binario. Cubrir PNG, JPEG y resultado vacío.
3. **AC-02**: comparar el mapa de errores. La entrada inválida ya coincide
   (400 ↔ INVALID_ARGUMENT); el modelo ausente al construir ya coincide
   (503 ↔ UNAVAILABLE). Falta traducir `DetectorNotConfiguredError` lanzado dentro de
   `detect()` en REST, que hoy escapa como excepción del servidor.
4. **AC-03**: todas las pruebas usan el detector simulado; se comprueba que no se
   lee `PPE_MODEL_PATH` y que el detector se invoca una vez por protocolo.

## Archivos

- `tests/test_paridad_protocolos.py` — nuevo, 13 pruebas (objetivo: 12).
- `src/ppe_detection/api/app.py` — único cambio de producción: envolver la llamada a
  `detect()` para mapear `DetectorNotConfiguredError` a 503.
- `specs/063-hu-062-paridad-rest-grpc/` — spec, plan y tareas.

## Decisiones

- Reutilizar `client.call_status` para extraer código y detalle gRPC, evitando duplicar
  lógica de `RpcError`.
- No tocar el servidor gRPC: ya hace el mapeo correcto.
- No usar red ni pesos: se inyecta el detector en ambos adaptadores.

## Riesgos

- Que `TestClient` propague excepciones del detector: se verifica con el detector que
  falla en `detect()` y se corrige en `app.py`.
- Que el orden de detecciones cambie por `build_inference_result`: se comprueba con
  seis clases y se valida que conserva el orden.
