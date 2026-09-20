"""Trace-only body for Judgment Garden.

This records what an intervention *would* do. It does not execute Kaggriculture.
"""
from dataclasses import dataclass
from typing import Optional

from .interventions import InterventionIntent, InterventionKind, validate_intent


@dataclass(frozen=True)
class ActionSnapshot:
    closure_active: bool
    harvestable: bool
    market_action: str
    farmer_action: str


@dataclass(frozen=True)
class InterventionTrace:
    kind: InterventionKind
    eligible: bool
    before_market: str
    after_market: str
    before_farmer: str
    after_farmer: str
    executed: bool = False
    reason: str = "trace_only"


def trace(intent: InterventionIntent, state: ActionSnapshot) -> InterventionTrace:
    validate_intent(intent)

    eligible = False
    market = state.market_action
    farmer = state.farmer_action

    if intent.kind is InterventionKind.CONTROL:
        eligible = state.closure_active
    elif intent.kind is InterventionKind.SUPPRESS_HIRE:
        eligible = state.closure_active and state.market_action == "HIRE"
        if eligible:
            market = "PASS"
    elif intent.kind is InterventionKind.EARLY_HARVEST:
        eligible = state.closure_active and state.harvestable
        if eligible:
            farmer = "HARVEST"

    return InterventionTrace(
        kind=intent.kind,
        eligible=eligible,
        before_market=state.market_action,
        after_market=market,
        before_farmer=state.farmer_action,
        after_farmer=farmer,
    )
