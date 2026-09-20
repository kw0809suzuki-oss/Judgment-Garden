"""Return bounded experience abstractions to candidate generation.

Experience may change local probe priority without promoting a permanent rule.
"""
from dataclasses import replace
from typing import Iterable, Tuple

from .abstraction import ExperienceAbstraction
from .selector import Candidate


def return_experience(
    candidates: Iterable[Candidate],
    abstractions: Iterable[ExperienceAbstraction],
) -> Tuple[Candidate, ...]:
    by_probe = {a.probe_name: a for a in abstractions}
    out = []

    for candidate in candidates:
        abstraction = by_probe.get(candidate.name)
        if (
            abstraction is not None
            and abstraction.direction == "stable_negative_terminal_self"
            and abstraction.realization == "observed"
            and abstraction.comparable_count > 0
        ):
            # Do not delete, contradict, or adopt a rule. The experienced probe
            # remains available but no longer gets information-gain priority
            # over an untried direction in this local selection cycle.
            out.append(replace(candidate, expected_space_reduction=0))
        else:
            out.append(candidate)

    return tuple(out)
