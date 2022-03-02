from gherkin.common import Angle, Goal, DIRECTION, Rotation, SPEED
from gherkin.model import Robot
from gherkin.model.base import RotatingBase


def test_check_angle_match():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(190)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(190))
    assert robot._check_angle(goal)


def test_check_angle_inverse():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(190)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(10))
    assert robot._check_angle(goal)


def test_check_angle_mismatch():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(190)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(180))
    assert not robot._check_angle(goal)


def test_determine_rotation_clockwise_obvious_fast():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(190)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(225))
    expected: Rotation = Rotation(DIRECTION.CLOCKWISE, SPEED.FAST)
    assert robot._determine_rotation(goal) == expected


def test_determine_rotation_clockwise_obvious_fine():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(190)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(193))
    expected: Rotation = Rotation(DIRECTION.CLOCKWISE, SPEED.FINE)
    assert robot._determine_rotation(goal) == expected


def test_determine_rotation_counterclockwise_obvious_fast():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(190)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(175))
    expected: Rotation = Rotation(DIRECTION.COUNTER_CLOCKWISE, SPEED.FAST)
    assert robot._determine_rotation(goal) == expected


def test_determine_rotation_counterclockwise_obvious_fine():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(190)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(186))
    expected: Rotation = Rotation(DIRECTION.COUNTER_CLOCKWISE, SPEED.FINE)
    assert robot._determine_rotation(goal) == expected


def test_determine_rotation_clockwise_cross_horizon_fast():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(300)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(20))
    expected: Rotation = Rotation(DIRECTION.CLOCKWISE, SPEED.FAST)
    assert robot._determine_rotation(goal) == expected


def test_determine_rotation_clockwise_cross_horizon_fine():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(359)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(1))
    expected: Rotation = Rotation(DIRECTION.CLOCKWISE, SPEED.FINE)
    assert robot._determine_rotation(goal) == expected


def test_determine_rotation_counterclockwise_cross_horizon_fast():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(60)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(300))
    expected: Rotation = Rotation(DIRECTION.COUNTER_CLOCKWISE, SPEED.FAST)
    assert robot._determine_rotation(goal) == expected


def test_determine_rotation_counterclockwise_cross_horizon_fine():
    robot: Robot = Robot(offset=1, base=RotatingBase(_angle=Angle(2)))
    goal: Goal = Goal(x=0, y=0, angle=Angle(358))
    expected: Rotation = Rotation(DIRECTION.COUNTER_CLOCKWISE, SPEED.FINE)
    assert robot._determine_rotation(goal) == expected


def test_evaluate_goal_no_change():
    robot: Robot = Robot(1)
    goal: Goal = Goal(x=50, y=50, angle=Angle(45))
    assert robot._evaluate_goal(goal) == goal

def test_evaluate_goal_optimal_angle_is_inverted():
    robot: Robot = Robot(1)
    goal: Goal = Goal(x=50, y=50, angle=Angle(270))
    expected: Goal = Goal(x=50, y=50, angle=Angle(90))
    assert robot._evaluate_goal(goal) == expected

def test_evaluate_goal_change_facing_given_angle():
    robot: Robot = Robot(1)
    goal: Goal = Goal(x=-50, y=50, angle=Angle(350))
    expected: Goal = Goal(x=50, y=50, angle=Angle(350))
    assert robot._evaluate_goal(goal) == expected

def test_evaluate_goal_change_facing_inverse_angle():
    robot: Robot = Robot(1)
    goal: Goal = Goal(x=50, y=50, angle=Angle(170))
    expected: Goal = Goal(x=-50, y=50, angle=Angle(350))
    assert robot._evaluate_goal(goal) == expected