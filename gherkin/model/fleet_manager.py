import pprint
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict

import pykka
from pykka import ActorProxy

from gherkin.model import Goal
from gherkin.model.common import Result
from gherkin.util import Visualizer


@dataclass
class FleetManager:
    """
    A class responsible for overseeing the distribution of work between a fleet of robots and receiving
    and handling their output.

    Args:
        robots: A list of ActorProxies of the robots in use
        visualizer: a visualizer to show the robots' progress
        id_robot: A mapping of robot proxy to its id for easy access
        robot_goals: A mapping of robot id to the goals they have been assigned
        work: A list of futures to be handled

    Note:
        id_robot and robot_goals are mapped by id in the __post_init__ because retrieving the ID from the robot
        in the middle of processing is a blocking call and produces weird behavior
    """
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
            self._assign_goal(goal)
        self._handle_results()

    def receive_goal(self, goal: Goal):
        self._assign_goal(goal)

    def _handle_results(self):
        """
        Joins the various futures of all the robots' work to produce an output once all work is completed
        Returns:

        """
        results: List[Result] = list(pykka.get_all(self.work))
        results_dict: Dict[str, List[Result]] = defaultdict(list)
        for result in results:
            results_dict[result.robot_id].append(result)
        self.visualizer.cleanup()
        pykka.ActorRegistry.stop_all()
        pprint.pprint(results_dict)

    def _assign_goal(self, goal):
        """
        Assigns the given goal to the robot who will be in the best position to reach it
        Args:
            goal: the desired end location of the robot arm

        Returns:

        """
        robot_id = self._select_robot(goal)
        self.robot_goals[robot_id].append(goal)
        self.work.append(self.id_robot[robot_id].reach(goal, self.visualizer))

    def _select_robot(self, goal: Goal) -> str:
        """
        Determines which robot in the fleet will best suited to reach the given goal, based on where it will be before
        attempting the action, and the balancing of work between the other robots.
        Args:
            goal: the desired end location of the robot arm

        Returns: the id of the robot that should be assigned this goal

        """
        for robot_id in self.id_robot.keys():
            if not self.robot_goals.get(robot_id):
                self.robot_goals[robot_id] = []
                return robot_id

        overworked = max(self.robot_goals.items(), key=(lambda value: len(value[1])))
        robots_with_headroom = dict(self.robot_goals)
        del robots_with_headroom[overworked[0]]
        robot_id, previous_goal = min(robots_with_headroom.items(), key=(lambda value: value[1][-1] - goal))
        return robot_id
