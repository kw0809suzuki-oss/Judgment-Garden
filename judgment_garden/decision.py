"""Pure decision step for Judgment Garden.

This is intentionally runtime-agnostic: State + Intent -> Decision.
It does not execute an external action.
"""
from dataclasses import dataclass

from .interventions import InterventionIntent
from .trace import ActionSnapshot, InterventionTrace, trace


@dataclass(frozen=True)
class Decision:
    trace: InterventionTrace
    market_action: str
    farmer_action: str
    executable: bool
    boundary: str


def decide(intent: InterventionIntent, state: ActionSnapshot) -> Decision:
    observed = trace(intent, state)
    return Decision(
        trace=observed,
        market_action=observed.after_market,
        farmer_action=observed.after_farmer,
        executable=False,
        boundary="decision_only_no_runtime_adapter",
    )
