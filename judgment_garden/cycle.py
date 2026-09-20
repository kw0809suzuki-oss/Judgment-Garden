"""One non-executing cognition cycle for Judgment Garden.

DirectionSpace -> candidates -> local probe selection -> intent -> Decision.
The cycle stops before runtime execution.
"""
from dataclasses import dataclass
from typing import Optional

from .decision import Decision, decide
from .generator import DirectionSpace, generate_candidates
from .interventions import BLIND_TEST_001, InterventionIntent
from .selector import Candidate, Selection, choose_next
from .trace import ActionSnapshot


@dataclass(frozen=True)
class CycleResult:
    candidates: tuple[Candidate, ...]
    selection: Selection
    intent: Optional[InterventionIntent]
    decision: Optional[Decision]
    boundary: str


def _intent_for(name: str) -> Optional[InterventionIntent]:
    return next((intent for intent in BLIND_TEST_001 if intent.kind.value == name), None)


def cognition_cycle(space: DirectionSpace, state: ActionSnapshot) -> CycleResult:
    candidates = generate_candidates(space)
    selection = choose_next(candidates)

    if selection.candidate is None:
        return CycleResult(
            candidates=candidates,
            selection=selection,
            intent=None,
            decision=None,
            boundary="return_no_safe_probe",
        )

    intent = _intent_for(selection.candidate.name)
    if intent is None:
        return CycleResult(
            candidates=candidates,
            selection=selection,
            intent=None,
            decision=None,
            boundary="return_unmapped_candidate",
        )

    decision = decide(intent, state)
    return CycleResult(
        candidates=candidates,
        selection=selection,
        intent=intent,
        decision=decision,
        boundary="stop_before_execution",
    )
