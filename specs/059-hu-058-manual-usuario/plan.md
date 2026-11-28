# Implementation Plan: HU-058 — Manual de usuario de la SPA

**Branch**: `feature/059-hu-058-manual-usuario` | **Date**: 2026-11-28 | **Spec**:
[spec.md](./spec.md)

**Input**: `specs/059-hu-058-manual-usuario/spec.md` e issue #114.

## Summary

Documentar el flujo rediseñado por HU-077 (#267) en `docs/manual/README.md` con cuatro
capturas reales tomadas en ejecución local, explicar el resultado «sin detecciones» y sus
límites, y cubrir los tres AC con cuatro pruebas estructurales.

## Technical Context

**Language/Version**: Markdown + PNG; Python 3.13 para pytest

**Primary Dependencies**: ninguna nueva; Vite existente y navegador local para capturas

**Storage**: `docs/manual/README.md` y `docs/manual/capturas/*.png`

**Testing**: pytest estático sobre el documento y los artefactos

**Target Platform**: documentación del repositorio

**Project Type**: documentación de usuario

**Performance Goals**: N/A

**Constraints**: no tocar `frontend/`, `docs/operacion/` ni HU-055; no declarar
validación remota; `docs/manual/` es propiedad de Eliana y `specs/` de Jesús (revisión)

**Scale/Scope**: 1 manual, 4 capturas, 1 archivo de pruebas, 3 artefactos de spec

## Constitution Check

- **Spec Kit antes de implementar**: spec/plan/tasks creados antes del código. ✅
- **Test-first**: cuatro pruebas referencian AC-01/AC-02/AC-03. ✅
- **Una HU por PR**: solo HU-058. ✅
- **Propiedad**: no se tocan archivos `[[locked]]`; se pide revisión ajena. ✅
- **Sin secretos ni datos personales**: capturas de demo local. ✅

## Project Structure

```text
docs/manual/README.md                     # manual del flujo rediseñado
docs/manual/capturas/01-seleccion.png     # captura local del paso 01
docs/manual/capturas/02-analisis.png      # captura local del paso 02
docs/manual/capturas/03-resultados.png    # captura local del paso 03
docs/manual/capturas/04-sin-detecciones.png
tests/test_manual_usuario_spa.py          # 4 pruebas estructurales
specs/059-hu-058-manual-usuario/          # spec/plan/tasks
```

## Design decisions

1. **La SPA ya fusionada es la fuente**: no se reabre HU-077 ni se cambia `frontend/`.
2. **Capturas honestas**: se toman con Vite local y una API simulada; el manual lo dice
   explícitamente para no confundirlas con el sitio desplegado.
3. **Cautela en resultados vacíos**: el manual distingue «sin detecciones» de «sin EPP»
   y remite a HU-004/HU-059 para los mensajes exactos.
4. **Pruebas estáticas**: validan contenido, enlaces, firma PNG y procedencia; no
   vuelven a ejecutar la suite del frontend ya cubierta por #267.

## Risks

| Riesgo | Mitigación |
|---|---|
| Capturas ilegibles en el visor de GitHub | PNG de 1280×900 y alt text descriptivo |
| El manual contradiga la UI actual | Los textos se copian de los componentes de #267 |
| Confundir demo con producción | Aviso explícito y prueba que lo exige |
| `docs/curso/PRUEBAS.md` quede desactualizado | Archivo `[[locked]]` de Jesús: se reporta, no se edita |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | `tests/test_manual_usuario_spa.py::test_ac_01_flujo_con_capturas_reales` |
| AC-02 | `tests/test_manual_usuario_spa.py::test_ac_02_sin_detecciones_y_limites_explicitos` |
| AC-03 | `tests/test_manual_usuario_spa.py::test_ac_03_estructura_y_enlaces_del_manual` |
| AC-01/03 | `tests/test_manual_usuario_spa.py::test_capturas_declaran_origen_local` |
