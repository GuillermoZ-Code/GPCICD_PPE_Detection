# ADR 0012 — CODEOWNERS generado y checks obligatorios

- **Fecha:** 2026-11-25
- **Estado:** Aceptada
- **Decisores:** Grupo 4
- **Actualiza:** ADR 0004 (Gitflow, Spec Kit y estrategia de merge)

## Contexto

El ADR 0004 fijó que la protección de ramas es una **regla escrita** y no una
configuración técnica de GitHub. Durante el M4 cuatro agentes escriben en paralelo
y `docs/curso/propiedad.toml` declara dueños y archivos de un solo escritor. La
HU-082 pide que la revisión por dueño y los checks necesarios queden verificables
sin depender de la memoria del equipo.

Ya existen tres piezas: el manifiesto de propiedad, el generador
`python -m ppe_detection.tools.ownership --write-codeowners` (objetivo `make
codeowners`) y los jobs del flujo de GitHub Actions. Falta dejar por escrito qué
checks se exigen y qué parte de la protección continúa pendiente de una decisión
del equipo.

## Decisión

1. `.github/CODEOWNERS` se genera desde `docs/curso/propiedad.toml`. No se edita a
   mano: `make codeowners` lo sobrescribe. La compuerta `make ownership-check`
   bloquea los archivos `[[locked]]` ajenos y avisa del resto.
2. Toda PR a `develop` debe llegar con estos siete checks en verde:

   | Check | Responsibility |
   | :--- | :--- |
   | `Asignar revisor` | un integrante distinto del autor queda como revisor |
   | `Calidad` | Ruff, formato y tipos |
   | `Frontend` | ESLint, Vitest y build de la SPA |
   | `Matriz` | pruebas de Python en la matriz soportada |
   | `Plantilla` | secciones obligatorias 1, 3, 4, 5, 6, 7 y 8 |
   | `Propiedad` | ningún archivo bloqueado tocado por otro dueño |
   | `Specs` | `spec.md`, `plan.md` y `tasks.md` de cada spec activa |

3. La revisión la pide CODEOWNERS al dueño de cada ruta; el autor nunca se
   autoaprueba. Esto conserva la **protección escrita** del ADR 0004.
4. Activar la protección técnica de `develop` y `main` con estos checks requeridos
   queda **pendiente de aprobación del equipo** y de permisos de administrador.
   Esta ADR propone la configuración; no afirma que ya esté activa ni la aplica.

## Alternativas consideradas

- **Editar CODEOWNERS a mano:** rápido, pero diverge del manifiesto y lo sobrescribe
  el generador. Descartada.
- **Activar branch protection sin aprobación:** contradice el ADR 0004 y la regla
  del equipo. Descartada por ahora.
- **Enumerar solo los checks que fallen:** deja huecos en la revisión. Descartada.

## Consecuencias

- La propiedad y los checks son auditables desde el repositorio.
- Si un job cambia de nombre, la prueba de esta HU falla y obliga a actualizar el
  ADR: la documentación no se queda silenciosamente desactualizada.
- Cuando el equipo apruebe la protección técnica, bastará con marcar los siete
  checks como requeridos en `develop` y `main` y registrar la fecha en un ADR nuevo.

## Referencias

- ADR 0004 — Gitflow, Spec Kit y estrategia de merge.
- `docs/curso/propiedad.toml` y `.github/CODEOWNERS`.
- `.github/workflows/` y `AGENTS.md` §0.4.
