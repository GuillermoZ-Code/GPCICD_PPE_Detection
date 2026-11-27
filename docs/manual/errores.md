# Catálogo de errores — API e interfaz

> HU-059 · M4-S3 · Fuente: `src/ppe_detection/api/app.py`, `src/ppe_detection/api/security.py`, `src/ppe_detection/io/images.py`, `src/ppe_detection/grpc/servicer.py`, `frontend/src/`.

Este catálogo documenta los códigos HTTP, estados gRPC y mensajes visibles en la SPA para que usuarios y desarrolladores puedan diagnosticar fallos sin soporte.

## 1. REST API

| Código | Endpoint / origen | Causa | Mensaje / detalle observado | Solución recomendada |
|---:|---|---|---|---|
| 200 | `GET /health`, `GET /health/live`, `POST /predict` | Operación exitosa. | `status=ok` o respuesta de predicción con detecciones. | No requiere acción. |
| 200 | `GET /health/ready` | Modelo cargado y listo. | `status=ready`, `model_loaded=true`. | No requiere acción. |
| 400 | `POST /predict` | Imagen vacía, formato no admitido por contenido, o bytes corruptos/no decodificables. | `El archivo está vacío.`; `Formato no admitido: se aceptan JPEG y PNG.`; `No se pudo decodificar la imagen.`; `La imagen supera el límite de 10 MB.` (límite por defecto de `validate_image_bytes`). | Enviar un JPEG/PNG válido, no vacío, menor al límite. Verificar que el archivo no esté dañado. |
| 401 | `POST /predict` | Falta `X-API-Key` o la clave no coincide con `PPE_API_KEYS`/`PPE_API_KEY`. | `X-API-Key inválida o ausente.`; cabecera `WWW-Authenticate: ApiKey`. | Configurar la clave correcta en el cliente. Si el despliegue no usa autenticación, dejar `PPE_API_KEYS` vacío. |
| 413 | `POST /predict` | El archivo supera `PPE_MAX_UPLOAD_MB` cuando la variable está configurada explícitamente. | `Archivo demasiado grande: el límite es {N} MB.` | Reducir el tamaño de la imagen o ajustar `PPE_MAX_UPLOAD_MB` dentro del rango permitido (0 < MB ≤ 1024). |
| 415 | `POST /predict` | MIME anunciado no es `image/png` ni `image/jpeg`. | `Tipo de archivo no permitido: se aceptan image/png e image/jpeg.` | Enviar el archivo con el tipo correcto y contenido JPEG/PNG real. |
| 422 | `POST /predict` | Validación FastAPI/Pydantic: falta `file`, `conf` fuera de 0.01..0.99, o forma del request inválida. | Respuesta de validación FastAPI (`detail` con errores de esquema/campo). | Revisar el contrato OpenAPI: enviar `file` multipart y `conf` opcional dentro del rango. |
| 503 | `GET /health/ready` | El proceso responde, pero el modelo no está cargado. | JSON con `status=not_ready`, `model_loaded=false`. | Esperar la carga del modelo, verificar `PPE_MODEL_PATH`/artefacto y consultar logs de arranque. |
| 503 | `POST /predict` | Detector no configurado o modelo no disponible en tiempo de inferencia. | `Modelo no configurado: defina PPE_MODEL_PATH o entregue un detector al crear la app.` u otro detalle de `DetectorNotConfiguredError`. | Configurar `PPE_MODEL_PATH`/`PPE_MODEL_SHA256` según el despliegue, confirmar que el artefacto existe y reiniciar el servicio. |

## 2. gRPC (`ppe.v1.PpeDetection/Detect`)

| Estado | Origen | Causa | Mensaje / detalle observado | Solución recomendada |
|---|---|---|---|---|
| OK | `PpeDetectionServicer.Detect` | Imagen válida e inferencia exitosa. | `PredictResponse` con detecciones, versión de modelo y latencia. | No requiere acción. |
| INVALID_ARGUMENT | `PpeDetectionServicer.Detect` | `validate_image_bytes` rechaza la imagen (vacía, formato, tamaño, corrupta). | Mensaje de `InvalidImageError`, p. ej. `Formato no admitido: se aceptan JPEG y PNG.` | Enviar bytes JPEG/PNG válidos. Verificar el campo `image` y el límite de 10 MB. |
| UNAVAILABLE | `PpeDetectionServicer.Detect` | `DetectorNotConfiguredError`: no hay modelo configurado/cargable. | Detalle de configuración del detector/modelo. | Configurar el modelo del servicio (`PPE_MODEL_PATH` o inyección de detector) y reiniciar. |
| INTERNAL | `PpeDetectionServicer.Detect` | Excepción no controlada durante la inferencia. | `Error de inferencia: <TipoExcepcion>`. | Revisar logs del servidor, versión del modelo, compatibilidad de dependencias y recursos del host. Reintentar tras corregir la causa. |

## 3. Interfaz web (SPA)

| Mensaje / estado UI | Capa | Causa probable | Acción recomendada |
|---|---|---|---|
| `La API respondió con estado {status}.` | `frontend/src/api/client.ts` | `fetch /predict` devolvió `response.ok === false`; el cliente HTTP actual no parsea el cuerpo de error. | Revisar la pestaña Network/Console, identificar el código HTTP y aplicar la solución de la tabla REST. |
| `No fue posible analizar la imagen. {detalle}` | `frontend/src/App.tsx` | Error de red, CORS, timeout del navegador, o excepción del cliente al llamar `/predict`. | Verificar conectividad con la API, configuración de CORS/proxy, y que la imagen cumpla formato/tamaño. |
| `No fue posible cargar la información del modelo. {detalle}` | `frontend/src/components/ModelInfo.tsx` | Falló `GET /health/ready` o la respuesta no fue OK. | Confirmar que la API esté disponible y que el modelo haya cargado; revisar 503 en `/health/ready`. |
| `No se detectaron EPP en la imagen. La inferencia terminó sin errores; la imagen puede no contener los objetos que el modelo reconoce.` | `frontend/src/App.tsx` | Predicción exitosa con lista de detecciones vacía. | Probar con otra imagen, revisar iluminación/encuadre y confirmar el modelo esperado en `/health/ready`. |
| `La confianza más alta fue {X}%, por debajo del umbral actual ({Y}%). Baja el umbral si quieres inspeccionar estas detecciones.` | `frontend/src/App.tsx` | Hay detecciones, pero todas quedan bajo el umbral seleccionado en la UI. | Bajar el umbral de confianza o usar una imagen con EPP más visible. |
| `La inferencia está tardando más de lo habitual. Sigue en curso; si el modelo está cargando por primera vez, puede demorar un poco.` | `frontend/src/App.tsx` | La petición sigue en curso y superó el umbral lento de UI. | Esperar; si persiste, revisar carga del modelo, CPU/memoria del despliegue y logs. |

## 4. Relación con pruebas

La prueba `tests/test_api_catalogo_errores.py` verifica que este catálogo contenga todos los códigos HTTP y estados gRPC usados por la API actual, además de los mensajes UI clave. Si se agrega un nuevo código/estado, debe actualizarse este documento y la prueba en el mismo cambio.