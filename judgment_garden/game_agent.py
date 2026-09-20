"""Game-agent bridge for Judgment Garden.

The bridge wraps an explicitly supplied base agent. Garden may transform the
base action only when a translator can safely expose market/farmer channels.
Without such a translator it returns the base action unchanged.
"""
from dataclasses import dataclass
from typing import Callable, Optional

from .cycle import CycleResult, cognition_cycle
from .generator import DirectionSpace
from .trace import ActionSnapshot


@dataclass(frozen=True)
class DecodedAction:
    market_action: str
    farmer_action: str


Decoder = Callable[[object], Optional[DecodedAction]]
Encoder = Callable[[DecodedAction, object], object]


def make_agent(
    base_agent: Callable[[dict], object],
    state_reader: Callable[[dict, DecodedAction], tuple[DirectionSpace, ActionSnapshot]],
    decode_action: Decoder,
    encode_action: Encoder,
    observe: Optional[Callable[[CycleResult, DecodedAction, DecodedAction], None]] = None,
):
    def agent(obs: dict):
        base_action = base_agent(obs)
        decoded = decode_action(base_action)
        if decoded is None:
            if observe is not None:
                observe(None, None, None)
            return base_action

        space, state = state_reader(obs, decoded)
        result = cognition_cycle(space, state)
        if result.decision is None:
            return base_action

        changed = DecodedAction(
            market_action=result.decision.market_action,
            farmer_action=result.decision.farmer_action,
        )
        if observe is not None:
            observe(result, decoded, changed)
        return encode_action(changed, base_action)

    return agent
