# Feature Specification: HU-007 — Interfaz gráfica del detector

**Feature Branch**: `feature/005-hu-007-interfaz`

**Created**: 2026-11-09

**Status**: Draft

**Input**: Issue #7 — "Utilizar el detector desde una interfaz gráfica", con la decisión
del equipo de sustituir Streamlit/Tkinter por una SPA **React + Vite + TypeScript**
(ADR 0006).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Analizar una imagen sin escribir comandos (Priority: P1)

Como usuario sin conocimientos de programación, quiero abrir una interfaz, seleccionar
una imagen y ver el resultado del detector, para interpretar el análisis sin tocar la
terminal.

**Why this priority**: es la cara visible del sistema y la evidencia de la sustentación.

**Independent Test**: con `npm run test` la aplicación se monta con un cliente simulado,
procesa una imagen y muestra las detecciones (o el mensaje de "sin EPP") sin backend,
sin GPU, sin dataset y sin red.

**Acceptance Scenarios**:

1. **Given** una interfaz en funcionamiento, **When** el usuario selecciona una imagen
   compatible y solicita el análisis, **Then** se ejecuta la inferencia y se presenta la
   imagen junto con el resultado.
2. **Given** un resultado con detecciones, **When** se muestra, **Then** el usuario
   identifica la categoría y la ubicación de cada objeto.
3. **Given** una inferencia sin detecciones, **When** se muestra, **Then** se informa
   que no se detectaron EPP y no se presenta un error.
4. **Given** un archivo inválido, **When** el usuario intenta analizarlo, **Then** ve un
   mensaje comprensible y la interfaz sigue disponible.

### Edge Cases

- Archivo de más de 10 MB o con extensión no admitida.
- Imagen sin detecciones.
- Error de red o API caída.
- Imagen muy grande o muy pequeña (el lienzo se ajusta al contenedor).
- Navegador sin `createImageBitmap` (se usa `FileReader`/`Image` como respaldo).
- Cliente simulado cuando `VITE_API_URL` no está definida.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: La interfaz MUST ser una SPA **React + Vite + TypeScript** en `frontend/`,
  tipada en modo estricto.
- **FR-002**: MUST aceptar imágenes JPEG y PNG por selector de archivo.
- **FR-003**: MUST enviar la imagen a un `DetectorClient`; si `VITE_API_URL` está
  definida usa HTTP, si no un cliente simulado determinista.
- **FR-004**: MUST mostrar la imagen con una caja por detección, escalada al tamaño de
  presentación.
- **FR-005**: MUST listar cada detección con su categoría legible y su confianza.
- **FR-006**: Sin detecciones MUST mostrar "No se detectaron EPP" y MUST NOT tratarlo
  como error.
- **FR-007**: Un archivo inválido MUST producir un mensaje comprensible y la interfaz
  MUST seguir operativa.
- **FR-008**: La interfaz MUST reportar EPP detectado, nunca cumplimiento normativo.
- **FR-009**: MUST compilar con `npm run build` y pasar `npm run test` y `npm run lint`.
- **FR-010**: El pie MUST enlazar el código fuente (AGPL) y atribuir el dataset
  CC-BY-4.0. *(AC propuesto en el backlog, pendiente de validación de Jesús; se
  implementa por ser requisito de licencia).*

### Key Entities

- **DetectorClient**: contrato `detect(file) → PredictResponse`.
- **Detection**: `class_id`, `class_name`, `confidence`, `bbox` `xyxy`,
  `image_width`, `image_height` (espejo del contrato TA-11).
- **PredictResponse**: detecciones, dimensiones y versión del modelo.

## Acceptance → Test

| AC | Prueba |
|----|--------|
| AC-007.1 Flujo completo | `src/App.test.tsx::muestra las detecciones de una imagen válida` |
| AC-007.2 Categoría y ubicación | `src/components/DetectionTable.test.tsx` + `src/components/AnnotatedCanvas.test.tsx` |
| AC-007.3 Sin detecciones | `src/App.test.tsx::informa cuando no hay detecciones sin tratarlo como error` |
| AC-007.4 Archivo inválido | `src/App.test.tsx::rechaza un archivo inválido y sigue disponible` |
| FR-003 Cliente | `src/api/client.test.ts` |
| FR-010 Atribución | `src/App.test.tsx::muestra el enlace al código fuente y la atribución` |

## Success Criteria *(mandatory)*

- **SC-001**: `npm run lint`, `npm run test` y `npm run build` en verde.
- **SC-002**: 100 % de las pruebas sin backend, GPU, dataset ni red.
- **SC-003**: Cada AC de la issue #7 tiene al menos una prueba.
- **SC-004**: El bundle de producción se sirve como estático y no se versiona.

## Assumptions

- El contrato HTTP definitivo es el de HU-006 (`POST /predict`, multipart `file`); el
  cliente HTTP se escribe contra esa forma provisional y se ajusta cuando #6 cierre.
- Mientras la API no exista, `VITE_API_URL` vacío activa el cliente simulado.
- El navegador dibuja las cajas con `<canvas>`; no se descarga una imagen anotada del
  servidor.
- Node.js LTS (24) y npm son parte del entorno de desarrollo frontend.
