"""Matriz de trazabilidad HU → issue → spec → PR → pruebas (HU-093).

Genera `docs/curso/TRAZABILIDAD.md` a partir de GitHub (`gh`), de `specs/` y de las
referencias `HU-NNN` en las pruebas. La compuerta `--check` falla si una HU cerrada no
tiene spec o pruebas, salvo las exenciones documentales declaradas abajo.

Uso:
    uv run python -m ppe_detection.tools.trazabilidad
    uv run python -m ppe_detection.tools.trazabilidad --write
    uv run python -m ppe_detection.tools.trazabilidad --check
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "curso" / "TRAZABILIDAD.md"

HU = re.compile(r"HU-(\d{3})")
SPEC_DIR = re.compile(r"^\d{3}-hu-(\d{3})-")
SPEC_TEST = re.compile(r"`([^`]*test[^`]*\.(?:py|tsx))`")
CLOSES = re.compile(r"closes\s+#(\d+)", re.IGNORECASE)
BRANCH_HU = re.compile(r"hu-(\d{3})")

#: HU cerradas que no llevan pruebas unitarias por naturaleza, con su motivo.
EXEMPTIONS = {
    "HU-016": "spike documental (SPI)",
    "HU-018": "entrenamiento en GPU; sin pruebas unitarias",
    "HU-019": "informe de evaluación; evidencia documental",
    "HU-023": "ADR; decisión documental",
    "HU-089": "creación de issues; entregable en GitHub",
}


@dataclass(frozen=True)
class TraceRow:
    """Una fila de la matriz."""

    hu: str
    issue: int | None
    state: str
    spec: str | None
    prs: tuple[int, ...]
    tests: tuple[str, ...]

    @property
    def missing(self) -> tuple[str, ...]:
        """Columnas que faltan para la trazabilidad completa."""
        problems: list[str] = []
        if not self.spec:
            problems.append("spec")
        if not self.prs:
            problems.append("pr")
        if not self.tests:
            problems.append("pruebas")
        return tuple(problems)


def parse_issues(payload: str) -> dict[str, dict[str, Any]]:
    """Convierte el JSON de `gh issue list` en un mapa HU → número y estado."""
    issues: dict[str, dict[str, Any]] = {}
    data = json.loads(payload)
    if not isinstance(data, list):
        raise ValueError("gh issue list debe devolver una lista")
    for issue in data:
        if not isinstance(issue, dict):
            continue
        match = HU.search(str(issue.get("title", "")))
        if match:
            issues[f"HU-{match.group(1)}"] = {
                "number": issue["number"],
                "state": issue["state"],
            }
    return issues


def specs_by_hu(root: Path) -> dict[str, str]:
    """Carpetas `specs/NNN-hu-NNN-slug` indexadas por HU."""
    specs: dict[str, str] = {}
    directory = root / "specs"
    if not directory.is_dir():
        return specs
    for path in sorted(directory.iterdir()):
        match = SPEC_DIR.match(path.name)
        if match and path.is_dir():
            specs[f"HU-{match.group(1)}"] = path.name
    return specs


def _module_mentions(path: Path) -> set[str]:
    """HU mencionadas en el encabezado del archivo (docstring o comentarios)."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        try:
            header = ast.get_docstring(ast.parse(text)) or ""
        except SyntaxError:
            return set()
    else:
        header = text.split("import", 1)[0]
    return {f"HU-{match.group(1)}" for match in HU.finditer(header)}


def tests_by_hu(root: Path) -> dict[str, set[str]]:
    """Archivos de prueba cuyo encabezado menciona `HU-NNN` (pytest y Vitest)."""
    tests: dict[str, set[str]] = {}
    for path in sorted((root / "tests").glob("test_*.py")):
        for hu in _module_mentions(path):
            tests.setdefault(hu, set()).add(f"tests/{path.name}")
    frontend = root / "frontend" / "src"
    if frontend.is_dir():
        for path in sorted(frontend.rglob("*.test.tsx")):
            for hu in _module_mentions(path):
                tests.setdefault(hu, set()).add(path.name)
    return tests


def spec_tests(root: Path, specs: dict[str, str]) -> dict[str, set[str]]:
    """Archivos citados en la tabla de aceptación de cada `spec.md`."""
    cited: dict[str, set[str]] = {}
    for hu, name in specs.items():
        spec_path = root / "specs" / name / "spec.md"
        if not spec_path.is_file():
            continue
        files = {
            Path(match.split("::")[0]).name
            for match in SPEC_TEST.findall(spec_path.read_text(encoding="utf-8"))
        }
        if files:
            cited[hu] = files
    return cited


def prs_by_hu(prs: list[dict[str, Any]], issue_to_hu: dict[int, str]) -> dict[str, set[int]]:
    """PRs fusionadas enlazadas por `Closes #N`, título o slug de la rama."""
    linked: dict[str, set[int]] = {}
    for pr in prs:
        hus: set[str] = set()
        number = int(pr["number"])
        body = str(pr.get("body") or "")
        for match in CLOSES.finditer(body):
            hu = issue_to_hu.get(int(match.group(1)))
            if hu:
                hus.add(hu)
        title = str(pr.get("title") or "")
        hus.update(f"HU-{match.group(1)}" for match in HU.finditer(title))
        branch = BRANCH_HU.search(str(pr.get("headRefName") or ""))
        if branch:
            hus.add(f"HU-{branch.group(1)}")
        for hu in hus:
            linked.setdefault(hu, set()).add(number)
    return linked


