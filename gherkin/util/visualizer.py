from typing import Tuple

import pygame
from numpy.lib import math

from gherkin.model import World, Robot, Goal


class Visualizer:
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)

    def __init__(self, world: World) -> None:
        """
        Note: while the Robot and World have the origin in the center of the
        visualization, rendering places (0, 0) in the top left corner.
        """
        pygame.init()
        pygame.font.init()
        self.world = world
        self.screen = pygame.display.set_mode((world.total_width, world.height + 100))
        pygame.display.set_caption('Gherkin Challenge')
        self.font = pygame.font.SysFont('freesansbolf.tff', 30)

    def display_world(self, goal: Goal, offset: int) -> None:
        """
        Display the world
        """
        goal = self.world.convert_to_display((goal.x, goal.y), offset)
        pygame.draw.circle(self.screen, self.RED, goal, 6)

    def display_robot(self, robot: Robot) -> None:
        """
        Display the robot
        """
        j0 = self.world.robot_origins[robot.offset]
        j1 = self.world.convert_to_display(robot.arm.joint_1_pos(), robot.offset)
        j2 = self.world.convert_to_display(robot.arm.joint_2_pos(), robot.offset)
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

    def draw_rotation_indicator(self, robot: Robot):
        """
        Draws a line to show the rotation of the robot arm as if from above, to indicate the it's planar angle
        """
        text = self.font.render('Rotating:', True, self.BLACK)
        self.screen.blit(text, (1, self.world.height + 50))
        center = (self.world.robot_origins[robot.offset][0], self.world.height + 60)
        line_length = 35
        x1 = center[0] + math.cos(math.radians(robot.base.angle.inverse.angle)) * line_length
        y1 = center[1] + math.sin(math.radians(robot.base.angle.inverse.angle)) * line_length
        x2 = center[0] + math.cos(math.radians(robot.base.angle.angle)) * line_length
        y2 = center[1] + math.sin(math.radians(robot.base.angle.angle)) * line_length
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        pygame.draw.circle(self.screen, self.BLACK, (cx, cy), 4)
        pygame.draw.line(self.screen, self.GREEN, (x1, y1), (cx, cy), 4)
        pygame.draw.line(self.screen, self.RED, (cx, cy), (x2, y2), 4)

    def update_display(self, robot: Robot, goal: Goal, success: bool):
        for event in pygame.event.get():
            # Keypress
            if event.type == pygame.KEYDOWN:
                # Escape key
                if event.key == pygame.K_ESCAPE:
                    return False
            # Window Close Button Clicked
            if event.type == pygame.QUIT:
                return False

        self.screen.fill(self.WHITE, (self.world.robot_width * robot.offset, 0, self.world.robot_width, self.screen.get_height()))

        self.display_world(goal, robot.offset)

        self.display_robot(robot)

        if success:
            text = self.font.render('Success!', True, self.BLACK)
            self.screen.blit(text, (self.world.robot_origins[robot.offset][0]-55, 1))

        pygame.display.flip()

    def cleanup(self) -> None:
        pygame.quit()