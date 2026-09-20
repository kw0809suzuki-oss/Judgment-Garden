"""Bounded candidate generation for Judgment Garden.

Generation is free inside an explicit DirectionSpace; promotion remains
controlled. No runtime action is executed here.
"""
from dataclasses import dataclass
from typing import Tuple

from .selector import Candidate


@dataclass(frozen=True)
class DirectionSpace:
    closure_active: bool
    hire_observed: bool
    harvestable: bool
    allow_control: bool = True
    allow_hire_suppression: bool = True
    allow_early_harvest: bool = True


def generate_candidates(space: DirectionSpace) -> Tuple[Candidate, ...]:
    out = []

    if space.allow_control:
        out.append(Candidate(
            name="closure_only",
            contradicted=False,
            executable=True,
            missing_cost=0,
            expected_space_reduction=0,
        ))

    if space.allow_hire_suppression and space.closure_active and space.hire_observed:
        out.append(Candidate(
            name="hire_stop_only",
            contradicted=False,
            executable=True,
            missing_cost=1,
            expected_space_reduction=1,
        ))

    if space.allow_early_harvest and space.closure_active and space.harvestable:
        out.append(Candidate(
            name="early_harvest_only",
            contradicted=False,
            executable=True,
            missing_cost=1,
            expected_space_reduction=1,
        ))

    return tuple(out)
