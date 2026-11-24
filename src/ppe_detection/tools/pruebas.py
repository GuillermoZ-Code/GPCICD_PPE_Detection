"""Conteo reproducible de pruebas (HU-094).

Cuenta los casos recolectados por pytest y por Vitest, resuelve el dueno de cada
archivo con `docs/curso/propiedad.toml` y genera `docs/curso/PRUEBAS.md`.

Uso:
    uv run python -m ppe_detection.tools.pruebas
    uv run python -m ppe_detection.tools.pruebas --write
    uv run python -m ppe_detection.tools.pruebas --skip-frontend
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ppe_detection.tools import ownership

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "curso" / "PRUEBAS.md"

_PYTEST_FILE_LINE = re.compile(r"^(?P<path>[^\s:]+\.py):\s*(?P<count>\d+)\s*$")
_PYTEST_ID_LINE = re.compile(r"^(?P<path>[^\s:]+\.py)::(?P<test>\S+)\s*$")
_FRONTEND_MARKER = "frontend/"
UNOWNED = "sin dueño"


@dataclass(frozen=True)
class ReportRow:
    """Una fila del informe: archivo, suite, pruebas y dueno visible."""

    path: str
    suite: str
    count: int
    owner: str


def count_pytest(output: str) -> dict[str, int]:
    """Cuenta casos por archivo a partir de la salida de `pytest --collect-only`."""
    counts: dict[str, int] = {}
    for line in output.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        file_match = _PYTEST_FILE_LINE.match(stripped)
        if file_match:
            counts[file_match["path"]] = int(file_match["count"])
            continue
        id_match = _PYTEST_ID_LINE.match(stripped)
        if id_match:
            path = id_match["path"]
            counts[path] = counts.get(path, 0) + 1
    return counts


def count_vitest(output: str) -> dict[str, int]:
    """Cuenta casos por archivo a partir de `vitest list --json`."""
    data = json.loads(output)
    if not isinstance(data, list):
        raise ValueError("vitest list --json debe devolver una lista")
    counts: dict[str, int] = {}
    for item in data:
        if not isinstance(item, dict):
            raise ValueError(f"caso de Vitest invalido: {item!r}")
        raw = item.get("file")
        if not isinstance(raw, str):
            raise ValueError(f"caso de Vitest sin archivo: {item!r}")
        path = _relative_frontend(raw)
        counts[path] = counts.get(path, 0) + 1
    return counts


def _relative_frontend(path: str) -> str:
    """Normaliza rutas absolutas de Windows a `frontend/...`."""
    normalized = path.replace("\\", "/")
    index = normalized.rfind(_FRONTEND_MARKER)
    return normalized[index:] if index != -1 else normalized


def build_rows(
    pytest_counts: dict[str, int],
    vitest_counts: dict[str, int],
    manifest: ownership.Manifest,
) -> list[ReportRow]:
    """Combina los conteos y resuelve el dueno de cada archivo."""
    rows: list[ReportRow] = []
    for suite, counts in (("pytest", pytest_counts), ("vitest", vitest_counts)):
        for path, count in sorted(counts.items()):
            login = ownership.owner_of(path, manifest)
            owner = manifest.names.get(login, login) if login else UNOWNED
            rows.append(ReportRow(path=path, suite=suite, count=count, owner=owner))
    return rows


def render_report(rows: list[ReportRow], generated_at: str | None = None) -> str:
    """Genera el Markdown del inventario."""
    stamp = generated_at or datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    pytest_rows = [row for row in rows if row.suite == "pytest"]
    vitest_rows = [row for row in rows if row.suite == "vitest"]
    pytest_total = sum(row.count for row in pytest_rows)
    vitest_total = sum(row.count for row in vitest_rows)

    lines = [
        "# Inventario de pruebas — GPCICD PPE Detection",
        "",
        f"> **Generado:** {stamp} · `make pruebas`",
        "> **Requisito del curso:** ≥ 400 pruebas unitarias (mínimo, no techo).",
        "> **Fuente:** casos recolectados por pytest y por Vitest; no se edita a mano.",
        "",
        "## 1. Resumen",
        "",
        "| Suite | Herramienta | Archivos | Pruebas | Comando |",
        "|-------|-------------|---------:|--------:|---------|",
        f"| Backend | pytest | {len(pytest_rows)} | {pytest_total} | `make test` |",
        f"| Frontend | Vitest | {len(vitest_rows)} | {vitest_total} | `make frontend-test` |",
        f"| **Total** | | **{len(rows)}** | **{pytest_total + vitest_total}** | "
        "`make check` + `make frontend-check` |",
        "",
        "## 2. Desglose por archivo",
        "",
        "| Archivo | Suite | Pruebas | Dueño |",
        "|---|---|---:|---|",
    ]
    lines.extend(f"| {row.path} | {row.suite} | {row.count} | {row.owner} |" for row in rows)
    lines.extend(
        [
            "",
            "## 3. Totales por integrante",
            "",
            "| Integrante | pytest | Vitest | Total |",
            "|---|---:|---:|---:|",
        ]
    )
    totals: dict[str, list[int]] = {}
    for row in rows:
        bucket = totals.setdefault(row.owner, [0, 0])
        bucket[0 if row.suite == "pytest" else 1] += row.count
    for owner in sorted(totals):
        backend, frontend = totals[owner]
        lines.append(f"| {owner} | {backend} | {frontend} | {backend + frontend} |")
    lines.extend(
        [
            "",
            "## 4. Cómo se actualiza",
            "",
            "```bash",
            "make pruebas        # imprime el resumen",
            "make pruebas-write  # regenera este archivo",
            "```",
            "",
            "El dueño de `docs/curso/PRUEBAS.md` lo regenera y lo commitea. El plan",
            "hacia 1.200 pruebas vive en `docs/curso/PLAN-PRUEBAS.md`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(path: Path, content: str) -> Path:
    """Escribe el informe en UTF-8 con salto de linea final."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if content.endswith("\n") else f"{content}\n", encoding="utf-8")
    return path


