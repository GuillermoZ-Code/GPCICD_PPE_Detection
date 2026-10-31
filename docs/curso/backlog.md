# Backlog — espejo de las issues

> **Fuente oficial:** GitHub Issues del repositorio. Este archivo es un espejo para el
> documento del curso y debe coincidir **1:1** con las issues, el tablero y `specs/`.
> Los AC se resumen aquí; la redacción literal vive en cada issue.
> Si hay una diferencia, **avisa al equipo antes de continuar**.
>
> **No cambiar títulos, AC ni SP sin aprobación de Jesús** (dueño del backlog).

## Resumen

| Sprint | Fechas | HUs | SP |
|--------|--------|-----|----|
| M3-S1 | 31/10–07/11/2026 | HU-001 a HU-007 | 28 |
| M3-S2 | 08/11–14/11/2026 | HU-008 a HU-013 | 26 |
| M4-S3 | 15/11–28/11/2026 | HU-014 y HU-015 | 13 |
| **Total** | | **15 HU** | **67** |

## M3-S1 — 31/10 a 07/11 (28 SP)

### HU-001 — Cargar una imagen para su análisis

- **Como** usuario del sistema de detección de EPP, **quiero** proporcionar una imagen
  digital, **para** que pueda ser analizada por el modelo.
- **SP:** 3 · **Labels:** `ep-01` `must-have` `Backend` `Testing` · **Milestone:** M3-S1.
- **Depende de:** TA-04 *(pendiente de creación/validación — Jesús)*.
- **AC:**
  - Imagen válida decodificada y entregada al preprocesamiento.
  - Dimensiones originales conservadas como metadatos.
  - La entrada no ejecuta inferencia y cumple el contrato de datos.
- **Spec:** pendiente de crear con Spec Kit.

### HU-002 — Detectar las seis categorías de EPP en una imagen

- **Como** usuario del sistema, **quiero** que el modelo identifique y localice EPP en
  una imagen, **para** conocer qué categorías fueron detectadas y dónde.
- **SP:** 8 · **Labels:** `ep-02` `must-have` `ML` · **Milestone:** M3-S1.
- **Depende de:** SPI-01, SPI-02, TA-02, TA-09 *(pendientes de validación — Jesús)*.
- **AC:**
  - Inferencia con modelo cargado; sin entrenamiento.
  - Catálogo de 6 clases: Helmet, Vest, Gloves, Goggles, Mask, Safety Shoe.
  - Cada detección incluye clase, coordenadas y confianza en [0,1].
  - Evaluación reproducible; no se asume que todas las predicciones sean correctas.
- **Spec:** pendiente de crear con Spec Kit.

### HU-003 — Visualizar las detecciones sobre la imagen

- **Como** usuario, **quiero** visualizar la ubicación y categoría de los EPP
  detectados, **para** interpretar los resultados.
- **SP:** 3 · **Labels:** `ep-02` `must-have` `Frontend` `ML` · **Milestone:** M3-S1.
- **Depende de:** #2.
- **AC:**
  - Cada detección se dibuja con caja, categoría y confianza.
  - Transformación espacial correcta según dimensiones originales.
  - Sin detecciones: no se dibujan cajas inexistentes.
- **Spec:** pendiente de crear con Spec Kit.

### HU-004 — Informar cuando no se detectan elementos de protección personal

- **Como** usuario, **quiero** recibir una indicación clara cuando el modelo no
  encuentre objetos, **para** distinguir una inferencia sin detecciones de un fallo.
- **SP:** 2 · **Labels:** `ep-01` `must-have` `Backend` `Frontend` · **Milestone:** M3-S1.
- **Depende de:** #2.
- **AC:**
  - Colección vacía y mensaje “no se detectaron EPP”.
  - No se clasifica como error de procesamiento.
  - No se afirma incumplimiento ni ausencia real de EPP.
- **Spec:** pendiente de crear con Spec Kit.

### HU-005 — Validar las imágenes recibidas

- **Como** usuario, **quiero** recibir una notificación comprensible cuando una imagen
  no pueda procesarse, **para** corregir la entrada sin fallos.
- **SP:** 2 · **Labels:** `ep-01` `must-have` `Backend` `Testing` · **Milestone:** M3-S1.
- **Depende de:** #1.
- **AC:**
  - Archivo corrupto rechazado sin ejecutar el detector.
  - Archivo vacío rechazado; el sistema sigue operativo.
  - Archivo compatible aceptado y enviado al preprocesamiento.
- **Spec:** pendiente de crear con Spec Kit.

### HU-006 — Consultar inferencias mediante una API REST con FastAPI

