"""
main.py
"""

from gherkin.model import Robot, World, Goal
from gherkin.util import Controller, Runner, generate_random_goal
from gherkin.visuals import Visualizer


def main() -> None:
    runner = build_problem()

    try:
        runner.run()
    except AssertionError as e:
        print(f'ERROR: {e}, Aborting.')
    except KeyboardInterrupt:
        pass
    finally:
        runner.cleanup()


def build_problem():
    height = 300
    width = 300
    robot_origin = (int(width / 2), int(height / 2))
    goal = generate_random_goal(Robot.min_reachable_radius(), Robot.max_reachable_radius())
    # This is to handle the concept of "facing" when it comes to the angle of rotation
    # Without this transformation, negative x values (spatially understood as "behind") at angles
    # that would cause the robot to rotate counterclockwise (any angle over 90 degrees) would
    # result in a nonsensical result (rotating "behind" and reaching "forward" for a -x value)
    if goal.angle.angle > 90 and goal.x < 0:
        goal = Goal(x=abs(goal.x), y=goal.y, angle=goal.angle)
    robot = Robot()
    controller = Controller(goal)
    world = World(width, height, robot_origin, goal)
    vis = Visualizer(world)
    runner = Runner(robot, controller, world, vis)
    return runner


if __name__ == '__main__':
    main()
