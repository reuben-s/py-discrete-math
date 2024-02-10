# Edge extends Entity

import math
import pygame
from pygame import gfxdraw

from Entity import Entity
from settings import (
    WHITE,
    HOLDING_TIME, 
    DOUBLE_CLICK_TIME
)

class Edge(Entity):
    def __init__(self, u, v, colour=WHITE, update=None):
        super().__init__(colour=colour, update=update)
        self.u = u # Start node
        self.v = v # End node

        self.mousedown = False    # Is mouse being held over node?
        self.clicked = False      # Has the button been clicked (Mouse down followed by mouse up)?
        self.holding = False      # Is the mouse being held over the node (mouse held down for more than HOLDING_TIME)?
        self.button = None        # Mouse button which clicked node
        self.double_click = False # Was node double clicked?

        self._last_clicked_time = None # Tracks the length of time between mouse down and mouse up
        self._last_mouse_up_time = 0

    def _is_clicked(self):
        mouse_pos = self.engine.get_mouse_pos()

        # Calculate the length of the line segment
        line_length = math.hypot(self.v.pos[0] - self.u.pos[0], self.v.pos[1] - self.u.pos[1])
                
        # Calculate the midpoint of the line segment
        mid_point = self._midpoint(self.u.pos, self.v.pos)
                
        range_width = line_length - 20 # 10px clearance either side of line

        # Calculate the distance from the click position to the line itself
        distance_to_line = self._point_to_line_distance(mouse_pos, self.u.pos, self.v.pos)

        # Check if the click position falls within the range around the midpoint
        # and if the distance to the line is within a reasonable threshold
        if (mid_point[0] - range_width / 2 <= mouse_pos[0] <= mid_point[0] + range_width / 2) and \
        (mid_point[1] - range_width / 2 <= mouse_pos[1] <= mid_point[1] + range_width / 2) and \
        (distance_to_line <= 10):  # Adjust this threshold as needed
            return True
        return False

    def draw(self):
        pygame.draw.line(self.engine._screen, self.colour, self.u.pos, self.v.pos, 2)

    # Method to calculate the distance between a point and a line segment
    def _point_to_line_distance(self, point, line_start, line_end):
        x1, y1 = line_start
        x2, y2 = line_end
        x0, y0 = point
        
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == dy == 0:  # Line is a point
            return math.hypot(x1 - x0, y1 - y0)

        t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx * dx + dy * dy)
        
        if t < 0:
            px, py = x1, y1
        elif t > 1:
            px, py = x2, y2
        else:
            px, py = x1 + t * dx, y1 + t * dy

        return math.hypot(x0 - px, y0 - py)

    # Method to calculate the midpoint of a line segment
    def _midpoint(self, line_start, line_end):
        return ((line_start[0] + line_end[0]) // 2, (line_start[1] + line_end[1]) // 2)
    
    def _update(self):
        current_time = pygame.time.get_ticks()

        if self._last_clicked_time is not None:
            if current_time - self._last_clicked_time > HOLDING_TIME:
                self.holding = True
            elif current_time - self._last_mouse_up_time < DOUBLE_CLICK_TIME:
                self.double_click = True

        if self.update is not None:
            self.update(self)
        self._reset()

    def _reset(self):
        if self.clicked:
            self.button = None
            self.double_click = False

        self.clicked = False