- **Como** desarrollador que necesita integrar el detector, **quiero** enviar imágenes
  a una API HTTP y recibir resultados estructurados, **para** usar el modelo sin
  depender de la interfaz gráfica.
- **SP:** 5 · **Labels:** `ep-03` `must-have` `Backend` · **Milestone:** M3-S1.
- **Depende de:** #2, #5.
- **AC:**
  - Inferencia HTTP exitosa conforme al esquema publicado.
  - Archivo inválido devuelve error de cliente; el servidor sigue disponible.
  - OpenAPI documenta operación, entrada y resultados.
  - Usa el artefacto cargado; no entrena.
- **Spec:** pendiente de crear con Spec Kit.

### HU-007 — Utilizar el detector desde una interfaz gráfica

- **Como** usuario sin conocimientos de programación, **quiero** acceder al detector
  mediante una interfaz gráfica, **para** analizar una imagen y consultar resultados.
- **SP:** 5 · **Labels:** `ep-03` `must-have` `Frontend` · **Milestone:** M3-S1.
- **Depende de:** #1, #3, #4, #5, #6.
- **AC:**
  - Flujo completo: seleccionar imagen, inferir, mostrar resultado.
  - Categoría y ubicación visibles para cada detección.
  - Sin detecciones: mensaje claro, sin error ficticio.
  - Archivo inválido: mensaje comprensible y la interfaz sigue disponible.
- **Spec:** pendiente de crear con Spec Kit.

## M3-S2 — 08/11 a 14/11 (26 SP)

### HU-008 — Evaluar el desempeño del modelo de detección

- **Como** evaluador del modelo, **quiero** medir su desempeño con métricas apropiadas,
  **para** conocer su capacidad y documentar limitaciones.
- **SP:** 5 · **Labels:** `ep-04` `must-have` `ML` `Testing` · **Milestone:** M3-S2.
- **Depende de:** #2, TA-02 *(pendiente de validación — Jesús)*.
- **AC:**
  - Informe reproducible con versión del modelo, partición y configuración.
  - Métricas globales y por clase (precision, recall, mAP).
  - Análisis de falsos positivos/negativos y limitaciones.
  - Partición de evaluación protegida y documentada.
- **Spec:** pendiente de crear con Spec Kit.

### HU-009 — Consultar y comparar experimentos en MLflow

- **Como** integrante del equipo ML, **quiero** consultar parámetros y resultados de
  las ejecuciones, **para** comparar experimentos y conservar trazabilidad.
- **SP:** 3 · **Labels:** `ep-04` `must-have` `ML` · **Milestone:** M3-S2.
- **Depende de:** #8.
- **AC:**
  - Run identificable con parámetros, métricas y referencia al modelo.
  - Dos runs distinguibles.
  - Referencia al artefacto sin almacenar pesos en Git.
- **Spec:** pendiente de crear con Spec Kit.

### HU-010 — Consumir inferencias mediante gRPC

- **Como** desarrollador integrador, **quiero** consumir la inferencia mediante gRPC,
  **para** disponer de un segundo mecanismo de integración.
- **SP:** 5 · **Labels:** `ep-03` `must-have` `Backend` · **Milestone:** M3-S2.
- **Depende de:** #6.
- **AC:**
  - Solicitud gRPC válida devuelve respuesta estructurada con las 6 clases.
  - REST y gRPC comparten semántica y no duplican el detector.
  - Solicitud inválida devuelve error definido y el servidor sigue disponible.
- **Spec:** pendiente de crear con Spec Kit.

### HU-011 — Ejecutar el sistema en un contenedor Docker CPU

- **Como** responsable de integración técnica, **quiero** ejecutar el sistema con sus
  dependencias y un modelo versionado en Docker, **para** reproducir la aplicación sin
  reconstruir el entorno.
- **SP:** 5 · **Labels:** `ep-04` `must-have` `Backend` `Testing` · **Milestone:** M3-S2.
- **Depende de:** #6, #7, #10.
- **AC:**
  - Build reproducible desde un entorno limpio.
  - Inferencia en CPU sin GPU dedicada.
  - Artefacto del modelo externo a Git.
  - Documentación de build, configuración y ejecución.
- **Spec:** pendiente de crear con Spec Kit.

### HU-012 — Ejecutar verificaciones automatizadas de calidad

- **Como** integrante del equipo, **quiero** ejecutar una suite automatizada de
  verificaciones, **para** detectar regresiones y validar contratos antes de integrar.
