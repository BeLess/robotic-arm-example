from gherkin.common import Rotation, DIRECTION, SPEED, Angle
from gherkin.model.base import RotatingBase


def test_rotating_clockwise_fast():
    base: RotatingBase = RotatingBase(_angle=Angle(90))
    rotation: Rotation = Rotation(DIRECTION.CLOCKWISE, SPEED.FAST)
    expected = Angle(95)
    base.rotate(rotation)
    assert base.angle == expected


def test_rotating_clockwise_fine():
    base: RotatingBase = RotatingBase(_angle=Angle(90))
    rotation: Rotation = Rotation(DIRECTION.CLOCKWISE, SPEED.FINE)
    expected = Angle(91)
    base.rotate(rotation)
    assert base.angle == expected


def test_rotating_counterclockwise_fast():
    base: RotatingBase = RotatingBase(_angle=Angle(90))
    rotation: Rotation = Rotation(DIRECTION.COUNTER_CLOCKWISE, SPEED.FAST)
    expected = Angle(85)
    base.rotate(rotation)
    assert base.angle == expected


def test_rotating_counterclockwise_fine():
    base: RotatingBase = RotatingBase(_angle=Angle(90))
    rotation: Rotation = Rotation(DIRECTION.COUNTER_CLOCKWISE, SPEED.FINE)
    expected = Angle(89)
    base.rotate(rotation)
    assert base.angle == expected