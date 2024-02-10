# Node extends Entity

import pygame

from Entity import Entity
from settings import (
    WHITE, 
    RADIUS, 
    HOLDING_TIME, 
    DOUBLE_CLICK_TIME
    )

class Node(Entity):
    def __init__(self, pos, colour=WHITE, radius=RADIUS, update=None):
        super().__init__(pos=pos, colour=colour, update=update)
        self.radius = radius

        self.mousedown = False    # Is mouse being held over node?
        self.clicked = False      # Has the button been clicked (Mouse down followed by mouse up)?
        self.holding = False      # Is the mouse being held over the node (mouse held down for more than HOLDING_TIME)?
        self.button = None        # Mouse button which clicked node
        self.double_click = False # Was node double clicked?

        self._last_clicked_time = None # Tracks the length of time between mouse down and mouse up
        self._last_mouse_up_time = 0

    def _is_clicked(self):
        # Check if node is being clicked
        mouse_pos = self.engine.get_mouse_pos()
        distance_squared = (self.pos[0] - mouse_pos[0])**2 + (self.pos[1] - mouse_pos[1])**2
        return True if (distance_squared <= self.radius**2) else False

    def draw(self):
        pygame.draw.circle(self.engine._screen, self.colour, self.pos, self.radius)

    def _update(self):
        current_time = pygame.time.get_ticks()

        if self._last_clicked_time is not None:
            if current_time - self._last_clicked_time > HOLDING_TIME:
                self.holding = True
            elif current_time - self._last_mouse_up_time < DOUBLE_CLICK_TIME:
                self.double_click = True

        if self._update is not None:
            self.update(self)
        self._reset()

    def _reset(self):
        if self.clicked:
            self.button = None
            self.double_click = False

        self.clicked = False