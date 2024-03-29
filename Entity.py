# Entity class represents an object within the game

from settings import RED
from MouseManager import MouseManager

class Entity:
    def __init__(self, pos=None, colour=RED, update=None):
        self.engine = None
        self.pos = pos
        self.colour = colour
        self.update = update
        self.focused = False
        
        self.mouse = MouseManager(self._is_clicked)

        self._delete = False

    def delete(self):
        self._delete = True

    def _is_clicked(self):
        return False

    def _recieve_keypress(self, event):
        return

    # Classes which extend Entity must implement these methods

    def draw(self):
        pass

    def _update(self):
        pass

    def _reset(self):
        pass