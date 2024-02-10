# Node extends entity

import pygame

from Entity import Entity
from settings import (RED, RADIUS, HOLDING_TIME)

class Node(Entity):
    def __init__(self, window, pos, colour=RED, radius=RADIUS, update=None):
        super().__init__(window, pos, colour)
        self.radius = radius
        self.update = update

        self.mousedown = False # Is mouse being held over node?
        self.clicked = False   # Has the button been clicked (Mouse down followed by mouse up)?
        self.holding = False   # Is the mouse being held over the node (mouse held down for more than 50ms)?
        self.button = None     # Mouse button which clicked node

        self._last_clicked_time = None # Tracks the length of time between mouse down and mouse up

    def _is_clicked(self):
        # Check if node is being clicked
        mouse_pos = self._window.get_mouse_pos()
        distance_squared = (self.pos[0] - mouse_pos[0])**2 + (self.pos[1] - mouse_pos[1])**2
        return True if (distance_squared <= self.radius**2) else False

    def draw(self):
        pygame.draw.circle(self._window._screen, self.colour, self.pos, self.radius)

    def _update(self):
        if self._last_clicked_time is not None:
            if pygame.time.get_ticks() - self._last_clicked_time > HOLDING_TIME:
                self.holding = True

        self.update(self)
        self._reset()

    def _reset(self):
        if self.clicked:
            self.button = None

        self.clicked = False