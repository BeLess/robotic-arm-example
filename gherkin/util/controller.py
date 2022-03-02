from dataclasses import dataclass, field
from typing import Tuple

from gherkin.model.robot import Robot


@dataclass()
class Controller:
    goal: Tuple[int, int]
    goal_theta_0: float = field(init=False)
    goal_theta_1: float = field(init=False)

    def __post_init__(self) -> None:
        self.goal_theta_0, self.goal_theta_1 = Robot.inverse(self.goal[0], self.goal[1])

    def step(self, robot: Robot) -> Robot:
        """
        Simple P controller
        """
        theta_0_error = self.goal_theta_0 - robot.theta_0
        theta_1_error = self.goal_theta_1 - robot.theta_1

        robot.theta_0 += theta_0_error / 10
        robot.theta_1 += theta_1_error / 10

        return robot