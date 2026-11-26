# Plan de implementación — HU-050 (spec 051)

**Rama**: `feature/051-hu-050-smoke-remoto` · **Issue**: #106 · **Spec**: `spec.md`

## Enfoque

Un único módulo de herramientas con transportes inyectables. El CLI usa `urllib` para
REST y el cliente gRPC existente; las pruebas sustituyen ambos por objetos simples.
No se tocan contratos ni dependencias.

## Estructura

- `src/ppe_detection/tools/smoke_remote.py`: tipos de transporte, comprobaciones,
  informe y CLI.
- `tests/test_smoke_remote.py`: 8 pruebas AAA con transportes simulados.
- `docs/operacion/fallos.md`: sección de verificación remota en el runbook.
- Esta spec, `plan.md` y `tasks.md`.

## Decisiones

1. `urllib.request` evita una dependencia HTTP nueva; el cuerpo multipart se construye
   con `email`-style boundaries del propio módulo.
2. Los transportes son callables inyectados en `run_checks`; `main` los construye con
   la configuración real y convierte excepciones en comprobaciones fallidas.
3. `/health/ready` es la compuerta de disponibilidad; si falla, se sigue reportando el
   resto para dar un diagnóstico completo, pero el código de salida es 1.
4. La versión del modelo se toma de `ready` y se compara con la de cada predicción.
5. La latencia se lee de `elapsed_ms` de la respuesta; no se mide el transporte.

## Riesgos y mitigación

- **Multipart mal formado**: se usa un boundary aleatorio y `Content-Disposition`
  explícito; la prueba simulada compara los bytes enviados.
- **Diferencia de errores gRPC**: se normaliza `grpc.RpcError` con `call_status` del
  cliente existente, sin depender de atributos dinámicos en el tipado.
- **Propiedad**: `src/ppe_detection/tools/` y `specs/` tienen dueño ajeno (aviso, no
  bloqueo); `docs/operacion/` y `tests/test_smoke_remote.py` son libres o de Eliana.
