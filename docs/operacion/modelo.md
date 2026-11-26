# Página «Acerca del modelo» (HU-079)

La SPA muestra la identidad del modelo que produjo las detecciones. Abre el botón
**ⓘ Acerca del modelo** de la barra superior. La vista consulta
`GET /health/ready` en la misma base de la API (`/api` por omisión, o
`VITE_API_URL`) sin cargar el artefacto ni lanzar inferencia.

## Datos mostrados

| Campo visible | Origen en `/health/ready` |
|---------------|---------------------------|
| Versión | `model_version` |
| Referencia (commit) | `model_reference` |
| SHA256 | `model_sha256` (`—` si es `null`) |
| Versión de API | `api_version` |

`ReadyResponse` no publica `commit`, `license` ni `source`. Por eso la vista
etiqueta `model_reference` como «Referencia (commit)» y muestra `api_version`
como versión de la API; los títulos y criterios de la issue #135 no se han
cambiado. La licencia y la fuente son enlaces estáticos, los mismos del pie de
la SPA:

- Código: <https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection> —
  AGPL-3.0-only.
- Dataset: <https://huggingface.co/datasets/51ddhesh/PPE_Detection> — CC-BY-4.0.

Si la API no responde o devuelve un estado distinto de 200 (incluido `503
not_ready`), la vista muestra un aviso de error y un botón **Reintentar**.

## Verificación

```bash
cd frontend
npm test -- --run src/components/ModelInfo.test.tsx
npm run lint
npm test
npm run build
```

Las cuatro pruebas simulan `fetch` con la respuesta exacta de `ReadyResponse`;
no necesitan API, modelo ni red. Contrato completo:
[`docs/architecture/contracts.md`](../architecture/contracts.md).