def collect_pytest(root: Path) -> dict[str, int]:
    """Lanza `pytest --collect-only` y devuelve el conteo por archivo."""
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "-q"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"pruebas: pytest fallo al recolectar\n{result.stderr.strip()}")
    return count_pytest(result.stdout)


def collect_vitest(root: Path) -> dict[str, int]:
    """Lanza `vitest list --json` y devuelve el conteo por archivo."""
    npx = shutil.which("npx")
    if npx is None:
        raise SystemExit("pruebas: no se encontro npx; instala Node o usa --skip-frontend")
    result = subprocess.run(
        [npx, "vitest", "list", "--json"],
        cwd=root / "frontend",
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"pruebas: vitest fallo al listar\n{result.stderr.strip()}")
    output = result.stdout
    start = output.find("[")
    if start == -1:
        raise SystemExit("pruebas: vitest no devolvio JSON")
    return count_vitest(output[start:])


def build_parser() -> argparse.ArgumentParser:
    """CLI del contador."""
    parser = argparse.ArgumentParser(
        prog="ppe-pruebas",
        description="Cuenta pruebas de pytest y Vitest y genera PRUEBAS.md (HU-094).",
    )
    parser.add_argument("--write", action="store_true", help="regenera PRUEBAS.md")
    parser.add_argument("--skip-frontend", action="store_true", help="cuenta solo pytest")
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help="raiz del repositorio")
    parser.add_argument("--output", type=Path, default=None, help="ruta del informe")
    parser.add_argument("--generated-at", default=None, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada del comando."""
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    pytest_counts = collect_pytest(root)
    vitest_counts = {} if args.skip_frontend else collect_vitest(root)
    manifest = ownership.load_manifest(root / "docs" / "curso" / "propiedad.toml")
    rows = build_rows(pytest_counts, vitest_counts, manifest)

    print(f"pytest: {sum(pytest_counts.values())} en {len(pytest_counts)} archivos")
    print(f"vitest: {sum(vitest_counts.values())} en {len(vitest_counts)} archivos")
    print(f"total:  {sum(row.count for row in rows)} en {len(rows)} archivos")

    report = render_report(rows, generated_at=args.generated_at)
    if args.write:
        target = args.output or (root / "docs" / "curso" / "PRUEBAS.md")
        write_report(target, report)
        print(f"pruebas: escrito {target}")
    else:
        print()
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
