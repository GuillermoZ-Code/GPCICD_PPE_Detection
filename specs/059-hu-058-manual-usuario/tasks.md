# Tasks: HU-058 — Manual de usuario de la SPA

**Input**: Design documents from `specs/059-hu-058-manual-usuario/`

**Prerequisites**: `plan.md`, `spec.md`

**Tests**: obligatorias (test-first). Cada AC tiene al menos una prueba que lo
referencia por su identificador.

## Phase 1: Setup

- [x] T001 Crear la rama `feature/059-hu-058-manual-usuario` desde `develop` actualizado
      (`c02db88`) y mover #114 a *In progress* en el tablero.
- [x] T002 Escribir `spec.md`, `plan.md` y `tasks.md` con los AC de la issue #114.
- [x] T003 Verificar dependencia: HU-077/#133 integrada por PR #267 en `develop`; #114
      asignada a Eliana. No se toca HU-055/#111.

## Phase 2: Pruebas (test-first)

- [x] T004 [AC-01] `tests/test_manual_usuario_spa.py`: pasos 01/02/03, tres capturas
      enlazadas y archivos PNG válidos.
- [x] T005 [AC-02] Explicación de «sin detecciones», umbral/filtros, clases y límite de
      cumplimiento, con su captura.
- [x] T006 [AC-03] Estructura de secciones, enlaces, fecha de verificación y aviso de
      origen local.
- [x] T007 [AC-01/03] Cuarta prueba que prohíbe presentar las capturas como validación
      remota.

## Phase 3: Documentación

- [x] T008 Generar cuatro capturas desde Vite local con API simulada; sin credenciales,
      sin Droplet y sin datos personales.
- [x] T009 Escribir `docs/manual/README.md` con el flujo completo, capturas, lectura de
      resultados, «sin detecciones», límites y enlace a `errores.md`.

## Phase 4: Cierre

- [x] T010 `uv run pytest -q tests/test_manual_usuario_spa.py` en verde (4 pruebas).
- [x] T011 `uv run python -m ppe_detection.tools.check_specs --check` y
      `make ownership-check` equivalentes en local.
- [x] T012 Commit, push y PR a `develop` con plantilla UAO, `Closes #114`, spec
      enlazada y revisor ajeno. Sin fusión ni autoaprobación.

## Evidencia local (2026-11-28)

- Test-first: las cuatro pruebas fallaron antes del manual y las capturas.
- Capturas: Vite en `127.0.0.1:5173`, API simulada en `127.0.0.1:8000`, navegador
  headless local; cuatro PNG escritos y verificados por firma y tamaño.
- Después del documento: 4/4 pruebas nuevas en verde; suite completa y compuertas
  locales reportadas solo con salida real en la descripción de la PR.

## Estado

- Implementación en `feature/059-hu-058-manual-usuario`.
- Issue #114 en *In progress*; PR abierta, pendiente de revisión ajena.
