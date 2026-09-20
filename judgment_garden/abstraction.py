"""Bounded abstraction over repeated observed outcomes.

This layer may summarize experience. It does not adopt or promote a rule.
"""
from dataclasses import dataclass
from typing import Iterable, Tuple

from .learning import Outcome, OutcomeStatus


@dataclass(frozen=True)
class ExperienceAbstraction:
    probe_name: str
    observed_count: int
    comparable_count: int
    positive_count: int
    negative_count: int
    neutral_count: int
    direction: str
    realization: str
    scope: str
    promote: bool
    reason: str


def abstract_experience(outcomes: Iterable[Outcome]) -> ExperienceAbstraction:
    xs: Tuple[Outcome, ...] = tuple(outcomes)
    if not xs:
        return ExperienceAbstraction(
            probe_name="unknown",
            observed_count=0,
            comparable_count=0,
            positive_count=0,
            negative_count=0,
            neutral_count=0,
            direction="unknown",
            realization="unknown",
            scope="no_experience",
            promote=False,
            reason="no_observed_experience",
        )

    names = {x.probe_name for x in xs}
    probe_name = next(iter(names)) if len(names) == 1 else "mixed"

    observed = tuple(x for x in xs if x.status is OutcomeStatus.OBSERVED)
    comparable = tuple(x for x in observed if x.terminal_self_delta is not None)
    positive = sum(x.terminal_self_delta > 0 for x in comparable)
    negative = sum(x.terminal_self_delta < 0 for x in comparable)
    neutral = sum(x.terminal_self_delta == 0 for x in comparable)

    if not comparable:
        direction = "unknown"
        reason = "goal_metric_missing"
    elif negative == len(comparable):
        direction = "stable_negative_terminal_self"
        reason = "repeated_observed_direction_not_adopted_as_rule"
    elif positive == len(comparable):
        direction = "stable_positive_terminal_self"
        reason = "repeated_observed_direction_not_adopted_as_rule"
    elif neutral == len(comparable):
        direction = "stable_neutral_terminal_self"
        reason = "repeated_observed_direction_not_adopted_as_rule"
    else:
        direction = "mixed_terminal_self"
        reason = "effect_direction_varies_across_experience"

    realization = (
        "observed"
        if len(observed) == len(xs)
        else "partial_or_missing"
    )

    return ExperienceAbstraction(
        probe_name=probe_name,
        observed_count=len(observed),
        comparable_count=len(comparable),
        positive_count=positive,
        negative_count=negative,
        neutral_count=neutral,
        direction=direction,
        realization=realization,
        scope="provided_experience_only",
        promote=False,
        reason=reason,
    )
