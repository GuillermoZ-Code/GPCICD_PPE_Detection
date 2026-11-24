"""Validador de specs SDD (HU-096).

Recorre `specs/`, exige `spec.md`, `plan.md` y `tasks.md`, comprueba las secciones
obligatorias y verifica que cada AC declarado tenga evidencia resoluble en su tabla de
aceptación. Las specs anteriores a 092 se validan solo por archivos (deuda histórica);
`--strict` aplica la regla completa a todas.

Uso:
    uv run python -m ppe_detection.tools.check_specs
    uv run python -m ppe_detection.tools.check_specs --check
    uv run python -m ppe_detection.tools.check_specs --strict
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Sequence
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SPECS_DIR = REPO_ROOT / "specs"

SPEC_FILES = ("spec.md", "plan.md", "tasks.md")
SECTIONS = ("## User Scenarios & Testing", "## Requirements", "## Success Criteria")
ACCEPTANCE = "## Acceptance →"
LEGACY_BEFORE = 92

SPEC_NAME = re.compile(r"^(?P<number>\d{3})-")
AC_DECL = re.compile(r"\*\*AC-(\d{1,2})\*\*")
AC_ROW = re.compile(r"^\|\s*AC-(\d{1,2})[^|]*\|(.+?)\|\s*$", re.M)
BACKTICK = re.compile(r"`([^`]+)`")
SECTION_REF = re.compile(r"§|\bTabla\b|\bADR\b|\bSPI\b|\binforme\b|\bAnexo\b")


def spec_dirs(root: Path) -> list[Path]:
    """Carpetas de spec ordenadas por número."""
    directory = root / "specs"
    if not directory.is_dir():
        return []
    return sorted(
        path for path in directory.iterdir() if path.is_dir() and SPEC_NAME.match(path.name)
    )


def spec_number(path: Path) -> int:
    """Número de la spec a partir del prefijo de la carpeta."""
    match = SPEC_NAME.match(path.name)
    return int(match.group("number")) if match else 0


def declared_acs(text: str) -> set[str]:
    """AC declarados en los escenarios de la spec."""
    return {f"AC-{int(number):02d}" for number in AC_DECL.findall(text)}


def acceptance_rows(text: str) -> dict[str, list[str]]:
    """Celdas de la tabla de aceptación, agrupadas por AC."""
    rows: dict[str, list[str]] = {}
    for match in AC_ROW.finditer(text):
        ac = f"AC-{int(match.group(1)):02d}"
        rows.setdefault(ac, []).append(match.group(2))
    return rows


def _test_corpus(root: Path) -> dict[str, str]:
    """Nombre y contenido de los archivos de prueba del backend y del frontend."""
    corpus: dict[str, str] = {}
    for path in (root / "tests").glob("test_*.py"):
        corpus[path.name] = path.read_text(encoding="utf-8")
    frontend = root / "frontend" / "src"
    if frontend.is_dir():
        for path in frontend.rglob("*.test.tsx"):
            corpus[path.name] = path.read_text(encoding="utf-8")
    return corpus


def _function_exists(reference: str, corpus: dict[str, str]) -> bool:
    """True si `archivo::funcion` nombra una función presente en el archivo."""
    if "::" not in reference:
        return True
    function = reference.split("::", 1)[1].strip()
    name = Path(reference.split("::", 1)[0]).name
    text = corpus.get(name, "")
    return bool(re.search(rf"\b{re.escape(function)}\b", text))


def resolves(root: Path, reference: str, corpus: dict[str, str]) -> bool:
    """Resuelve una referencia a prueba, documento o artefacto versionado."""
    raw = reference.split("::")[0].strip()
    name = Path(raw).name
    if raw.startswith("tests/") or (name.startswith("test_") and name.endswith(".py")):
        if name not in corpus:
            return False
        return _function_exists(reference, corpus)
    if name.endswith(".tsx") or name.endswith(".jsx"):
        return name in corpus
    if raw.startswith("docs/") or name.endswith(".md"):
        return (root / raw).is_file()
    if raw.endswith((".py", ".json", ".yml", ".yaml")):
        return (root / raw).is_file()
    return any(name in text for text in corpus.values())


def has_evidence(cell: str) -> bool:
    """True si la celda cita una referencia o una sección de un documento."""
    return bool(BACKTICK.findall(cell)) or bool(SECTION_REF.search(cell))


def _validate_spec(
    root: Path, spec_dir: Path, *, strict: bool, corpus: dict[str, str]
) -> list[str]:
    errors: list[str] = []
    for name in SPEC_FILES:
        if not (spec_dir / name).is_file():
            errors.append(f"{spec_dir.name}: falta {name}")

    spec_path = spec_dir / "spec.md"
    if not strict or not spec_path.is_file():
        return errors

    text = spec_path.read_text(encoding="utf-8")
    for section in SECTIONS:
        if section not in text:
            errors.append(f"{spec_dir.name}: falta la seccion {section!r}")
    if ACCEPTANCE not in text:
        errors.append(f"{spec_dir.name}: falta la seccion {ACCEPTANCE!r}")
        return errors

    rows = acceptance_rows(text)
    for ac in sorted(declared_acs(text)):
        cells = rows.get(ac)
        if not cells:
            errors.append(f"{spec_dir.name}: {ac} sin fila de evidencia")
            continue
        if not any(has_evidence(cell) for cell in cells):
            errors.append(f"{spec_dir.name}: {ac} sin evidencia")
            continue
        for cell in cells:
            for reference in BACKTICK.findall(cell):
                if not resolves(root, reference, corpus):
                    errors.append(
                        f"{spec_dir.name}: {ac} cita una referencia inexistente: {reference}"
                    )
    return errors


def validate(root: Path, *, strict: bool = False, legacy_before: int = LEGACY_BEFORE) -> list[str]:
    """Problemas encontrados en las specs del repositorio."""
    corpus = _test_corpus(root)
    errors: list[str] = []
    for spec_dir in spec_dirs(root):
        full_rule = strict or spec_number(spec_dir) >= legacy_before
        errors.extend(_validate_spec(root, spec_dir, strict=full_rule, corpus=corpus))
    return errors


def build_parser() -> argparse.ArgumentParser:
    """CLI del validador."""
    parser = argparse.ArgumentParser(
        prog="ppe-check-specs",
        description="Valida las specs SDD del repositorio (HU-096).",
    )
    parser.add_argument("--check", action="store_true", help="modo CI: falla con problemas")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="aplica la regla completa tambien a las specs anteriores a 092",
    )
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada."""
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    errors = validate(root, strict=args.strict)
    if errors:
        for error in errors:
            print(f"specs: {error}", file=sys.stderr)
        return 1
    print(f"specs: ok ({len(spec_dirs(root))} specs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
