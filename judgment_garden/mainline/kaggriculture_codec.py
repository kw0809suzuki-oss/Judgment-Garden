"""Concrete action codec for the observed Kaggriculture action shape.

Observed shape:
{"farmer": [...], "hands": [...], "market": [[...], ...]}
"""
from copy import deepcopy
from typing import Optional

from ..game_agent import DecodedAction


def decode(action: object) -> Optional[DecodedAction]:
    if not isinstance(action, dict):
        return None
    farmer = action.get("farmer")
    market = action.get("market")
    if not isinstance(farmer, list) or not isinstance(market, list):
        return None

    farmer_verb = farmer[0] if farmer else "PASS"
    market_verbs = [order[0] for order in market if isinstance(order, list) and order]
    market_verb = "HIRE" if "HIRE" in market_verbs else "PASS"
    return DecodedAction(market_action=market_verb, farmer_action=farmer_verb)


def encode(changed: DecodedAction, base_action: object) -> object:
    if not isinstance(base_action, dict):
        return base_action
    out = deepcopy(base_action)

    if changed.market_action == "PASS":
        orders = out.get("market", [])
        if isinstance(orders, list):
            out["market"] = [
                order for order in orders
                if not (isinstance(order, list) and order and order[0] == "HIRE")
            ]

    if changed.farmer_action == "HARVEST":
        # The observed action shape confirms the verb but not a safe target
        # relocation rule. Only replace an already target-valid farmer action.
        farmer = out.get("farmer")
        if isinstance(farmer, list) and farmer and farmer[0] == "HARVEST":
            out["farmer"] = farmer

    return out
