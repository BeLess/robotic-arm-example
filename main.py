"""
main.py
"""
import time
from typing import Tuple

import numpy as np
import pygame

from gherkin.model.robot import Robot
from gherkin.model.world import World


class Visualizer:
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)

    def __init__(self, world: World) -> None:
        """
        Note: while the Robot and World have the origin in the center of the
        visualization, rendering places (0, 0) in the top left corner.
        """
        pygame.init()
        pygame.font.init()
        self.world = world
        self.screen = pygame.display.set_mode((world.width, world.height))
        pygame.display.set_caption('Gherkin Challenge')
        self.font = pygame.font.SysFont('freesansbolf.tff', 30)

    def display_world(self) -> None:
        """
        Display the world
        """
        goal = self.world.convert_to_display(self.world.goal)
        pygame.draw.circle(self.screen, self.RED, goal, 6)

    def display_robot(self, robot: Robot) -> None:
        """
        Display the robot
        """
        j0 = self.world.robot_origin
        j1 = self.world.convert_to_display(robot.joint_1_pos())
        j2 = self.world.convert_to_display(robot.joint_2_pos())
        # Draw joint 0
        pygame.draw.circle(self.screen, self.BLACK, j0, 4)
        # Draw link 1
        pygame.draw.line(self.screen, self.BLACK, j0, j1, 2)
        # Draw joint 1
        pygame.draw.circle(self.screen, self.BLACK, j1, 4)
        # Draw link 2
        pygame.draw.line(self.screen, self.BLACK, j1, j2, 2)
        # Draw joint 2
        pygame.draw.circle(self.screen, self.BLACK, j2, 4)

    def update_display(self, robot: Robot, success: bool) -> bool:
        for event in pygame.event.get():
            # Keypress
            if event.type == pygame.KEYDOWN:
                # Escape key
                if event.key == pygame.K_ESCAPE:
                    return False
            # Window Close Button Clicked
            if event.type == pygame.QUIT:
                return False

        self.screen.fill(self.WHITE)

        self.display_world()

        self.display_robot(robot)

        if success:
            text = self.font.render('Success!', True, self.BLACK)
            self.screen.blit(text, (1, 1))

        pygame.display.flip()

        return True

    def cleanup(self) -> None:
        pygame.quit()


class Controller:
    def __init__(self, goal: Tuple[int, int]) -> None:
        self.goal = goal
        self.goal_theta_0, self.goal_theta_1 = Robot.inverse(self.goal[0], self.goal[1])

    def step(self, robot: Robot) -> Robot:
        """
        Simple P controller
        """
        theta_0_error = self.goal_theta_0 - robot.theta_0
        theta_1_error = self.goal_theta_1 - robot.theta_1

        robot.theta_0 += theta_0_error / 10
        robot.theta_1 += theta_1_error / 10

        return robot


class Runner:
    def __init__(
        self,
        robot: Robot,
        controller: Controller,
        world: World,
        vis: Visualizer
    ) -> None:
        self.robot = robot
        self.controller = controller
        self.world = world
        self.vis = vis

    def run(self) -> None:
        running = True

        while running:
            # Step the controller
            self.robot = self.controller.step(self.robot)

            # Check collisions
            # TODO

            # Check success
            success = self.check_success(self.robot, self.world.goal)

            # Update the display
            running = self.vis.update_display(self.robot, success)

            # sleep for Robot DT seconds, to force update rate
            time.sleep(self.robot.limits.DT)

    @staticmethod
    def check_success(robot: Robot, goal: Tuple[int, int]) -> bool:
        """
        Check that robot's joint 2 is very close to the goal.
        Don't not use exact comparision, to be robust to floating point calculations.
        """
        return np.allclose(robot.joint_2_pos(), goal, atol=0.25)

    def cleanup(self) -> None:
        self.vis.cleanup()


def generate_random_goal(min_radius: float, max_radius: float) -> Tuple[int, int]:
    """
    Generate a random goal that is reachable by the robot arm
    """
    # Ensure theta is not 0
    theta = (np.random.random() + np.finfo(float).eps) * 2 * np.pi
    # Ensure point is reachable
    r = np.random.uniform(low=min_radius, high=max_radius)

    x = int(r * np.cos(theta))
    y = int(r * np.sin(theta))

    return x, y


def main() -> None:
    height = 300
    width = 300

    robot_origin = (int(width / 2), int(height / 2))
    goal = generate_random_goal(Robot.min_reachable_radius(), Robot.max_reachable_radius())

    robot = Robot()
    controller = Controller(goal)
    world = World(width, height, robot_origin, goal)
    vis = Visualizer(world)

    runner = Runner(robot, controller, world, vis)

    try:
        runner.run()
    except AssertionError as e:
        print(f'ERROR: {e}, Aborting.')
    except KeyboardInterrupt:
        pass
    finally:
        runner.cleanup()


if __name__ == '__main__':
    main()
