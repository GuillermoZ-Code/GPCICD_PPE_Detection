# Plan: HU-061 — README con badges y enlaces públicos del M4

**Input**: `specs/062-hu-061-readme-badges/spec.md` e issue #117.

## Enfoque

1. **Verificar la dependencia**: HU-065 (#121) está implementada y fusionada en la
   PR #218 (`merge_commit 35d8b97`): workflow `mirror-gitlab.yml`, push con el mismo
   SHA y token enmascarado. La issue externa sigue abierta por cierre administrativo;
   no se cierra desde esta HU ni se toma como bloqueo.
2. **Tests primero**: crear `tests/test_readme_badges.py` con 4 pruebas AAA que lean
   `README.md` como texto (sin red, sin modelo y sin credenciales): AC-01 ×2, AC-02
   ×1, AC-03 ×1. Ejecutar solo ese archivo en rojo.
3. **Implementación**: añadir los cuatro badgesM4 al bloque existente, crear la
   sección «Enlaces públicos del M4» con remoto HTTPS, Registry derivado del proyecto
   GitLab verificado, `CONSTITUTION.md` y `<URL_PUBLICA>` como plantilla, y registrar
   la sección en la tabla de contenidos. El badge de Docker Hub queda como
   «pendiente» y enlaza #124 (HU-068 abierta) sin inventar namespace.
4. **Validación**: ejecutar solo las pruebas focalizadas en verde, comprobar formato
   de Markdown con `ruff format --check`, `check_specs` y propiedad; no repetir la
   suite completa sin necesidad.
5. **Entrega**: dos commits (test-first y docs), push y PR a `develop` con plantilla
   UAO y `Closes #117`; mover la tarjeta a *In review*, sin aprobar ni fusionar.

## Archivos

- `tests/test_readme_badges.py` — nuevo; 4 pruebas AAA.
- `README.md` — modificado; badges, sección pública y TOC.
- `specs/062-hu-061-readme-badges/` — spec, plan y tareas.

## Decisiones

- El proyecto GitLab es `educacional-group/GPCICD_PPE_Detection` según el workflow
  fusionado en HU-065; el Registry se deriva de él, no se inventa un dominio.
- El badge de Docker Hub señala HU-068 (#124), que sigue abierta: «pendiente».
- La URL pública MaaS se deja como `<URL_PUBLICA>` hasta que HU-053 cree el Space.
- La licencia del badge es AGPL-3.0-only y apunta al archivo `./LICENSE` versionado.
- No se tocan `ESTADO.md`, `backlog.md`, `PRUEBAS.md`, `uv.lock` ni
  `package-lock.json`: son de un solo escritor.

## Riesgos

- Que el evaluador interprete el badge «pendiente» como fallo: se explica en la
  sección pública con el enlace a la HU que lo resolverá.
- Que un badge externo cambie de URL: se usa la ruta canónica documentada en la
  spec de HU-065 y en la documentación del repositorio.
- Que el formateador de Markdown reescriba ejemplos: no se añaden bloques Python.
