import numpy as np

from gherkin.model import Goal, Angle


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
