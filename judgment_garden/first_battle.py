"""First-battle wiring for the bounded HIRE-stop Garden probe.

A concrete base agent must be supplied by the caller. No existing repository is
imported implicitly.
"""
from dataclasses import dataclass

from .game_agent import DecodedAction, make_agent
from .from_mainline.kaggriculture_codec import decode, encode
from .from_mainline.kaggriculture_state import read_hire_stop_state


@dataclass
class BattleTelemetry:
    cognition_cycles: int = 0
    changed_actions: int = 0
    hire_suppressions: int = 0
    bridge_calls: int = 0
    decode_failures: int = 0


def make_hire_stop_agent(base_agent, telemetry=None):
    telemetry = telemetry or BattleTelemetry()

    def observe(result, before, after):
        telemetry.bridge_calls += 1
        if result is None:
            telemetry.decode_failures += 1
            return
        telemetry.cognition_cycles += 1
        if before != after:
            telemetry.changed_actions += 1
        if before.market_action == "HIRE" and after.market_action == "PASS":
            telemetry.hire_suppressions += 1

    agent = make_agent(
        base_agent=base_agent,
        state_reader=read_hire_stop_state,
        decode_action=decode,
        encode_action=encode,
        observe=observe,
    )
    agent.garden_telemetry = telemetry
    return agent