def build_rows(
    issues: dict[str, dict[str, Any]],
    specs: dict[str, str],
    tests: dict[str, set[str]],
    prs: dict[str, set[int]],
) -> list[TraceRow]:
    """Combina las fuentes en filas ordenadas por HU."""
    rows: list[TraceRow] = []
    for hu in sorted(issues):
        issue = issues[hu]
        state = "cerrada" if issue["state"] == "CLOSED" else "abierta"
        rows.append(
            TraceRow(
                hu=hu,
                issue=int(issue["number"]),
                state=state,
                spec=specs.get(hu),
                prs=tuple(sorted(prs.get(hu, set()))),
                tests=tuple(sorted(tests.get(hu, set()))),
            )
        )
    return rows


def check(rows: list[TraceRow], exemptions: dict[str, str]) -> list[str]:
    """HU cerradas sin spec o pruebas, fuera de las exenciones."""
    failures: list[str] = []
    for row in rows:
        if row.state != "cerrada" or row.hu in exemptions:
            continue
        missing = [item for item in row.missing if item in {"spec", "pruebas"}]
        if missing:
            failures.append(f"{row.hu}: falta {', '.join(missing)}")
    return failures


def render(rows: list[TraceRow], generated_at: str | None = None) -> str:
    """Genera el Markdown de la matriz."""
    stamp = generated_at or datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    complete = sum(1 for row in rows if not row.missing)
    lines = [
        "# Matriz de trazabilidad — GPCICD PPE Detection",
        "",
        f"> **Generado:** {stamp} · `make trazabilidad-write`",
        f"> **HU:** {len(rows)} · completas: {complete} · incompletas: {len(rows) - complete}",
        "> **Fuente:** GitHub Issues y PRs, `specs/` y referencias `HU-NNN` en las pruebas.",
        "> **Exenciones:** " + ", ".join(f"{hu} ({reason})" for hu, reason in EXEMPTIONS.items()),
        "",
        "| HU | Issue | Estado | Spec | PR | Pruebas | Falta |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        issue = f"[#{row.issue}](../../issues/{row.issue})" if row.issue else "—"
        spec = f"[{row.spec}](../../specs/{row.spec}/)" if row.spec else "—"
        prs = ", ".join(f"[#{number}](../../pull/{number})" for number in row.prs) or "—"
        tests = ", ".join(f"`{name}`" for name in row.tests) or "—"
        missing = ", ".join(row.missing) or "—"
        lines.append(f"| {row.hu} | {issue} | {row.state} | {spec} | {prs} | {tests} | {missing} |")
    lines.extend(
        [
            "",
            "## Cómo se actualiza",
            "",
            "```bash",
            "make trazabilidad        # imprime la matriz",
            "make trazabilidad-write  # regenera este archivo",
            "make trazabilidad-check  # compuerta de CI",
            "```",
            "",
            "No se edita a mano. La compuerta falla si una HU cerrada no tiene spec o",
            "pruebas; las exenciones documentales se declaran en el módulo con su motivo.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(path: Path, content: str) -> Path:
    """Escribe la matriz en UTF-8 con salto final."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if content.endswith("\n") else f"{content}\n", encoding="utf-8")
    return path


def _gh_json(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", check=False
    )
    if result.returncode != 0:
        raise SystemExit(f"trazabilidad: gh fallo\n{result.stderr.strip()}")
    return result.stdout


def load_issues() -> dict[str, dict[str, Any]]:
    """Issues del repositorio, abiertas y cerradas."""
    payload = _gh_json(
        "issue", "list", "--state", "all", "--limit", "400", "--json", "number,title,state"
    )
    return parse_issues(payload)


def load_prs() -> list[dict[str, Any]]:
    """PRs fusionadas del repositorio."""
    payload = _gh_json(
        "pr",
        "list",
        "--state",
        "merged",
        "--limit",
        "400",
        "--json",
        "number,title,body,headRefName",
    )
    data = json.loads(payload)
    return [item for item in data if isinstance(item, dict)]


def build_parser() -> argparse.ArgumentParser:
    """CLI de la matriz."""
    parser = argparse.ArgumentParser(
        prog="ppe-trazabilidad",
        description="Genera y valida la matriz HU → issue → spec → PR → pruebas (HU-093).",
    )
    parser.add_argument("--write", action="store_true", help="regenera TRAZABILIDAD.md")
    parser.add_argument(
        "--check",
        action="store_true",
        help="falla si una HU cerrada esta incompleta",
    )
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--generated-at", default=None, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada."""
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    issues = load_issues()
    issue_to_hu = {int(issue["number"]): hu for hu, issue in issues.items()}
    specs = specs_by_hu(root)
    tests = tests_by_hu(root)
    for hu, files in spec_tests(root, specs).items():
        tests.setdefault(hu, set()).update(files)
    rows = build_rows(issues, specs, tests, prs_by_hu(load_prs(), issue_to_hu))

    if args.check:
        failures = check(rows, EXEMPTIONS)
        if failures:
            for failure in failures:
                print(f"trazabilidad: {failure}", file=sys.stderr)
            return 1
        print(f"trazabilidad: ok ({len(rows)} HU)")
        return 0

    report = render(rows, generated_at=args.generated_at)
    if args.write:
        target = args.output or (root / "docs" / "curso" / "TRAZABILIDAD.md")
        write_report(target, report)
        print(f"trazabilidad: escrito {target}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
