"""Isolated Kaggriculture battle runner for Judgment Garden.

This module mirrors only the public execution shape discovered in flow-hand:
make("kaggriculture", seed) -> env.run(agents) -> rewards.

It does not import or modify flow-hand, relation-flow-agent, or the existing
Combat Model.
"""
from dataclasses import dataclass
from typing import Callable, Sequence

from .learning import Outcome, OutcomeStatus


Agent = Callable[[dict], object]


@dataclass(frozen=True)
class MatchSpec:
    probe_name: str
    seed: int
    seat: int


def run_match(
    spec: MatchSpec,
    garden_agent: Agent,
    opponent: Agent | str,
) -> Outcome:
    try:
        from kaggle_environments import make
    except ImportError:
        return Outcome(
            probe_name=spec.probe_name,
            status=OutcomeStatus.NOT_EXECUTED,
        )

    agents: list[Agent | str] = [opponent, opponent]
    agents[spec.seat] = garden_agent

    env = make("kaggriculture", configuration={"seed": spec.seed}, debug=False)
    env.run(agents)
    rewards: Sequence[float] = [state.reward for state in env.state]

    own = float(rewards[spec.seat])
    other = float(rewards[1 - spec.seat])
    return Outcome(
        probe_name=spec.probe_name,
        status=OutcomeStatus.OBSERVED,
        terminal_self_delta=own,
        margin_delta=own - other,
        win_delta=1.0 if own > other else (0.0 if own == other else -1.0),
    )
