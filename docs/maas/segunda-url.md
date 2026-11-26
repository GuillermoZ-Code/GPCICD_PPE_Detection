# Segunda URL pública del modelo (HU-053)

Esta guía deja listo para publicar el servicio en una segunda URL pública,
`<SPACE_URL>`, como alternativa al Droplet. El dominio real se escribe al crear
el Space; **no se inventa** un nombre ni se simula un despliegue sin credenciales.

## 1. Decisión del destino (AC-01)

| Opción | Ventaja | Coste / requisito |
|--------|---------|-------------------|
| Google Cloud Run | Escalado a cero y capa gratuita | Proyecto GCP con facturación y `gcloud` |
| Hugging Face Spaces (Docker) | Misma comunidad que el dataset, sin tarjeta de crédito | Cuenta HF con Docker Spaces disponible |

**Elegida:** Hugging Face Spaces con Docker SDK. La capa gratuita cubre el
tráfico de demostración del curso y evita configurar facturación; Cloud Run
queda como alternativa documentada si el equipo dispone de proyecto GCP.

El contenedor expone el puerto `7860`, que es el que espera Spaces, y sirve la
API FastAPI con uvicorn en `0.0.0.0`. La inferencia es CPU: la réplica no promete
GPU ni latencias del Droplet. El límite de entrada sigue siendo 10 MB por imagen
JPEG/PNG y el resultado depende de los pesos, que no viajan en la imagen.

> **Bloqueo operativo (registrado en la issue #109):** crear el Space remoto
> requiere una cuenta de Hugging Face con Docker Spaces habilitado y permisos
> para publicar. Esta sesión no dispone de esa credencial, así que los artefactos
> quedan listos y verificados, pero la URL `<SPACE_URL>` no se ha creado. No se
> marca la HU como terminada hasta que el Space exista y se compruebe.

## 2. Artefactos y atribución (AC-02)

- `deploy/maas-alt/Dockerfile`: imagen CPU con dependencias fijadas por `uv.lock`.
- `deploy/maas-alt/.dockerignore`: excluye secretos, pesos, datos y entornos.
- `deploy/maas-alt/README.md`: tarjeta pública del Space. Hugging Face la
  renderiza en la página del Space, por lo que la atribución es visible sin
  entrar al código.

En esa tarjeta se indican juntos el enlace al código
<https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection> bajo AGPL-3.0-only y el
dataset <https://huggingface.co/datasets/51ddhesh/PPE_Detection> con licencia del
dataset CC-BY-4.0. La licencia del dataset no relicencia el código: AGPL-3.0-only
sigue gobernando la implementación. El resultado no evalúa cumplimiento (no hay
clase `person` ni `no-EPP`).

## 3. Construcción y prueba local (AC-03)

Desde la raíz del repositorio:

```bash
docker build -f deploy/maas-alt/Dockerfile -t gpcicd-ppe-alt:ci .
docker run --rm -p 7860:7860 \
  -e PPE_MODEL_PATH=/models/best.pt \
  -v <DIR_MODELES>:/models:ro gpcicd-ppe-alt:ci
curl -sS http://localhost:7860/health
```

La imagen usa `uv sync --frozen`, sin `pip` y sin `requirements.txt`. Los pesos
quedan **fuera de la imagen** y se montan en ejecución; su SHA-256 debe
corresponder con el manifest de HU-026. Sin `PPE_MODEL_PATH`, `/health` informa
`model_loaded: false` y `/predict` responde 503, pero el servicio sigue vivo.

Los secretos (`HF_TOKEN` para publicar y, cuando se active HU-051, la clave de
API) se declaran solo en la sección *Secrets* del Space y no se versionan en el
repositorio ni se copian al contexto de construcción: `.dockerignore` excluye
`.env`, `.venv`, `*.pt`, `data/` y `runs/`.

## 4. Publicación reproducible

1. En Hugging Face, pulsar **New Space** y elegir *Docker* como SDK.
2. Subir el contenido de `deploy/maas-alt/` como raíz del Space y el código fuente
   del proyecto en el mismo repositorio, respetando el contexto de build de la
   raíz. Definir el puerto `7860`.
3. Configurar en *Secrets* solo las variables necesarias: `PPE_MODEL_PATH` y, si
   aplica, `HF_TOKEN` para descargar pesos desde un repositorio privado.
4. Esperar a que el build termine y comprobar `GET /health` en `<SPACE_URL>`.
5. Anotar la URL definitiva en la issue #109 y actualizar la guía
   `docs/maas/README.md` (HU-052) y los enlaces públicos del README (HU-061).

Hasta que el paso 5 ocurra, esta HU queda en revisión con el bloqueo documentado;
no se afirma que existe una URL operativa.

## Verificación

```bash
uv run pytest -o addopts="" -q tests/test_segunda_url_publica.py
```

Las 16 pruebas son estructurales: validan decisión, atribución y reproducibilidad
sin depender de red ni de credenciales.
