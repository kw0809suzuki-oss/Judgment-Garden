"""Experience feedback for Judgment Garden candidate selection.

An abstraction may alter the next local probe choice without promoting a
general rule. Stable negative experience makes repeating the same probe
contradicted only inside the supplied experience scope.
"""
from dataclasses import replace
from typing import Iterable, Tuple

from .abstraction import ExperienceAbstraction
from .selector import Candidate


def return_experience(
    candidates: Iterable[Candidate],
    abstraction: ExperienceAbstraction,
) -> Tuple[Candidate, ...]:
    out = []
    for candidate in candidates:
        if (
            candidate.name == abstraction.probe_name
            and abstraction.realization == "observed"
            and abstraction.direction == "stable_negative_terminal_self"
        ):
            out.append(replace(candidate, contradicted=True))
        else:
            out.append(candidate)
    return tuple(out)
