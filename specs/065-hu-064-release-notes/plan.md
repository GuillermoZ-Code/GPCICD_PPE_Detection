# Plan: HU-064 — Notas de versión v1.0.0 y CHANGELOG

**Input**: `specs/065-hu-064-release-notes/spec.md` e issue #120.

## Enfoque

1. **Tests primero**: crear `tests/test_changelog.py` con cuatro pruebas que lean
   `CHANGELOG.md` desde la raíz y comprueben encabezado Keep a Changelog, orden de
   secciones, enlaces reales y categorías con fecha ISO.
2. **Contenido**: redactar `CHANGELOG.md` con `Unreleased` y `[1.0.0] - 2026-11-27`
   (fecha prevista), organizado por Added/Changed/Fixed.
3. **Trazabilidad**: cada entrada M4 enlaza la issue HU y el PR correspondiente
   (HU-044/045/047/048/056/057/062, HU-030/031); las entregas M2/M3 se resumen sin
   números inventados.
4. **Validación**: ejecutar las pruebas, la suite completa, ruff, formato, ty y la
   compuerta de propiedad.

## Archivos

- `CHANGELOG.md` — nuevo; registro de cambios y notas de v1.0.0.
- `tests/test_changelog.py` — nuevo; 4 pruebas de formato.
- `specs/065-hu-064-release-notes/` — spec, plan y tareas.

## Decisiones

- Mantener el formato canónico de Keep a Changelog para que otras herramientas lo lean.
- No publicar tag: el CHANGELOG queda listo y el release lo decide el equipo.
- Usar enlaces absolutos al repositorio `GuillermoZ-Code/GPCICD_PPE_Detection`.

## Riesgos

- Que algún PR citado se fusione después: se marca su estado como «en revisión» en la
  entrada en vez de afirmar que ya está en `develop`.
- Que la fecha prevista cambie: queda explícita en el encabezado de la versión.
