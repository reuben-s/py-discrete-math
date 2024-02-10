# Node extends Entity

from pygame import gfxdraw

from Entity import Entity
from Edge import Edge
from settings import (
    WHITE, 
    RADIUS
    )

class Node(Entity):
    def __init__(self, pos, colour=WHITE, radius=RADIUS, update=None):
        super().__init__(pos=pos, colour=colour, update=update)
        self.radius = radius

        self.mouse.is_clicked = self._is_clicked

    def _is_clicked(self):
        # Check if node is being clicked
        mouse_pos = self.engine.get_mouse_pos()
        distance_squared = (self.pos[0] - mouse_pos[0])**2 + (self.pos[1] - mouse_pos[1])**2
        return True if (distance_squared <= self.radius**2) else False

    def draw(self):
        #pygame.draw.circle(self.engine._screen, self.colour, self.pos, self.radius)
        gfxdraw.filled_circle(self.engine._screen, self.pos[0], self.pos[1], self.radius + 2, self.colour)
        gfxdraw.aacircle(self.engine._screen, self.pos[0], self.pos[1], self.radius + 2, self.colour)

    def _update(self):
        self.mouse._update()

        if self.update is not None:
            self.update(self)
        self._reset()

    def _reset(self):
        self.mouse._reset()

    def delete(self):
        self._delete = True
        # Remove all edges connected to node
        entities_copy = self.engine._entities[:]
        for entity in filter(lambda entity: type(entity) == Edge, entities_copy):
            if entity.u == self or entity.v == self:
                self.engine._entities.remove(entity)
        # Reset cache
        self.engine.cache["pending_node"] = None