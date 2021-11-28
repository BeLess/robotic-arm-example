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
        run_fleet(4, 100)
        #run_single(10)
    except AssertionError as e:
        print(f'ERROR: {e}, Aborting.')
        exit(0)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'ERROR: {e}, aborting')
        exit(0)
    finally:
        input("Press enter to exit:")
        exit(0)


def run_fleet(num_robots: int, num_goals: int):
    robots = itertools.cycle([Robot.start(i).proxy() for i in range(num_robots)])
    goals = [generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius()) for _ in range(num_goals)]
    vis = generate_visualizer(num_robots)
    results = []
    for goal in goals:
        results.append(next(robots).reach(goal, vis))

    goals_to_successes = zip(goals, pykka.get_all(results))
    pprint.pprint(list(goals_to_successes))
    pykka.ActorRegistry.stop_all()


def run_single(num_goals: int):
    vis = generate_visualizer(1)
    goals = [generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius()) for _ in range(num_goals)]
    robot = Robot(1)
    for goal in goals:
        robot.reach(goal, vis)


def generate_visualizer(num_robots: int):
    height = 300
    robot_width = 300
    total_width = robot_width * num_robots
    robot_origins = [(int(robot_width / 2) + (robot_width * i), int(height / 2)) for i in range(num_robots)]
    world = World(total_width, robot_width, height, robot_origins)
    vis = Visualizer(world)
    return vis


if __name__ == '__main__':
    main()