- **SP:** 5 · **Labels:** `ep-04` `must-have` `Testing` · **Milestone:** M3-S2.
- **Depende de:** contratos de #6, #7 y #10.
- **AC:**
  - pytest finaliza satisfactoriamente e informa el resultado.
  - Una regresión deliberada hace fallar la suite.
  - Ruff reporta incumplimientos configurados.
  - Pruebas unitarias sin GPU ni dataset completo.
- **Spec:** pendiente de crear con Spec Kit.

### HU-013 — Consultar la versión del modelo utilizado

- **Como** evaluador técnico, **quiero** identificar la versión del modelo que generó
  una inferencia, **para** relacionar resultados con configuración y desempeño.
- **SP:** 3 · **Labels:** `ep-04` `should-have` `ML` `Backend` · **Milestone:** M3-S2.
- **Depende de:** #2, #9.
- **AC:**
  - Referencia verificable de la versión usada en la inferencia.
  - Dos versiones distintas se pueden distinguir.
  - Artefacto identificable fuera de Git.
- **Spec:** pendiente de crear con Spec Kit.

## M4-S3 — 15/11 a 28/11 (13 SP)

### HU-014 — Publicar versiones mediante un pipeline CI/CD con compuertas de calidad

- **Como** responsable del despliegue, **quiero** publicar versiones solo después de
  verificaciones automáticas, **para** reducir el riesgo de cambios defectuosos.
- **SP:** 8 · **Labels:** `ep-05` `must-have` `Backend` `Testing` · **Milestone:** M4-S3.
- **Depende de:** #11, #12, TA-10 *(pendiente de validación — Jesús)*.
- **AC:**
  - Build, deploy y smoke exitosos con cambios autorizados.
  - Una compuerta fallida bloquea la publicación.
  - Credenciales obtenidas de forma segura, sin exponerse.
  - Versión desplegada asociada al modelo; pesos fuera de Git.
- **Spec:** pendiente de crear con Spec Kit.

### HU-015 — Comprobar el funcionamiento del sistema desplegado

- **Como** responsable técnico de la aplicación desplegada, **quiero** consultar su
  estado y eventos técnicos, **para** comprobar si el servicio funciona y diagnosticar
  errores.
- **SP:** 5 · **Labels:** `ep-05` `must-have` `Backend` `Testing` · **Milestone:** M4-S3.
- **Depende de:** #14.
- **AC:**
  - Healthcheck responde con el estado del componente y el contrato publicado.
  - Una imagen válida produce una inferencia real con el artefacto configurado.
  - Errores controlados se registran sin credenciales ni secretos.
  - Evidencia de estado, inferencia y operación para la demostración.
- **Spec:** pendiente de crear con Spec Kit.

## Pendiente de validación (Jesús)

> Esta sección **no modifica** los títulos, AC ni SP de las issues. Es una propuesta
> para que el dueño del backlog decida.

### TA/SPI propuestas (no creadas todavía)

| ID | Título | SP | Sprint | Motivo |
|----|--------|----|--------|--------|
| TA-04 | Contrato de entrada y decodificación de imágenes | 3 | M3-S1 | Habilita HU-001/HU-005 |
| TA-11 | Contract-first: contrato `Image → list[Detection]` y detector simulado | 3 | M3-S1 | Desbloquea HU-006/007/010 |
| SPI-01 | Spike: selección y compatibilidad del detector YOLO | 3 | M3-S1 | Habilita HU-002 |
| TA-02 | Contrato numérico de pre/postprocesamiento | 5 | M3-S1 | Habilita HU-002/HU-008 |
| TA-09 | Descarga, verificación y versionado del artefacto | 3 | M3-S1 | Habilita HU-002/HU-013 |
| SPI-02 | Spike: baseline de fine-tuning y evaluación | 3 | M3-S1 | Habilita HU-002/HU-008 |
| TA-10 | Dependencias C++ y Docker CPU | 5 | M3-S2 | Habilita HU-011/HU-014 |

**Total propuesto:** 25 SP.

### Incoherencia de SP

- **HU-002 = 8 SP**, pero sus dependencias **SPI-01 (3) + SPI-02 (3) + TA-02 (5) +
  TA-09 (3) = 14 SP**.
- Opciones:
  - **(a)** Re-estimar las HU padre para absorber el trabajo de TA/SPI.
  - **(b)** Dejar las TA/SPI **sin SP propio** y anotarlas como “incluido en HU-xxx”.
- **No se cambia ningún SP de HU sin aprobación de Jesús.**

### Tablero

- El tablero Kanban es entregable de Jesús. No se crea desde el repo.
- Si ya existe un GitHub Project del grupo, solo falta enlazar las 15 issues y las
  TA/SPI aprobadas.
