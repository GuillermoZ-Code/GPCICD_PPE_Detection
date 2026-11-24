"""Informe de cumplimiento de la rúbrica del M4 (HU-113).

Mantiene la lista de ítems de la rúbrica con su evidencia y responsable, comprueba si la
evidencia existe en el repositorio y genera `docs/entrega/RUBRICA-M4.md` con el estado
✔/✘.

Uso:
    uv run python -m ppe_detection.tools.rubrica --write
    uv run python -m ppe_detection.tools.rubrica --check
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "entrega" / "RUBRICA-M4.md"
CUTOFF = "27/11/2026"


@dataclass(frozen=True)
class RubricItem:
    """Un ítem de la rúbrica con su evidencia y responsable."""

    id: str
    area: str
    criterion: str
    evidence: str
    owner: str


@dataclass(frozen=True)
class ReportRow:
    """Ítem evaluado contra el repositorio."""

    item: RubricItem
    exists: bool


RUBRIC: tuple[RubricItem, ...] = (
    RubricItem(
        "R-01",
        "Pipeline",
        "CI/CD con compuertas de calidad",
        ".github/workflows/ci.yml",
        "Guillermo",
    ),
    RubricItem("R-02", "Contenedor", "Imagen Docker CPU reproducible", "Dockerfile", "Eliana"),
    RubricItem("R-03", "Modelo", "Artefacto versionado por SHA256", "models.lock", "Hernán"),
    RubricItem(
        "R-04", "Modelo", "Informe de evaluación comparativa", "docs/evaluation/YOLO26.md", "Hernán"
    ),
    RubricItem(
        "R-05",
        "Modelo",
        "ADR del modelo productivo",
        "docs/adr/0009-modelo-productivo.md",
        "Hernán",
    ),
    RubricItem(
        "R-06",
        "Trazabilidad",
        "Matriz HU → issue → spec → PR → pruebas",
        "docs/curso/TRAZABILIDAD.md",
        "Jesús",
    ),
    RubricItem(
        "R-07", "Pruebas", "Inventario generado de pruebas", "docs/curso/PRUEBAS.md", "Jesús"
    ),
    RubricItem("R-08", "Backlog", "Espejo 1:1 de las issues", "docs/curso/backlog.md", "Jesús"),
    RubricItem(
        "R-09", "API", "Healthcheck y contrato REST", "src/ppe_detection/api/app.py", "Eliana"
    ),
    RubricItem("R-10", "Interfaz", "SPA React operativa", "frontend/src/App.tsx", "Guillermo"),
    RubricItem("R-11", "Operación", "Runbook de Docker", "docs/operacion/docker.md", "Eliana"),
    RubricItem(
        "R-12", "Documentación", "Mapa de documentación y glosario", "docs/README.md", "Jesús"
    ),
    RubricItem(
        "R-13", "Riesgos", "Registro de riesgos del cierre", "docs/curso/M4/RIESGOS.md", "Jesús"
    ),
    RubricItem("R-14", "Equipo", "Retrospectiva y acciones", "docs/curso/M4/RETRO.md", "Jesús"),
)


def validate_items(items: Sequence[RubricItem]) -> list[str]:
    """Ítems mal formados: sin id, criterio, evidencia o responsable."""
    errors: list[str] = []
    for item in items:
        if not (item.id and item.criterion and item.evidence and item.owner):
            errors.append(f"{item.id or '?'}: falta id, criterio, evidencia o responsable")
    return errors


def build_rows(root: Path, items: Sequence[RubricItem]) -> list[ReportRow]:
    """Evalúa cada ítem contra el repositorio."""
    return [ReportRow(item=item, exists=(root / item.evidence).exists()) for item in items]


def render(rows: Sequence[ReportRow], generated_at: str | None = None) -> str:
    """Genera el Markdown del informe."""
    stamp = generated_at or datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    ok = sum(1 for row in rows if row.exists)
    lines = [
        "# Cumplimiento de la rúbrica — M4",
        "",
        f"> **Generado:** {stamp} · `make rubrica-write`",
        f"> **Ítems:** {len(rows)} · cumplidos: {ok} · pendientes: {len(rows) - ok}",
        f"> **Fecha de corte:** {CUTOFF}",
        "",
        "| ID | Área | Criterio | Evidencia | Responsable | Estado |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        mark = "✔" if row.exists else "✘"
        lines.append(
            f"| {row.item.id} | {row.item.area} | {row.item.criterion} | "
            f"`{row.item.evidence}` | {row.item.owner} | {mark} |"
        )
    lines.extend(
        [
            "",
            "## Criterio",
            "",
            "- ✔: la evidencia existe en el repositorio.",
            f"- ✘: falta o está pendiente; la HU responsable la completa antes del {CUTOFF}.",
            "- El informe se regenera con `make rubrica-write`; no se edita a mano.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(path: Path, content: str) -> Path:
    """Escribe el informe en UTF-8 con salto final."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content if content.endswith("\n") else f"{content}\n", encoding="utf-8")
    return path


def build_parser() -> argparse.ArgumentParser:
    """CLI del informe."""
    parser = argparse.ArgumentParser(
        prog="ppe-rubrica",
        description="Genera y valida el informe de la rubrica del M4 (HU-113).",
    )
    parser.add_argument("--write", action="store_true", help="regenera RUBRICA-M4.md")
    parser.add_argument("--check", action="store_true", help="valida los items de la rubrica")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--generated-at", default=None, help=argparse.SUPPRESS)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada."""
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    errors = validate_items(RUBRIC)
    if errors:
        for error in errors:
            print(f"rubrica: {error}", file=sys.stderr)
        return 1
    rows = build_rows(root, RUBRIC)
    report = render(rows, generated_at=args.generated_at)
    if args.check:
        ok = sum(1 for row in rows if row.exists)
        print(f"rubrica: ok ({len(rows)} items, {ok} con evidencia)")
        return 0
    if args.write:
        target = args.output or (root / "docs" / "entrega" / "RUBRICA-M4.md")
        write_report(target, report)
        print(f"rubrica: escrito {target}")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
