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
        difference = stimulus.observed_difference.lower()
        if "premise" in difference and "stale" in difference:
            out.append(StimulusQuestion(
                name="strategy_premise_freshness",
                source_id=stimulus.stimulus_id,
                executable=False,
                reason="external_difference_opens_question_not_strategy",
            ))
        if "not observed" in difference and ("not evidence" in difference or "absent" in difference):
            out.append(StimulusQuestion(
                name="unobserved_alternative_preservation",
                source_id=stimulus.stimulus_id,
                executable=False,
                reason="missing_observation_opens_preservation_question",
            ))
        if "intake contract" in difference or ("re-entry" in difference and "testable" in difference):
            out.append(StimulusQuestion(
                name="explicit_evidence_request",
                source_id=stimulus.stimulus_id,
                executable=False,
                reason="repeated_boundary_opens_evidence_request_question",
            ))
    return tuple(out)


def relate_questions(questions: Iterable[StimulusQuestion]) -> Tuple[StimulusQuestion, ...]:
    questions = tuple(questions)
    names = {q.name for q in questions}
    out = list(questions)
    if {
        "strategy_premise_freshness",
        "unobserved_alternative_preservation",
    }.issubset(names):
        out.append(StimulusQuestion(
            name="recheck_alternatives_when_premise_changes",
            source_id="RELATION-001",
            executable=False,
            reason="relation_candidate_from_two_external_differences",
        ))
    return tuple(out)


def extend_candidate_space(
    candidates: Iterable[Candidate],
    questions: Iterable[StimulusQuestion],
) -> Tuple[Candidate, ...]:
    out = list(candidates)
    for q in questions:
        if q.name in {
            "strategy_premise_freshness",
            "unobserved_alternative_preservation",
            "recheck_alternatives_when_premise_changes",
            "explicit_evidence_request",
        }:
            out.append(Candidate(
                name=q.name,
                contradicted=False,
                executable=q.executable,
                missing_cost=1,
                expected_space_reduction=1,
            ))
    return tuple(out)
