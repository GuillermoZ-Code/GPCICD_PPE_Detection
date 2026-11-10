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
| M3-S1 | 31/10–07/11/2026 | HU-001 a HU-007 | 11 |
| M3-S2 | 08/11–14/11/2026 | HU-008 a HU-013 | 8 |
| M4-S3 | 15/11–28/11/2026 | HU-014 y HU-015 | 3 |
| **Total** | | **15 HU** | **22** |

> **Reestimación del M3 (04/11/2026).** Los SP de las 15 HU pasaron de 67 a 22 para
> alinearse con la planificación del documento del M2 (`Doc_Mod2_EPP.pdf`, §3.3),
> aprobada por Jesús. El tablero de GitHub Projects ya refleja el total de 22.
>
> La **preparación del M3** (P1–P4) suma 12 SP adicionales y no está registrada como
> issues, igual que en el documento: el plan completo son **34 SP**, de los cuales el
> tablero solo puede medir 22.

## Responsables

Asignación vigente en GitHub, tomada del documento del M2. Único cambio respecto al
PDF: **HU-002 pasa de Jesús a Hernán** (transferencia temporal desde el 04/11/2026),
porque Jesús no estaba disponible esa semana y HU-002 tiene holgura cero en la ruta
crítica.

| Persona | GitHub | HU | SP HU | Preparación | SP prep |
|---------|--------|----|------:|-------------|--------:|
| Hernán Estrada | `HestradaUAO` | HU-001, HU-002, HU-005, HU-006, HU-012 | 8 | P4 entorno y contratos | 3 |
| Eliana Cardona | `ElianaCardona` | HU-004, HU-010, HU-011, HU-014 | 6 | P3 artefacto y versión | 3 |
| Guillermo Zabala | `GuillermoZ-Code` | HU-003, HU-007, HU-015 | 4 | P1 alcance y licencias | 3 |
| Jesús Riveros | `jesusriverosUAO` | HU-008, HU-009, HU-013 | 4 | P2 datos y particiones | 3 |
| **Total** | | **15 HU** | **22** | **4 actividades** | **12** |

Las actividades de preparación no son issues; su alcance y evidencia viven en
[`M3/README.md`](M3/README.md). La ruta crítica del plan es
`P → HU-002 → HU-006 → HU-007 → HU-011 → HU-014 → HU-015`.

## M3-S1 — 31/10 a 07/11 (11 SP)

### HU-001 — Cargar una imagen para su análisis

- **Como** usuario del sistema de detección de EPP, **quiero** proporcionar una imagen
  digital, **para** que pueda ser analizada por el modelo.
- **SP:** 1 · **Labels:** `ep-01` `must-have` `Backend` `Testing` · **Milestone:** M3-S1.
- **Depende de:** TA-04 *(absorbida en P4; el contrato se implementó con HU-001)*.
- **AC:**
  - Imagen válida decodificada y entregada al preprocesamiento.
  - Dimensiones originales conservadas como metadatos.
  - La entrada no ejecuta inferencia y cumple el contrato de datos.
- **Spec:** [`specs/002-hu-001-carga-imagen`](../../specs/002-hu-001-carga-imagen/spec.md) · PR #28.

### HU-002 — Detectar las seis categorías de EPP en una imagen

- **Como** usuario del sistema, **quiero** que el modelo identifique y localice EPP en
  una imagen, **para** conocer qué categorías fueron detectadas y dónde.
- **SP:** 3 · **Labels:** `ep-02` `must-have` `ML` · **Milestone:** M3-S1.
- **Depende de:** SPI-01, SPI-02, TA-02, TA-09 *(absorbidas en P1–P4; SPI-01/SPI-02 cerrados)*.
- **AC:**
  - Inferencia con modelo cargado; sin entrenamiento.
  - Catálogo de 6 clases: Helmet, Vest, Gloves, Goggles, Mask, Safety Shoe.
  - Cada detección incluye clase, coordenadas y confianza en [0,1].
  - Evaluación reproducible; no se asume que todas las predicciones sean correctas.
- **Spec:** [`specs/003-hu-002-deteccion`](../../specs/003-hu-002-deteccion/spec.md) · PR #30.

### HU-003 — Visualizar las detecciones sobre la imagen

- **Como** usuario, **quiero** visualizar la ubicación y categoría de los EPP
  detectados, **para** interpretar los resultados.
- **SP:** 1 · **Labels:** `ep-02` `must-have` `Frontend` `ML` · **Milestone:** M3-S1.
- **Depende de:** #2.
- **AC:**
  - Cada detección se dibuja con caja, categoría y confianza.
  - Transformación espacial correcta según dimensiones originales.
  - Sin detecciones: no se dibujan cajas inexistentes.
- **Spec:** [`specs/004-hu-003-visualizacion`](../../specs/004-hu-003-visualizacion/spec.md) · PR #33.

