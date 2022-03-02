from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple


@dataclass(frozen=True, order=True, eq=True)
class Angle:
    angle: int

    @property
    def inverse(self) -> "Angle":
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


class Goal(NamedTuple):
    x: int
    y: int
    angle: Angle


class Rotation(NamedTuple):
    direction: DIRECTION
    speed: SPEED
