"""Bounded external stimulus for Judgment Garden.

A stimulus is material, not a rule. It may open a question in candidate space
without asserting that the observed pattern transfers to strategy.
"""
from dataclasses import dataclass
from typing import Iterable, Tuple

from .selector import Candidate


@dataclass(frozen=True)
class Stimulus:
    stimulus_id: str
    observed_difference: str
    known: str
    unknown: str
    boundary: str
    status: str = "MATERIAL"


@dataclass(frozen=True)
class StimulusQuestion:
    name: str
    source_id: str
    executable: bool
    reason: str


def ingest_stimulus(stimuli: Iterable[Stimulus]) -> Tuple[StimulusQuestion, ...]:
    out = []
    for stimulus in stimuli:
        if stimulus.status != "MATERIAL":
            continue
        # STIMULUS 001 contains a freshness difference. We do not transfer it
        # as a tactic. We only expose the unresolved question it creates.
        if "premise" in stimulus.observed_difference.lower() and "stale" in stimulus.observed_difference.lower():
            out.append(StimulusQuestion(
                name="strategy_premise_freshness",
                source_id=stimulus.stimulus_id,
                executable=False,
                reason="external_difference_opens_question_not_strategy",
            ))
    return tuple(out)


def extend_candidate_space(
    candidates: Iterable[Candidate],
    questions: Iterable[StimulusQuestion],
) -> Tuple[Candidate, ...]:
    out = list(candidates)
    for q in questions:
        if q.name == "strategy_premise_freshness":
            out.append(Candidate(
                name=q.name,
                contradicted=False,
                executable=q.executable,
                missing_cost=1,
                expected_space_reduction=1,
            ))
    return tuple(out)
