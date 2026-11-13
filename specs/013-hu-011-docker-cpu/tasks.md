# Tasks: HU-011 — Ejecutar el sistema en un contenedor Docker CPU

**Branch**: `feature/012-hu-011-docker-cpu` · **Issue**: #11 · **Spec**: [spec.md](spec.md)

## 1. Especificación (Spec Kit)

- [x] T1.1 Crear `specs/013-hu-011-docker-cpu/spec.md` con los AC de la issue.
- [x] T1.2 Registrar el plan de diseño y las alternativas (`plan.md`).
- [x] T1.3 Listar tareas verificables (`tasks.md`).
- [ ] T1.4 Enlazar la spec en `specs/README.md` y `docs/curso/backlog.md`.

## 2. Pruebas primero (test-first)

- [ ] T2.1 Registrar la marca `docker` en `pyproject.toml`.
- [ ] T2.2 `tests/test_docker.py`: pruebas estáticas de AC-011.1 (uv + lock,
      libglib/libgomp, entrypoint con finales Unix), AC-011.3 (sin pesos en el
      Dockerfile, `.dockerignore`, `.gitignore`, montaje `:ro`) y AC-011.4
      (runbook con build/config/arranque/inferencia).
- [ ] T2.3 `tests/test_docker.py`: prueba `@pytest.mark.docker` de AC-011.2
      (REST + gRPC dentro del contenedor con el contrato de HU-006/HU-010).
- [ ] T2.4 Verificar que las estáticas fallan antes de la implementación (rojo).

## 3. Dependencias y resolución CPU

- [ ] T3.1 Extra `grpc` (`grpcio`) en `pyproject.toml` como runtime.
- [ ] T3.2 Índice `pytorch-cpu` + `tool.uv.sources` con marcador
      `sys_platform == 'linux'` para `torch`/`torchvision`.
- [ ] T3.3 Regenerar `uv.lock` (`uv lock`) y verificar que el entorno Windows no
      cambia (`uv sync` sin reinstalar versiones).

## 4. Contenedor

- [ ] T4.1 `Dockerfile` multi-stage: `frontend-builder` (node:24), `runtime`
      (python:3.13-slim + uv + `libglib2.0-0t64`, `libgomp1`), `web` (nginx).
- [ ] T4.2 `docker/entrypoint.sh` con `PPE_SERVICES` (`rest`, `grpc`, `rest,grpc`)
      y advertencia si el artefacto no existe; finales de línea Unix.
- [ ] T4.3 `docker/nginx.conf` para el build estático de la SPA.
- [ ] T4.4 `.dockerignore` bloqueando pesos, datasets, secretos y cachés.
- [ ] T4.5 `compose.yml` con `api`, `grpc` y `frontend` montando
      `${PPE_MODELS_DIR:-./artifacts}:/models:ro`.
- [ ] T4.6 Targets del `Makefile`: `docker-build`, `docker-build-web`,
      `docker-up`, `docker-down`, `docker-smoke`.

## 5. Validación (evidencia para la issue #11)

- [ ] T5.1 `make check` + `uv build` en verde.
- [ ] T5.2 `uv run pre-commit run --all-files` en verde.
- [ ] T5.3 Construcción desde entorno limpio: `docker build --no-cache
      --target runtime` exitosa.
- [ ] T5.4 Dentro de la imagen: `import cv2, torch, ultralytics` con
      `torch.cuda.is_available() == False`.
- [ ] T5.5 `best.pt` montado read-only: verificación SHA256 y prueba de que el
      sistema de archivos es de solo lectura dentro del contenedor.
- [ ] T5.6 Inferencia dentro del contenedor: REST `POST /predict` y gRPC
      `Detect` conforme al contrato (prueba `docker` en verde + log de salida).
- [ ] T5.7 Compose: `api` + `grpc` + `frontend` arriba; SPA servida en 8080 y
      respuesta de `/predict` desde el flujo documentado.

## 6. Documentación y cierre

- [ ] T6.1 `docs/operacion/docker.md` (runbook completo de HU-011).
- [ ] T6.2 `README.md`: Docker en «Iniciar servicios», fila de estado y árbol.
- [ ] T6.3 `CONSTITUTION.md` §5/§8/§11 actualizados en el mismo commit.
- [ ] T6.4 `docs/curso/backlog.md`, `docs/curso/M3/README.md`,
      `docs/curso/PRUEBAS.md`, `specs/README.md` y `AGENTS.md` sincronizados.
- [ ] T6.5 PR a `develop` (plantilla UAO, `Closes #11`, spec enlazada) y
      evidencia adjunta a la issue; DoD pendiente de revisión/aprobación.
