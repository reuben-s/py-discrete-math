# Entity class represents an object within the game

from settings import RED

class Entity:
    def __init__(self, window, pos, colour=RED):
        self._window = window
        self.pos = pos
        self.colour = colour