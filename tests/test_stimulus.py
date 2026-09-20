from judgment_garden.generator import DirectionSpace, generate_candidates
from judgment_garden.selector import choose_next
from judgment_garden.stimulus import Stimulus, extend_candidate_space, ingest_stimulus


def test_factory_freshness_stimulus_opens_question_without_teaching_tactic():
    stimulus = Stimulus(
        stimulus_id="STIMULUS-001",
        observed_difference="A previously valid work premise can become stale when newer evidence appears.",
        known="Freshness and evidence quality are separate concerns.",
        unknown="Whether the same pattern matters inside Garden strategy choice.",
        boundary="Do not infer that newer evidence is sufficient, true, or final.",
    )

    space = DirectionSpace(
        closure_active=True,
        hire_observed=True,
        harvestable=False,
    )
    before = generate_candidates(space)
    questions = ingest_stimulus((stimulus,))
    after = extend_candidate_space(before, questions)

    assert len(questions) == 1
    assert questions[0].name == "strategy_premise_freshness"
    assert questions[0].executable is False

    names_before = {c.name for c in before}
    names_after = {c.name for c in after}
    assert "strategy_premise_freshness" not in names_before
    assert "strategy_premise_freshness" in names_after

    opened = next(c for c in after if c.name == "strategy_premise_freshness")
    assert opened.executable is False
    assert opened.contradicted is False

    # Material changed the candidate/question space, but cannot become the
    # selected runtime action merely because it arrived from the factory.
    assert choose_next(after).candidate.name == "hire_stop_only"
