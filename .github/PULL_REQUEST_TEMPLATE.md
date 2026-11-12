<!--
╔══════════════════════════════════════════════════════════════════════════╗
║  📌 PLANTILLA DE PULL REQUEST — GPCICD PPE Detection · Grupo 4 · UAO     ║
╚══════════════════════════════════════════════════════════════════════════╝

1. Esta plantilla se carga automáticamente en cada Pull Request del repositorio.
2. Una PR = UN solo propósito (una funcionalidad, una corrección o un refactor
   pequeño). Si mezclas varias historias, la revisión se rechaza.
3. La PR va a `develop`; `develop → main` solo en la entrega del módulo.
4. La PR NO se fusiona sin al menos UNA revisión aprobada de otro integrante.
5. Proyecto: detección de Equipos de Protección Personal (EPP) con visión por
   computador, curso GPCICD M2-M4.
6. La automatización y gestión del repositorio desde el asistente se realiza
   con el MCP de GitHub y la cuenta UAO (`GuillermoZ-Code`).
-->

## 1. Identificación de la Pull Request

| Campo | Valor |
| :--- | :--- |
| **Equipo / Grupo** | Grupo 4 |
| **Integrantes que participaron** | *(nombres de quienes escribieron código en esta PR)* |
| **Proyecto** | GPCICD PPE Detection — Detección de EPP (M2-M4) |
| **Rama origen ➔ destino** | `feature/…` ➔ `develop` *(o `develop` ➔ `main` en release)* |
| **Issue / Ticket asociado** | `Closes #__` *(tablero de GitHub Projects)* |
| **Spec asociada** | `specs/__-hu-___/spec.md` *(si aplica)* |
| **Milestone** | `M3-S1` / `M3-S2` / `M4-S3` |
| **Módulo / Entrega** | *(M2 · M3 · M4 — semana correspondiente)* |
| **Cuenta UAO para el MCP** | `GuillermoZ-Code` |

---

## 2. Título de la Pull Request (Conventional Commits)

El título **debe** comenzar con un prefijo, escribirse en imperativo y tener **≤ 72 caracteres**.

| Prefijo | Cuándo usarlo | Ejemplo |
| :--- | :--- | :--- |
| `feat:` | Nueva funcionalidad o módulo del pipeline | `feat(detector): agregar inferencia sobre video` |
| `fix:` | Corrección de bug, warning o deprecación | `fix(preprocess): corregir normalización de bounding boxes` |
| `test:` | Pruebas unitarias nuevas o refactorizadas | `test(postprocess): cubrir NMS con cajas solapadas` |
| `refactor:` | Clean Code sin cambiar el comportamiento | `refactor(data): separar carga y validación del dataset` |
| `chore:` | `uv`, Makefile, CI, dependencias o configuración | `chore(ci): ejecutar pytest sin GPU` |
| `docs:` | README, docstrings masivos, `docs/` | `docs(readme): documentar métricas del baseline` |

> 💡 Puedes añadir alcance entre paréntesis: `feat(detect): …`

---

## 3. Tipo de cambio

- [ ] `feat` — Nueva funcionalidad
- [ ] `fix` — Corrección de error
- [ ] `test` — Pruebas unitarias
- [ ] `refactor` — Mejora de estructura (Clean Code)
- [ ] `chore` — Infraestructura, dependencias o configuración
- [ ] `docs` — Documentación
- [ ] ⚠️ **Breaking change** (si lo marcas, describe el impacto en la sección 8)

---

## 4. Capas del pipeline y archivos afectados

Marca las capas que toca esta PR (ajusta los nombres a los módulos reales del proyecto):

- [ ] **Datos / ingesta** — lectura de imágenes o video, dataset y anotaciones
      (`src/ppe_detection/io/`, `dataset.py`)
- [ ] **Preprocesamiento** — resize, normalización, aumentos y validación
      (`preprocess.py`, `transforms.py`)
- [ ] **Modelo / detector** — carga del modelo, inferencia y configuración
      (`model.py`, `load_model.py`, `detect.py`)
