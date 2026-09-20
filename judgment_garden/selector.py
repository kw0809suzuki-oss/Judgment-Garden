"""Small candidate selector for Judgment Garden.

It chooses the next evidence-producing comparison from explicit candidate
metadata. It does not claim a universal score and does not execute actions.
"""
from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class Candidate:
    name: str
    contradicted: bool
    executable: bool
    missing_cost: int
    expected_space_reduction: int


@dataclass(frozen=True)
class Selection:
    candidate: Optional[Candidate]
    boundary: str


def choose_next(candidates: Iterable[Candidate]) -> Selection:
    pool = [c for c in candidates if not c.contradicted and c.executable]
    if not pool:
        return Selection(None, "no_boundary_safe_executable_candidate")

    # Prefer more candidate-space reduction; use lower missing-cost only as
    # a tie-breaker. This is a local probe rule, not a universal utility score.
    pool.sort(key=lambda c: (-c.expected_space_reduction, c.missing_cost, c.name))
    return Selection(pool[0], "local_probe_choice")
