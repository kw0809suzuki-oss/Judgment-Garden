"""Evidence-return layer for Judgment Garden.

This records observed outcomes and derives bounded update proposals.
It does not rewrite judgment axes automatically.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class OutcomeStatus(str, Enum):
    OBSERVED = "observed"
    NOT_OBSERVED = "not_observed"
    NOT_EXECUTED = "not_executed"


@dataclass(frozen=True)
class Outcome:
    probe_name: str
    status: OutcomeStatus
    terminal_self_delta: Optional[float] = None
    margin_delta: Optional[float] = None
    win_delta: Optional[float] = None


@dataclass(frozen=True)
class UpdateProposal:
    probe_name: str
    direction: str
    evidence_scope: str
    promote: bool
    reason: str


def propose_update(outcome: Outcome) -> UpdateProposal:
    if outcome.status is not OutcomeStatus.OBSERVED:
        return UpdateProposal(
            probe_name=outcome.probe_name,
            direction="unknown",
            evidence_scope=outcome.status.value,
            promote=False,
            reason="missing_outcome_is_not_negative_evidence",
        )

    if outcome.terminal_self_delta is None:
        return UpdateProposal(
            probe_name=outcome.probe_name,
            direction="unknown",
            evidence_scope="observed_without_terminal_self",
            promote=False,
            reason="goal_metric_missing",
        )

    if outcome.terminal_self_delta > 0:
        direction = "positive_terminal_self"
    elif outcome.terminal_self_delta < 0:
        direction = "negative_terminal_self"
    else:
        direction = "neutral_terminal_self"

    return UpdateProposal(
        probe_name=outcome.probe_name,
        direction=direction,
        evidence_scope="terminal_self_only",
        promote=False,
        reason="proposal_requires_separate_adoption_boundary",
    )
