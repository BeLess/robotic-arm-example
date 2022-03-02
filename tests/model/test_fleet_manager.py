from typing import List

import pykka
from pykka import ActorProxy

from gherkin.common import Goal, Angle
from gherkin.model import Robot
from gherkin.model.arm import Arm
from gherkin.model.fleet_manager import FleetManager
from gherkin.util import generate_random_goal


def test_robot_assignment_idle_robot():
    goals: List[Goal] = [generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius()) for _ in range(3)]
    robot1: ActorProxy = Robot.start(offset=1, id="1").proxy()
    robot2: ActorProxy = Robot.start(offset=2, id="2").proxy()
    manager: FleetManager = FleetManager(
        robots=[robot1, robot2],
        visualizer=None,
        robot_goals={"2": goals}
    )
    goal: Goal = generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius())
    expected = "1"
    result: str = manager._select_robot(goal)
    pykka.ActorRegistry.stop_all()
    assert result == expected


def test_robot_assignment_ignore_overworked_robot():
    goals: List[Goal] = [generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius()) for _ in range(3)]
    goal1: Goal = generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius())
    goal2: Goal = generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius())
    robot1: ActorProxy = Robot.start(offset=1, id="1").proxy()
    robot2: ActorProxy = Robot.start(offset=2, id="2").proxy()
    robot3: ActorProxy = Robot.start(offset=3, id="3").proxy()
    manager: FleetManager = FleetManager(
        robots=[robot1, robot2, robot3],
        visualizer=None,
        robot_goals={"1": [goal1], "2": goals, "3": [goal2]}
    )
    goal: Goal = generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius())
    result: str = manager._select_robot(goal)
    pykka.ActorRegistry.stop_all()
    assert result != "2"


def test_robot_assignment_closest_goal():
    goal1: Goal = Goal(x=50, y=-75, angle=Angle(135))
    goal2: Goal = Goal(x=-130, y=-12, angle=Angle(32))
    new_goal: Goal = Goal(x=40, y=-62, angle=Angle(96))
    robot1: ActorProxy = Robot.start(offset=1, id="1").proxy()
    robot2: ActorProxy = Robot.start(offset=2, id="2").proxy()
    manager: FleetManager = FleetManager(
        robots=[robot1, robot2],
        visualizer=None,
        robot_goals={"1": [goal1], "2": [goal2]}
    )
    goal: Goal = generate_random_goal(Arm.min_reachable_radius(), Arm.max_reachable_radius())
    result: str = manager._select_robot(new_goal)
    pykka.ActorRegistry.stop_all()
    assert result != "1"
