# Changelog

Todas las notas significativas de este proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) y el
versionamiento [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> `v1.0.0` se publicó el **2026-11-28**; `v1.1.0` documenta las HUs de accesibilidad, historial, manual y capacidad. Las notas de v1.0.0 se conservan como registro histórico.

## [Unreleased]

Sin cambios pendientes.

## [1.1.0] - 2026-11-28

### Added

- [HU-080](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/136) — Accesibilidad WCAG 2.2 AA: enlace de salto, foco al resultado, `aria-live`/`aria-busy`, foco del diálogo y contraste AA en ambos temas (PR #275).
- [HU-088](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/144) — Historial de la sesión en la SPA: lista con miniatura, conteo y modelo, detalle por clase y limpieza; solo en `localStorage` (PR #276).
- [HU-058](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/114) — Manual de usuario de la SPA con capturas (PR #272).
- [HU-109](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/165) — Registro de capacidad y velocidad real del M4 (PR #273).

### Changed

- SPA: flujo de carga, progreso y resultados de HU-077 integrado en la entrega.
- Documentación de release v1.0.0 y runbook de despliegue actualizados.

## [1.0.0] - 2026-11-28

Estas son las notas de v1.0.0 de la entrega M4 (fecha prevista). Las entradas enlazan la historia y su PR;
cuando el PR sigue abierto se indica explícitamente para no afirmar una fusión que
no ocurrió. Las entregas M2 y M3 quedan resumidas como base de esta versión.

### Added

- [HU-045](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/101) — Healthchecks `live` y `ready` para observar el estado del servicio REST ([PR #209](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/209), en revisión).
- [HU-047](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/103) — Logs JSON con `request_id` para correlacionar peticiones y respuestas ([PR #211](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/211), en revisión).
- [HU-056](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/112) — Runbook de diagnóstico con seis etapas, comandos y tres fallos simulados ([PR #213](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/213), en revisión).
- [HU-057](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/113) — Guion de sustentación M4, checklist del entorno y registro de ensayo cronometrado ([PR #214](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/214), en revisión).

### Changed

- [HU-044](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/100) — Validación de la configuración por entorno antes de arrancar la API ([PR #210](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/210), en revisión).
- [HU-048](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/104) — Límites configurables de tamaño y tipo MIME en `POST /predict`, preservando el comportamiento M3 cuando no se configura el límite ([PR #212](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/212), en revisión).
- [HU-062](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/118) — Contrato REST/gRPC alineado: mismas detecciones, metadatos y mapeo de errores con detector simulado compartido ([PR #216](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/216), en revisión).

### Fixed

- [HU-062](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/118) — `DetectorNotConfiguredError` durante `detect()` responde HTTP 503 en REST, igual que `UNAVAILABLE` en gRPC ([PR #216](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/216), en revisión).
- [HU-056](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/112) — El registro de ensayos separa la validación estática del documento del ensayo real del equipo, marcado como pendiente ([PR #213](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/213), en revisión).
- [HU-057](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/113) — El guion de sustentación no afirma tiempos reales ni ensayos no ejecutados ([PR #214](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/pull/214), en revisión).

## [0.3.0] - 2026-11-14

Entrega del módulo 3: API REST y gRPC sobre el contrato compartido, detector YOLO
con artefacto versionado por SHA256, evaluación y pruebas automatizadas. Las HUs y
PRs de esa entrega se registran en `docs/curso/TRAZABILIDAD.md`, de un solo escritor.

## [0.2.0] - 2026-10-31

Entrega del módulo 2: alcance, arquitectura, dataset y plan de trabajo.

## [0.1.0] - 2026-10-17

Inicio del proyecto y configuración base del repositorio.
