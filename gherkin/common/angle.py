from dataclasses import dataclass


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