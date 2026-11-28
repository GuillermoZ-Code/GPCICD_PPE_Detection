"""Compuerta de propiedad de archivos (HU-082).

Compara los archivos que toca una rama con el manifiesto
`docs/curso/propiedad.toml` y decide si el autor puede escribirlos.

Reglas:
    1. Archivo en `[[locked]]` con otro dueño  -> FALLA (código 1).
    2. Archivo con otro dueño en `[[owner]]`  -> ADVERTENCIA (no falla).
    3. Sin dueño declarado                    -> libre.

La advertencia existe porque la revisión ya la pide CODEOWNERS: bloquear
todo archivo ajeno convertiría cada HU cruzada en un cuello de botella.

Uso:
    uv run python -m ppe_detection.tools.ownership --base origin/develop
    uv run python -m ppe_detection.tools.ownership --base origin/develop --author ElianaCardona
    uv run python -m ppe_detection.tools.ownership --write-codeowners
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPO_ROOT / "docs" / "curso" / "propiedad.toml"
CODEOWNERS_PATH = REPO_ROOT / ".github" / "CODEOWNERS"
DEFAULT_BASE = "origin/develop"


@dataclass(frozen=True)
class Manifest:
    """Manifiesto leído: dueños por patrón y archivos bloqueados."""

    owners: dict[str, tuple[str, ...]] = field(default_factory=dict)
    locked: dict[str, str] = field(default_factory=dict)
    names: dict[str, str] = field(default_factory=dict)

    def patterns(self) -> list[tuple[str, str]]:
        """Pares (patrón, dueño) de todas las rutas declaradas."""
        pairs: list[tuple[str, str]] = []
        for owner, patterns in self.owners.items():
            pairs.extend((pattern, owner) for pattern in patterns)
        pairs.extend(self.locked.items())
        return pairs


def load_manifest(path: Path | None = None) -> Manifest:
    """Lee el manifiesto TOML y devuelve sus dueños y bloqueos."""
    import tomllib

    manifest_path = path or MANIFEST_PATH
    with manifest_path.open("rb") as handle:
        data = tomllib.load(handle)

    owners: dict[str, tuple[str, ...]] = {}
    names: dict[str, str] = {}
    for entry in data.get("owner", []):
        github = entry["github"]
        owners[github] = tuple(entry.get("paths", ()))
        names[github] = entry.get("nombre", github)

    locked: dict[str, str] = {}
    for entry in data.get("locked", []):
        locked[entry["path"]] = entry["owner"]

    if not owners:
        raise ValueError(f"{manifest_path} no declara ningún dueño en [[owner]]")
    return Manifest(owners=owners, locked=locked, names=names)


def specificity(pattern: str) -> tuple[int, int, int]:
    """Clave de especificidad: más carpetas y menos comodines gana."""
    depth = pattern.count("/")
    literals = sum(1 for char in pattern if char not in "*?[")
    return (depth, literals, len(pattern))


def matches(path: str, pattern: str) -> bool:
    """True si la ruta cae dentro del patrón (globo o carpeta)."""
    if pattern.endswith("/"):
        return path.startswith(pattern)
    return path == pattern or fnmatch(path, pattern)


def owner_of(path: str, manifest: Manifest) -> str | None:
    """Dueño de una ruta según `[[owner]]`, o None si no está declarada."""
    best: str | None = None
    best_key: tuple[int, int, int] | None = None
    for candidate, patterns in manifest.owners.items():
        for pattern in patterns:
            if matches(path, pattern):
                key = specificity(pattern)
                if best_key is None or key > best_key:
                    best, best_key = candidate, key
    return best


def lock_of(path: str, manifest: Manifest) -> str | None:
    """Dueño del archivo si está en `[[locked]]`, o None."""
    locked = [
        (pattern, owner) for pattern, owner in manifest.locked.items() if matches(path, pattern)
    ]
    if not locked:
        return None
    return max(locked, key=lambda pair: specificity(pair[0]))[1]


@dataclass
class Report:
    """Resultado de evaluar un conjunto de rutas."""

    blocked: list[tuple[str, str]] = field(default_factory=list)
    foreign: list[tuple[str, str]] = field(default_factory=list)
    unowned: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True si ningún archivo bloqueado pertenece a otro."""
        return not self.blocked


def evaluate(paths: list[str], author: str | None, manifest: Manifest) -> Report:
    """Clasifica las rutas tocadas frente al manifiesto."""
    report = Report()
    for path in paths:
        locked_owner = lock_of(path, manifest)
        if locked_owner is not None and author and locked_owner != author:
            report.blocked.append((path, locked_owner))
            continue
        owner = owner_of(path, manifest)
        if owner is None:
            report.unowned.append(path)
        elif author and owner != author:
            report.foreign.append((path, owner))
    return report


def changed_files(base: str, root: Path | None = None) -> list[str]:
    """Rutas modificadas, añadidas o renombradas frente a `base`."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
        cwd=root or REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or f"no se pudo comparar con {base}"
        raise SystemExit(f"ownership: {message}")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def render_codeowners(manifest: Manifest) -> str:
    """Genera el contenido de `.github/CODEOWNERS` desde el manifiesto."""
    lines = [
        "# Generado por `make codeowners` desde docs/curso/propiedad.toml.",
        "# No editar a mano: se sobrescribe.",
        "",
    ]
    unique: dict[str, str] = {}
    for pattern, owner in manifest.patterns():
        unique.setdefault(pattern, owner)
    for pattern, owner in sorted(unique.items(), key=lambda pair: specificity(pair[0])):
        lines.append(f"{pattern} @{owner}")
    return "\n".join(lines) + "\n"


def write_codeowners(manifest: Manifest, path: Path | None = None) -> Path:
    """Escribe CODEOWNERS y devuelve la ruta usada."""
    target = path or CODEOWNERS_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_codeowners(manifest), encoding="utf-8")
    return target


def build_parser() -> argparse.ArgumentParser:
    """CLI de la compuerta."""
    parser = argparse.ArgumentParser(prog="ownership", description=__doc__)
    parser.add_argument("--base", default=DEFAULT_BASE, help="referencia contra la que comparar")
    parser.add_argument("--author", help="usuario de GitHub que firma el cambio")
    parser.add_argument("--manifest", type=Path, help="ruta alternativa al manifiesto")
    parser.add_argument("--write-codeowners", action="store_true", help="regenera CODEOWNERS")
    parser.add_argument("--quiet", action="store_true", help="no imprime rutas libres")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Punto de entrada; devuelve 1 si toca un archivo bloqueado ajeno."""
    args = build_parser().parse_args(argv)
    manifest = load_manifest(args.manifest)

    if args.write_codeowners:
        target = write_codeowners(manifest)
        print(f"CODEOWNERS escrito en {target.relative_to(REPO_ROOT)}")
        return 0

    paths = changed_files(args.base)
    report = evaluate(paths, args.author, manifest)

    for path, owner in report.blocked:
        print(f"BLOQUEADO  {path}  pertenece a @{owner}")
    for path, owner in report.foreign:
        print(f"aviso      {path}  revisa @{owner}")
    if not args.quiet:
        for path in report.unowned:
            print(f"libre      {path}")

    if report.blocked:
        print(
            "\nownership: hay archivos de un solo escritor en el cambio.\n"
            "Pide el cambio a su dueño o abre un issue; no lo edites en esta rama.",
            file=sys.stderr,
        )
        return 1

    print(f"ownership: ok ({len(paths)} archivos, {len(report.foreign)} con aviso)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
