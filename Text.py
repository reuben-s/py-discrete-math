# Text extends Entity

import pygame

from Entity import Entity
from settings import ( WHITE )

class Text(Entity):
    def __init__(self, text, pos=(0,0), colour=WHITE, font=None, font_size=18, update=None):
        super().__init__(pos=pos, colour=colour, update=update)
        self.text = text
        self.font = pygame.font.Font(font, font_size)

    def draw(self):
        # Render the text
        text_surface = self.font.render(self.text, True, WHITE)
        
        # Get the rectangle of the text surface
        text_rect = text_surface.get_rect()
        text_rect.topleft = self.pos
        
        # Blit the text onto the screen
        self.engine._screen.blit(text_surface, text_rect)

    def _update(self):
        if self.update is not None:
            self.update(self)
        self._reset()

    def _reset(self):
        pass