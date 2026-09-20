"""Execution boundary for Judgment Garden.

The adapter executes only against an explicitly supplied local callable.
No Kaggriculture runtime is imported here.
"""
from dataclasses import dataclass
from typing import Callable

from .decision import Decision


@dataclass(frozen=True)
class ExecutionReceipt:
    attempted: bool
    applied: bool
    market_action: str
    farmer_action: str
    boundary: str


def execute_with(
    decision: Decision,
    apply_actions: Callable[[str, str], bool],
    *,
    authorized: bool = False,
) -> ExecutionReceipt:
    if not authorized:
        return ExecutionReceipt(
            attempted=False,
            applied=False,
            market_action=decision.market_action,
            farmer_action=decision.farmer_action,
            boundary="authorization_required",
        )

    applied = bool(apply_actions(decision.market_action, decision.farmer_action))
    return ExecutionReceipt(
        attempted=True,
        applied=applied,
        market_action=decision.market_action,
        farmer_action=decision.farmer_action,
        boundary="local_callable_only",
    )
