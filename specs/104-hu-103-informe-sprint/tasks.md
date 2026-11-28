# Tareas — HU-103 Informe de sprint

**Issue**: #159 · **Spec**: `spec.md` · **Plan**: `plan.md`

## Implementación

- [x] T1. Módulo `sprint.py` con `Closed`, `Point`, `burndown`, `velocity_by_person` y
      `deviation`.
- [x] T2. Exportar los cierres del tablero y calcular el burndown real.
- [x] T3. Redactar `docs/curso/M4/SPRINT.md` con resumen, tabla diaria y velocidad.

## Pruebas (8 objetivo)

- [x] T4. Burndown con datos simulados y sin cierres.
- [x] T5. Errores de total inválido y de cierres por encima del total.
- [x] T6. Velocidad por integrante y dueño ausente.
- [x] T7. Desviación con signo y plan cero.
- [x] T8. Aritmética y monotonía de la tabla del documento.
- [x] T9. Restante final igual a la suma de HU abiertas.

## Cierre

- [ ] T10. `make check` en verde.
- [ ] T11. `make ownership-check` sin bloqueos.
- [ ] T12. PR con la plantilla UAO y `Closes #159`.
- [ ] T13. Actualizar `PRUEBAS.md` al fusionar #270 (evitar conflicto).
