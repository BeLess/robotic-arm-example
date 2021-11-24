from typing import Tuple, Union


class World:
    def __init__(
        self,
        width: int,
        height: int,
        robot_origin: Tuple[int, int],
        goal: Tuple[int, int]
    ) -> None:
        self.width = width
        self.height = height
        self.robot_origin = robot_origin
        self.goal = goal

    def convert_to_display(
            self, point: Tuple[Union[int, float], Union[int, float]]) -> Tuple[int, int]:
        """
        Convert a point from the robot coordinate system to the display coordinate system
        """
        robot_x, robot_y = point
        offset_x, offset_y = self.robot_origin

        return int(offset_x + robot_x), int(offset_y - robot_y)