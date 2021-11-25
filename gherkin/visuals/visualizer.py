from typing import Tuple, Optional

import pygame
from numpy.lib import math

from gherkin.model import World, Robot, Rotation


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
        self.screen = pygame.display.set_mode((world.width, world.height + 100))
        pygame.display.set_caption('Gherkin Challenge')
        self.font = pygame.font.SysFont('freesansbolf.tff', 30)

    def display_world(self) -> None:
        """
        Display the world
        """
        goal = self.world.convert_to_display((self.world.goal.x, self.world.goal.y))
        pygame.draw.circle(self.screen, self.RED, goal, 6)


    def display_robot(self, robot: Robot, rotation: Optional[Rotation]) -> None:
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
        self.draw_rotation_indicator(robot)

    def draw_rotation_indicator(self, robot):
        """
        Draws a line to show the rotation of the robot arm as if from above, to indicate the it's planar angle
        """
        text = self.font.render('Rotating:', True, self.BLACK)
        self.screen.blit(text, (1, self.world.height + 50))
        center = (130, self.world.height + 60)
        radar_len = 25
        x1 = center[0] + math.cos(math.radians(robot.angle.inverse.angle)) * radar_len
        y1 = center[1] + math.sin(math.radians(robot.angle.inverse.angle)) * radar_len
        x2 = center[0] + math.cos(math.radians(robot.angle.angle)) * radar_len
        y2 = center[1] + math.sin(math.radians(robot.angle.angle)) * radar_len
        pygame.draw.circle(self.screen, self.BLACK, center, 4)
        pygame.draw.line(self.screen, self.BLACK, (x1, y1), (x2, y2), 3)

    def update_display(self, robot: Robot, success: bool, rotation: Optional[Rotation]) -> bool:
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

        self.display_robot(robot, rotation)

        if success:
            text = self.font.render('Success!', True, self.BLACK)
            self.screen.blit(text, (1, 1))

        pygame.display.flip()

        return True

    def cleanup(self) -> None:
        pygame.quit()