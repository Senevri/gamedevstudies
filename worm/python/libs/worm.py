import logging
from dataclasses import dataclass


import pygame
from pygame.locals import *


logging.basicConfig()
logger = logging.getLogger("Worm")
logging.getLogger("Worm").setLevel(logging.DEBUG)
logger.warn = logger.warning


@dataclass
class State():
    window_caption: str = ""
    times: int = 0
    quit_game: bool = False

class PyGame:
    def __init__(self, state: State):
        self.state = state
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 800, 800


    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE)
        self._running = True
        pygame.display.set_caption(self.state.window_caption + str(self.state.times))

    def on_event(self, event):
        logger.info(f"Event! {event}")
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        #logger.info(f"Loop!")
        pass

    def on_render(self):
        #logger.info(f"Render!")
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
