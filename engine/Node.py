# Node extends entity

import pygame

from Entity import Entity
from settings import (RED, RADIUS)

class Node(Entity):
    def __init__(self, window, pos, colour=RED, radius=RADIUS, update=None):
        super().__init__(window, pos, colour)
        self.radius = radius
        self.update = update
        self.clicked = False

    def _is_clicked(self):
        # Check if node is being clicked
        mouse_pos = pygame.mouse.get_pos()
        distance_squared = (self.pos[0] - mouse_pos[0])**2 + (self.pos[1] - mouse_pos[1])**2
        if (distance_squared <= self.radius**2):
            self.clicked = True
        return self.clicked

    def draw(self):
        pygame.draw.circle(self._window._screen, self.colour, self.pos, self.radius)
