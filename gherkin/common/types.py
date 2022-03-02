from dataclasses import dataclass
from datetime import datetime
from typing import NamedTuple, Optional

from gherkin.common.enums import DIRECTION, SPEED
from gherkin.common.angle import Angle


@dataclass(order=True, eq=True)
class Goal:
    x: int
    y: int
    angle: Angle

    def __sub__(self, other):
        if type(other) == Goal:
            x_diff = abs(self.x - other.x)
            y_diff = abs(self.y - other.y)
            angle_diff = self.angle - other.angle
            return x_diff, y_diff, angle_diff
        else:
            raise TypeError


class Rotation(NamedTuple):
    direction: DIRECTION
    speed: SPEED


class Result(NamedTuple):
    robot_id: str
    goal: Goal
    success: bool
    completed_at: datetime
    error: Optional[Exception]
