# Edge extends Entity

import math
import pygame

from Entity import Entity
from settings import ( 
    WHITE,
    EDGE_WIDTH,
    EDGE_WEIGHT_OFFSET,
    EDGE_CLICK_ZONE
    )

class Edge(Entity):
    def __init__(self, u, v, colour=WHITE, update=None, weight=math.inf):
        super().__init__(colour=colour, update=update)
        self.u = u # Start node
        self.v = v # End node
        self.weight = weight

        self.mouse.is_clicked = self._is_clicked

    def _is_clicked(self):
        mouse_pos = self.engine.get_mouse_pos()

        # Calculate the length of the line segment
        line_length = math.hypot(self.v.pos[0] - self.u.pos[0], self.v.pos[1] - self.u.pos[1])
                
        # Calculate the midpoint of the line segment
        mid_point = self.__midpoint(self.u.pos, self.v.pos)
                
        range_width = line_length - (EDGE_CLICK_ZONE * 2)

        # Calculate the distance from the click position to the line itself
        distance_to_line = self.__point_to_line_distance(mouse_pos, self.u.pos, self.v.pos)

        # Check if the click position falls within the range around the midpoint
        # and if the distance to the line is within a reasonable threshold
        if (mid_point[0] - range_width / 2 <= mouse_pos[0] <= mid_point[0] + range_width / 2) and \
        (mid_point[1] - range_width / 2 <= mouse_pos[1] <= mid_point[1] + range_width / 2) and \
        (distance_to_line <= 10):  # Adjust this threshold as needed
            return True
        return False

    def draw(self):
        if self.weight is not math.inf:
            # Calculate midpoint of the edge
            midpoint = self.__midpoint(self.v.pos, self.u.pos)

            # Calculate angle of the edge
            angle = math.atan2(self.v.pos[1] - self.u.pos[1], self.v.pos[0] - self.u.pos[0])

            # Calculate offset from the midpoint perpendicular to the edge
            offset_x = EDGE_WEIGHT_OFFSET * math.sin(angle)
            offset_y = -EDGE_WEIGHT_OFFSET * math.cos(angle)

            # Calculate endpoint for the perpendicular line
            perp_endpoint = (int(midpoint[0] + offset_x), int(midpoint[1] + offset_y))

            # Draw the text
            text = str(self.weight)
            font = pygame.font.SysFont(None, 20)
            text_surface = font.render(text, True, self.colour)
            self.engine._screen.blit(text_surface, perp_endpoint)

        # Draw the main line
        pygame.draw.line(self.engine._screen, self.colour, self.u.pos, self.v.pos, EDGE_WIDTH)

    # Method to calculate the distance between a point and a line segment
    def __point_to_line_distance(self, point, line_start, line_end):
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
    def __midpoint(self, line_start, line_end):
        return ((line_start[0] + line_end[0]) // 2, (line_start[1] + line_end[1]) // 2)
    
    def _update(self):
        self.mouse._update()

        if self.update is not None:
            self.update(self)
        self._reset()

    def _reset(self):
        self.mouse._reset()