# Regla: propiedad de archivos y trabajo en paralelo

> Se carga junto con `AGENTS.md`. Si hay conflicto, manda `AGENTS.md` §0.4.

## Antes de escribir una línea

1. Abre `docs/curso/M4/ASIGNACION.md` y localiza tu fila.
2. Verifica que la HU siga en *Todo* o *Ready* en el tablero. Si está *In progress*
   con otro assignee, **elige otra**.
3. Mueve la HU a *In progress* y asígnatela. Ese es el candado.
4. Crea la rama `feature/<spec>-hu-<id>-<slug>` desde `develop`.

## Rutas

- Tu dueño de ruta está en `docs/curso/propiedad.toml` (`[[owner]]`).
- Antes de commitear: `make ownership-check`.
  - `BLOQUEADO` → **no lo toques**. Abre un issue o pídelo en el issue de la HU.
  - `aviso` → puedes seguir; la revisión la pedirá CODEOWNERS.
- Nunca edites a mano `.github/CODEOWNERS`: se genera con `make codeowners`.

## Archivos que no son tuyos aunque parezcan libres

`AGENTS.md`, `CONSTITUTION.md`, `Makefile`, `uv.lock`, `frontend/package-lock.json`,
`tests/conftest.py`, `docs/curso/ESTADO.md`, `docs/curso/backlog.md`,
`docs/curso/PRUEBAS.md`. Todos están en `[[locked]]`.

## Git

- **Prohibido** `git push` a `develop` o `main`. Solo ramas `feature/*`.
- `git pull --rebase origin develop` antes de cada push.
- Un PR = una HU. Si detectas un arreglo colateral, ábrelo como issue.
- El autor nunca aprueba su PR. Pide revisión a otro integrante.

## Cierre

- `make check` verde **antes** de abrir el PR.
- No ejecutes `make estado-write`: el bloque de estado se actualiza solo en la
  sesión de cierre, por una persona.
- Al fusionar, mueve la HU a *Done* y cierra la issue a mano.
