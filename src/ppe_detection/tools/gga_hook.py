"""Hook opcional de GGA para pre-commit (HU-075).

Si `gga` no está instalado, el hook termina con 0 y no bloquea el commit. Si está
instalado, ejecuta `gga run` y propaga su código de salida. No usa red por sí mismo:
GGA decide el proveedor configurado en `.gga`.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from collections.abc import Callable, Sequence


def gga_available(which: Callable[[str], str | None] = shutil.which) -> bool:
    """Indica si el ejecutable `gga` está en el PATH."""
    return which("gga") is not None


def run_gga(
    args: Sequence[str] = (),
    *,
    which: Callable[[str], str | None] = shutil.which,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> int:
    """Ejecuta GGA si existe; devuelve 0 cuando no está instalado."""
    if not gga_available(which):
        return 0
    command = ["gga", "run", *args]
    completed = runner(command, check=False)
    return int(completed.returncode)


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada del hook; imprime el motivo cuando se omite."""
    args = list(sys.argv[1:] if argv is None else argv)
    if not gga_available():
        print("GGA no está instalado; se omite la revisión opcional.")
        return 0
    return run_gga(args)


if __name__ == "__main__":
    raise SystemExit(main())