- [ ] **Post-procesamiento** — NMS, umbrales y filtrado de detecciones
      (`postprocess.py`)
- [ ] **Evaluación / métricas** — mAP, precision, recall, F1 y reportes
      (`evaluate.py`, `metrics.py`)
- [ ] **API / RPC / UI** — FastAPI, gRPC o la SPA React (`frontend/`)
      (`api/`, `grpc/`, `ui/`)
- [ ] **Pruebas** (`tests/test_*.py`)
- [ ] **Infraestructura** (`Dockerfile`, `pyproject.toml`, `uv.lock`, `Makefile`, `.github/workflows/`)
- [ ] **Documentación y licencia** (`README.md`, `docs/**`, `CONSTITUTION.md`, `LICENSE`)

---

## 5. Descripción de los cambios

**Historia de usuario / problema que resuelve:**
*(ej. «Como evaluador necesito procesar un video completo y obtener el conteo de EPP por fotograma para medir el desempeño del detector»)*

### 📝 Resumen técnico

*(qué cambió, en qué archivos y por qué; sé concreto)*

-

### 🧩 Justificación de diseño (Clean Code)

- **Alta cohesión:** *(por qué este módulo tiene una única responsabilidad)*
- **Bajo acoplamiento:** *(qué contrato/interfaz se usa y qué NO se conoce del módulo vecino)*
- **Contrato de entrada/salida:** *(firma y tipos; ej. `uint8 (H,W,3) ➔ list[Detection]`)*

### 🔀 Alternativas consideradas y trade-offs

- **Opción A:** … **Opción B:** … → **Elegida:** … porque…

---

## 6. Evidencia de pruebas (obligatoria)

```bash
# Ejecutar SOLO lo relacionado con esta PR y luego la suite completa
uv run pytest -v tests/test_<modulo>.py
uv run pytest -v
uv run ruff check src/ tests/
uv run ty check

# Verificación completa del proyecto y del paquete
make check
uv build
```

| Métrica | Valor |
| :--- | :--- |
| **Pruebas nuevas en esta PR** | __ |
| **Total acumulado del proyecto** | __ |
| **Cobertura del módulo tocado** | __ % *(si aplica)* |
| **Métrica del detector** | mAP@0.5: __ · Precision: __ · Recall: __ *(si aplica)* |

- [ ] Adjunté la **salida de `pytest`** o una captura de pantalla con el resultado.
- [ ] `make check` y `uv build` están en verde.
- [ ] El pipeline de **GitHub Actions** quedó en verde.
- [ ] Si la PR toca inferencia, adjunté un **ejemplo de entrada/salida** o la métrica correspondiente.
- [ ] La spec de Spec Kit está enlazada y sus AC están cubiertos.

### AC → prueba

| AC | Prueba pytest | ¿Pasa? |
| :--- | :--- | :---: |
| AC-01 | `tests/test_...py::test_...` | [ ] |
| AC-02 | `tests/test_...py::test_...` | [ ] |
| AC-03 | `tests/test_...py::test_...` | [ ] |

> **Test-first:** las pruebas se escriben antes de la implementación. Excepciones:
> SPI y specs de documentación. `/speckit.analyze` marca como error un AC sin prueba.
> **Sin umbral de cobertura:** el requisito de la entrega es **≥ 400 pruebas
> unitarias** (mínimo, no techo). Ver `docs/curso/PLAN-PRUEBAS.md`.

---

## 7. Checklist obligatorio pre-PR (Reglas de Juego UAO)

**Entorno y dependencias**
- [ ] Corrí todo con **`uv`** sobre **Python 3.13** (sin `pip`, sin `requirements.txt`).
- [ ] `uv run pytest -v` pasa **completo** y sin *warnings* ni deprecaciones.
- [ ] `uv run ruff check src/ tests/` y `uv run ty check` sin hallazgos.
- [ ] Si agregué una dependencia, actualicé `pyproject.toml` **y** `uv.lock` en el mismo commit.

