# Feature Specification: HU-011 — Ejecutar el sistema en un contenedor Docker CPU

**Feature Branch**: `feature/012-hu-011-docker-cpu`

**Created**: 2026-11-11

**Status**: En curso (rama)

**Input**: Issue #11 — «HU-011 — Ejecutar el sistema en un contenedor Docker CPU».
Asignada a ElianaCardona (EP-04, Must Have, M3-S2, 2 SP). Depende de HU-006
(fusionada, PR #42), HU-007 (fusionada, PR #35) y HU-010 (fusionada, PR #46):
el paquete local completo es REST + gRPC + SPA React. El requisito de origen es
el entregable de «aplicación completa en local» del Módulo 3.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Construcción reproducible (Priority: P1)

Como responsable de integración técnica, quiero construir la imagen Docker con
`uv` y `uv.lock`, para reproducir el entorno del proyecto sin pasos manuales.

**Why this priority**: sin una imagen reproducible no hay contenedor que validar.

**Independent Test**: el Dockerfile copia `pyproject.toml` y `uv.lock` y ejecuta
`uv sync --frozen` (sin `pip` ni `requirements.txt`), instala las bibliotecas del
sistema que OpenCV/torch necesitan en Debian slim y la imagen se construye desde
un entorno limpio.

**Acceptance Scenarios** (AC-011.1 de la issue #11):

1. **AC-011.1**: **Dado** el repositorio con archivos de dependencias y código
   válidos, **Cuando** se construye la imagen Docker desde un entorno limpio,
   **Entonces** el proceso concluye correctamente utilizando las dependencias
   declaradas en `uv.lock`.

### User Story 2 — Inferencia en CPU dentro del contenedor (Priority: P1)

Como evaluador técnico, quiero ejecutar el contenedor sin GPU y lanzarle una
solicitud de inferencia, para comprobar que el servicio responde conforme al
contrato con el servicio corriendo dentro del contenedor.

**Why this priority**: es el valor funcional de la HU; los AC anteriores solo
preparan el entorno.

**Independent Test**: con la imagen construida y el contenedor iniciado
(`PPE_SERVICES=rest,grpc`), una imagen de prueba produce una respuesta REST
(`POST /predict`) y una respuesta gRPC (`ppe.v1/Detect`) con los campos del
contrato (`detections`, dimensiones, `model_version`, `elapsed_ms`), CPU only.

**Acceptance Scenarios** (AC-011.2 de la issue #11):

1. **AC-011.2**: **Dado** el contenedor configurado con un artefacto de modelo
   compatible, **Cuando** se inicia sin una GPU dedicada, **Entonces** se puede
   ejecutar una solicitud de inferencia de prueba, **Y** se obtiene una respuesta
   conforme al contrato de HU-006 (REST) y HU-010 (gRPC).

### User Story 3 — Separación de artefactos (Priority: P2)

Como responsable del repositorio, quiero que el modelo entre al contenedor por
un montaje externo a Git, para que pesos, datasets y credenciales queden fuera
del repositorio y de la imagen.

**Why this priority**: el modelo real se entrenó fuera del repo; la imagen no
debe contenerlo y debe funcionar sin Colab ni reentrenamiento.

**Independent Test**: `.dockerignore` y `.gitignore` bloquean `*.pt`, `artifacts/`,
`weights/`, `datasets/` y `.env`; el Dockerfile no copia pesos; `compose.yml` monta
el directorio de modelos `read-only`; el contenedor no puede escribir en el
montaje y arranca con `PPE_MODEL_PATH=/models/best.pt`.

**Acceptance Scenarios** (AC-011.3 de la issue #11):

1. **AC-011.3**: **Dado** un modelo entrenado previamente en Google Colab,
   **Cuando** se prepara el entorno local, **Entonces** el artefacto se
   incorpora mediante un mecanismo externo a Git (montaje read-only), **Y** la
   aplicación no requiere acceder a Colab ni reentrenar.

### User Story 4 — Documentación de puesta en marcha (Priority: P2)

Como integrante del equipo, quiero instrucciones verificables de construcción,
configuración y arranque, para repetir la demo del M3 sin reconstruir el entorno
a mano.

**Why this priority**: la issue pide un entregable verificable; sin documentación
el contenedor no es reproducible para el resto del equipo.

**Independent Test**: `docs/operacion/docker.md` explica cómo construir, cómo
configurar el artefacto y las variables, cómo iniciar el contenedor y cómo
repetir la inferencia por REST, gRPC y la interfaz (SPA servida con nginx).

**Acceptance Scenarios** (AC-011.4 de la issue #11):

1. **AC-011.4**: **Dado** el repositorio, **Cuando** un integrante sigue las
   instrucciones de ejecución, **Entonces** puede identificar los pasos para
   construir, configurar e iniciar el contenedor, **Y** repetir la inferencia
   con REST, la interfaz y gRPC.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El `Dockerfile` MUST ser multi-stage con dos targets:
  `runtime` (backend Python) y `web` (SPA estática con nginx), construidos desde
  el contexto del repositorio.
- **FR-002**: El target `runtime` MUST copiar `pyproject.toml`, `uv.lock`,
  `README.md`, `LICENSE` y `src/`, y ejecutar `uv sync --frozen --no-dev
  --extra inference --extra grpc`; está prohibido `pip` y `requirements.txt`.
- **FR-003**: La imagen MUST instalar las bibliotecas del sistema necesarias por
  OpenCV headless y PyTorch CPU en Debian trixie (`libgl1`, `libglib2.0-0t64`,
  `libgomp1`, `libquadmath0`, `libxcb1`, `ca-certificates`) con
  `--no-install-recommends`.
- **FR-004**: La resolución de PyTorch en Linux MUST usar el índice CPU de
  PyTorch (`pytorch-cpu` en `tool.uv.sources` con el marcador
  `sys_platform == 'linux'`) para que la imagen no contenga CUDA; en Windows y
  macOS la resolución se mantiene en PyPI.
- **FR-005**: El paquete MUST declarar `grpcio` y `protobuf` como dependencias
  de runtime (extra `grpc`) porque el servidor gRPC de HU-010 forma parte del
  paquete desplegable y los stubs importan `google.protobuf`; `grpcio-tools`
  permanece como dependencia de desarrollo.
- **FR-006**: El contenedor MUST exponer REST (8000) y gRPC (9000) y seleccionar
  los servicios con `PPE_SERVICES` (`rest`, `grpc`, `both`; por omisión `rest,grpc`)
  a través de `docker/entrypoint.sh`.
- **FR-007**: El artefacto del modelo MUST proveerse por montaje read-only
  (`/models`) y `PPE_MODEL_PATH=/models/best.pt`; el Dockerfile MUST NOT copiar
  pesos, datasets ni credenciales, y `.dockerignore` MUST excluirlos
  (`*.pt`, `*.pth`, `*.onnx`, `artifacts/`, `weights/`, `datasets/`, `data/`,
  `.env`, `*.zip`, cachés y `node_modules`).
- **FR-008**: El target `web` MUST construir la SPA con Node 24 (`npm ci` +
  `npm run build`) y `VITE_API_URL` como build-arg (por omisión
  `http://localhost:8000`), y servirla con nginx configurado para SPA.
- **FR-009**: `compose.yml` MUST definir `api`, `grpc` y `frontend` con el mismo
  volumen read-only `${PPE_MODELS_DIR:-./artifacts}:/models:ro` y CORS de la API
  abierto a la SPA servida en el puerto 8080.
- **FR-010**: El `Makefile` MUST exponer `docker-build`, `docker-build-web`,
  `docker-up`, `docker-down` y `docker-smoke`.
- **FR-011**: Las pruebas MUST cubrir cada AC: estáticas para AC-011.1,
  AC-011.3 y AC-011.4 (corren en CI sin Docker) y una prueba marcada `docker`
  para AC-011.2 que arranca el contenedor y verifica REST + gRPC; la prueba de
  contenedor se omite sin Docker, sin imagen o sin artefacto local y se activa
  con `PPE_DOCKER_SMOKE=1` y `PPE_DOCKER_MODEL=<ruta de best.pt>`.
- **FR-012**: El runbook `docs/operacion/docker.md` MUST documentar construcción,
  verificación del artefacto (SHA256), configuración, arranque (single-container
  y compose), inferencia REST/gRPC/SPA, comprobación del montaje read-only y
  solución de problemas.

## Success Criteria *(mandatory)*

- **SC-001**: Cada AC tiene al menos una prueba pytest que lo referencia
  (`AC-011.x` en el nombre o docstring); las estáticas corren en `make check`
  y la prueba `docker` se salta en CI sin hardware adicional.
- **SC-002**: `make check` y `uv build` en verde con las pruebas nuevas;
  `uv run pre-commit run --all-files` en verde.
- **SC-003**: La imagen `runtime` se construye con `--no-cache` desde un entorno
  limpio y dentro de ella importan `cv2`, `torch` y `ultralytics` con
  `torch.cuda.is_available() == False`.
- **SC-004**: La inferencia de prueba dentro del contenedor responde conforme al
  contrato por REST y por gRPC con `best.pt` (SHA256 `96ba99a7…c828`) montado
  read-only, sin Colab y sin reentrenamiento.
- **SC-005**: La construcción, configuración, arranque e inferencia quedan
  documentados en `README.md`, `docs/operacion/docker.md` y esta spec.

## Edge Cases

- Sin `PPE_MODEL_PATH` (o montaje ausente): la API REST responde **503** y gRPC
  **UNAVAILABLE**; el contrato de HU-005/HU-006/HU-010 no cambia dentro del
  contenedor y el entrypoint advierte en el log.
- El montaje read-only impide escribir en `/models` (evidencia de AC-011.3).
- Puertos 8000/9000/8080 ocupados: los comandos documentan cómo cambiarlos con
  `PPE_API_PORT`, `PPE_GRPC_PORT` y `PPE_WEB_PORT` en compose.
- Primera petición lenta (~30–60 s): torch carga el artefacto en la primera
  solicitud; las siguientes son rápidas (patrón ya documentado en
  `docs/operacion/demo-local.md`).
- La SPA compilada hornea `VITE_API_URL`: si la API no está en
  `http://localhost:8000`, hay que reconstruir el target `web` con otro
  build-arg (documentado como limitación).

## Out of Scope

- Despliegue en Droplet, CI/CD de publicación y healthcheck `/health`
  (HU-014/HU-015, M4).
- MLflow dentro del contenedor (HU-009 corre en el entorno local del equipo).
- Entrenamiento, descarga de pesos por red, Colab o reentrenamiento.
- GPU/CUDA, multi-arquitectura (ARM) y orquestación productiva (Kubernetes).
- Autenticación, TLS y balanceo de carga.
- Cambios al contrato REST (HU-006), gRPC (HU-010) o SPA (HU-007).
