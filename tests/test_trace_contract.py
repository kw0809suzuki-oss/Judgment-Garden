from judgment_garden.interventions import BLIND_TEST_001, InterventionKind
from judgment_garden.trace import ActionSnapshot, trace


def test_control_never_changes_actions():
    intent = next(x for x in BLIND_TEST_001 if x.kind is InterventionKind.CONTROL)
    state = ActionSnapshot(True, True, "HIRE", "PASS")
    out = trace(intent, state)
    assert out.eligible
    assert out.before_market == out.after_market == "HIRE"
    assert out.before_farmer == out.after_farmer == "PASS"
    assert out.executed is False


def test_hire_stop_changes_only_hire_under_closure():
    intent = next(x for x in BLIND_TEST_001 if x.kind is InterventionKind.SUPPRESS_HIRE)
    on = trace(intent, ActionSnapshot(True, False, "HIRE", "PASS"))
    off = trace(intent, ActionSnapshot(False, False, "HIRE", "PASS"))
    other = trace(intent, ActionSnapshot(True, False, "SELL", "PASS"))
    assert on.eligible and on.after_market == "PASS"
    assert not off.eligible and off.after_market == "HIRE"
    assert not other.eligible and other.after_market == "SELL"
    assert on.after_farmer == "PASS"


def test_early_harvest_requires_closure_and_harvestable():
    intent = next(x for x in BLIND_TEST_001 if x.kind is InterventionKind.EARLY_HARVEST)
    on = trace(intent, ActionSnapshot(True, True, "PASS", "WATER"))
    no_crop = trace(intent, ActionSnapshot(True, False, "PASS", "WATER"))
    no_closure = trace(intent, ActionSnapshot(False, True, "PASS", "WATER"))
    assert on.eligible and on.after_farmer == "HARVEST"
    assert not no_crop.eligible and no_crop.after_farmer == "WATER"
    assert not no_closure.eligible and no_closure.after_farmer == "WATER"
    assert on.after_market == "PASS"