**Calidad de código**
- [ ] Docstrings y *type hints* en cada función/clase pública.
- [ ] Sin `print()` de depuración, sin código comentado muerto y sin `TODO` sin issue.
- [ ] Nombres descriptivos; una sola responsabilidad por función.
- [ ] Sin credenciales, tokens ni rutas personales en el código.

**Estructura, datos y reproducibilidad**
- [ ] Código en `src/`, pruebas en `tests/`, sin `.ipynb`; Colab/Kaggle solo como **cómputo GPU** ejecutando un script versionado con `uv`.
- [ ] Cada AC de la spec tiene al menos una prueba pytest que lo referencia (test-first).
- [ ] `.gitignore` cubre pesos (`*.pt`, `*.pth`, `*.onnx`, `*.h5`), `data/`, `runs/`, `mlruns/`, `.venv/` y `.ipynb`.
- [ ] Verifiqué que **ningún archivo binario pesado** entró al commit (`git status`).
- [ ] Los datasets y pesos **no se versionan**; documenté cómo obtenerlos o generarlos.
- [ ] Registré **semilla, umbrales y versión del modelo** para que la inferencia sea reproducible.
- [ ] Las imágenes con personas se usan con permiso y sin datos personales innecesarios.
- [ ] No hay clase `person` ni `no-EPP`; el resultado no se presenta como cumplimiento normativo.

**Git y proceso**
- [ ] La PR es **pequeña y de un solo propósito**; la rama está actualizada desde `develop`.
- [ ] Los commits usan *Conventional Commits* con mensajes descriptivos.
- [ ] **Assignee = autor**; **reviewers = otros integrantes**; el autor no se aprueba.
- [ ] La PR se creó o actualizó con el **MCP de GitHub** y la **cuenta UAO**.
- [ ] La PR enlaza su issue (`Closes #N`) y su spec.
- [ ] Actualicé `docs/curso/ESTADO.md` y `AGENTS.md` §0 (`make estado-write` + bitácora); si cambió el stack o el estado, también `README.md` y `CONSTITUTION.md`.

---

## 8. Impacto y riesgos

- **Módulos / archivos de mayor riesgo:** …
- **¿Rompe compatibilidad?** Sí / No — *si aplica, describe la migración*
- **¿Afecta las métricas del detector?** Sí / No — *si aplica, adjunta el antes/después*
- **¿Requiere GPU, datos o pesos externos para probarse?** *(idealmente no; indica cómo se probó en CPU)*
- **Plan de reversión:** *(ej. `git revert` o restaurar desde `develop`)*

---

## 9. Checklist del revisor (para el compañero que aprueba)

- [ ] El código hace **exactamente** lo que promete el título (alcance cerrado).
- [ ] Se respeta la **responsabilidad única** de cada módulo (alta cohesión).
- [ ] El módulo nuevo **no** accede a estructuras internas de otro (bajo acoplamiento).
- [ ] Las pruebas cubren casos borde: imagen vacía, `NaN`, forma/dimensión, tipo de dato y escena sin detecciones.
- [ ] No hay secretos, binarios pesados ni `.ipynb` en el diff.
- [ ] Ausencia de duplicación innecesaria; nombres claros.
- [ ] Comentarios y docstrings explican **el porqué**, no el qué obvio.
- [ ] La inferencia es reproducible (semilla, umbrales y versión del modelo registrados).
- [ ] Se respetan los límites del dataset (sin `person`, sin `no-EPP`, sin juicio de cumplimiento).
- [ ] Aprobada por **al menos un integrante** antes de fusionar a `develop`.

---

## 10. Firma y revisión

| Integrante | Rol en la PR | ¿Revisó y aprobó? |
| :--- | :--- | :--- |
| | Autor / Desarrollador | — |
| | Revisor de código | [ ] Aprobado |
| | Revisor de código | [ ] Aprobado |

> 🔒 **Regla del curso:** la fusión a `develop` la hace el autor **después** de la
> aprobación de un compañero. El release `develop → main` se hace **solo** en la
> entrega del módulo y **siempre con merge commit**, nunca squash. No se hace `push`
> directo a `main` ni a `develop`.
