# Plan: HU-059 — Catálogo de errores de API e interfaz

## Enfoque

Documentar el contrato de errores actual sin cambiar comportamiento runtime. La fuente de verdad son los códigos/estados presentes en la API y servicer gRPC; la UI se mapea a causas y soluciones.

## Archivos

- `docs/manual/errores.md` — catálogo principal.
- `tests/test_api_catalogo_errores.py` — cobertura AC-01..AC-03.
- `specs/060-hu-059-catalogo-errores/{spec,plan,tasks}.md` — SDD.

## Diseño

1. Inventariar códigos REST desde `api/app.py`, `api/security.py`, `io/images.py`.
2. Inventariar estados gRPC desde `grpc/servicer.py` (`INVALID_ARGUMENT`, `UNAVAILABLE`, `INTERNAL`) y `OK`.
3. Inventariar mensajes UI desde `frontend/src/App.tsx`, `frontend/src/api/client.ts`, `frontend/src/components/ModelInfo.tsx`.
4. Escribir catálogo con tablas por capa: REST, gRPC, UI.
5. Prueba: parsea catálogo y verifica presencia de todos los códigos/estados y mensajes UI clave.

## Verificación

```bash
uv run pytest -v tests/test_api_catalogo_errores.py
uv run pytest -o addopts="" -q
uv run pre-commit run --all-files --show-diff-on-failure
```

## Riesgos

- Códigos implícitos de FastAPI (422) pueden omitirse si solo se buscan `HTTPException`; la prueba debe incluir el contrato esperado.
- El catálogo puede quedar desalineado si cambia la API; la prueba lo detecta.