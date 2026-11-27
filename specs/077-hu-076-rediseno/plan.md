# Implementation Plan: HU-076 — Rediseño visual

**Branch**: `feature/077-hu-076-rediseno` | **Date**: 2026-11-27 | **Spec**:
[spec.md](./spec.md)

## Summary

Sustituir el aspecto de panel oscuro genérico por un sistema de diseño con identidad de
inspección de seguridad: papel, tinta, una banda de amarillo de señal y tipografía
condensada. El marcado y los textos se conservan; el cambio llega por tokens y por un
archivo `design.css` que se carga después del CSS existente.

## Technical Context

**Language/Version**: CSS moderno (custom properties), React 19, Vite 8, TypeScript 6

**Primary Dependencies**: ninguna nueva; Google Fonts por CSS con pila de respaldo

**Testing**: Vitest + Testing Library (93 pruebas existentes) y build de producción

**Target Platform**: navegadores modernos; SPA servida por nginx

**Project Type**: interfaz web

**Constraints**: no romper textos ni roles que usan las pruebas; sin dependencias nuevas

**Scale/Scope**: 1 archivo de diseño, 2 temas, 5 acentos

## Constitution Check

- **Sin dependencias nuevas**: las fuentes se cargan por CSS. ✅
- **Test-first**: se conservan las pruebas existentes y se valida con lint/test/build. ✅
- **Accesibilidad**: foco visible y `prefers-reduced-motion`. ✅
- **AGPL**: los créditos siguen en el pie. ✅

## Project Structure

```text
frontend/src/design.css      # nuevo: tokens, tipografía y armazón
frontend/src/main.tsx        # importa design.css después de styles.css
frontend/index.html          # fuentes y theme-color
specs/077-hu-076-rediseno/
```

## Design plan

**Concepto:** hoja de inspección pegada en la pared del taller.

| Token | Oscuro | Claro | Uso |
|---|---|---|---|
| `--bg` | `#101210` | `#edefe9` | fondo |
| `--panel-solid` | `#191d18` | `#ffffff` | paneles |
| `--text` | `#ecefe7` | `#14170f` | tinta |
| `--muted` | `#9aa396` | `#5c6357` | texto secundario |
| `--line` | `#2a2f29` | `#cdd2c7` | reglas |
| `--accent` | `#f5c400` | `#f5c400` | señal |

**Tipografía:** Barlow Condensed (titulares, cifras) + Barlow (texto). Una
superfamilia, dos anchos, herencia de señalización vial.

**Principios:**
1. Un solo elemento grita: la banda de señal. El resto es tinta sobre papel.
2. El dato manda: cifras tabulares y reglas, no tarjetas flotantes.
3. Radio 0–2 px, sin sombras, sin degradados.
4. El movimiento se reserva para la llegada del resultado.

## Risks

| Riesgo | Mitigación |
|---|---|
| Fuente externa no disponible | Pila de respaldo del sistema |
| Contraste insuficiente en claro | Tinta casi negra sobre papel frío; AA |
| Selectores que se pisan | Archivo cargado después y con la misma especificidad |

## Testing strategy

| AC | Prueba |
|---|---|
| AC-01 | Revisión del bloque de tokens en `design.css` |
| AC-02 | `npm run test` (roles y textos) y `npm run build` |
| AC-03 | Alternar tema en la SPA y comprobar el contraste a mano |
