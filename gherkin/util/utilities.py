import numpy as np

from gherkin.common import Angle, Goal
from gherkin.model import World
from gherkin.util.visualizer import Visualizer


def generate_random_goal(min_radius: float, max_radius: float) -> Goal:
    """
    Generate a random goal that is reachable by the robot arm
    """
    # Ensure theta is not 0
    theta = (np.random.random() + np.finfo(float).eps) * 2 * np.pi
    # Ensure point is reachable
    r = np.random.uniform(low=min_radius, high=max_radius)

    x = int(r * np.cos(theta))
    y = int(r * np.sin(theta))
    angle = Angle(np.random.randint(low=0, high=180))
    return Goal(x, y, angle)


def generate_visualizer(num_robots: int):
    """
    Generates a Visualizer object with parameters based on the number of robots
    Args:
        num_robots: how many robots will be in the fleet

    Returns: A visualizer object built for the current problem space
    Notes:
        Currently only scales horizontally.

    """
    height = 300
    robot_width = 300
    total_width = robot_width * num_robots
    robot_origins = [(int(robot_width / 2) + (robot_width * i), int(height / 2)) for i in range(num_robots)]
    world = World(total_width, robot_width, height, robot_origins)
    vis = Visualizer(world)
    return vis