### HU-004 — Informar cuando no se detectan elementos de protección personal

- **Como** usuario, **quiero** recibir una indicación clara cuando el modelo no
  encuentre objetos, **para** distinguir una inferencia sin detecciones de un fallo.
- **SP:** 1 · **Labels:** `ep-01` `must-have` `Backend` `Frontend` · **Milestone:** M3-S1.
- **Depende de:** #2.
- **AC:**
  - Colección vacía y mensaje "no se detectaron EPP".
  - No se clasifica como error de procesamiento.
  - No se afirma incumplimiento ni ausencia real de EPP.
- **Spec:** [`specs/006-hu-004-informe-sin-detecciones`](../../specs/006-hu-004-informe-sin-detecciones/spec.md) · PR #34.

### HU-005 — Validar las imágenes recibidas

- **Como** usuario, **quiero** recibir una notificación comprensible cuando una imagen
  no pueda procesarse, **para** corregir la entrada sin fallos.
- **SP:** 1 · **Labels:** `ep-01` `must-have` `Backend` `Testing` · **Milestone:** M3-S1.
- **Depende de:** #1.
- **AC:**
  - Archivo corrupto rechazado sin ejecutar el detector.
  - Archivo vacío rechazado; el sistema sigue operativo.
  - Archivo compatible aceptado y enviado al preprocesamiento.
- **Spec:** [`specs/007-hu-005-validacion-imagenes`](../../specs/007-hu-005-validacion-imagenes/spec.md) · rama `feature/007-hu-005-validacion-imagenes`.

### HU-006 — Consultar inferencias mediante una API REST con FastAPI

- **Como** desarrollador que necesita integrar el detector, **quiero** enviar imágenes
  a una API HTTP y recibir resultados estructurados, **para** usar el modelo sin
  depender de la interfaz gráfica.
- **SP:** 2 · **Labels:** `ep-03` `must-have` `Backend` · **Milestone:** M3-S1.
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
- **SP:** 2 · **Labels:** `ep-03` `must-have` `Frontend` · **Milestone:** M3-S1.
- **Depende de:** #1, #3, #4, #5, #6.
- **AC:**
  - Flujo completo: seleccionar imagen, inferir, mostrar resultado.
  - Categoría y ubicación visibles para cada detección.
  - Sin detecciones: mensaje claro, sin error ficticio.
  - Archivo inválido: mensaje comprensible y la interfaz sigue disponible.
- **Spec:** [`specs/005-hu-007-interfaz`](../../specs/005-hu-007-interfaz/spec.md) · PR #35.

## M3-S2 — 08/11 a 14/11 (8 SP)

### HU-008 — Evaluar el desempeño del modelo de detección

- **Como** evaluador del modelo, **quiero** medir su desempeño con métricas apropiadas,
  **para** conocer su capacidad y documentar limitaciones.
- **SP:** 2 · **Labels:** `ep-04` `must-have` `ML` `Testing` · **Milestone:** M3-S2.
- **Depende de:** #2 (cerrada), TA-02 *(absorbida en P4)*.
- **AC:**
  - Informe reproducible con versión del modelo, partición y configuración.
  - Métricas globales y por clase (precision, recall, mAP).
  - Análisis de falsos positivos/negativos y limitaciones.
  - Partición de evaluación protegida y documentada.
- **Spec:** pendiente de crear con Spec Kit.

### HU-009 — Consultar y comparar experimentos en MLflow

- **Como** integrante del equipo ML, **quiero** consultar parámetros y resultados de
  las ejecuciones, **para** comparar experimentos y conservar trazabilidad.
- **SP:** 1 · **Labels:** `ep-04` `must-have` `ML` · **Milestone:** M3-S2.
- **Depende de:** #8.
- **AC:**
  - Run identificable con parámetros, métricas y referencia al modelo.
  - Dos runs distinguibles.
  - Referencia al artefacto sin almacenar pesos en Git.
- **Spec:** pendiente de crear con Spec Kit.

### HU-010 — Consumir inferencias mediante gRPC

- **Como** desarrollador integrador, **quiero** consumir la inferencia mediante gRPC,
  **para** disponer de un segundo mecanismo de integración.
- **SP:** 1 · **Labels:** `ep-03` `must-have` `Backend` · **Milestone:** M3-S2.
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
- **SP:** 2 · **Labels:** `ep-04` `must-have` `Backend` `Testing` · **Milestone:** M3-S2.
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
- **SP:** 1 · **Labels:** `ep-04` `must-have` `Testing` · **Milestone:** M3-S2.
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
- **SP:** 1 · **Labels:** `ep-04` `should-have` `ML` `Backend` · **Milestone:** M3-S2.
- **Depende de:** #2, #9.
- **AC:**
  - Referencia verificable de la versión usada en la inferencia.
  - Dos versiones distintas se pueden distinguir.
  - Artefacto identificable fuera de Git.
