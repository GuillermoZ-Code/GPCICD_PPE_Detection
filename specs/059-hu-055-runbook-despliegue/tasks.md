# Tareas — HU-055 Runbook de despliegue y rollback

**Issue**: #111 · **Spec**: `spec.md` · **Plan**: `plan.md`

## Implementación

- [x] T1. Verificar el runbook existente y sus secciones.
- [x] T2. Crear la spec de la HU (trazabilidad).
- [x] T3. Añadir la prueba estructural.

## Pruebas (8 objetivo)

- [x] T4. Secciones obligatorias y cobertura de HU-055.
- [x] T5. Despliegue por pipeline y manual con comandos exactos.
- [x] T6. Rollback por tag y `.deployed_env`.
- [x] T7. Diagnóstico, aprovisionamiento y apagado.
- [x] T8. Modelo `:ro`, SHA256 y ausencia de secretos.

## Cierre

- [ ] T9. `make check` en verde.
- [ ] T10. `make ownership-check` sin bloqueos.
- [ ] T11. PR con la plantilla UAO y `Closes #111`.
