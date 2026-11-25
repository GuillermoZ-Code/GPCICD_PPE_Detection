# Plan de implementación — HU-083 (spec 084)

**Rama**: `feature/084-hu-083-ci-docker-trivy` · **Issue**: #139 · **Spec**: `spec.md`

## Enfoque

Añadir un único job al workflow de CI ya existente. El job construye la imagen que
se despliega, ejecuta un smoke que no necesita pesos y escanea esa misma imagen con
Trivy. El SARIF se sube como artefacto. La verificación local es estática: 8 pruebas
leen el workflow y el runbook, sin Docker.

## Estructura

- `.github/workflows/ci.yml`: job `docker` (build, smoke, Trivy, artefacto).
- `tests/test_ci_docker_trivy.py`: 8 pruebas AAA con trazabilidad AC.
- `docs/operacion/docker.md`: sección de CI y descarga del reporte.
- `specs/084-hu-083-ci-docker-trivy/`: spec, plan y tareas.

## Decisiones

1. El smoke usa `python -c "from ppe_detection.api import create_app; ..."` dentro
   de la imagen: comprueba que el paquete y la API se construyen sin modelo.
2. Trivy corre con `exit-code: '0'`: reporta HIGH/CRITICAL sin convertir hallazgos
   heredados en un fallo; el job sí falla si el build, el smoke o la subida fallan.
3. `if-no-files-found: error` evita un artefacto vacío silencioso.
4. `permissions` del job: `contents: read` y `actions: write`.

## Riesgos y mitigación

- **Imagen sin modelo**: `create_app()` no dispara el arranque que carga pesos.
- **Versión de Trivy**: se fija `@0.33.0` en lugar de `@master` para repetibilidad.
- **Propiedad**: `.github/` pertenece a Guillermo (aviso, no bloqueo); CODEOWNERS
  pedirá su revisión. `docs/operacion/` es de Eliana; las pruebas son libres.
