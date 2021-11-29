import pprint
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict

import pykka
from pykka import ActorProxy

from gherkin.model import Robot, Goal
from gherkin.model.common import Result
from gherkin.util import Visualizer


@dataclass
class FleetManager:
    robots: List[ActorProxy]
    visualizer: Visualizer
    id_robot: Dict[str, ActorProxy] = field(default_factory=defaultdict)
    robot_goals: Dict[str, List[Goal]] = field(default_factory=dict)
    work: List = field(default_factory=list)

    def __post_init__(self):
        for robot in self.robots:
            self.id_robot[robot.id.get()] = robot

    def receive_goals(self, goals: List[Goal]):
        for goal in goals:
            robot_id = self._select_robot(goal)
            self.robot_goals[robot_id].append(goal)
            self.work.append(self.id_robot[robot_id].reach(goal, self.visualizer))
        results: List[Result] = list(pykka.get_all(self.work))
        results_dict: Dict[str, List[Result]] = defaultdict(list)
        for result in results:
            results_dict[result.robot_id].append(result)

        self.visualizer.cleanup()
        pykka.ActorRegistry.stop_all()
        pprint.pprint(results_dict)

    def _select_robot(self, goal: Goal):
        for robot_id in self.id_robot.keys():
            if not self.robot_goals.get(robot_id):
                self.robot_goals[robot_id] = []
                return robot_id

        overworked = max(self.robot_goals.items(), key=(lambda value: len(value[1])))
        robots_with_headroom = dict(self.robot_goals)
        del robots_with_headroom[overworked[0]]
        robot_id, previous_goal = min(self.robot_goals.items(), key=(lambda value: value[1][-1] - goal))
        return robot_id
