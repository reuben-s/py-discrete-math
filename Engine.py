import pygame
from settings import WIDTH, HEIGHT, FPS, BLACK, Button

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
        
        self.cache = {}

        self._running = True
        self._clicked_entity_index = -1
        self._entities = []
    
    def start(self, cb):
        # Main loop
        while self._running:
            # Reset screen
            self._screen.fill(self.bg_colour)
            # Get mouse positions
            self.mouse_pos = pygame.mouse.get_pos()

            self.handle_events()
            self.update_entities()
            self.render_entities()
            cb(self)

            self.clicked = False

            # Update the display
            pygame.display.flip()
            # Cap the frame rate
            pygame.time.Clock().tick(FPS)

    def handle_events(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_up(event)

    def handle_mouse_down(self, event):
        # Handle mouse button down event
        for i, entity in enumerate(self._entities):
            if entity._is_clicked():
                self._clicked_entity_index = i

                if event.button == Button.LEFT_CLICK.value:
                    entity.button = Button.LEFT_CLICK
                elif event.button == Button.RIGHT_CLICK.value:
                    entity.button = Button.RIGHT_CLICK

                if not entity.mousedown:
                    entity._last_clicked_time = pygame.time.get_ticks()

                entity.mousedown = True

                break
        else:
            self.clicked = True

    def handle_mouse_up(self, event):
        # Handle mouse button up event
        if self._clicked_entity_index != -1:
            if self._entities[self._clicked_entity_index]._is_clicked():
                self._entities[self._clicked_entity_index].clicked = True if not self._entities[self._clicked_entity_index].holding else False

            self._entities[self._clicked_entity_index].mousedown = False
            self._entities[self._clicked_entity_index]._last_clicked_time = None
            self._entities[self._clicked_entity_index]._last_mouse_up_time = pygame.time.get_ticks()
            self._entities[self._clicked_entity_index].holding = False
            self._clicked_entity_index = -1

    def update_entities(self):
        # Update entities
        for entity in self._entities:
            entity._update()
            if entity._delete:
                self._entities.remove(entity)

    def render_entities(self):
        # Render entities
        for entity in self._entities:
            entity.draw()

    def set_window_title(self, title):
        pygame.display.set_caption(title)

    def get_mouse_pos(self):
        return pygame.mouse.get_pos()

    def new(self, entity):
        entity.engine = self
        self._entities.append(entity)