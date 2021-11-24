from enum import Enum
from collections import namedtuple

Goal = namedtuple("Goal", ["x", "y", "angle"])


class DIRECTION(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class SPEED(Enum):
    FAST = "FAST"
    FINE = "FINE"
