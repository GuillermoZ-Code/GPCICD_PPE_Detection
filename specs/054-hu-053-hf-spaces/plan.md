# Plan de implementación — HU-053 (spec 054)

**Rama**: `feature/054-hu-053-hf-spaces` · **Issue**: #109 · **Spec**: `spec.md`

## Enfoque

Preparar un paquete de despliegue alternativo reproducible para Hugging Face
Spaces (Docker) y documentar la decisión, la atribución visible y el runbook. No
se intenta crear el Space remoto sin credenciales: el bloqueo se registra en la
issue.

## Estructura

- `deploy/maas-alt/Dockerfile`: imagen CPU con uv congelado y servidor en 7860.
- `deploy/maas-alt/.dockerignore`: excluye secretos, pesos, datos y entornos.
- `deploy/maas-alt/README.md`: tarjeta pública del Space con licencias y enlaces.
- `docs/maas/segunda-url.md`: decisión, runbook y límites.
- `tests/test_segunda_url_publica.py`: 16 pruebas (AC-01 ×6, AC-02 ×4, AC-03 ×6).
- `specs/054-hu-053-hf-spaces/`: spec, plan y tareas.

## Decisiones

1. **HF Spaces Docker** frente a Cloud Run: capa gratuita sin tarjeta de crédito
   y mismo ecosistema que el dataset; Cloud Run queda documentado como alternativa
   si se dispone de proyecto GCP con facturación.
2. El contenedor expone el puerto 7860 que espera Spaces y arranca uvicorn con
   `0.0.0.0`, sin entrypoint interactivo.
3. `uv sync --frozen` sobre `uv.lock` para reproducibilidad; sin `pip`.
4. Los pesos no se copian a la imagen: se inyectan en ejecución, verificados por
   SHA-256 (HU-026). Sin modelo, `/health` reporta `degraded`.
5. Secretos (`HF_TOKEN`, claves de HU-051) solo como *Secrets* del Space, nunca
   en el Dockerfile, la tarjeta ni el repositorio.
6. La URL se deja como `<SPACE_URL>` hasta que exista el Space; no se inventa un
   dominio ni se simula un despliegue.

## Riesgos y mitigación

- **Credenciales:** si no hay cuenta HF con Docker Spaces, no se publica; se
  registra el bloqueo concreto en la issue y la PR queda en revisión.
- **Propiedad:** `deploy/` es de Guillermo (aviso), `docs/maas/` y `.env.example`
  son de Eliana, `specs/` es de Jesús (aviso); las pruebas son libres.
- **Modelo:** sin pesos públicos el Space sirve chequeos de salud pero no
  inferencia; el runbook lo declara explícitamente.
