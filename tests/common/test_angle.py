from gherkin.common import Angle


def test_angle_increase_simple_angle():
    angle1: Angle = Angle(5)
    angle2: Angle = Angle(10)
    expected: Angle = Angle(15)
    assert angle1 + angle2 == expected


def test_angle_increase_simple_int():
    angle1: Angle = Angle(5)
    angle2: int = 10
    expected: Angle = Angle(15)
    assert angle1 + angle2 == expected


def test_angle_increase_rollover_angle():
    angle1: Angle = Angle(300)
    angle2: Angle = Angle(90)
    expected: Angle = Angle(30)
    assert angle1 + angle2 == expected


def test_angle_increase_rollover_int():
    angle1: Angle = Angle(300)
    angle2: int = 90
    expected: Angle = Angle(30)
    assert angle1 + angle2 == expected


def test_angle_decrease_simple_angle():
    angle1: Angle = Angle(10)
    angle2: Angle = Angle(8)
    expected: Angle = Angle(2)
    assert angle1 - angle2 == expected


def test_angle_decrease_simple_int():
    angle1: Angle = Angle(10)
    angle2: int = 8
    expected: Angle = Angle(2)
    assert angle1 - angle2 == expected


def test_angle_decrease_rollover_angle():
    angle1: Angle = Angle(90)
    angle2: Angle = Angle(130)
    expected: Angle = Angle(320)
    assert angle1 - angle2 == expected


def test_angle_decrease_rollover_int():
    angle1: Angle = Angle(90)
    angle2: int = 130
    expected: Angle = Angle(320)
    assert angle1 - angle2 == expected

def test_angle_inverse():
    assert Angle(32).inverse == Angle(212)