- **Spec:** pendiente de crear con Spec Kit.

## M4-S3 — 15/11 a 28/11 (3 SP)

### HU-014 — Publicar versiones mediante un pipeline CI/CD con compuertas de calidad

- **Como** responsable del despliegue, **quiero** publicar versiones solo después de
  verificaciones automáticas, **para** reducir el riesgo de cambios defectuosos.
- **SP:** 2 · **Labels:** `ep-05` `must-have` `Backend` `Testing` · **Milestone:** M4-S3.
- **Depende de:** #11, #12, TA-10 *(absorbida en P4)*.
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
- **SP:** 1 · **Labels:** `ep-05` `must-have` `Backend` `Testing` · **Milestone:** M4-S3.
- **Depende de:** #14.
- **AC:**
  - Healthcheck responde con el estado del componente y el contrato publicado.
  - Una imagen válida produce una inferencia real con el artefacto configurado.
  - Errores controlados se registran sin credenciales ni secretos.
  - Evidencia de estado, inferencia y operación para la demostración.
- **Spec:** pendiente de crear con Spec Kit.

## Decisiones de planificación

> Esta sección **no modifica** los títulos, AC ni SP de las issues. Recoge las
> decisiones de planificación y los pendientes reales del dueño del backlog.

### TA/SPI absorbidas en P1–P4 (referencia histórica)

| ID | Título | SP | Sprint | Motivo |
|----|--------|----|--------|--------|
| TA-04 | Contrato de entrada y decodificación de imágenes | 3 | M3-S1 | Habilita HU-001/HU-005 |
| TA-11 | Contract-first: contrato `Image → list[Detection]` y detector simulado | 3 | M3-S1 | Desbloquea HU-006/007/010 |
| SPI-01 | Spike: selección y compatibilidad del detector YOLO | 3 | M3-S1 | Habilita HU-002 |
| TA-02 | Contrato numérico de pre/postprocesamiento | 5 | M3-S1 | Habilita HU-002/HU-008 |
| TA-09 | Descarga, verificación y versionado del artefacto | 3 | M3-S1 | Habilita HU-002/HU-013 |
| SPI-02 | Spike: baseline de fine-tuning y evaluación | 3 | M3-S1 | Habilita HU-002/HU-008 |
| TA-10 | Dependencias C++ y Docker CPU | 5 | M3-S2 | Habilita HU-011/HU-014 |
| TA-EDA | EDA del dataset | 3 | M3-S1 | Habilita HU-002/HU-008 |

**Total de referencia:** 28 SP con TA-EDA (25 SP sin TA-EDA). No se suman al total
oficial: la reestimación las absorbió en P1–P4.

> **Actualización del 04/11/2026:** la reestimación absorbió este trabajo en las
> actividades de preparación P1–P4 (12 SP), que no son issues. Estas TA/SPI no se
> crean como tickets salvo que Jesús decida lo contrario.

### TA-EDA — EDA del dataset (absorbida en P4; completada)

- **Objetivo:** entender el dataset antes de entrenar y dejar la descarga reproducible.
- **AC propuestos:**
  - Conteo de imágenes por split (`train/valid/test`).
  - Objetos por clase y desbalance entre las seis clases.
  - Imágenes sin etiquetas y cajas inválidas/fuera de rango.
  - Descarga reproducible del `PPE.zip` con **SHA256** y ruta configurable.
  - Reporte en `docs/spikes/` o `docs/dataset/`; sin `.ipynb` versionado.
- **SP:** 3 (propuesto).
- **Estado:** completada por Hernán; ver [`docs/dataset/EDA.md`](../../dataset/EDA.md).

### AC propuestos para HU-007 y HU-015 (AGPL, sin modificar issues)

- **HU-007 (interfaz):** la vista debe incluir un enlace visible a “Código fuente”
  (repo o URL de descarga) y la atribución CC-BY-4.0 del dataset.
- **HU-015 (sistema desplegado):** el healthcheck o la página de operación debe
  exponer el enlace al código fuente de la versión desplegada y la atribución del
  dataset.
- **Validación:** Jesús; no se modifican las issues hasta su aprobación.

### Incoherencia de SP — resuelta

La reestimación del 04/11/2026 fijó **HU-002 en 3 SP** y absorbió el trabajo de las
TA/SPI en las actividades de preparación P1–P4 (12 SP), que no son issues. Con eso
desaparece la diferencia entre HU-002 (antes 8 SP) y sus dependencias (antes 14 SP).

### Tablero

- El tablero es <https://github.com/users/GuillermoZ-Code/projects/1>; las 15 issues
  están enlazadas y el campo `Estimate` suma 22.
- Las TA/SPI no se crean como issues mientras no lo decida Jesús.
