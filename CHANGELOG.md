# Changelog

Todas las notas significativas de este proyecto se documentan en este archivo.
El formato sigue [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) y el
versionamiento [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> `v1.0.0` tiene **fecha prevista de entrega** 2026-11-27 según
> `docs/entrega/RUBRICA-M4.md`. Las PR marcadas como «en revisión» están abiertas y
> aún no se han fusionado en `develop`: se enlazan como evidencia de la HU, no como
> contenido ya publicado en la rama de entrega.

## [Unreleased]

### Added

- [HU-064](https://github.com/GuillermoZ-Code/GPCICD_PPE_Detection/issues/120) — Registro de cambios y notas de v1.0.0 con enlaces a HUs y PRs; PR en preparación.

### Changed

- Sin cambios adicionales desde la fecha de corte de `v1.0.0`.

### Fixed

- Sin correcciones adicionales desde la fecha de corte de `v1.0.0`.

## [1.0.0] - 2026-11-27

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
