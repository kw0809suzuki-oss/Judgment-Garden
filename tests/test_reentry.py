from judgment_garden.abstraction import abstract_experience
from judgment_garden.generator import DirectionSpace, generate_candidates
from judgment_garden.learning import Outcome, OutcomeStatus
from judgment_garden.reentry import return_experience
from judgment_garden.selector import choose_next


def test_negative_hire_experience_returns_as_priority_change_not_rule():
    outcomes = [
        Outcome("hire_stop_only", OutcomeStatus.OBSERVED, delta, margin)
        for delta, margin in (
            (-16209.0, -12993.0),
            (-21128.0, -19557.0),
            (-23863.0, -25625.0),
            (-20025.0, -35218.0),
            (-19356.0, -12904.0),
        )
    ]
    learned = abstract_experience(outcomes)

    space = DirectionSpace(
        closure_active=True,
        hire_observed=True,
        harvestable=True,
    )
    before = generate_candidates(space)
    after = return_experience(before, (learned,))

    hire = next(c for c in after if c.name == "hire_stop_only")
    harvest = next(c for c in after if c.name == "early_harvest_only")

    assert hire.contradicted is False
    assert hire.executable is True
    assert hire.expected_space_reduction == 0
    assert harvest.expected_space_reduction == 1
    assert choose_next(after).candidate.name == "early_harvest_only"
    assert learned.promote is False
