"""Burndown y velocidad del sprint a partir de las HUs cerradas (HU-103/HU-109).

El módulo es puro: recibe la lista de cierres (día, SP y dueño) y devuelve la serie
del burndown, la velocidad por integrante y la desviación frente al plan. La entrada
real se exporta del tablero; las pruebas usan datos simulados.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date


class SprintError(ValueError):
    """Los datos del sprint no son coherentes."""


@dataclass(frozen=True, slots=True)
class Closed:
    """Una HU cerrada: día del cierre, SP y dueño."""

    day: date
    sp: int
    owner: str | None = None


@dataclass(frozen=True, slots=True)
class Point:
    """Punto del burndown: SP cerrados ese día y SP restantes."""

    day: date
    closed_sp: int
    remaining_sp: int


def burndown(closed: Iterable[Closed], total_sp: int) -> list[Point]:
    """Serie de SP restantes por día, ordenada y sin negativos.

    Args:
        closed: cierres del sprint; se agrupan por día.
        total_sp: SP comprometidos al inicio del sprint.

    Returns:
        Un punto por cada día con cierres, en orden cronológico.

    Raises:
        SprintError: si el total no es positivo, un SP no es positivo o los cierres
            superan el total.
    """
    if total_sp <= 0:
        raise SprintError("total_sp debe ser positivo")
    per_day: dict[date, int] = {}
    for item in closed:
        if item.sp <= 0:
            raise SprintError(f"SP inválido para {item.day}: {item.sp}")
        per_day[item.day] = per_day.get(item.day, 0) + item.sp
    if sum(per_day.values()) > total_sp:
        raise SprintError("los cierres superan el total comprometido")
    remaining = total_sp
    points: list[Point] = []
    for day in sorted(per_day):
        remaining -= per_day[day]
        points.append(Point(day=day, closed_sp=per_day[day], remaining_sp=remaining))
    return points


def velocity_by_person(closed: Iterable[Closed]) -> dict[str, int]:
    """SP cerrados por integrante, en orden alfabético."""
    totals: dict[str, int] = {}
    for item in closed:
        if item.owner is None:
            continue
        totals[item.owner] = totals.get(item.owner, 0) + item.sp
    return dict(sorted(totals.items()))


def deviation(planned: int, delivered: int) -> float:
    """Desviación porcentual de lo entregado frente a lo planificado."""
    if planned <= 0:
        raise SprintError("planned debe ser positivo")
    return round((delivered - planned) / planned * 100, 1)


def capacity(delivered_sp: int, people: int, days: int) -> float:
    """SP entregados por persona y día (capacidad real del equipo)."""
    if people <= 0 or days <= 0:
        raise SprintError("people y days deben ser positivos")
    return round(delivered_sp / (people * days), 2)


__all__ = [
    "Closed",
    "Point",
    "SprintError",
    "burndown",
    "capacity",
    "deviation",
    "velocity_by_person",
]
