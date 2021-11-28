import time
import uuid
from typing import Tuple

import numpy as np
from dataclasses import dataclass, field
from pykka import ThreadingActor

from gherkin.model.arm import Arm
from gherkin.model.base import RotatingBase
from gherkin.model.common import Rotation, Goal, DIRECTION, SPEED


@dataclass()
class Robot(ThreadingActor):
    """
    A controller for a number of different motorized parts working in concert to reach a goal/perform an actioon

    Args:
        arm: A double jointed arm responsible for reaching in a 2d space
        base: A base capable of rotating 360 degrees in order to reach a goal in 3d space
    """
    id: str = field(default_factory=lambda: str(uuid.uuid1())[:8])
    arm: Arm = field(default_factory=Arm)
    base: RotatingBase = field(default_factory=RotatingBase)

    def __post_init__(self):
        super().__init__()

    def reach(self, goal: Goal, vis=None) -> Tuple[str, Goal, bool]:
        """
        Given a goal with (x, y, angle) coordinates, manipulate the various parts of the robot until the goal is reached
        If a visualizer is given, this also updates the visualization of the process
        Args:
            goal: a representation of the desired location of the end position of the robot arm
            vis: an optional visualizer component for the robot to keep updated

        Returns:

        """
        print(f"{self.id} recieved goal: {goal}")
        found_angle = False
        success = False
        goal = self._evaluate_goal(goal)
        goal_theta_0, goal_theta_1 = self.arm.inverse(goal.x, goal.y)

        while not success:
            # Step the controller
            if not self._check_angle(goal):
                rotation = self._determine_rotation(goal) if not found_angle else None
                if rotation:
                    self._rotate(rotation)

            else:
                try:
                    self._move_arm(goal_theta_0, goal_theta_1)
                    success = self._check_success(goal)
                except Exception as e:
                    return self.id, goal, False

            if vis:
                vis.update_display(self, goal, success)
        self.arm.reset()
        return self.id, goal, True

    def _check_success(self, goal: Goal) -> bool:
        """
        Check that robot's joint 2 is very close to the goal.
        Don't not use exact comparison, to be robust to floating point calculations.
        """

        return np.allclose(self.arm.joint_2_pos(), (goal.x, goal.y), atol=0.25)

    def _check_angle(self, goal: Goal) -> bool:
        """
        Check that the robots angle matches the angle of the goal.
        Because the arm can reach "behind" the point of rotation, reflective angles are functionally equivalent
        """
        return (self.base.angle == goal.angle) or (self.base.angle.inverse == goal.angle)

    def _rotate(self, rotation: Rotation) -> None:
        """
        Tells the robot's base to rotate in a specified direction at a specified speed
        Args:
            rotation: the direction and speed of the desired rotation

        Returns:

        """
        self.base.rotate(rotation.direction, rotation.speed)
        time.sleep(self.base.limits.DT)

    def _move_arm(self, goal_theta_0, goal_theta_1) -> None:
        """
        Given the difference between current position and the goal, instructs the arm joints to move towards the goal
        Args:
            goal_theta_0:
            goal_theta_1:

        Returns:

        """
        theta_0_error = goal_theta_0 - self.arm.theta_0
        theta_1_error = goal_theta_1 - self.arm.theta_1
        self.arm.theta_0 += theta_0_error / 10
        self.arm.theta_1 += theta_1_error / 10

        time.sleep(self.arm.limits.DT)

    def _determine_rotation(self, goal: Goal) -> Rotation:
        """
        Determines the ideal direction (clockwise or counterclockwise and speed (based on the robots limits)
        to rotate the base in order to reach the goal.
        Args:
            goal: a representation of the desired location of the end position of the robot arm
        Returns:

        """
        direction = DIRECTION.CLOCKWISE if ((goal.angle - self.base.angle).angle % 360 < 180) else DIRECTION.COUNTER_CLOCKWISE

        difference = abs(self.base.angle.angle - goal.angle.angle)
        speed = SPEED.FAST if difference > self.base.limits.FAST_ROTATION_SPEED else SPEED.FINE

        return Rotation(direction, speed)

    def _evaluate_goal(self, goal: Goal) -> Goal:
        """
        This is to handle the concept of "facing" when it comes to the angle of rotation
        Without this transformation, negative x values (spatially understood as "behind") at angles
        that would cause the robot to rotate counterclockwise (any angle over 90 degrees) would
        result in a nonsensical result (rotating "behind" and reaching "forward" for a -x value)
        """

        optimal_angle = goal.angle if self.base.angle + 90 > goal.angle else goal.angle.inverse
        goal = Goal(
            x=(-goal.x) if optimal_angle.angle > 180 and goal.x < 0 else goal.x,
            y=goal.y,
            angle=optimal_angle
        )

        return goal
