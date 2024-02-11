# Textbox extends Entity

import pygame

from Entity import Entity
from settings import ( 
    WHITE, 
    HEIGHT,
    WIDTH, 
    TEXTBOX_HEIGHT, 
    TEXTBOX_WIDTH, 
    TEXTBOX_MARGIN 
    )

class Textbox(Entity):
    def __init__(self, placeholder="", colour=WHITE, update=None, input=None):
        super().__init__(colour=colour, update=update)
        self.font = pygame.font.Font(None, 32)
        self.placeholder = placeholder
        self.text = self.placeholder
        self.input = input

        self.hide_placeholder = False
        self.entered = False

        # Dimensions of textbox
        self.textbox_x = WIDTH - TEXTBOX_WIDTH - TEXTBOX_MARGIN
        self.textbox_y = HEIGHT - TEXTBOX_HEIGHT - TEXTBOX_MARGIN

        # Textbox
        self.textbox_rect = pygame.Rect(self.textbox_x, self.textbox_y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT)

        self.mouse.is_clicked = self._is_clicked

    def _recieve_keypress(self, event):
        if self._delete:
            return

        match event.key:
            case pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            case _:
                if event.key == pygame.K_RETURN:
                    self.entered = True

                if self.input is not None:
                    self.input(self, event.unicode)
                else:
                    self.text += event.unicode

    def _is_clicked(self):
        # Check if textbox is being clicked
        mouse_pos = self.engine.get_mouse_pos()
        return self.textbox_rect.collidepoint(mouse_pos)

    def draw(self):
        # Render textbox
        pygame.draw.rect(self.engine._screen, self.colour, self.textbox_rect, 2)
        if self.text:
            text_surface = self.font.render(self.text, True, self.colour)
            self.engine._screen.blit(text_surface, (self.textbox_rect.x + 5, self.textbox_rect.y + 5))

    def reset_input(self):
        self.text = self.placeholder
        self.hide_placeholder = False

    def _reset(self):
        pass

    def _update(self):
        # Built in logic to handle user interaction with Textbox
        if self.focused and not self.hide_placeholder:
            self.hide_placeholder = True
            self.text = ""
        elif self.text == "" and not self.focused:
            self.text = self.placeholder
            self.hide_placeholder = False

        self.mouse._update()

        if self.update is not None:
            self.update(self)
        self._reset()

    def _reset(self):
        self.mouse._reset()