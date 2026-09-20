import importlib.util
from kaggle_environments import make

from judgment_garden.abstraction import abstract_experience
from judgment_garden.experienced_battle import make_experienced_agent
from judgment_garden.first_battle import make_hire_stop_agent
from judgment_garden.learning import Outcome, OutcomeStatus


DELTAS = (
    (-16209.0, -12993.0),
    (-21128.0, -19557.0),
    (-23863.0, -25625.0),
    (-20025.0, -35218.0),
    (-19356.0, -12904.0),
)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def play(agent, opponent, seed):
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    env.run([agent, opponent])
    return env.state[0].reward, env.state[1].reward


def main():
    base = load("base_agent.py", "garden_base_compare")
    opponent = "opponents/lonespear.py"
    seeds = (4142, 1729, 2718, 8080, 1209)

    experience = abstract_experience(
        Outcome("hire_stop_only", OutcomeStatus.OBSERVED, d, m)
        for d, m in DELTAS
    )

    for seed in seeds:
        before_agent = make_hire_stop_agent(base.agent)
        after_agent = make_experienced_agent(base.agent, experience)

        before = play(before_agent, opponent, seed)
        after = play(after_agent, opponent, seed)

        bt = before_agent.garden_telemetry
        at = after_agent.garden_telemetry
        print(f"LEARNING_COMPARE seed={seed} seat=0 opponent=lonespear")
        print(f"BEFORE self={before[0]} opp={before[1]} margin={before[0]-before[1]} hire_suppressions={bt.hire_suppressions}")
        print(f"AFTER self={after[0]} opp={after[1]} margin={after[0]-after[1]} hire_suppressions={at.hire_suppressions} selected_hire={at.selected_hire} selected_other={at.selected_other}")
        print(f"DELTA_AFTER_MINUS_BEFORE self={after[0]-before[0]} margin={(after[0]-after[1])-(before[0]-before[1])}")


if __name__ == "__main__":
    main()
