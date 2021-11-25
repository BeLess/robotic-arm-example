import time
from dataclasses import dataclass

import numpy as np

from gherkin.model import DIRECTION, Goal, Robot, Rotation, SPEED, World
from gherkin.util.controller import Controller
from gherkin.visuals.visualizer import Visualizer


@dataclass()
class Runner:
    robot: Robot
    controller: Controller
    world: World
    vis: Visualizer

    def run(self) -> None:
        running = True
        found_angle = False
        success = False

        while running:
            # Step the controller
            rotation = determine_rotation(self.robot, self.world.goal) if not found_angle else None
            self.robot = self.controller.step(self.robot, rotation)

            # Check collisions
            # TODO

            found_angle = self.check_angle(self.robot, self.world.goal)
            if found_angle:
                # Check success
                success = self.check_success(self.robot, self.world.goal)

            # Update the display
            running = self.vis.update_display(self.robot, success)

            # sleep for Robot DT seconds, to force update rate
            time.sleep(self.robot.limits.DT)

    @staticmethod
    def check_success(robot: Robot, goal: Goal) -> bool:
        """
        Check that robot's joint 2 is very close to the goal.
        Don't not use exact comparison, to be robust to floating point calculations.
        """

        return np.allclose(robot.joint_2_pos(), (goal.x, goal.y), atol=0.25)

    @staticmethod
    def check_angle(robot: Robot, goal: Goal) -> bool:
        """
        Check that the robots angle matches the angle of the goal.
        Because the arm can reach "behind" the point of rotation, reflective angles are functionally equivalent
        """
        return (robot.angle == goal.angle) or ((robot.angle - 180) == goal.angle)

    def cleanup(self) -> None:
        self.vis.cleanup()


def determine_rotation(robot: Robot, goal: Goal) -> Rotation:
    direction, difference = deterimine_direction_rotation_cheap(robot, goal)
    speed = SPEED.FAST if difference > robot.limits.FAST_ROTATION_SPEED else SPEED.FINE

    return Rotation(direction, speed)


def deterimine_direction_rotation_cheap(robot: Robot, goal: Goal):
    """
    Determines the optimal rotation of the arm, if rotating the entire robot is cheaper than manipulating the arm
    """
    difference_cw = abs(robot.angle.angle - goal.angle.angle)
    difference_ccw = abs(robot.angle.inverse.angle - goal.angle.angle)
    direction, difference = (DIRECTION.CLOCKWISE, difference_cw) if difference_cw < difference_ccw \
        else (DIRECTION.COUNTER_CLOCKWISE, difference_ccw)
    return direction, difference


# todo: Figure out of this makes sense
def deterimine_direction_arm_cheap(robot: Robot, goal:Goal):
    """
    Determines the optimal rotation of the arm, if manipulating the arm is cheaper than rotating the robot
    """
    difference_cw = abs(robot.angle.angle - goal.angle.angle)
    difference_ccw = abs(robot.angle.angle - goal.angle.inverse.angle)
    return difference_cw, difference_ccw

def determine_arm_facing(robot: Robot, goal: Goal) -> bool:
    """
    determines whether the arm is "facing" the same direction as the target
    """
    if (robot.joint_2_pos()[0] > 0 and goal.x > 0) or (robot.joint_2_pos()[0] < 0 and goal.x < 0):
        return True
    return False

