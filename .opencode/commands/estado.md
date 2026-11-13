---
description: Muestra el estado operativo del proyecto (git, PRs, issues) y permite guardarlo en ESTADO.md
---

## Uso

```text
$ARGUMENTS
```

- **Sin argumentos:** ejecuta `make estado` y presenta la salida tal cual.
- **Con `write` o `guardar`:** ejecuta `make estado-write` y después añade una
  entrada a la bitácora de `docs/curso/ESTADO.md` con **hecho**, **en vuelo** y
  **siguiente**.

## Reglas

- No inventes datos: si `gh` no está disponible, dilo y muestra solo lo que devuelva
  `git`.
- No cambies issues, tablero ni backlog desde este comando.
- Si el bloque generado no coincide con `git log`, gana `git` y hay que avisar.
