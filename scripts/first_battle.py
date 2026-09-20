import importlib.util
from kaggle_environments import make

from judgment_garden.first_battle import make_hire_stop_agent


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
    control = play(base.agent, opponent)
    candidate = play(make_hire_stop_agent(base.agent), opponent)
    print(f"GARDEN_FIRST_BATTLE seed=4142 seat=0 opponent=lonespear")
    print(f"CONTROL self={control[0]} opp={control[1]} margin={control[0]-control[1]}")
    print(f"CANDIDATE self={candidate[0]} opp={candidate[1]} margin={candidate[0]-candidate[1]}")
    print(f"DELTA self={candidate[0]-control[0]} margin={(candidate[0]-candidate[1])-(control[0]-control[1])}")


if __name__ == "__main__":
    main()
