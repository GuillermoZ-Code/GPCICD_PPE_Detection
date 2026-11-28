# Tareas — HU-110 MLflow en el Droplet

**Issue**: #166 · **Spec**: `spec.md` · **Plan**: `plan.md`

## Implementación

- [x] T1. Servicio `mlflow` con perfil, volumen, comando y healthcheck.
- [x] T2. Ruta `/mlflow/*` en Caddy con basic auth y sin quitar el prefijo.
- [x] T3. Variables en `.env.example` y sección 9 del runbook.

## Pruebas (16 objetivo)

- [x] T4. Servicio, perfil, imagen y ausencia de puertos publicados.
- [x] T5. Persistencia de SQLite y artefactos en el host.
- [x] T6. Prefijo, healthcheck y reinicio.
- [x] T7. Caddy: auth, proxy y ausencia de credenciales.
- [x] T8. Runbook: arranque, respaldo y seguridad.

## Cierre

- [ ] T9. `make check` en verde.
- [ ] T10. `make ownership-check` sin bloqueos.
- [ ] T11. PR con la plantilla UAO y `Closes #166`.
