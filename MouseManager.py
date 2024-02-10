# Abstracts mouse management

import pygame

from settings import (
    HOLDING_TIME, 
    DOUBLE_CLICK_TIME,
    Button
    )

class MouseManager:
    def __init__(self, is_clicked):
        self.is_clicked = is_clicked

        self.mousedown = False    # Is mouse being held over entity?
        self.clicked = False      # Has the button been clicked (Mouse down followed by mouse up)?
        self.holding = False      # Is the mouse being held over the entity (mouse held down for more than HOLDING_TIME)?
        self.button = None        # Mouse button which clicked node
        self.double_click = False # Was entity double clicked?

        self._last_clicked_time = None # Tracks the length of time between mouse down and mouse up
        self._last_mouse_up_time = 0   # Stores the last time the mouse was released

    def _update(self):
        current_time = pygame.time.get_ticks()
        if self._last_clicked_time is not None:
            if current_time - self._last_clicked_time > HOLDING_TIME:
                self.holding = True
            elif current_time - self._last_mouse_up_time < DOUBLE_CLICK_TIME:
                print("Double click")
                self.double_click = True

    def _reset(self):
        if self.clicked:
            self.button = None
            self.double_click = False

        self.clicked = False

    def up(self):
        # Handle mouse button up event
        if self.is_clicked():
            self.clicked = True if not self.holding else False
        
        self.mousedown = False
        self._last_clicked_time = None
        self._last_mouse_up_time = pygame.time.get_ticks()
        self.holding = False

    def down(self, event_button):
        if self.is_clicked():
            if event_button == Button.LEFT_CLICK.value:
                self.button = Button.LEFT_CLICK
            elif event_button == Button.RIGHT_CLICK.value:
                self.button = Button.RIGHT_CLICK

            if not self.mousedown:
                self._last_clicked_time = pygame.time.get_ticks()

            self.mousedown = True

            return True
        else:
            return False