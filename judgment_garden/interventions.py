"""Judgment Garden intervention contract.

Pure representation only. This module does not import or mutate the existing
Kaggriculture runtime.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class InterventionKind(str, Enum):
    CONTROL = "closure_only"
    SUPPRESS_HIRE = "hire_stop_only"
    EARLY_HARVEST = "early_harvest_only"


@dataclass(frozen=True)
class InterventionIntent:
    kind: InterventionKind
    trigger: str
    target_channel: Optional[str]
    target_action: Optional[str]
    replacement_action: Optional[str]
    evidence_status: str = "precommitted_not_executed"


BLIND_TEST_001 = (
    InterventionIntent(
        kind=InterventionKind.CONTROL,
        trigger="closure_active",
        target_channel=None,
        target_action=None,
        replacement_action=None,
    ),
    InterventionIntent(
        kind=InterventionKind.SUPPRESS_HIRE,
        trigger="closure_active",
        target_channel="market",
        target_action="HIRE",
        replacement_action="PASS",
    ),
    InterventionIntent(
        kind=InterventionKind.EARLY_HARVEST,
        trigger="closure_active_and_harvestable",
        target_channel="farmer",
        target_action=None,
        replacement_action="HARVEST",
    ),
)


def validate_intent(intent: InterventionIntent) -> None:
    """Reject representation drift before any runtime adapter exists."""
    if intent.kind is InterventionKind.CONTROL:
        if any((intent.target_channel, intent.target_action, intent.replacement_action)):
            raise ValueError("control must not mutate an action")
        return

    if intent.kind is InterventionKind.SUPPRESS_HIRE:
        if (intent.target_channel, intent.target_action, intent.replacement_action) != (
            "market", "HIRE", "PASS"
        ):
            raise ValueError("HIRE suppression contract drift")
        return

    if intent.kind is InterventionKind.EARLY_HARVEST:
        if intent.target_channel != "farmer" or intent.replacement_action != "HARVEST":
            raise ValueError("HARVEST contract drift")
        return

    raise ValueError("unknown intervention")
