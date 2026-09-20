import importlib.util
from kaggle_environments import make

from judgment_garden.first_battle import make_hire_stop_agent


def counted(agent, counter):
    def wrapped(obs):
        counter["calls"] += 1
        return agent(obs)
    return wrapped


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def play(agent, opponent, seed=4142, seat=0):
    env = make("kaggriculture", configuration={"seed": seed}, debug=False)
    agents = [opponent, opponent]
    agents[seat] = agent
    env.run(agents)
    rewards = [state.reward for state in env.state]
    return rewards[seat], rewards[1-seat]


def main():
    base = load("base_agent.py", "garden_base")
    opponent = "opponents/lonespear.py"
    control_calls = {"calls": 0}
    control = play(counted(base.agent, control_calls), opponent)
    garden_agent = make_hire_stop_agent(base.agent)
    candidate_calls = {"calls": 0}
    # Keep the Garden wrapper as the direct callable. Kaggriculture treats
    # nested closure wrappers as a one-shot/error boundary in this harness.
    # Count entry on the Garden agent itself so the callable remains stable.
    original_garden = garden_agent
    def garden_entry(obs):
        candidate_calls["calls"] += 1
        return original_garden(obs)
    candidate = play(garden_entry, opponent)
    print(f"GARDEN_FIRST_BATTLE seed=4142 seat=0 opponent=lonespear")
    print(f"CONTROL self={control[0]} opp={control[1]} margin={control[0]-control[1]}")
    print(f"CANDIDATE self={candidate[0]} opp={candidate[1]} margin={candidate[0]-candidate[1]}")
    print(f"DELTA self={candidate[0]-control[0]} margin={(candidate[0]-candidate[1])-(control[0]-control[1])}")
    t = garden_agent.garden_telemetry
    print(f"ENTRY control_calls={control_calls['calls']} candidate_calls={candidate_calls['calls']}")
    print(f"TRACE bridge_calls={t.bridge_calls} decode_failures={t.decode_failures} cognition_cycles={t.cognition_cycles} changed_actions={t.changed_actions} hire_suppressions={t.hire_suppressions}")


if __name__ == "__main__":
    main()
