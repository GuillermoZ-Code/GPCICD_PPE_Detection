"""Estado operativo del proyecto: git, PRs e issues en un solo comando.

Uso:
    uv run python -m ppe_detection.tools.estado           # imprime el estado
    uv run python -m ppe_detection.tools.estado --write   # actualiza ESTADO.md
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
BACKLOG_PATH = REPO_ROOT / "docs" / "curso" / "backlog.md"
ESTADO_PATH = REPO_ROOT / "docs" / "curso" / "ESTADO.md"
GENERATED_START = "<!-- estado:inicio -->"
GENERATED_END = "<!-- estado:fin -->"

HU_HEADING = re.compile(r"^### (HU-\d{3})\b")
HU_IN_TITLE = re.compile(r"HU-(\d{3})")
SP_VALUE = re.compile(r"\*\*SP:\*\*\s*(\d+)")
LINKED_ISSUE = re.compile(r"closes\s+#(\d+)", re.IGNORECASE)

FAILED_STATES = frozenset({"FAILURE", "CANCELLED", "TIMED_OUT", "ACTION_REQUIRED", "ERROR"})
RUNNING_STATES = frozenset({"IN_PROGRESS", "QUEUED", "PENDING", "WAITING", "EXPECTED"})
REVIEW_STATES = {
    "APPROVED": "aprobada",
    "REVIEW_REQUIRED": "pendiente",
    "CHANGES_REQUESTED": "cambios",
}


@dataclass(frozen=True)
class PullRequest:
    """PR abierta y su estado de revisión y CI."""

    number: int
    title: str
    base: str
    review: str
    checks: str
    issue: int | None = None


@dataclass(frozen=True)
class Issue:
    """Issue abierta con su milestone y su estimación."""

    number: int
    title: str
    milestone: str
    sp: int


@dataclass(frozen=True)
class Report:
    """Foto del estado del proyecto en un momento dado."""

    generated_at: datetime
    branch: str
    dirty: int
    ahead: int
    behind: int
    develop: str
    commits: tuple[str, ...]
    prs: tuple[PullRequest, ...]
    issues: tuple[Issue, ...]
    warnings: tuple[str, ...]


def run(command: Sequence[str]) -> str | None:
    """Ejecuta un comando de solo lectura y devuelve su salida o ``None``."""
    try:
        result = subprocess.run(
            list(command),
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def parse_backlog_sp(text: str) -> dict[str, int]:
    """Extrae los SP por HU del backlog espejo."""
    points: dict[str, int] = {}
    current: str | None = None
    for line in text.splitlines():
        heading = HU_HEADING.match(line)
        if heading:
            current = heading.group(1)
            continue
        if current is None or "**SP:**" not in line:
            continue
        match = SP_VALUE.search(line)
        if match:
            points[current] = int(match.group(1))
    return points


def summarize_review(decision: str) -> str:
    """Traduce el estado de revisión de GitHub."""
    if not decision:
        return "—"
    return REVIEW_STATES.get(decision.upper(), decision.lower())


def summarize_checks(rollup: object) -> str:
    """Resume el resultado de las comprobaciones de CI de una PR."""
    if not isinstance(rollup, list):
        return "—"
    states = []
    for item in rollup:
        if not isinstance(item, dict):
            continue
        value = item.get("conclusion") or item.get("state") or ""
        states.append(str(value).upper())
    if not states:
        return "—"
    if any(state in FAILED_STATES for state in states):
        return "fallo"
    if any(state in RUNNING_STATES for state in states):
        return "en curso"
    return "ok"


def _collect_git(warnings: list[str]) -> dict[str, Any]:
    branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"]) or "?"
    status = run(["git", "status", "--porcelain"]) or ""
    dirty = len([line for line in status.splitlines() if line.strip()])
    behind = 0
    ahead = 0
    counts = run(["git", "rev-list", "--left-right", "--count", "origin/develop...HEAD"])
    if counts is None:
        warnings.append("sin `origin/develop`: ejecuta `git fetch` antes de fiarte del estado")
    else:
        parts = counts.split()
        if len(parts) == 2:
            behind, ahead = int(parts[0]), int(parts[1])
    develop = run(["git", "log", "-1", "--format=%h (%cs)", "origin/develop"]) or "?"
    commits = tuple((run(["git", "log", "--oneline", "-5", "HEAD"]) or "").splitlines())
    return {
        "branch": branch,
        "dirty": dirty,
        "ahead": ahead,
        "behind": behind,
        "develop": develop,
        "commits": commits,
    }


def _collect_prs(warnings: list[str]) -> tuple[PullRequest, ...]:
    raw = run(
        [
            "gh",
            "pr",
            "list",
            "--state",
            "open",
            "--limit",
            "30",
            "--json",
            "number,title,body,baseRefName,reviewDecision,statusCheckRollup",
        ]
    )
    if raw is None:
        warnings.append("`gh` no disponible o sin sesión: PRs e issues sin actualizar")
        return ()
    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        warnings.append("`gh pr list` devolvió JSON inválido")
        return ()
    prs = []
    for item in items:
        if not isinstance(item, dict):
            continue
        linked = LINKED_ISSUE.search(str(item.get("body") or ""))
        prs.append(
            PullRequest(
                number=int(item.get("number", 0)),
                title=str(item.get("title", "")),
                base=str(item.get("baseRefName", "")),
                review=summarize_review(str(item.get("reviewDecision") or "")),
                checks=summarize_checks(item.get("statusCheckRollup")),
                issue=int(linked.group(1)) if linked else None,
            )
        )
    return tuple(prs)


def _collect_issues(points: dict[str, int], warnings: list[str]) -> tuple[Issue, ...]:
    raw = run(
        [
            "gh",
            "issue",
            "list",
            "--state",
            "open",
            "--limit",
            "100",
            "--json",
            "number,title,milestone",
        ]
    )
    if raw is None:
        if not warnings:
            warnings.append("`gh` no disponible o sin sesión: issues sin actualizar")
        return ()
    try:
        items = json.loads(raw)
    except json.JSONDecodeError:
        warnings.append("`gh issue list` devolvió JSON inválido")
        return ()
    issues = []
    for item in items:
        if not isinstance(item, dict):
            continue
        milestone = item.get("milestone")
        title = str(item.get("title", ""))
        match = HU_IN_TITLE.search(title)
        issues.append(
            Issue(
                number=int(item.get("number", 0)),
                title=title,
                milestone=str(milestone.get("title") or "sin milestone")
                if isinstance(milestone, dict)
                else "sin milestone",
                sp=points.get(f"HU-{match.group(1)}", 0) if match else 0,
            )
        )
    return tuple(sorted(issues, key=lambda issue: issue.number))


def collect() -> Report:
    """Reúne el estado desde git, GitHub y el backlog."""
    warnings: list[str] = []
    git_state = _collect_git(warnings)
    points = (
        parse_backlog_sp(BACKLOG_PATH.read_text(encoding="utf-8")) if BACKLOG_PATH.exists() else {}
    )
    if not points:
        warnings.append("no se pudieron leer los SP de `docs/curso/backlog.md`")
    prs = _collect_prs(warnings)
    issues = _collect_issues(points, warnings)
    return Report(
        generated_at=datetime.now(UTC),
        branch=str(git_state["branch"]),
        dirty=int(git_state["dirty"]),
        ahead=int(git_state["ahead"]),
        behind=int(git_state["behind"]),
        develop=str(git_state["develop"]),
        commits=tuple(git_state["commits"]),
        prs=prs,
        issues=issues,
        warnings=tuple(warnings),
    )


def _next_issue(report: Report) -> Issue | None:
    linked = {pr.issue for pr in report.prs if pr.issue is not None}
    pending = [issue for issue in report.issues if issue.number not in linked]
    return pending[0] if pending else None


def render(report: Report) -> str:
    """Genera el bloque de estado en Markdown."""
    dirty = "limpia" if report.dirty == 0 else f"{report.dirty} archivo(s) sin commit"
    branch_line = (
        f"**Rama:** `{report.branch}` · {dirty} · "
        f"+{report.ahead}/-{report.behind} vs `origin/develop`"
    )
    lines = [
        f"**Generado:** {report.generated_at.astimezone(UTC).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        branch_line,
        f"**develop:** {report.develop}",
        "",
        "**Últimos commits:**",
    ]
    if report.commits:
        lines.extend(f"- `{commit}`" for commit in report.commits)
    else:
        lines.append("- (sin commits)")

    lines.extend(["", f"**Pull requests abiertas ({len(report.prs)}):**"])
    if report.prs:
        for pr in report.prs:
            lines.append(
                f"- #{pr.number} {pr.title} → `{pr.base}` · revisión: {pr.review} · CI: {pr.checks}"
            )
    else:
        lines.append("- ninguna")

    total = sum(issue.sp for issue in report.issues)
    lines.extend(["", f"**Issues abiertas: {len(report.issues)} · {total} SP**"])
    milestones: dict[str, list[Issue]] = {}
    for issue in report.issues:
        milestones.setdefault(issue.milestone, []).append(issue)
    for name in sorted(milestones):
        group = milestones[name]
        sp = sum(issue.sp for issue in group)
        numbers = " ".join(f"#{issue.number}" for issue in group)
        lines.append(f"- {name} ({sp} SP): {numbers}")

    linked = [f"#{pr.issue} (PR #{pr.number})" for pr in report.prs if pr.issue is not None]
    lines.extend(["", f"**En revisión:** {', '.join(linked) if linked else 'ninguna'}"])

    next_issue = _next_issue(report)
    if next_issue is None:
        lines.append("**Siguiente por orden:** sin issues abiertas")
    else:
        lines.append(f"**Siguiente por orden:** #{next_issue.number} {next_issue.title}")

    if report.warnings:
        lines.extend(["", "**Avisos:**"])
        lines.extend(f"- {warning}" for warning in report.warnings)
    return "\n".join(lines)


def replace_block(document: str, block: str) -> str:
    """Sustituye el bloque generado y conserva la bitácora."""
    start = document.find(GENERATED_START)
    end = document.find(GENERATED_END)
    if start == -1 or end == -1 or end < start:
        raise ValueError("ESTADO.md no tiene los marcadores estado:inicio/estado:fin")
    header = document[: start + len(GENERATED_START)]
    footer = document[end:]
    return f"{header}\n{block}\n{footer}"


def main(argv: Sequence[str] | None = None) -> int:
    """Punto de entrada del comando de estado."""
    parser = argparse.ArgumentParser(
        prog="estado",
        description="Muestra el estado operativo del proyecto y permite guardarlo.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="actualiza el bloque generado de docs/curso/ESTADO.md",
    )
    args = parser.parse_args(argv)

    report = collect()
    text = render(report)
    if not args.write:
        print(text)
        return 0
    if not ESTADO_PATH.exists():
        print(f"No existe {ESTADO_PATH.relative_to(REPO_ROOT)}")
        return 1
    document = ESTADO_PATH.read_text(encoding="utf-8")
    ESTADO_PATH.write_text(replace_block(document, text), encoding="utf-8", newline="\n")
    print(f"Actualizado {ESTADO_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
