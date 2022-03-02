import time

import numpy as np
from dataclasses import dataclass, field

from gherkin.model.arm import Arm
from gherkin.model.base import RotatingBase
from gherkin.model.common import Rotation, Goal, DIRECTION, SPEED


@dataclass()
class Robot:
    arm: Arm = field(default_factory=Arm)
    base: RotatingBase = field(default_factory=RotatingBase)

    def reach(self, goal: Goal, vis) -> None:
        found_angle = False
        success = False
        goal = self._evaluate_goal(goal)
        goal_theta_0, goal_theta_1 = self.arm.inverse(goal.x, goal.y)

        while not success:
            # Step the controller
            if not found_angle:
                rotation = self._determine_rotation(goal) if not found_angle else None
                if rotation:
                    self._rotate(rotation)
                    found_angle = self._check_angle(goal)

            else:
                self._move_arm(goal_theta_0, goal_theta_1)
                success = self._check_success(goal)

            # Update the display
            vis.update_display(self, goal, success)

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

    def _rotate(self, rotation: Rotation):
        self.base.rotate(rotation.direction, rotation.speed)
        time.sleep(self.base.limits.DT)

    def _move_arm(self, goal_theta_0, goal_theta_1):
        theta_0_error = goal_theta_0 - self.arm.theta_0
        theta_1_error = goal_theta_1 - self.arm.theta_1
        self.arm.theta_0 += theta_0_error / 10
        self.arm.theta_1 += theta_1_error / 10

        time.sleep(self.arm.limits.DT)

        return Robot

    def _determine_rotation(self, goal: Goal) -> Rotation:
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
