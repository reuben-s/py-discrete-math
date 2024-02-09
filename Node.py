import pygame
from constants import WHITE, RADIUS

class Node:
    def __init__(self, pos, radius=RADIUS, colour=WHITE):
        self.pos = pos
        self.colour = colour
        self.radius = radius
        self.dragging = True

    def is_clicked(self, mouse_pos):
        # Check if the mouse click is within the node.
        distance_squared = (self.pos[0] - mouse_pos[0])**2 + (self.pos[1] - mouse_pos[1])**2
        return distance_squared <= self.radius**2

    def set_dragging(self, value):
        # Set the dragging state of the node.
        self.dragging = value

    def is_dragging(self):
        # Check if the node is being dragged.
        return self.dragging

    def set_position(self, new_pos):
        # Set the position of the node.
        self.pos = new_pos

    def draw(self, screen):
        # Draw the node on the screen.
        pygame.draw.circle(screen, self.colour, self.pos, self.radius)
