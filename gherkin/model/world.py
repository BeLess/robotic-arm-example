from dataclasses import dataclass
from typing import Tuple, Union, List


@dataclass()
class World:
    """
    A container for the general state of the world, for visualization purposes

    Args:
        width: the width of the problem space in pixels
        height: the height of the problem space in pixels
        robot_origin: the coordinates of the robot in this spaceS
    """
    total_width: int
    robot_width: int
    height: int
    robot_origins: List[Tuple[int, int]]

    def convert_to_display(self, point: Tuple[Union[int, float], Union[int, float]], offset: int) -> Tuple[int, int]:
        """
        Convert a point from the robot coordinate system to the display coordinate system
        """
        robot_x, robot_y = point
        offset_x, offset_y = self.robot_origins[offset]

        return int(offset_x + robot_x), int(offset_y - robot_y)