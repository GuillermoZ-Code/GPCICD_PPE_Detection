"""Informe de calidad del proyecto (HU-012)."""

from __future__ import annotations

import argparse
import subprocess
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Check:
    """Una verificación de calidad con su comando."""

    name: str
    command: tuple[str, ...]


@dataclass(frozen=True)
class Result:
    """Resultado de una verificación."""

    check: Check
    returncode: int
    output: str

    @property
    def passed(self) -> bool:
        """Indica si la verificación terminó correctamente."""
        return self.returncode == 0


DEFAULT_CHECKS: tuple[Check, ...] = (
    Check("ruff", ("ruff", "check", ".")),
    Check("formato", ("ruff", "format", "--check", ".")),
    Check("tipos", ("ty", "check")),
    Check("pruebas", ("pytest", "-q")),
)


def run_check(check: Check, cwd: Path = REPO_ROOT) -> Result:
    """Ejecuta una verificación y captura su salida."""
    try:
        completed = subprocess.run(
            list(check.command),
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return Result(check=check, returncode=127, output=str(exc))
    output = f"{completed.stdout or ''}{completed.stderr or ''}".strip()
    return Result(check=check, returncode=completed.returncode, output=output)


def run_all(
    checks: Sequence[Check] = DEFAULT_CHECKS,
    runner: Callable[[Check], Result] = run_check,
) -> list[Result]:
    """Ejecuta todas las verificaciones."""
    return [runner(check) for check in checks]


def render_report(results: Sequence[Result]) -> str:
    """Genera el informe legible de la ejecución."""
    lines = ["Informe de calidad", ""]
    for result in results:
        status = "OK" if result.passed else "FALLO"
        lines.append(f"[{status}] {result.check.name} (exit {result.returncode})")
        if not result.passed and result.output:
            lines.append(result.output)
    passed = sum(1 for result in results if result.passed)
    lines.extend(["", f"Resultado: {passed}/{len(results)} verificaciones correctas"])
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    """Ejecuta las verificaciones y devuelve 0 solo si todas pasan."""
    parser = argparse.ArgumentParser(
        prog="calidad",
        description="Ejecuta lint, formato, tipos y pruebas con un informe único.",
    )
    parser.parse_args(argv)
    results = run_all()
    print(render_report(results))
    return 0 if all(result.passed for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
