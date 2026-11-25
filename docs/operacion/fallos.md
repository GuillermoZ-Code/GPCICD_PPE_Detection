# Runbook de diagnóstico de fallos (M4)

Guía para responder una falla simulada durante la sustentación. Recorre las etapas
en orden; no saltes a la siguiente sin descartar la anterior. Sustituye los marcadores
`<...>` por los valores del entorno. **No pegues tokens ni contraseñas en el chat ni
en el issue.**

## Árbol de decisión

### Etapa 1 — pipeline

- **Síntoma:** el merge no disparó el pipeline o un job quedó en `failed`.
- **Diagnóstico:** `glab ci status` y, si hay un job rojo, `glab ci view <job>`;
  `glab ci trace <job>` muestra el log completo.
- **Acción:** corregir el commit que rompió la compuerta (Ruff, formato, `ty`,
  pytest u `ownership`) y repetir el pipeline. No fusionar con el job rojo.

### Etapa 2 — registry

- **Síntoma:** el job `build_image` falla al subir, o el deploy descarga una imagen
  antigua.
- **Verificación:** comparar el SHA de la imagen publicada con el commit desplegado;
  revisar los permisos del token de Registry en las variables CI enmascaradas.
- **Acción:** republicar la imagen con el tag del commit y confirmar que el manifiesto
  expuesto coincide. Nunca exponer el token: solo verificar que existe.

### Etapa 3 — SSH

- **Síntoma:** `Permission denied`, `Connection timed out` o el job `deploy` no entra
  al Droplet.
- **Verificación:** comprobar la llave y el usuario del secret de CI, que el puerto
  SSH esté abierto y que el directorio de destino exista.
- **Acción:** restaurar la llave en variables CI enmascaradas y repetir el deploy.
  Si el host cambió, actualizar la variable con el Code Reviewer.

### Etapa 4 — contenedor

- **Síntoma:** `/health` no responde, el contenedor se reinicia o aparece `unhealthy`.
- **Verificación:** `docker ps -a --filter name=ppe` y los logs del contenedor.
- **Acción:** leer el error de arranque; si es configuración, corregir el `.env` del
  host; si es el modelo, pasar a la etapa 6. Reiniciar solo tras identificar la causa.

### Etapa 5 — proxy

- **Síntoma:** el dominio responde 502/504 o el API funciona por puerto pero no por
  HTTPS.
- **Verificación:** comparar `curl` al puerto interno contra `curl` al dominio; revisar
  que el upstream del proxy apunte al contenedor correcto.
- **Acción:** corregir el upstream o el certificado y recargar el proxy. No desactivar
  HTTPS como «solución rápida».

### Etapa 6 — modelo

- **Síntoma:** `/health` responde bien pero `/predict` falla, devuelve vacío o carga
  un artefacto distinto al esperado.
- **Verificación:** consultar el metadata de la respuesta y comparar `model_sha256`
  con `models.lock`; comprobar que el archivo de pesos esté montado y legible.
- **Acción:** restaurar el artefacto versionado correspondiente y reiniciar el API.
  Si la respuesta no muestra EPP, verificar umbrales antes de hablar de fallo.

## Recetario de comandos

| Herramienta | Comando | Cómo leer la salida |
| :--- | :--- | :--- |
| `glab` | `glab ci status` / `glab ci trace <job>` | **Interpretación:** muestra el job que falló y el log; un `exit 1` en Ruff o pytest señala la compuerta rota. |
| `docker logs` | `docker logs --tail 200 <contenedor>` | **Interpretación:** revela excepciones de arranque, falta de pesos o errores de configuración del API. |
| `docker inspect` | `docker inspect --format '{{.State.Health.Status}} {{.State.RestartCount}}' <contenedor>` | **Interpretación:** `unhealthy` o un `RestartCount` creciente confirma inestabilidad del contenedor. |
| `curl` | `curl -fsS https://<host>/health` | **Interpretación:** un 200 con `model_loaded: true` descarta red y proxy; un 502/504 apunta al proxy. |

Comandos adicionales: `ssh <usuario>@<host>` para inspeccionar el Droplet y
`curl -fsS -X POST -F file=@<imagen> https://<host>/predict` para validar inferencia.
**Advertencia:** `docker restart`, `docker compose down` y cualquier cambio de `.env`
interrumpen el servicio; ejecutarlos solo después de identificar la causa y avisar al
equipo.

## Fallos simulados

### F1 — Pipeline rojo por compuerta de propiedad

- **Síntoma:** PR en rojo; el job `ownership` marca un archivo `[[locked]]` ajeno.
- **Verificación:** `glab ci trace ownership` muestra la ruta y el dueño; comparar con
  `docs/curso/propiedad.toml`.
- **Acción:** mover el cambio a la HU/rama de su dueño o quitar el archivo del diff;
  no editar `propiedad.toml` ni `CODEOWNERS` a mano.
- **Resultado esperado:** el job `ownership` pasa y el PR queda listo para revisión
  sin tocar archivos bloqueados.

### F2 — Contenedor unhealthy por pesos ausentes

- **Síntoma:** `/health` no responde y `docker ps` marca `unhealthy`.
- **Verificación:** `docker logs --tail 200 <contenedor>` muestra error al abrir el
  artefacto; `docker inspect` confirma reinicios.
- **Acción:** montar el artefacto versionado en `PPE_MODELS_DIR`, verificar el SHA256
  y reiniciar el servicio avisando al equipo.
- **Resultado esperado:** `/health` devuelve 200 con el modelo cargado y `/predict`
  responde con las seis clases posibles, sin clase `person` ni `no-EPP`.

### F3 — Proxy devuelve 502 aunque el API está sano

- **Síntoma:** el dominio falla con 502 pero `curl` al puerto interno del API responde.
- **Verificación:** `curl -fsS https://<host>/health` contra `curl -fsS http://127.0.0.1:<puerto>/health`
  desde el Droplet; revisar el upstream del proxy.
- **Acción:** corregir el upstream para que apunte al contenedor activo y recargar la
  configuración del proxy; conservar HTTPS.
- **Resultado esperado:** el healthcheck por dominio y la inferencia por dominio
  devuelven 200 sin cambios en el código del detector.

## Registro de ensayos

| Validación | Estado | Evidencia |
| :--- | :--- | :--- |
| **Validación estática** del documento (etapas, comandos y tres fallos simulados) | Realizada por Eliana Cardona el 2026-11-24 con `uv run pytest tests/test_docs_runbook_fallos.py` | 6 pruebas automatizadas sobre este archivo |
| **Ensayo del equipo** (tres fallos simulados, cronometrado en la sesión M4) | **Pendiente** — requiere el entorno de despliegue y la participación del equipo | Completar fecha, participantes y resultado real al ejecutar la prueba en vivo |

> El registro distingue la revisión documental del ensayo real. No se afirma que el
> equipo haya ejecutado los tres fallos hasta que se complete la segunda fila.

## Referencias

- [`docker.md`](./docker.md) — arranque local y compose.
- [`demo-local.md`](./demo-local.md) — demostración de inferencia.
- [`RUBRICA-M4.md`](../entrega/RUBRICA-M4.md) — criterios de la sustentación.
