# Feature Specification: HU-076 — Rediseño visual con `frontend-design`

**Feature Branch**: `feature/077-hu-076-rediseno`

**Created**: 2026-11-27

**Status**: En implementación

**Input**: Issue #132 — «HU-076 — Rediseño visual: sistema de diseño con
`frontend-design`». Épica `ep-11`, 5 SP, 16 pruebas objetivo. Depende de HU-074.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - La interfaz parece una herramienta de seguridad, no una plantilla (Priority: P1)

Como evaluador, quiero que la aplicación se vea como una hoja de inspección de seguridad
industrial, para que el producto se recuerde por su oficio y no por el aspecto genérico
de panel oscuro con tarjetas.

**Why this priority**: la rúbrica del M4 incluye la interfaz; hoy usa la paleta oscura
con degradados y tarjetas redondeadas que se confunde con cualquier plantilla.

**Independent Test**: al abrir la SPA, la cabecera es una banda amarilla de señal con el
titular en tipografía condensada, el resto es papel y tinta con reglas de 1 px, y el
resultado se lee como un reporte con cifras tabulares.

**Acceptance Scenarios** (AC de la issue #132):

1. **AC-01**: **Dado** el sistema de diseño, **Cuando** se revisa, **Entonces** hay una
   paleta de 4–6 colores con nombre y una escala tipográfica documentada.
2. **AC-02**: **Dado** el rediseño, **Cuando** se aplica, **Entonces** la cabecera, los
   paneles, la tabla y los botones siguen el mismo lenguaje visual.
3. **AC-03**: **Dado** el modo claro y el oscuro, **Cuando** se alternan, **Entonces** el
   contraste se mantiene y no aparecen colores fuera de la paleta.

### Edge Cases

- **Sin conexión a Google Fonts**: la pila de respaldo mantiene la jerarquía.
- **`prefers-reduced-motion`**: no hay animaciones de entrada.
- **Pantalla pequeña**: las dos columnas pasan a una y las cifras se apilan.
- **Acento alternativo**: los cinco acentos del panel de configuración siguen
  funcionando.

## Requirements *(mandatory)*

- **FR-001**: La paleta MUST declararse como tokens CSS con nombre y valor.
- **FR-002**: La tipografía MUST ser una superfamilia con un ancho condensado para
  titulares y otro para texto.
- **FR-003**: Los paneles MUST usar reglas de 1 px y radio 0–2 px, sin sombras.
- **FR-004**: El único color de acento fuerte MUST ser el amarillo de señal.
- **FR-005**: La interfaz MUST respetar `prefers-reduced-motion` y el foco visible.
- **FR-006**: Los textos y roles que usan las pruebas MUST conservarse.

## Success Criteria *(mandatory)*

- **SC-001**: `npm run lint`, `npm run test` y `npm run build` en verde.
- **SC-002**: La SPA servida muestra la banda de señal y la tipografía nueva.
- **SC-003**: El contraste texto/fondo cumple AA en ambos temas.

## Assumptions

- El marcado se mantiene; el cambio llega por tokens y por un archivo de diseño.
- No se añaden dependencias de JavaScript; las fuentes se cargan por CSS.
