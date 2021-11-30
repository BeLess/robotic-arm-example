from typing import Tuple

import pytest

from gherkin.common import Goal, Angle


def test_goal_subtraction():
    goal1: Goal = Goal(x=30, y=-12, angle=Angle(127))
    goal2: Goal = Goal(x=-10, y=50, angle=Angle(90))
    expected: Tuple[float, float, Angle] = (40, 62, Angle(37))
    assert goal1-goal2 == expected


def test_goal_subtraction_error():
    goal1: Goal = Goal(x=30, y=-12, angle=Angle(127))
    goal2: Tuple[float, float, Angle] = (40, 62, Angle(37))
    with pytest.raises(TypeError):
        goal1-goal2
