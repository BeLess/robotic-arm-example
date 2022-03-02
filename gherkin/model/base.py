from dataclasses import dataclass, field

from gherkin.model import Angle, DIRECTION, SPEED


@dataclass
class RotationLimits:
    FAST_ROTATION_SPEED: int = 5
    FINE_ROTATION_SPEED: int = 1
    DT: float = 0.066


@dataclass
class RotatingBase:
    limits: RotationLimits = field(default_factory=RotationLimits)
    _angle: Angle = Angle(0)  # degrees

    @property
    def angle(self) -> Angle:
        return self._angle

    def rotate(self, direction: DIRECTION, speed: SPEED) -> None:
        rotation_rate = self.limits.FAST_ROTATION_SPEED if speed == SPEED.FAST else self.limits.FINE_ROTATION_SPEED
        print(f"Rotating robot {rotation_rate} degrees {direction.value}")
        if direction == DIRECTION.CLOCKWISE:
            self._angle += rotation_rate
        else:
            self._angle -= rotation_rate
