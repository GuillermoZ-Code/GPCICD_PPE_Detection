# Tareas — HU-106 `make estado` con GitLab

**Issue**: #162 · **Spec**: `spec.md` · **Plan**: `plan.md`

## Implementación

- [x] T1. Añadir `Pipeline` y los campos `pipeline`/`gitlab_note` a `Report`.
- [x] T2. Implementar `parse_pipeline()` con validación de `status`, `sha` y `web_url`.
- [x] T3. Implementar `_collect_gitlab()` con `shutil.which` y `glab api`.
- [x] T4. Integrar la consulta en `collect()`.
- [x] T5. Renderizar la línea `**GitLab:**` o la nota de indisponibilidad.

## Pruebas (12 objetivo)

- [x] T6. `parse_pipeline`: lista, objeto único, lista vacía, campos faltantes, JSON inválido.
- [x] T7. `render`: pipeline visible, SHA corto y nota sin `glab`.
- [x] T8. `_collect_gitlab`: sin `glab`, con `glab` simulado y con comando fallido.
- [x] T9. Constante de la rama de integración.

## Cierre

- [ ] T10. `make check` en verde.
- [ ] T11. `make ownership-check` sin bloqueos.
- [ ] T12. PR con la plantilla UAO y `Closes #162`.
