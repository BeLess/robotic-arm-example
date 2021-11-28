from dataclasses import dataclass, field
from typing import Tuple, List

import numpy as np


@dataclass
class ArmLimits:
    """
    A class responsible for containing the physical limits of a robotic arm
    """
    JOINT_LIMITS: Tuple[float, float] = (-6.28, 6.28)
    MAX_VELOCITY = 15
    MAX_ACCELERATION = 50
    DT = 0.033


@dataclass()
class Arm:
    _theta_0: float = 0  # radians
    _theta_1: float = 0  # radians
    link_1: float = 75.  # pixels
    link_2: float = 50.  # pixels
    all_theta_0: List[float] = field(default_factory=list)
    all_theta_1: List[float] = field(default_factory=list)
    limits: ArmLimits = field(default_factory=ArmLimits)

    @property
    def theta_0(self) -> float:
        return self._theta_0

    @theta_0.setter
    def theta_0(self, value: float) -> None:
        self.all_theta_0.append(value)
        self._theta_0 = value

    @property
    def theta_1(self) -> float:
        return self._theta_1

    @theta_1.setter
    def theta_1(self, value: float) -> None:
        self.all_theta_1.append(value)
        self._theta_1 = value

    def joint_1_pos(self) -> Tuple[float, float]:
        """
        Compute the x, y position of joint 1
        """
        return self.link_1 * np.cos(self.theta_0), self.link_1 * np.sin(self.theta_0)

    def joint_2_pos(self) -> Tuple[float, float]:
        """
        Compute the x, y position of joint 2
        """
        return self.forward(self.theta_0, self.theta_1)

    @classmethod
    def forward(cls, theta_0: float, theta_1: float) -> Tuple[float, float]:
        """
        Compute the x, y position of the end of the links from the joint angles
        """
        x = cls.link_1 * np.cos(theta_0) + cls.link_2 * np.cos(theta_0 + theta_1)
        y = cls.link_1 * np.sin(theta_0) + cls.link_2 * np.sin(theta_0 + theta_1)

        return x, y

    @classmethod
    def inverse(cls, x: float, y: float) -> Tuple[float, float]:
        """
        Compute the joint angles from the position of the end of the links
        """
        theta_1 = np.arccos((x ** 2 + y ** 2 - cls.link_1 ** 2 - cls.link_2 ** 2)
                            / (2 * cls.link_1 * cls.link_2))
        theta_0 = np.arctan2(y, x) - \
            np.arctan((cls.link_2 * np.sin(theta_1)) /
                      (cls.link_1 + cls.link_2 * np.cos(theta_1)))

        return theta_0, theta_1

    @classmethod
    def min_reachable_radius(cls) -> float:
        return max(cls.link_1 - cls.link_2, 0)

    @classmethod
    def max_reachable_radius(cls) -> float:
        return cls.link_1 + cls.link_2


