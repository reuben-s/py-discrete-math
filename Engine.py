import pygame
from settings import (
    WIDTH, 
    HEIGHT, 
    FPS, 
    BLACK,
    Button
    )

class Engine:
    def __init__(
            self,
            width=WIDTH,
            height=HEIGHT,
            bg_colour=BLACK
            ):
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self.bg_colour = bg_colour
        self.clicked = False
        self.button = None

        self.cache = {}

        self._running = True
        self._clicked_entity = None
        self._focused = None
        self._entities = []
    
    def start(self, cb):
        # Main loop
        while self._running:
            # Reset screen
            self._screen.fill(self.bg_colour)
            # Get mouse positions
            self.mouse_pos = pygame.mouse.get_pos()

            self._handle_events()
            self._update_entities()
            self._render_entities()
            cb(self)

            self.clicked = False
            self.button = None

            # Update the display
            pygame.display.flip()
            # Cap the frame rate
            pygame.time.Clock().tick(FPS)

    def _handle_events(self):
        # Handle events
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self._running = False
                case pygame.MOUSEBUTTONDOWN:
                    self._handle_mouse_down(event)
                case pygame.MOUSEBUTTONUP:
                    self._handle_mouse_up(event)
                case pygame.KEYDOWN:
                    self._handle_keydown(event)

    def _handle_mouse_down(self, event):
        # Handle mouse button down event
        for entity in self._entities:
            if entity.mouse.down(event.button):
                self._clicked_entity = entity
                if entity != self._focused:
                    if self._focused is not None:
                        self._focused.focused = False
                    entity.focused = True
                    self._focused = entity
                break
        else:
            if event.button == Button.LEFT_CLICK.value:
                self.button = Button.LEFT_CLICK
            elif event.button == Button.RIGHT_CLICK.value:
                self.button = Button.RIGHT_CLICK
            self.clicked = True

    def _handle_mouse_up(self, event):
        # Handle mouse button up event
        if self._clicked_entity is not None:
            self._clicked_entity.mouse.up()
            self._clicked_entity = None

    def _handle_keydown(self, event):
        # Focused entities will recieve keypress events
        if self._focused is None:
            return
        
        self._focused._recieve_keypress(event)

    def _update_entities(self):
        # Update entities
        for entity in self._entities:
            entity._update()
            if entity._delete:
                self._entities.remove(entity)

    def _render_entities(self):
        # Render entities
        for entity in self._entities:
            entity.draw()

    def set_focused(self, entity):
        entity.focused = True
        if self._focused is not None:
            self._focused.focused = False
        self._focused = entity

    def set_window_title(self, title):
        pygame.display.set_caption(title)

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def new(self, entity):
        entity.engine = self
        self._entities.append(entity)
