# Plan de implementación — HU-084 (spec 085)

**Rama**: `feature/085-hu-084-optimizar-imagen` · **Issue**: #140 · **Spec**: `spec.md`

## Enfoque

Separar la resolución de dependencias de la imagen publicada. `runtime-deps`
ejecuta uv sobre los manifiestos y el código; `runtime` hereda la misma base de
Python, instala solo las librerías del sistema, copia `.venv` y `src`, crea un
usuario sin privilegios y cambia a él antes del `ENTRYPOINT`. La caché de uv se
desactiva y la lista de apt se borra en la misma capa.

## Estructura

- `Dockerfile`: etapas `runtime-deps` y `runtime` optimizadas; `web` intacta.
- `tests/test_optimizacion_imagen.py`: 4 pruebas estáticas AAA con trazabilidad AC.
- `docs/operacion/docker.md`: sección nueva con tamaño antes/después y comando de medición.
- `specs/085-hu-084-optimizar-imagen/`: spec, plan y tareas.

## Decisiones

1. `.venv` se copia con `COPY --chown` desde `runtime-deps`; no se instala uv en
   la etapa final.
2. Se conserva `src/` en el runtime porque el proyecto se instala en modo editable.
3. `UV_NO_CACHE=1` evita bytes de caché sin depender de capas de limpieza.
4. `USER appuser` se declara después de `chmod` y antes de `ENTRYPOINT`.
5. El tamaño se mide en un runner con Docker con el mismo comando para ambas
   versiones del `Dockerfile` y se registra en MB antes de abrir la PR.

## Riesgos y mitigación

- **Permisos**: `PYTHONDONTWRITEBYTECODE=1` ya está fijado; los archivos se copian
  con `--chown=appuser:appuser`.
- **Compatibilidad**: las pruebas de HU-011 y el smoke de HU-083 Se ejecutan sin
  cambios para verificar que el target `runtime` sigue sirviendo la API.
- **Propiedad**: `Dockerfile` pertenece a Guillermo (aviso, no bloqueo);
  `docs/operacion/` es de Eliana; las pruebas son libres.
