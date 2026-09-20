"""First-battle wiring for the bounded HIRE-stop Garden probe.

A concrete base agent must be supplied by the caller. No existing repository is
imported implicitly.
"""
from .game_agent import make_agent
from .kaggriculture_codec import decode, encode
from .kaggriculture_state import read_hire_stop_state


def make_hire_stop_agent(base_agent):
    return make_agent(
        base_agent=base_agent,
        state_reader=read_hire_stop_state,
        decode_action=decode,
        encode_action=encode,
    )
