"""Experienced-battle wiring.

Returns observed experience to Garden's candidate priority. This does not
promote a permanent rule and does not invent an early-HARVEST target.
"""
from dataclasses import dataclass

from .abstraction import ExperienceAbstraction
from .cycle import CycleResult
from .decision import decide
from .generator import DirectionSpace, generate_candidates
from .game_agent import DecodedAction
from .interventions import BLIND_TEST_001
from .from_mainline.kaggriculture_codec import decode, encode
from .reentry import return_experience
from .selector import choose_next
from .trace import ActionSnapshot


@dataclass
class ExperiencedTelemetry:
    calls: int = 0
    hire_suppressions: int = 0
    returned_experience_cycles: int = 0
    selected_hire: int = 0
    selected_other: int = 0


def _intent_for(name):
    return next((x for x in BLIND_TEST_001 if x.kind.value == name), None)


def make_experienced_agent(base_agent, abstraction: ExperienceAbstraction, telemetry=None):
    telemetry = telemetry or ExperiencedTelemetry()

    def agent(obs):
        telemetry.calls += 1
        base_action = base_agent(obs)
        decoded = decode(base_action)
        if decoded is None:
            return base_action

        day = int(obs.get("day", 0))
        closure_active = (30 - day) <= 14
        space = DirectionSpace(
            closure_active=closure_active,
            hire_observed=decoded.market_action == "HIRE",
            harvestable=False,
            allow_hire_suppression=True,
            allow_early_harvest=False,
        )
        state = ActionSnapshot(
            closure_active=closure_active,
            harvestable=False,
            market_action=decoded.market_action,
            farmer_action=decoded.farmer_action,
        )

        candidates = generate_candidates(space)
        returned = return_experience(candidates, (abstraction,))
        selection = choose_next(returned)
        telemetry.returned_experience_cycles += 1

        if selection.candidate is None:
            return base_action
        if selection.candidate.name == "hire_stop_only":
            telemetry.selected_hire += 1
        else:
            telemetry.selected_other += 1

        intent = _intent_for(selection.candidate.name)
        if intent is None:
            return base_action
        decision = decide(intent, state)
        changed = DecodedAction(decision.market_action, decision.farmer_action)
        if decoded.market_action == "HIRE" and changed.market_action == "PASS":
            telemetry.hire_suppressions += 1
        return encode(changed, base_action)

    agent.garden_telemetry = telemetry
    return agent
