import time
from dataclasses import dataclass

import numpy as np

from gherkin.model import Goal, Robot, Rotation, World
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
        success = False

        while running:
            # Step the controller
            self.robot = self.controller.step(self.robot, None)

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
