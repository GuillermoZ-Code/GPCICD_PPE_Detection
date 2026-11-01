# ADR 0005 — Contract-first con detector simulado

- **Fecha:** 2026-10-31
- **Estado:** Aceptada
- **Decisores:** Grupo 4

## Contexto

La ruta crítica del M3 es `HU-002 → HU-006 → HU-010 → HU-011` y, con 1 SP ≈ 1 día,
supera el tiempo disponible si se implementa en serie. API, interfaz y gRPC no
necesitan el modelo real para avanzar; necesitan un contrato estable.

## Decisión

Definir primero el contrato:

```text
ImageData → Detector.detect() → list[Detection]
```

- `ImageData`: arreglo `uint8 HxWx3` RGB, dimensiones originales, formato y fuente.
- `Detection`: `class_id`, `class_name`, `confidence` en `[0,1]`, `bbox` `xyxy`,
  `image_width`, `image_height`.
- `Detector`: protocolo con `detect(image: ImageData) -> list[Detection]`.
- `FakeDetector`: implementación determinista para pruebas (vacío o cajas fijas).
- Pruebas de contrato: lista vacía, cajas válidas, confianza en rango, catálogo de
  6 clases.
- Documentación en `docs/architecture/contracts.md` (se crea con la TA).

La TA de contract-first se ejecuta al inicio del M3. Las HU de API (HU-006), interfaz
(HU-007) y gRPC (HU-010) consumen el contrato y el `FakeDetector` hasta que HU-002
entregue el detector real.

## Alternativas consideradas

- **Implementar el detector primero:** bloquea API/UI/gRPC y alarga la ruta crítica.
- **Mocks ad hoc por cada HU:** duplica contratos y genera divergencias.
- **Contrato solo documental:** no permite pruebas ni integración temprana.

## Consecuencias

- API, UI y gRPC avanzan en paralelo con el modelo.
- El contrato es la fuente para REST, gRPC y Streamlit.
- El detector real debe cumplir el mismo contrato; si no, se ajusta el contrato con
  un nuevo ADR.
- La TA no implementa el modelo ni entrena; solo define tipos, interfaz y fake.

## Referencias

- `CONSTITUTION.md` §7 y §10.
- `docs/curso/backlog.md` (HU-002, HU-006, HU-007, HU-010).
- `specs/001-ta-contract-first/`.
