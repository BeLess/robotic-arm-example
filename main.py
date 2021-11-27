"""
main.py
"""

from gherkin.model import Robot, World, Goal
from gherkin.model.arm import Arm
from gherkin.util import generate_random_goal, Visualizer


def main() -> None:
    height = 300
    width = 300
    robot_origin = (int(width / 2), int(height / 2))
    goal = generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius())
    robot = Robot()
    world = World(width, height, robot_origin)
    vis = Visualizer(world)

    try:
        robot.reach(goal, vis)
        input("prompt: ")
    except AssertionError as e:
        print(f'ERROR: {e}, Aborting.')
    except KeyboardInterrupt:
        pass
    finally:
        vis.cleanup()


if __name__ == '__main__':
    main()
