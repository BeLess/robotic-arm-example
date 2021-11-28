"""
main.py
"""
import itertools
import pprint

import pykka

from gherkin.model import Robot, World, Goal
from gherkin.model.arm import Arm
from gherkin.util import generate_random_goal, Visualizer


def main() -> None:
    try:
        run_fleet(4, 10)
        #run_single(10)
    except AssertionError as e:
        print(f'ERROR: {e}, Aborting.')
    except KeyboardInterrupt:
        pass
    finally:
        input("Press enter to exit:")
        exit(0)


def run_fleet(num_robots: int, num_goals: int):
    robots = itertools.cycle([Robot.start().proxy() for _ in range(num_robots)])
    goals = [generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius()) for _ in range(num_goals)]
    results = []
    for goal in goals:
        results.append(next(robots).reach(goal))

    goals_to_successes = zip(goals, pykka.get_all(results))
    pprint.pprint(list(goals_to_successes))
    pykka.ActorRegistry.stop_all()


def run_single(num_goals: int):
    vis = generate_visualizer()
    goals = [generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius()) for _ in range(num_goals)]
    robot = Robot()
    for goal in goals:
        robot.reach(goal, vis)


def generate_visualizer():
    height = 300
    width = 300
    robot_origin = (int(width / 2), int(height / 2))
    world = World(width, height, robot_origin)
    vis = Visualizer(world)
    return vis


if __name__ == '__main__':
    main()
