# Entity class represents an object within the game

from settings import RED

class Entity:
    def __init__(self, pos=None, colour=RED, update=None):
        self.engine = None
        self.pos = pos
        self.colour = colour
        self.update = update
        
        self._delete = False

    def delete(self):
        self._delete = True

    def _is_clicked(self):
        return False

    # Classes which extend Entity must implement these methods

    def draw(self):
        pass

    def _update(self):
        pass

    def _reset(self):
        pass