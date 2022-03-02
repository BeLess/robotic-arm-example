import time
from dataclasses import dataclass
from typing import Tuple

import numpy as np

from gherkin.model.robot import Robot
from gherkin.model.world import World
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

        while running:
            # Step the controller
            self.robot = self.controller.step(self.robot)

            # Check collisions
            # TODO

            # Check success
            success = self.check_success(self.robot, self.world.goal)

            # Update the display
            running = self.vis.update_display(self.robot, success)

            # sleep for Robot DT seconds, to force update rate
            time.sleep(self.robot.limits.DT)

    @staticmethod
    def check_success(robot: Robot, goal: Tuple[int, int]) -> bool:
        """
        Check that robot's joint 2 is very close to the goal.
        Don't not use exact comparision, to be robust to floating point calculations.
        """
        return np.allclose(robot.joint_2_pos(), goal, atol=0.25)

    def cleanup(self) -> None:
        self.vis.cleanup()