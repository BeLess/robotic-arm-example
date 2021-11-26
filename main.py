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
    # This is to handle the concept of "facing" when it comes to the angle of rotation
    # Without this transformation, negative x values (spatially understood as "behind") at angles
    # that would cause the robot to rotate counterclockwise (any angle over 90 degrees) would
    # result in a nonsensical result (rotating "behind" and reaching "forward" for a -x value)
    if goal.angle.angle > 90 and goal.x < 0:
        goal = Goal(x=abs(goal.x), y=goal.y, angle=goal.angle)
    robot = Robot()
    world = World(width, height, robot_origin, goal)
    vis = Visualizer(world)

    try:
        robot.reach(goal, vis)
    except AssertionError as e:
        print(f'ERROR: {e}, Aborting.')
    except KeyboardInterrupt:
        pass
    finally:
        vis.cleanup()


if __name__ == '__main__':
    main()
