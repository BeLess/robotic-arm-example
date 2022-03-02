"""
main.py
"""
import itertools
import pprint

import pykka

from gherkin.model import Robot
from gherkin.model.arm import Arm
from gherkin.model.fleet_manager import FleetManager
from gherkin.util import generate_random_goal
from gherkin.util.utilities import generate_visualizer


def main() -> None:
    try:
        run_fleet(2, 8)
        #run_single(10)
    except Exception as e:
        print(f'ERROR: {e}, Aborting.')
        exit(0)
    except KeyboardInterrupt:
        pass


def run_fleet(num_robots: int, num_goals: int):
    robots = [Robot.start(i).proxy() for i in range(num_robots)]
    vis = generate_visualizer(num_robots)
    fleet_manager = FleetManager(robots, vis)
    fleet_manager.receive_goals(
        [generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius()) for _ in range(num_goals)]
    )


def run_single(num_goals: int):
    vis = generate_visualizer(1)
    goals = [generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius()) for _ in range(num_goals)]
    robot = Robot(0)
    for goal in goals:
        robot.reach(goal, vis)


if __name__ == '__main__':
    main()
