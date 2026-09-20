"""Battle port contract for Judgment Garden.

This is the seam between Garden decisions and a real Kaggriculture runner.
No external repository is imported or modified here.
"""
from dataclasses import dataclass
from typing import Protocol

from .decision import Decision
from .learning import Outcome


@dataclass(frozen=True)
class BattleRequest:
    probe_name: str
    seed: int
    seat: int
    decision: Decision


class BattleRunner(Protocol):
    def run(self, request: BattleRequest) -> Outcome:
        ...


def run_battle(runner: BattleRunner, request: BattleRequest) -> Outcome:
    """Execute only through an explicitly supplied battle runner."""
    return runner.run(request)
