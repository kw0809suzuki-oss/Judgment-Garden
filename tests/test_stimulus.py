from judgment_garden.generator import DirectionSpace, generate_candidates
from judgment_garden.selector import choose_next
from judgment_garden.stimulus import Stimulus, extend_candidate_space, ingest_stimulus, relate_questions


def test_factory_freshness_stimulus_opens_question_without_teaching_tactic():
    stimulus = Stimulus(
        stimulus_id="STIMULUS-001",
        observed_difference="A previously valid work premise can become stale when newer evidence appears.",
        known="Freshness and evidence quality are separate concerns.",
        unknown="Whether the same pattern matters inside Garden strategy choice.",
        boundary="Do not infer that newer evidence is sufficient, true, or final.",
    )
    space = DirectionSpace(closure_active=True, hire_observed=True, harvestable=False)
    before = generate_candidates(space)
    questions = ingest_stimulus((stimulus,))
    after = extend_candidate_space(before, questions)
    assert len(questions) == 1
    assert questions[0].name == "strategy_premise_freshness"
    assert questions[0].executable is False
    assert "strategy_premise_freshness" not in {c.name for c in before}
    assert "strategy_premise_freshness" in {c.name for c in after}
    assert choose_next(after).candidate.name == "hire_stop_only"


def test_two_factory_materials_form_relation_without_runtime_adoption():
    first = Stimulus(
        "STIMULUS-001",
        "A previously valid work premise can become stale when newer evidence appears.",
        "Freshness and evidence quality are separate concerns.",
        "Whether the same pattern matters inside Garden strategy choice.",
        "Do not infer that newer evidence is sufficient, true, or final.",
    )
    second = Stimulus(
        "STIMULUS-002",
        "A candidate not observed is not evidence that the candidate was absent.",
        "Missing observation and negative evidence are different states.",
        "Whether Garden collapses unobserved alternatives too early.",
        "Do not reconstruct hidden internal candidates as facts.",
    )
    related = relate_questions(ingest_stimulus((first, second)))
    names = {q.name for q in related}
    assert "strategy_premise_freshness" in names
    assert "unobserved_alternative_preservation" in names
    assert "recheck_alternatives_when_premise_changes" in names
    relation = next(q for q in related if q.name == "recheck_alternatives_when_premise_changes")
    assert relation.executable is False
    before = generate_candidates(DirectionSpace(True, True, False))
    after = extend_candidate_space(before, related)
    assert "recheck_alternatives_when_premise_changes" in {c.name for c in after}
    assert choose_next(after).candidate.name == "hire_stop_only"
