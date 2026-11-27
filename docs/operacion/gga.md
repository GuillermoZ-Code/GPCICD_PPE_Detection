# GGA — revisión de código con IA (opcional)

> **Qué es:** Gentleman Guardian Angel, un CLI que revisa los cambios con un modelo de
> IA antes de commitear. Se apoya en el proveedor configurado en [`.gga`](../../.gga)
> y en las reglas de [`CONSTITUTION.md`](../../CONSTITUTION.md).
>
> **Qué no es:** no sustituye la revisión humana, `make check`, la CI ni la aprobación
> de otro integrante. Es una ayuda **opcional y no bloqueante** (ADR 0011).

## 1. Instalación

GGA se instala una vez por equipo y no se versiona. Si el comando no existe, el hook
del repositorio termina con 0 y el commit sigue:

```bash
gga --version
```

El repositorio solo versiona `.gga`, el hook de pre-commit y este runbook.

## 2. Configuración

`.gga` usa el proveedor local de OpenCode:

```text
PROVIDER="opencode"
RULES_FILE="CONSTITUTION.md"
PR_BASE_BRANCH="develop"
```

No hay tokens en `.gga`; el proveedor toma sus credenciales del entorno local. Si un
equipo no tiene OpenCode configurado, GGA falla, pero el equipo puede desactivar el
hook sin afectar el resto del proyecto.

## 3. Uso

```bash
# Revisar el último commit
gga run --ci

# Revisar toda la rama contra develop
gga run --pr-mode

# Revisar solo el diff de la PR
gga run --pr-mode --diff-only

# Revisar los archivos preparados
gga run
```

El hook de pre-commit ejecuta `gga run` automáticamente si el binario está instalado.
Si no está instalado, imprime un aviso y no bloquea.

## 4. Reglas revisadas

GGA lee `CONSTITUTION.md`; por eso no se duplican aquí. Las revisiones deben vigilar,
como mínimo:

- `uv` como único gestor; nada de `pip` ni `requirements.txt`.
- Pruebas ABC/AAA y trazabilidad `AC-NN` → prueba.
- Pesos, datasets y secretos fuera de Git.
- Sin `person` ni `no-EPP`; no se juzga cumplimiento normativo.
- AGPL y atribución del dataset CC-BY-4.0.
- Reproducibilidad: semilla, modelo, tamaño y umbrales.

## 5. Evidencia de una revisión real

La revisión se ejecuta sobre el diff de una PR y su salida se adjunta en el comentario
de la PR. Ejemplo de invocación:

```bash
gga run --pr-mode --diff-only
```

El resultado se registra en la PR; **no** se copian credenciales ni rutas locales.

**Evidencia del 2026-11-27:** con `gga v2.10.1`, proveedor `opencode` y los patrones
`src/*,tests/*,frontend/src/*,deploy/*`, la revisión de `gga_hook.py` y
`tests/test_gga.py` devolvió `STATUS: PASSED`. La salida completa se adjunta en la PR
de HU-075.

## 6. Desactivar

Si un equipo no quiere usar GGA, puede quitar el hook local con:

```bash
uv run pre-commit uninstall
```

O dejar el hook instalado: el wrapper de `ppe_detection.tools.gga_hook` no bloquea si
`gga` no está en el `PATH`.
