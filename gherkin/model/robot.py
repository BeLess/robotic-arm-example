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
        running = True
        found_angle = False
        success= False
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
        return (self.base.angle == goal.angle) or ((self.base.angle - 180) == goal.angle)

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
        difference_cw = abs(self.base.angle.angle - goal.angle.angle)
        difference_ccw = abs(self.base.angle.inverse.angle - goal.angle.angle)
        direction, difference = (DIRECTION.CLOCKWISE, difference_cw) if difference_cw < difference_ccw \
            else (DIRECTION.COUNTER_CLOCKWISE, difference_ccw)
        speed = SPEED.FAST if difference > self.base.limits.FAST_ROTATION_SPEED else SPEED.FINE

        return Rotation(direction, speed)
