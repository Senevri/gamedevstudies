from dataclasses import dataclass

import pygame
from pygame import Surface
# from pygame.locals import (

# )

try:
    from libs import log
except ImportError:
    from . import log

logger = log.getLogger(__name__)


@dataclass
class State():
    window_caption: str = ""
    times: int = 0
    quit_game: bool = False

class PyGame:
    _display_surf: Surface

    def __init__(self, state: State):
        logger.info(__name__)
        self.state = state
        self._running = True

        self.size = self.weight, self.height = 800, 800


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self._running = True
        pygame.display.set_caption(self.state.window_caption + str(self.state.times))

    def on_event(self, event):
        #logger.info(f"Event! {event}")
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        #logger.info(f"Loop!")
        pass

    def on_render(self):
        self._display_surf.fill((0,0,0))
        pygame.draw.rect(self._display_surf, pygame.Color(255,0,0), pygame.Rect(100,100, 24,24))

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            #logger.info("running")
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            #Reload libs here
        self.on_cleanup()
