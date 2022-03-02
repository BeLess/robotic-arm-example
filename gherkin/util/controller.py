import logging
from dataclasses import dataclass, field
from typing import Optional

from gherkin.model import Goal, Robot, Rotation



@dataclass()
class Controller:
    goal: Goal
    goal_theta_0: float = field(init=False)
    goal_theta_1: float = field(init=False)

    def __post_init__(self) -> None:
        self.goal_theta_0, self.goal_theta_1 = Robot.inverse(self.goal[0], self.goal[1])

    def step(self, robot: Robot, rotation: Optional[Rotation]) -> Robot:
        """
        Simple P controller
        """
        if rotation:
            self._rotate_robot(robot, rotation)
        else:
            self._move_arm(robot)

        return robot

    def _rotate_robot(self, robot: Robot, rotation: Rotation):
        robot.rotate(rotation.direction, rotation.speed)
        return robot

    def _move_arm(self, robot: Robot):
        theta_0_error = self.goal_theta_0 - robot.theta_0
        theta_1_error = self.goal_theta_1 - robot.theta_1
        robot.theta_0 += theta_0_error / 10
        robot.theta_1 += theta_1_error / 10

        return Robot
