from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NamedTuple, Optional


@dataclass(frozen=True, order=True, eq=True)
class Angle:
    """
    A utility class responsible for angle math
    """
    angle: int

    @property
    def inverse(self) -> "Angle":
        """

        Returns: The inverse angle of this angle
        """
        return self - 180

    def __add__(self, other) -> "Angle":
        if type(other) == Angle:
            new = self.angle + other.angle
        elif type(other) == int:
            new = self.angle + other
        else:
            raise TypeError(f"Expected Angle or in, but got {type(other)}")
        return Angle(new - 360) if new > 359 else Angle(new)

    def __sub__(self, other) -> "Angle":
        if type(other) == Angle:
            new = self.angle - other.angle
        elif type(other) == int:
            new = self.angle - other
        else:
            raise TypeError(f"Expected Angle or in, but got {type(other)}")
        return Angle(new + 360) if new < 0 else Angle(new)


class DIRECTION(Enum):
    CLOCKWISE = "CLOCKWISE"
    COUNTER_CLOCKWISE = "COUNTER_CLOCKWISE"


class SPEED(Enum):
    FAST = "FAST"
    FINE = "FINE"


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
