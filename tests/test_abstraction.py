from judgment_garden.abstraction import abstract_experience
from judgment_garden.learning import Outcome, OutcomeStatus


def test_five_executed_negative_experiences_abstract_without_promotion():
    deltas = (
        (-16209.0, -12993.0),
        (-21128.0, -19557.0),
        (-23863.0, -25625.0),
        (-20025.0, -35218.0),
        (-19356.0, -12904.0),
    )
    outcomes = [
        Outcome(
            probe_name="hire_stop_only",
            status=OutcomeStatus.OBSERVED,
            terminal_self_delta=self_delta,
            margin_delta=margin_delta,
        )
        for self_delta, margin_delta in deltas
    ]

    result = abstract_experience(outcomes)

    assert result.probe_name == "hire_stop_only"
    assert result.observed_count == 5
    assert result.comparable_count == 5
    assert result.negative_count == 5
    assert result.positive_count == 0
    assert result.direction == "stable_negative_terminal_self"
    assert result.realization == "observed"
    assert result.scope == "provided_experience_only"
    assert result.promote is False
    assert result.reason == "repeated_observed_direction_not_adopted_as_rule"
