# Plan de implementación — HU-082 (spec 083)

**Rama**: `feature/083-hu-082-codeowners-checks` · **Issue**: #138 · **Spec**: `spec.md`

## Enfoque

Cerrar la parte verificable de la HU sin tocar la configuración de GitHub: CODEOWNERS
ya se genera desde `propiedad.toml` y la compuerta ya corre en CI. Añadimos un ADR que
registra los checks requeridos y el estado de la protección, más pruebas que bloquean
la deriva entre manifiesto, archivo generado y decisión documentada.

## Estructura

- `specs/083-hu-082-codeowners-checks/`: spec, plan y tareas.
- `tests/test_codeowners_hu082.py`: 4 pruebas AAA de configuración y documentación.
- `docs/adr/0012-codeowners-checks-obligatorios.md`: decisión que actualiza ADR 0004.
- `docs/adr/README.md`: índice con la nueva decisión.

## Decisiones

1. No regenerar CODEOWNERS: el contenido actual ya coincide con el manifiesto; la
   prueba lo verifica y evita un cambio sin efecto.
2. AC-02 se documenta como **protección escrita pendiente de aprobación**: no se
   activa branch protection sin consentimiento del equipo (AGENTS.md §0.4.4).
3. Los siete checks se enumeran por su nombre real de job en GitHub Actions.
4. ADR 0004 queda intacto; 0012 lo complementa (ADR append-only).

## Riesgos y mitigación

- **Deriva del generador**: comparar el texto completo, no solo líneas sueltas.
- **Cambio de nombres de jobs**: la prueba falla y obliga a actualizar el ADR.
- **Propiedad**: `.github/` y `docs/adr/` pertenecen a Guillermo (aviso, no bloqueo);
  CODEOWNERS pedirá su revisión automáticamente.
