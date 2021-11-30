from dataclasses import dataclass, field

from gherkin.common import Angle, DIRECTION, SPEED


@dataclass
class RotationLimits:
    """
    A class responsible for containing the physical limits of a rotating base

    Args:
        FAST_ROTATION_SPEED: the number of degrees moved/cycle when moving large distances
        FINE_ROTATION_SPEED: the number of degrees moved/cycle when zeroing in on a desire angle
        DT: The length of a cycle to execute a given command
    """
    FAST_ROTATION_SPEED: int = 5
    FINE_ROTATION_SPEED: int = 1
    DT: float = 0.066


@dataclass
class RotatingBase:
    """
    A class responsible for manging the state and functionality of a rotating base for the robot

    Args:
        limits: the physical limitations of the base
        _angle: The current angle of the "front" of the base
    """
    limits: RotationLimits = field(default_factory=RotationLimits)
    _angle: Angle = Angle(0)  # degrees

    @property
    def angle(self) -> Angle:
        return self._angle

    def rotate(self, direction: DIRECTION, speed: SPEED) -> None:
        """
        Rotates increases or decreases the angle of the base, determined by the robot
        Args:
            direction: Clockwise or Counterclockwise
            speed: FINE or FAST, referring to the base's limits

        Returns:

        """
        rotation_rate = self.limits.FAST_ROTATION_SPEED if speed == SPEED.FAST else self.limits.FINE_ROTATION_SPEED
        if direction == DIRECTION.CLOCKWISE:
            self._angle += rotation_rate
        else:
            self._angle -= rotation_rate
