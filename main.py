"""
main.py
"""

from gherkin.model import Robot, World
from gherkin.util import Controller, Runner, generate_random_goal
from gherkin.visuals import Visualizer


def main() -> None:
    height = 300
    width = 300

    robot_origin = (int(width / 2), int(height / 2))
    goal = generate_random_goal(Robot.min_reachable_radius(), Robot.max_reachable_radius())

    robot = Robot()
    controller = Controller(goal)
    world = World(width, height, robot_origin, goal)
    vis = Visualizer(world)

    runner = Runner(robot, controller, world, vis)

    try:
        runner.run()
    except AssertionError as e:
        print(f'ERROR: {e}, Aborting.')
    except KeyboardInterrupt:
        pass
    finally:
        runner.cleanup()


if __name__ == '__main__':
    main()
