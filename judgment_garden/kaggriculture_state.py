"""Minimal state reader for the first HIRE-stop battle.

Closure is deliberately narrow: remaining_days <= 14, matching the observed
working comparison variant. This is a battle fixture, not an adopted rule.
"""
from .generator import DirectionSpace
from .game_agent import DecodedAction
from .trace import ActionSnapshot


def read_hire_stop_state(obs: dict, decoded: DecodedAction):
    day = int(obs.get("day", 0))
    closure_active = (30 - day) <= 14

    space = DirectionSpace(
        closure_active=closure_active,
        hire_observed=decoded.market_action == "HIRE",
        harvestable=False,
        allow_hire_suppression=True,
        allow_early_harvest=False,
    )
    snapshot = ActionSnapshot(
        closure_active=closure_active,
        harvestable=False,
        market_action=decoded.market_action,
        farmer_action=decoded.farmer_action,
    )
    return space, snapshot
