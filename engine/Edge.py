# Edge extends Entity

import pygame

from Entity import Entity
from settings import (
    WHITE
)

class Edge(Entity):
    def __init__(self, u, v, colour=WHITE, update=None):
        super().__init__(colour=colour, update=update)
        self.u = u # Start node
        self.v = v # End node

    def _is_clicked(self):
        return False

    def draw(self):
        pygame.draw.line(self.engine._screen, self.colour, self.u.pos, self.v.pos, 3)

    def _update(self):
        if self.update is not None:
            self.update(self)
        self._reset()

    def _reset(self):
        pass