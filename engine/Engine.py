import pygame

from settings import (
    WIDTH,
    HEIGHT,
    FPS
)

class Engine:
    def __init__(
            self,
            width=WIDTH,
            height=HEIGHT
            ):
        pygame.init()
        self._screen = pygame.display.set_mode((width, height))
        self._running = True

        self.clicked = False
        self._clicked_entity_index = -1
        self._entities = []
    
    def start(self, cb):
        # Main loop
        while self._running:
            # Get mouse positions
            self.mouse_pos = pygame.mouse.get_pos()
            print(len(self._entities))
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self._running = False

                    case pygame.MOUSEBUTTONDOWN:
                        for i, entity in enumerate(self._entities):
                            if entity._is_clicked():
                                self._clicked_entity_index = i
                                break
                        else:
                            self.clicked = True

                    case pygame.MOUSEBUTTONUP:
                        if self._clicked_entity_index != -1 and event.button == 1:
                            self._entities[i].clicked = False
                            self._clicked_entity_index = -1

            # Render entities
            for entity in self._entities:
                entity.update(entity)
                entity.draw()

            cb(self)

            self.clicked = False

            # Update the display
            pygame.display.flip()
            # Cap the frame rate
            pygame.time.Clock().tick(FPS)

    def set_window_title(self, title):
        pygame.display.set_caption(title)

    def new(self, entity):
        self._entities.append(entity)